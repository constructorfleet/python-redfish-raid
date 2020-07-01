import json

import argparse

from const import *
from di import get_run_application_usecase


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

    parser.add_argument('--showallinfo', default=False, action="store_true", dest="show_all",
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

    parser.add_argument('--nagios', default=False, action='store_true', dest="nagios",
                        help='Check health and output in Nagios format.')
    # parser.add_argument('-c', default=False, action='store_true', dest="nagios_critical",
    #                     help='Use with --nagios: make the check go critical when a disk fails.')
    # parser.add_argument('-i', '--ignorewritecache', dest='nagios_ignorewritecache',
    #                     default=False, action='store_true',
    #                     help='Use with --nagios: ignore the write cache setting.')


def main():
    """Main entry point to Redfish RAID."""

    parser = argparse.ArgumentParser(description="Redfish integration with RAID controller.")
    _api_args(parser)
    _command_args(parser)

    args = parser.parse_args()
    #print(str(args))

    results = get_run_application_usecase(args.api_type,
                                          args.login_host,
                                          args.login_account,
                                          args.login_password,
                                          args,
                                          system=args.system,
                                          api_prefix=args.api_prefix)()
    with open('data.out', 'w') as writer:
        writer.write(results)
    print(results)


if __name__ == '__main__':
    """Main entrypoint handler."""
    main()
