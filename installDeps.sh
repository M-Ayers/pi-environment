#!/usr/bin/env bash
file='./requirements.txt'
if [ -f $file ]; then
  if command -v pip > /dev/null; then
    pip install -r $file
  else
    echo "Pip not installed."
    exit 1
  fi
else
  echo "Can't find ${file}"
  exit 1
fi