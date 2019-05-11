# =============================================================================
#  IMPORTS
# =============================================================================
from os import getenv
from getpass import getpass
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def push(api, args):
    '''Creates a challenge
    '''
    args.username = args.username or input("Scoreboard username: ")
    args.password = args.password or getpass("Scoreboard password: ")
    result = await api.push(args.host, args.port, args.username, args.password, args.no_verify_ssl)
    return result['pushed']

def setup_push(subparsers):
    '''Setup push subparser
    '''
    parser = subparsers.add_parser('push', help="push challenges configuration to the scoreboard.")
    parser.add_argument('--host', default=getenv('MKCTF_SB_HOST', 'scoreboard.ctf.insecurity-insa.fr'), help="scoreboard host, overrides MKCTF_SB_HOST (env)")
    parser.add_argument('--port', default=getenv('MKCTF_SB_PORT', 443), type=int, help="scoreboard port, overrides MKCTF_SB_PORT (env)")
    parser.add_argument('-u', '--username', default=getenv('MKCTF_SB_USER'), help="scoreboard username, overrides MKCTF_SB_USER (env)")
    parser.add_argument('-p', '--password', default=getenv('MKCTF_SB_PSWD'), help="scoreboard password, overrides MKCTF_SB_PSWD (env). Using this option is strongly discouraged.")
    parser.add_argument('--no-verify-ssl', action='store_true', help="Disable SSL checks. Using this option is strongly discouraged.")
    parser.set_defaults(func=push)
