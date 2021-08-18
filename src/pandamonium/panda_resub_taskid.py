#!/usr/bin/env python

"""
Resubmit jobs with pbook

Runs on pure python beauty.
"""

import argparse
import sys

try:
    from pandaclient import PBookCore
except ImportError:
    try:
        from pandatools import PBookCore
    except ImportError:
        print("Failed to load PandaClient, please set up locally")
        sys.exit(1)

_h_jobid = 'panda taskid, you can also pipe them'
_h_kill = 'kill any running jobs before retrying them'

epi = 'Thanks ATLAS. Thatlas.'


def get_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epi,
    )
    parser.add_argument('taskids', type=int, nargs='*', help=_h_jobid)
    parser.add_argument('-b', '--build', action='store_true')
    parser.add_argument('-n', '--nfiles', type=int)
    parser.add_argument('-x', '--exclude-sites', nargs="*")
    parser.add_argument('-m', '--new-site', action='store_true')
    parser.add_argument('-k', '--kill', action='store_true', help=_h_kill)
    args = parser.parse_args()
    if not args.taskids and sys.stdin.isatty():
        parser.print_usage()
        sys.exit('ERROR: need to pipe in a taskid')
    return args


def retry(jobs, args):
    # enforceEnter, verbose, restoreDB
    pbook = PBookCore.PBookCore()
    retry_opts = {}
    if args.build:
        retry_opts['retryBuild'] = True
    if args.nfiles or args.exclude_sites or args.new_site:
        new_opts = {}
        if args.nfiles:
            new_opts['nFilesPerJob'] = args.nfiles
        if args.exclude_sites:
            new_opts['excludeSite'] = ','.join(args.exclude_sites)
        if args.new_site:
            new_opts['newSite'] = True
        retry_opts['newOpts'] = new_opts
    for job in jobs:
        if args.kill:
            cmd = pbook.killAndRetry
        else:
            cmd = pbook.retry
        cmd(job, **retry_opts)


def stdin_iter():
    for line in sys.stdin:
        for job in line.split():
            yield int(job)


def main():
    args = get_args()

    jobs = []
    if not args.taskids:
        jobs = stdin_iter()
    else:
        jobs = args.taskids

    retry(jobs, args)


if __name__ == "__main__":
    main()
