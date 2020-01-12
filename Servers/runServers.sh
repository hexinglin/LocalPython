#!/usr/bin/env bash

export PYTHONPATH=$(cd `dirname $0`; pwd)
python3 $(cd `dirname $0`; pwd)/manage.py runserver 0.0.0.0:8000

