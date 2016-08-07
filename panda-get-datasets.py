#!/usr/bin/env python3

"""
Script to retreve datasets (input or output) in submitted jobs
"""
# help strings
_h_taskname='initial search string'
_h_user='full user name (as listed on panda)'
_h_stream='stream name fragment to filter for'
_h_days='only look back this many days'
# defaults
_def_user='Daniel Hay Guest'
_def_stream='OUT'

from urllib import request, parse
import json
import sys
import re
import argparse

_broken_states = {'aborted', 'broken'}
_headers = {'Accept': 'application/json',
            'Content-Type':'application/json',
            'User-Agent':'User-Agent: curl/7.43.0'}

def get_args():
    d = ' (default: %(default)s)'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('taskname', help=_h_taskname)
    parser.add_argument('-u','--user', help=_h_user + d, default=_def_user)
    parser.add_argument('-s','--stream', help=_h_stream + d,
                        default=_def_stream)
    parser.add_argument('-d','--days', help=_h_days, type=int)
    return parser.parse_args()

def get_taskids(taskname, user, days=None):
    pars = {
        'taskname': taskname,
        'produsername': user,
    }
    if days is not None:
        pars['days'] = days
    url = 'http://bigpanda.cern.ch/tasks/?' + parse.urlencode(pars)
    req = request.Request(url, headers=_headers)
    ret_json = request.urlopen(req).read().decode('utf-8')
    for entry in json.loads(ret_json):
        yield entry['jeditaskid']

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


def run():
    args = get_args()
    for taskid in get_taskids(args.taskname, args.user, args.days):
        for ds in get_ds(taskid, args.stream):
            sys.stdout.write(ds + '\n')

if __name__ == '__main__':
    run()
