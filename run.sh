#!/usr/bin/env bash

cd /var/log
touch $CM_LOG_FILE

supervisord -c /supervisord.conf
