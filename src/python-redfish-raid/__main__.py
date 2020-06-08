import json

import argparse

from const import DEFAULT_API, COMMAND_SHOW_ALL, COMMAND_NAGIOS, COMMAND_SHOW_PR, COMMAND_SHOW_CC, \
    COMMAND_SHOW_BBU, COMMAND_SHOW_ENC, COMMAND_SHOW_DISKS, COMMAND_SHOW_LOGICAL
from domain.usecases.configs.GetSystemConfigUseCase import GetSystemConfigUseCase
from domain.usecases.configs.LoadConfigurationUseCase import LoadConfigurationUseCase
from framework.client import get_client

from domain.usecases.api.ConnectUseCase import ConnectUseCase
from domain.usecases.api.DisconnectUseCase import DisconnectUseCase
from domain.usecases.api.InvokeApiUseCase import InvokeApiUseCase
from domain.usecases.models.CacheModelUseCase import CacheModelUseCase
from domain.usecases.models.GetCachedModelUseCase import GetCachedModelUseCase
from domain.usecases.models.GetModelCache import GetModelCacheUseCase
from domain.usecases.models.GetLinkedModelsUseCase import GetLinkedModelsUseCase


def get_load_configuration_usecase():
    """Get configuration loader use case."""
    return LoadConfigurationUseCase()


def get_system_configuration_usecase(load_config, system):
    """"Get system configuration use case."""
    return GetSystemConfigUseCase(load_config(system))


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


def get_invoke_api_usecase(client):
    """Get invoke api usecase."""
    return InvokeApiUseCase(client, get_model_cached_usecase(), get_cache_model_usecase())


def get_linked_models_usecase(invoke_api):
    """Get use case for retrieving linked models."""
    return GetLinkedModelsUseCase(get_model_cached_usecase(), invoke_api)


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
    parser.add_argument("--system", dest="system", required=True, type=str,
                        help="System manufacturer.")
    parser.add_argument("--prefix", dest="api_prefix", type=str,
                        default="/redfish/v1", help="Api client prefix.")


def _command_args(parser):
    """Parse and handle command arguments."""

    parser.add_argument('--showallinfo', default=True, action="store_true", dest="show_all",
                        help='Display a dump of the interesting adapter info.')
    parser.add_argument('--showprinfo', default=False, action="store_true", dest="show_pr",
                        help='Display a dump of the Patrol Read statuses of all adapters.')
    parser.add_argument('--showccinfo', default=False, action="store_true", dest="show_cc",
                        help='Display a dump of the Consistency Check statuses of all adapters.')
    parser.add_argument('--showbbuinfo', default=False, action="store_true", dest="show_bbu",
                        help='Display a dump of the Battery Backup Unit statuses of all adapters.')
    parser.add_argument('--showencinfo', default=False, action="store_true", dest="show_enc",
                        help='Display a dump of the enclosure information of all adapters.')

    parser.add_argument('--showdisks', default=False, action="store_true", dest="show_disks",
                        help='Dump all disks with their error counters and firmware states.')
    parser.add_argument('--showlogical', default=False, action='store_true', dest="show_logical",
                        help='Display a dump of all logical disks and their members.')
    # parser.add_argument('--showfailed', default=True, dest="show_failed",
    #                     help='Display disks in Unconfigured(bad) or Predictive failure.')
    # parser.add_argument('--showmissing', default=False, action='store_true', dest="show_missing",
    #                     help='Display disks that are missing.')

    # parser.add_argument('--nagios', default=False, action='store_true', dest="nagios",
    #                     help='Check health and output in Nagios format.')
    # parser.add_argument('-c', default=False, action='store_true', dest="nagios_critical",
    #                     help='Use with --nagios: make the check go critical when a disk fails.')
    # parser.add_argument('-i', '--ignorewritecache', dest='nagios_ignorewritecache',
    #                     default=False, action='store_true',
    #                     help='Use with --nagios: ignore the write cache setting.')


def _get_command(args):
    """Get the command from the args."""
    # TODO : More dynamic
    # if args.nagios:
    #     return COMMAND_NAGIOS
    if args.show_all:
        return COMMAND_SHOW_ALL
    if args.show_pr:
        return COMMAND_SHOW_PR
    if args.show_cc:
        return COMMAND_SHOW_CC
    if args.show_bbu:
        return COMMAND_SHOW_BBU
    if args.show_enc:
        return COMMAND_SHOW_ENC
    if args.show_disks:
        return COMMAND_SHOW_DISKS
    if args.show_logical:
        return COMMAND_SHOW_LOGICAL


def main():
    """Main entry point to Redfish RAID."""

    parser = argparse.ArgumentParser(description="Redfish integration with RAID controller.")
    # subparsers = parser.add_subparsers()
    _api_args(parser)
    _command_args(parser)

    args = parser.parse_args()
    print(str(args))
    system_config = get_system_configuration_usecase(get_load_configuration_usecase(), args.system)()
    client = get_client(args.api_type,
                        args.login_host,
                        args.login_account,
                        args.login_password,
                        prefix=args.api_prefix)
    connect = get_connect_usecase(client)
    disconnect = get_disconnect_usecase(client)
    invoke_api = get_invoke_api_usecase(client)
    get_linked_models = get_linked_models_usecase(invoke_api)

    connect()
    try:
        prefix = system_config.get_prefix(_get_command(args)) or args.api_prefix
        data = invoke_api(prefix, recurse=True)
        data.set_linked_models(get_linked_models(data))
        results = json.dumps(data, indent=2, sort_keys=True)
        # TODO: Report use case
        with open('data.json', 'w') as writer:
            writer.write(results)
        print(results)
    finally:
        disconnect()


if __name__ == '__main__':
    """Main entrypoint handler."""
    main()
