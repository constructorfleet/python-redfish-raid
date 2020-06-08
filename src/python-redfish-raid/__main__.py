import json

import argparse

from const import DEFAULT_API
from framework.client import get_client

from domain.usecases.api.ConnectUseCase import ConnectUseCase
from domain.usecases.api.DisconnectUseCase import DisconnectUseCase
from domain.usecases.api.RecurseApiUseCase import RecurseApiUseCase
from domain.usecases.models.CacheModelUseCase import CacheModelUseCase
from domain.usecases.models.GetCachedModelUseCase import GetCachedModelUseCase
from domain.usecases.models.GetModelCache import GetModelCacheUseCase


def get_connect_usecase(client):
    """Get connect use case."""
    return ConnectUseCase(client)


def get_disconnect_usecase(client):
    """Get disconnect use case."""
    return DisconnectUseCase(client)


def get_model_cache():
    """Get model cache use case."""
    return GetModelCacheUseCase()()


def get_cache_model_usecase():
    """Get use case for caching models."""
    return CacheModelUseCase(get_model_cache())


def get_model_cached_usecase():
    """Get use case for retrieving cached models."""
    return GetCachedModelUseCase(get_model_cache())


def get_recurse_api_usecase(client):
    """Get recurse api usecase."""
    return RecurseApiUseCase(client, get_model_cached_usecase(), get_cache_model_usecase())


def _api_args(parser):
    """Client api arguments."""
    parser.add_argument("--api", dest="api_type", required=False, type=str, default=DEFAULT_API,
                        help="API implementation name.")
    parser.add_argument("--host", dest="login_host", required=True, type=str,
                        help="Host to connect to.")
    parser.add_argument("--account", dest="login_account", required=True, type=str,
                        help="Redfish account for authentication.")
    parser.add_argument("--password", dest="login_password", required=True, type=str,
                        help="Redfish account password for authentication.")
    parser.add_argument("--prefix", dest="api_prefix", type=str,
                        default="/redfish/v1", help="Api client prefix.")


def _legacy_args(parser):
    """Parse and handle legacy arguments."""

    parser.add_argument('--showdisks', default=False, action='store_true', dest="show_disks",
                        help='Dump all disks with their error counters and firmware states.')
    parser.add_argument('--showfailed', default=True, action='store_true', dest="show_failed",
                        help='Display disks in Unconfigured(bad) or Predictive failure.')
    parser.add_argument('--showmissing', default=False, action='store_true', dest="show_missing",
                        help='Display disks that are missing.')
    parser.add_argument('--showlogical', default=False, action='store_true', dest="show_logical",
                        help='Display a dump of all logical disks and their members.')
    parser.add_argument('--showallinfo', default=False, action='store_true', dest="show_all",
                        help='Display a dump of the interesting adapter info.')
    parser.add_argument('--showprinfo', default=False, action='store_true', dest="show_pr",
                        help='Display a dump of the Patrol Read statuses of all adapters.')
    parser.add_argument('--showccinfo', default=False, action='store_true', dest="show_cc",
                        help='Display a dump of the Consistency Check statuses of all adapters.')
    parser.add_argument('--showbbuinfo', default=False, action='store_true', dest="show_bbu",
                        help='Display a dump of the Battery Backup Unit statuses of all adapters.')
    parser.add_argument('--showencinfo', default=False, action='store_true', dest="show_enclosure",
                        help='Display a dump of the enclosure information of all adapters.')
    parser.add_argument('--nagios', default=False, action='store_true', dest="nagios",
                        help='Check health and output in Nagios format.')
    parser.add_argument('-c', default=False, action='store_true', dest="nagios_critical",
                        help='Use with --nagios: make the check go critical when a disk fails.')
    parser.add_argument('-i', '--ignorewritecache', dest='nagios_ignorewritecache',
                        default=False, action='store_true',
                        help='Use with --nagios: ignore the write cache setting.')


def _show_command(parser):
    """Parse show command sub-arguments."""

    parser.add_argument('--disks', default=False, action='store_true', dest="show_disks",
                        help='Dump all disks with their error counters and firmware states')
    parser.add_argument('--failed', default=True, action='store_true', dest="show_failed",
                        help='Display disks in Unconfigured(bad) or Predictive failure state')
    parser.add_argument('--missing', default=False, action='store_true', dest="show_missing",
                        help='Display disks that are missing.')
    parser.add_argument('--logical', default=False, action='store_true', dest="show_logical",
                        help='Display a dump of all logical disks and their members.')
    parser.add_argument('--all', default=False, action='store_true', dest="show_all",
                        help='Display a dump of the interesting adapter info.')
    parser.add_argument('--patrol-read', default=False, action='store_true', dest="show_pr",
                        help='Display a dump of the Patrol Read statuses of all adapters.')
    parser.add_argument('--ccinfo', default=False, action='store_true', dest="show_cc",
                        help='Display a dump of the Consistency Check statuses of all adapters.')
    parser.add_argument('--bbu', default=False, action='store_true', dest="show_bbu",
                        help='Display a dump of the Battery Backup Unit statuses of all adapters.')
    parser.add_argument('--enclosure', default=False, action='store_true', dest="show_enclosure",
                        help='Display a dump of the enclosure information of all adapters.')


def _nagios_command(parser):
    """Parse nagios command sub arguments."""

    parser.add_argument('--critical', default=False, action='store_true', dest="nagios_critical",
                        help='When disk fails, force the check to critical.')
    parser.add_argument('-i', '--ignore-write-cache', dest='nagios_ignorewritecache',
                        default=False, action='store_true',
                        help='Ignore the write cache settings.')


def main():
    """Main entry point to Redfish RAID."""

    parser = argparse.ArgumentParser(description="Redfish integration with RAID controller.")
    # subparsers = parser.add_subparsers()
    _api_args(parser)
    # _legacy_args(parser)
    # _show_command(subparsers.add_parser('show', help="Display information specified by arguments."))
    # _nagios_command(subparsers.add_parser('nagios', help="Nagios monitoring information."))

    args = parser.parse_args()
    print(str(args))
    client = get_client(args.api_type,
                        args.login_host,
                        args.login_account,
                        args.login_password,
                        prefix=args.api_prefix)
    connect = get_connect_usecase(client)
    disconnect = get_disconnect_usecase(client)
    recurse = get_recurse_api_usecase(client)

    connect()
    try:
        data = recurse(args.api_prefix)
        results = json.dumps(data, indent=2, sort_keys=True)
        with open('data.json', 'w') as writer:
            writer.write(results)
        print(results)
    finally:
        disconnect()


if __name__ == '__main__':
    """Main entrypoint handler."""
    main()
