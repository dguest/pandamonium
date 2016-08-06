#!/usr/bin/env python3

from urllib import request, parse
import json
import sys
import re

_ok_states = {'done', 'finished'}
_headers = {'Accept': 'application/json',
            'Content-Type':'application/json',
            'User-Agent':'User-Agent: curl/7.43.0'}

def get_broken_taskids(taskname='group.perf-flavtag*',
                       user='Daniel Hay Guest',
                       taskname_tag = 'v5.holistic'):
    pars = {
        'taskname': taskname,
        'produsername': user,
    }
    url = 'http://bigpanda.cern.ch/tasks/?' + parse.urlencode(pars)
    req = request.Request(url, headers=_headers)
    ret_json = request.urlopen(req).read().decode('utf-8')
    for entry in json.loads(ret_json):
        if taskname_tag not in entry['taskname']:
            continue
        if entry['status'] not in _ok_states:
            yield entry['jeditaskid']

def run():
    for taskid in get_broken_taskids():
        params = parse.urlencode({'jeditaskid': taskid})
        url = 'http://bigpanda.cern.ch/tasks/?' + params
        req = request.Request(url, headers=_headers)
        stuff = request.urlopen(req).read().decode('utf-8')
        for entry in json.loads(stuff):
            for ds in entry['datasets']:
                print(ds['datasetname'])




if __name__ == '__main__':
    run()
