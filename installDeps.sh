#!/usr/bin/env bash
file='./requirements.txt'
if [ -f $file ]; then
  if command -v pip3 > /dev/null; then
    pip3 install -r $file
  else
    echo "Pip3 not installed."
    exit 1
  fi
else
  echo "Can't find ${file}"
  exit 1
fi
