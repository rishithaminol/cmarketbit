#!/usr/bin/env bash

cd /var/log

if [ -f /.env ]; then
    source /.env
fi

touch $CM_LOG_FILE

supervisord -c /supervisord.conf
