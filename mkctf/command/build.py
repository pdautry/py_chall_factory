'''
file: build.py
date: 2018-03-02
author: paul.dautry
purpose:

'''
# =============================================================================
#  IMPORTS
# =============================================================================
from termcolor import colored
from mkctf.helper.log import app_log
from mkctf.helper.formatting import returncode2str
# =============================================================================
#  FUNCTIONS
# =============================================================================
async def build(args, repo):
    '''Builds one or more challenges
    '''
    if not args.force and not repo.cli.confirm('do you really want to build?'):
        return {'status': True} if args.json else True

    no_color, timeout = args.no_color, args.timeout
    tags, slug = args.tags, args.slug

    chall_sep = '=' * 80
    sep = '-' * 35
    exc_sep = '{sep} [EXCEPT] {sep}'.format(sep=sep)
    out_sep = '{sep} [STDOUT] {sep}'.format(sep=sep)
    err_sep = '{sep} [STDERR] {sep}'.format(sep=sep)

    if not no_color:
        chall_sep = colored(chall_sep, 'blue', attrs=['bold'])
        exc_sep = colored(exc_sep, 'magenta')
        out_sep = colored(out_sep, 'blue')
        err_sep = colored(err_sep, 'red')

    success = True
    results = []

    for challenge in repo.scan(tags):
        if slug is None or slug == challenge.slug:

            exception = None

            try:
                (code, stdout, stderr) = await challenge.build(timeout)
            except Exception as e:
                exception = e
                success = False
                code = -1

            if args.json:
                results.append({
                    'slug': challenge.slug,
                    'tags': challenge.tags,
                    'code': code,
                    'stdout': stdout,
                    'stderr': stderr,
                    'exception': exception
                })
            else:
                chall_description = f"{challenge.slug}{challenge.tags}"
                if not no_color:
                    chall_description = colored(chall_description, 'blue')

                chall_status = returncode2str(code, args.no_color)

                print(chall_sep)
                print(f"{chall_description} {chall_status}")

                if code < 0:
                    print(exc_sep)
                    print(exception)
                elif code > 0:
                    print(out_sep)
                    print(stdout.decode().strip())
                    print(err_sep)
                    print(stderr.decode().strip())

    return results if args.json else success
