#!/bin/sh
set -e

# first arg is `-o` or `--option`
if [ "${1#-}" != "$1" ]; then
	set -- tg_upload_proxy_api "$@"
fi

# if our command is empty - run tg_upload_proxy_api
if [ "$1" = "" ]; then
	set -- tg_upload_proxy_api
fi

exec "$@"
