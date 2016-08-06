#!/usr/bin/env python3

"""
Script to retreve the input datasets for jobs that can't be restarted.
"""
# help strings
_h_taskname='initial search string'
_h_user='full user name (as listed on panda)'
# defaults
_def_taskname='group.perf-flavtag*v5.holistic*'
_def_user='Daniel Hay Guest'

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
    parser.add_argument('taskname', nargs='?', help=_h_taskname + d,
                        default=_def_taskname)
    parser.add_argument('-u','--user', help=_h_user + d, default=_def_user)
    return parser.parse_args()

def get_broken_taskids(taskname, user):
    pars = {
        'taskname': taskname,
        'produsername': user,
    }
    url = 'http://bigpanda.cern.ch/tasks/?' + parse.urlencode(pars)
    req = request.Request(url, headers=_headers)
    ret_json = request.urlopen(req).read().decode('utf-8')
    for entry in json.loads(ret_json):
        if entry['status'] in _broken_states:
            yield entry['jeditaskid']

def get_input_ds(taskid):
    params = parse.urlencode({'jeditaskid': taskid})
    url = 'http://bigpanda.cern.ch/tasks/?' + params
    req = request.Request(url, headers=_headers)
    stuff = request.urlopen(req).read().decode('utf-8')
    containers = set()
    for entry in json.loads(stuff):
        datasets = entry['datasets']
        streams = {ds['streamname']: ds for ds in datasets}
        containers.add(streams['IN']['containername'])
    assert len(containers) == 1
    return containers.pop()

def run():
    args = get_args()
    for taskid in get_broken_taskids(args.taskname, args.user):
        sys.stdout.write(get_input_ds(taskid) + '\n')

if __name__ == '__main__':
    run()
