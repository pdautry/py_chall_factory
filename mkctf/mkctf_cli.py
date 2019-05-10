#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from signal import SIGINT, SIGTERM
from asyncio import get_event_loop
from pathlib import Path
from argparse import ArgumentParser
from mkctf import __version__
from mkctf.api import MKCTFAPI, MKCTFAPIException
from mkctf.cli.command import *
from mkctf.helper.log import (
    app_log,
    log_enable_debug,
    log_enable_logging
)
# =============================================================================
#  GLOBALS
# =============================================================================
__banner__ = r"""
           _     ____ _____ _____    ____ _     ___
 _ __ ___ | | __/ ___|_   _|  ___|  / ___| |   |_ _|
| '_ ` _ \| |/ / |     | | | |_    | |   | |    | |
| | | | | |   <| |___  | | |  _|   | |___| |___ | |
|_| |_| |_|_|\_\\____| |_| |_|      \____|_____|___| v{}

""".format(__version__)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    '''Parse command line arguments
    '''
    parser = ArgumentParser(add_help=True, description="A CLI to manage a mkCTF repository")
    parser.add_argument('--yes', '-y', action='store_true', help="some operations will stop asking for confirmation")
    parser.add_argument('--quiet', '-q', action='store_true', help="disable logging")
    parser.add_argument('--debug', '-d', action='store_true', help="enable debug messages")
    parser.add_argument('--repo-dir', '-r', type=Path, default=Path.cwd(), help="absolute path of a mkCTF repository directory")
    # -- add subparsers
    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True
    setup_init(subparsers)
    setup_enum(subparsers)
    setup_build(subparsers)
    setup_create(subparsers)
    setup_delete(subparsers)
    setup_enable(subparsers)
    setup_export(subparsers)
    setup_deploy(subparsers)
    setup_status(subparsers)
    setup_disable(subparsers)
    setup_configure(subparsers)
    setup_renew_flag(subparsers)
    setup_update_meta(subparsers)
    # -- parse args and pre-process if needed
    return parser.parse_args()

def sigint_handler():
    '''Handles user interrupt signal
    '''
    app_log.warning("\nOuch... you just killed me... (x_x)")
    loop = get_event_loop()
    loop.stop()
    loop.close()

async def main():
    '''Main function
    '''
    app_log.info(__banner__)
    args = parse_args()
    log_enable_debug(args.debug)
    log_enable_logging(not args.quiet)
    app_log.debug(args)
    try:
        api = MKCTFAPI(args.repo_dir)
        rcode = 0 if await args.func(api, args) else 1
    except MKCTFAPIException as exc:
        app_log.critical(f"critical error: {exc.args[0]}")
        rcode = 1
    except:
        app_log.exception("Ouch... unhandled exception... (>_<)")
        rcode = 2
    return rcode

def app():
    '''mkctf-cli script entry point
    '''
    loop = get_event_loop()
    loop.add_signal_handler(SIGINT, sigint_handler)
    loop.add_signal_handler(SIGTERM, sigint_handler)
    rcode = loop.run_until_complete(main())
    loop.close()
    return rcode
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    exit(app())
