import argparse

from time import sleep

from prometheus_client import start_http_server, Gauge

temp_guage = Gauge('pi_env_temp_1', 'Temperature Gauge 1')
humidity_guage = Gauge('pi_env_humidity_1', 'Humidity Gauge 1')


def parser():
    parser = argparse.ArgumentParser(description='a simple environment monitoring and publishing utility for raspberry pi.')
    parser.add_argument('-i', '--interval', help='interval frequency, in seconds, for environment polling. (default: 5 seconds, minimum: 5 seconds)', metavar='<interval>', default=5, required=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parser()
    temp_guage.set(0)
    humidity_guage.set(0)
    start_http_server(9101)
    while True:
        temp_guage.inc()
        humidity_guage.inc()
        sleep(args.interval)