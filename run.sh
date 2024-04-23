#!/usr/bin/env bash

cd /var/log
source /.env
touch $CM_LOG_FILE

supervisord -c /supervisord.conf
