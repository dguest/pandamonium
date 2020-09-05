#!/usr/bin/env python

"""
Kill jobs with pbook

Runs on pure python beauty.
"""

_h_jobid = 'panda taskid, you can also pipe them'

epi = 'Thanks ATLAS. Thatlas.'

import sys, os
import argparse

from pandatools import PBookCore


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


if __name__ == '__main__':
    args = get_args()

    try:
        from pandatools import PBookCore
    except ImportError:
        print("Failed to load PandaClient, please set up locally")
        sys.exit(1)

    jobs = []
    if not args.taskids:
        jobs = stdin_iter()
    else:
        jobs = args.taskids

    kill(jobs, args)
