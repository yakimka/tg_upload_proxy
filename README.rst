.. image:: https://github.com/yakimka/tg_upload_proxy/workflows/build/badge.svg
.. image:: https://codecov.io/gh/yakimka/tg_upload_proxy/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/yakimka/tg_upload_proxy

Telegram Upload Proxy
=====================

Telegram Bot Api allows you to upload files up to 50 megabytes only.

You can use tg_upload_proxy for avoid this limit. This app uses MTProto for interaction with Telegram Bot API.

Quote from `telethon <https://docs.telethon.dev/en/latest/concepts/botapi-vs-mtproto.html#what-is-bot-api/>`_ documentation:

    Bot API is simply an HTTP endpoint which translates your requests to it into MTProto calls through tdlib, their bot backend.

    Both official applications and third-party clients (like your own applications) logged in as either user or bots can use MTProto to communicate directly with Telegram’s API (which is not the HTTP bot API).

Instalation
-----------
::

    python setup.py install

or you can use Docker:

::

    docker run -p 8081:8081 -e TG_API_ID="API_ID" -e TG_API_HASH="API_HASH" -e TG_BOT_TOKEN="BOT_TOKEN" yakim/tg_upload_proxy

Open `http://127.0.0.1:8081/docs/ <http://127.0.0.1:8081/docs/>`_ page in browser.

Configuration
-------------

App take configuration from these environment variables:
::

    TG_API_ID - API ID from my.telegram.org
    TG_API_HASH - API Hash from my.telegram.org
    TG_BOT_TOKEN - telegram bot token


List of available arguments:
::

    tg_upload_proxy_api --help

API Documentation
-----------------

You can find Swagger UI on /docs/ page
