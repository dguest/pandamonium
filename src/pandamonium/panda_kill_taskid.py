#!/usr/bin/env python

"""
Kill jobs with pbook

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

epi = 'Thanks ATLAS. Thatlas.'


def get_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epi,
    )
    parser.add_argument('taskids', type=int, nargs='*', help=_h_jobid)
    args = parser.parse_args()
    if not args.taskids and sys.stdin.isatty():
        parser.print_usage()
        sys.exit('ERROR: need to pipe in a taskid')
    return args


def kill(jobs, args):
    # enforceEnter, verbose, restoreDB
    pbook = PBookCore.PBookCore()

    for job in jobs:
        pbook.kill(job)


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

    kill(jobs, args)


if __name__ == "__main__":
    main()
