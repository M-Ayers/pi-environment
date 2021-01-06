from pigpio_dht import DHT22
import argparse

from time import sleep
from prometheus_client import start_http_server, Gauge
from w1thermsensor import W1ThermSensor

gpio_1 = 21

temp_gauge_1 = Gauge('pi_env_temp_1', 'Temperature Gauge 1 - DS18B20')
temp_gauge_2 = Gauge('pi_env_temp_2', 'Temperature Gauge 2 - DHT22')
humidity_gauge = Gauge('pi_env_humidity_1', 'Humidity Gauge 1 - DHT22')


def parser():
    parser = argparse.ArgumentParser(description='a simple environment monitoring and publishing utility for raspberry pi.')
    parser.add_argument('-t', '--temp_interval', help='interval frequency, in seconds, for environment polling. use value lower than 5 to disable. (default: 0, minimum: 5 seconds)', metavar='<interval>', default=0, required=False)
    parser.add_argument('-h', '--humidity_interval', help='interval frequency, in seconds, for environment polling.  use value lower than 5 to disable. (default: 0, minimum: 5 seconds)', metavar='<interval>', default=0, required=False)
    return parser.parse_args()

def prepareDS18():
    ds18 = W1ThermSensor()
    temp_gauge_1.set(0)
    return ds18

def prepareDHT22(gpio):
    dht22 = DHT22(gpio)
    temp_gauge_2.set(0)
    humidity_gauge.set(0)
    return dht22

if __name__ == '__main__':
    args = parser()
    temp_enabled = args.temp_interval >= 5
    humidity_enabled = args.humidity_interval >= 5

    if temp_enabled:
        ds18_1 = prepareDS18()
    if humidity_enabled:
        dht22_1 = prepareDHT22(gpio_1)

    start_http_server(9101)

    while True:
        if temp_enabled:
            temp_gauge_1.set(ds18_1.get_temperature())

        if humidity_enabled:
            dht22_response = dht22_1.read(retries=2)
            if dht22_response.valid:
                temp_gauge_2.set(dht22_response.temp_c)
                humidity_gauge.set(dht22_response.humidity)

        sleep(args.interval)