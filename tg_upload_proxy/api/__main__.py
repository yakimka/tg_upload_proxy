import argparse
import os
from sys import argv

import sentry_sdk
from aiohttp.web import run_app
from aiomisc.log import LogFormat, basic_config
from configargparse import ArgumentParser
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from setproctitle import setproctitle

from tg_upload_proxy.api.app import create_app
from tg_upload_proxy.utils.argparse import positive_int, clear_environ

ENV_VAR_PREFIX = 'TGFU_'

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX, allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

group = parser.add_argument_group('API Options')
group.add_argument('--api-address', default='0.0.0.0',  # noqa: S104
                   help='IPv4/IPv6 address API server would listen on')
group.add_argument('--api-port', type=positive_int, default=8081,
                   help='TCP port API server would listen on')

group = parser.add_argument_group('Logging options')
group.add_argument('--log-level', default='info',
                   choices=('debug', 'info', 'warning', 'error', 'fatal'))
group.add_argument('--log-format', choices=LogFormat.choices(),
                   default='color')
group.add_argument('--sentry-dsn')
group.add_argument('--sentry-environment')


def main():
    args = parser.parse_args()
    sentry_sdk.init(
        dsn=args.sentry_dsn,
        environment=args.sentry_environment,
        integrations=[AioHttpIntegration()]
    )

    # Clear env variables of the app after start for security reasons.
    # Clear variables that starts with ENV_VAR_PREFIX.
    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))

    # For processing logs in a separate thread.
    basic_config(args.log_level, args.log_format, buffered=True)

    setproctitle(os.path.basename(argv[0]))

    app = create_app()
    run_app(app, host=args.api_address, port=args.api_port)


if __name__ == '__main__':
    main()
