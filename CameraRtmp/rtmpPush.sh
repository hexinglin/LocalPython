#!/usr/bin/env bash
pathw=$(cd `dirname $0`; pwd)
export PYTHONPATH=${pathw}
python3 ${pathw}/rtmpPush.py >> ${pathw}/log.log

