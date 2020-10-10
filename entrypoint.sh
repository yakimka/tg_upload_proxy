#!/bin/sh
set -e

# first arg is `-o` or `--option`
if [ "${1#-}" != "$1" ]; then
	set -- tg_file_uploader_api "$@"
fi

# if our command is empty - run tg_file_uploader_api
if [ "$1" = "" ]; then
	set -- tg_file_uploader_api
fi

exec "$@"
