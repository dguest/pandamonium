#!/usr/bin/env python3

from urllib import request, parse
import json
import sys
import re

_ok_states = {'done', 'finished'}

def run():
    taskname_tag = 'v5.holistic'
    params = parse.urlencode({
        # 'taskname': 'user.dguest*',
        # 'taskname': 'group.perf-flavtag*',
        'taskid': 9147919,
        # 'days': 5,
        # 'produsername': 'Daniel Hay Guest',
        # 'datasets': 'yes'
    })
    print(params)
    # return 0
    url = 'http://bigpanda.cern.ch/tasks/?' + params
    headers = {'Accept': 'application/json',
               'Content-Type':'application/json',
               'User-Agent':'User-Agent: curl/7.43.0'}
    req = request.Request(url, headers=headers)
    stuff = request.urlopen(req).read().decode('utf-8')
    print(json.dumps(json.loads(stuff), indent=2))
    for entry in json.loads(stuff):
        # if entry['status'] in _ok_states:
        #     continue
        # if taskname_tag not in entry['taskname']:
        #     continue
        print(entry)
        for ds in entry['datasets']:
            print(ds['datasetname'])




if __name__ == '__main__':
    run()
