#!/usr/bin/env python3

"""
Script to retreve datasets (input or output) in submitted jobs
"""
# help strings
_h_taskname='initial search string'
_h_user='full user name (as listed on panda)'
_h_stream='stream name fragment to filter for'
_h_days='only look back this many days'
_h_state='prefix dataset name with state'
# defaults
_def_user='Daniel Hay Guest'
_def_stream='OUT'

from urllib import request, parse
import json
import sys
import re
import argparse

_headers = {'Accept': 'application/json',
            'Content-Type':'application/json',
            'User-Agent':'User-Agent: curl/7.43.0'}

def get_args():
    d = ' (default: %(default)s)'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('taskname', help=_h_taskname)
    parser.add_argument('-u','--user', help=_h_user + d, default=_def_user)
    parser.add_argument('-d','--days', help=_h_days, type=int)
    addinfo = parser.add_mutually_exclusive_group()
    addinfo.add_argument('-a', '--status', action='store_true', help=_h_state)
    addinfo.add_argument('-s','--stream', help=_h_stream + d,
                         default=_def_stream)
    return parser.parse_args()

def get_datasets(taskname, user, days=None):
    pars = {
        'taskname': taskname,
        'produsername': user,
    }
    if days is not None:
        pars['days'] = days
    url = 'http://bigpanda.cern.ch/tasks/?' + parse.urlencode(pars)
    req = request.Request(url, headers=_headers)
    return json.loads(request.urlopen(req).read().decode('utf-8'))

def get_ds(taskid, streamfrag):
    params = parse.urlencode({'jeditaskid': taskid})
    url = 'http://bigpanda.cern.ch/tasks/?' + params
    req = request.Request(url, headers=_headers)
    stuff = request.urlopen(req).read().decode('utf-8')
    # containers = set()
    for entry in json.loads(stuff):
        datasets = entry['datasets']
        streams = {ds['streamname']: ds for ds in datasets}
        for stream, ds in streams.items():
            if streamfrag.upper() in stream:
                yield streams[stream]['containername']


RED = '\033[0;91m'
RED_BLINK = '\033[5;91m'
RED_BOLD = '\033[1;91m'
RED_UBOLD = '\033[4;1;91m'
GREEN = '\033[0;92m'
YELLOW = '\033[0;93m'
BLUE = '\033[1;94m'
MAGENTA = '\033[0;95m'
CYAN = '\033[0;96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

_color_dic = {
    'running': BLUE,
    'submitting': CYAN,
    'registered': MAGENTA,
    'ready': MAGENTA,
    'done': GREEN,
    'finished': YELLOW,
    'broken': RED_BOLD,
    'aborted': RED,
    'failed': RED,
    }
def getstatus(task):
    color = ENDC
    if sys.stdout.isatty():
        color = _color_dic.get(task['superstatus'], ENDC)
    status_color = color + task['status'] + ENDC
    return '{s:<20} {t:<120}'.format(s=status_color, t=task['taskname'])

def run():
    args = get_args()
    for task in get_datasets(args.taskname, args.user, args.days):
        if args.status:
            sys.stdout.write(getstatus(task) + '\n')
        else:
            for ds in get_ds(task['jeditaskid'], args.stream):
                sys.stdout.write(ds + '\n')

if __name__ == '__main__':
    run()
