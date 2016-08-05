#!/usr/bin/env python3

from urllib import request
import json

def run():
    url = 'http://bigpanda.cern.ch/tasks/?taskname=user.dguest*&days=8'
    headers = {'Accept:': 'application/json',
               'Content-Type:':'application/json'}
    req = request.Request(url, headers=headers)
    stuff = request.urlopen(req).read().decode('utf-8')
    dic = json.loads(stuff)
    print(json.dumps(dic, indent=2))

if __name__ == '__main__':
    run()
