#!/usr/bin/env python

"""
Script to retreve datasets (input or output) in submitted jobs

With a specified search string, will search for datasets with that
name. If the name doesn't end in `*` or `/`, append a wildcard.
if the string is '-', the datasets are read from stdin.

The user name can be specified via environment variable to reduce
clutter.
"""

import argparse
import datetime
import json
import os
import re
import sys

# Attempt to default to Python 3
try:
    from urllib.parse import urlencode
    from urllib.request import Request
    from urllib.request import urlopen
except:
    from urllib import urlencode

    from urllib2 import Request
    from urllib2 import urlopen

# help strings
_h_taskname = 'initial search string'
_h_user = 'full user name, or blank for all'
_h_stream = 'stream name fragment to filter for'
_h_site = 'list grid site(s) where job ran'
_h_days = 'only look back this many days'
_h_clean = 'clean output: better for cut or grep'
_h_taskid = 'output only JEDI taskid. Useful for piping. See the PanDA JEDI docs for more information on JEDITASKID.'
_h_print_browser_string = (
    'don\'t run query, just print string to copy into browser'
)
_h_print_json_reply = (
    'don\'t format output, just print the json reply from the server'
)
_h_metadata = 'print the contents of userMetadata.json'
_h_force_update = 'don\'t allow caching on the server, (force with timestamp)'
_h_filter = 'filter for jobs in some states states (i.e. broken, running...)'
_h_range = (
    'filter for jobs in some range of task IDs (i.e 11506-11606, 12000-)'
)
_h_more_info_string = (
    'The Danny Antrim option: print even more information about your jobs!'
)
# defaults
_def_user = 'GRID_USER_NAME'
_def_stream = 'OUT'

_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


def get_args():
    c = ' (default: %(const)s)'
    user = os.environ.get(_def_user, '')
    if not user:
        de = ' (please set {} environment variable)'.format(_def_user)
    else:
        de = ' (set via {} variable to "%(default)s")'.format(_def_user)
    de += (
        ' Note that this should be your full name,'
        ' i.e. "Daniel Joseph Antrim"'
    )
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    userenv = 'RUCIO_ACCOUNT' if 'RUCIO_ACCOUNT' in os.environ else 'USER'
    parser.add_argument(
        'taskname',
        help=_h_taskname,
        nargs='?',
        default="user.{}".format(os.environ[userenv]),
    )
    parser.add_argument('-u', '--user', help=_h_user + de, default=user)
    parser.add_argument('-d', '--days', help=_h_days, type=int)
    addinfo = parser.add_mutually_exclusive_group()
    addinfo.add_argument(
        '-s',
        '--stream',
        help=_h_stream + c,
        nargs='?',
        default=None,
        const=_def_stream,
    )
    addinfo.add_argument(
        '-g', '--grid-site', action='store_true', help=_h_site
    )
    parser.add_argument('-c', '--clean', action='store_true', help=_h_clean)
    parser.add_argument('--force-color', action='store_true')
    parser.add_argument('-t', '--taskid', action='store_true', help=_h_taskid)
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        '-b',
        '--print-browser-string',
        action='store_true',
        help=_h_print_browser_string,
    )
    output.add_argument(
        '-j',
        '--print-json-reply',
        action='store_true',
        help=_h_print_json_reply,
    )
    output.add_argument(
        '-m', '--metadata', action='store_true', help=_h_metadata
    )
    parser.add_argument(
        '-i', '--filter', help=_h_filter, nargs='+', dest='filt'
    )
    parser.add_argument('-r', '--range', help=_h_range, dest='rnge')
    output.add_argument(
        '-a', '--more-info', action='store_true', help=_h_more_info_string
    )
    parser.add_argument(
        '-f', '--force', action='store_true', help=_h_force_update
    )

    args = parser.parse_args()
    if not args.taskname and sys.stdin.isatty():
        parser.print_usage()
        sys.exit('ERROR: need to pipe datasets or specify a search string')
    return args


def get_request(
    taskname, user, days=None, json=True, force=False, metadata=False
):
    pars = {'taskname': taskname, 'datasets': True, 'limit': 10000}
    if metadata:
        pars['extra'] = 'metastruct'
    if user:
        pars['username'] = user
    if json:
        pars['json'] = 1
    if force:
        pars['timestamp'] = datetime.datetime.utcnow().strftime('%H:%M:%S')
    if days is not None:
        pars['days'] = days
    url = 'https://bigpanda.cern.ch/tasks/?' + urlencode(pars)
    return Request(url, headers=_headers)


def get_jobid_request(id, days=None, force=False):
    pars = {
        'jeditaskid': id,
        'limit': 10000,
        'json': 1,
        'fields': 'metastruct',
    }
    if force:
        pars['timestamp'] = datetime.datetime.utcnow().strftime('%H:%M:%S')
    if days is not None:
        pars['days'] = days
    url = 'https://bigpanda.cern.ch/jobs/?' + urlencode(pars)
    return Request(url, headers=_headers)


_error_ds_re = re.compile('"([^ "]*)"')


def get_ds_stream(entry, streamfrag):
    datasets = entry['datasets']
    # in some cases the input dataset no longer exists, try to extract
    # it
    if not datasets and streamfrag.lower().startswith('in'):
        ed = 'errordialog'
        if ed in entry:
            yield _error_ds_re.search(entry[ed]).group(1)
    streams = {ds['streamname']: ds for ds in datasets}
    for stream, ds in streams.items():
        if streamfrag.upper() in stream:
            st = streams[stream]
            yield st['containername'] or st['datasetname']


def get_ds_site(entry):
    datasets = entry['datasets']
    out_ds = set(ds['site'] for ds in datasets)
    return ' '.join(out_ds - set([""]))


RED = '\033[0;91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'

_color_dic = {
    'running': BLUE + BOLD,
    'submitting': CYAN,
    'registered': MAGENTA,
    'ready': MAGENTA,
    'done': GREEN,
    'finished': YELLOW,
    'broken': RED + BOLD,
    'aborted': RED,
    'failed': RED,
}


def getstatus(task, args):
    if args.clean:
        fmt_string = '{s} {i} {p:.0%} {t} '
    elif args.taskid:
        fmt_string = '{i}'
    elif args.more_info:
        fmt_string = '{s:<{l}} {j: <9} {i:<9} {p: <6.0%} {f: <6.0%} {t} '
    else:
        fmt_string = '{s:<{l}} {i:<9} {p: <6.0%} {t} '
    if (sys.stdout.isatty() and not args.clean) or args.force_color:
        color = _color_dic.get(task['superstatus'], ENDC)
        status_color = color + task['status'] + ENDC
        nonprlen = len(color) + len(ENDC)
    else:
        status_color = task['status']
        nonprlen = 0

    if not args.taskid:
        if args.more_info:
            outputString = fmt_string.format(
                s=status_color,
                t=task['taskname'],
                j=task['jeditaskid'],
                i=task['reqid'],
                l=(11 + nonprlen),
                p=task['dsinfo']["pctfinished"] / 100.0,
                f=task['dsinfo']["pctfailed"] / 100.0,
            )
        else:
            outputString = fmt_string.format(
                s=status_color,
                t=task['taskname'],
                i=task['jeditaskid'],
                l=(11 + nonprlen),
                p=task['dsinfo']["pctfinished"] / 100.0,
            )
    if args.taskid:
        outputString = fmt_string.format(i=task['jeditaskid'])

    return outputString


def format_meta(task, days, force):
    jobs = task.get('jobs_metadata', {}).values()
    if not jobs and task['status'] in {'done', 'finished'}:
        req = get_jobid_request(task['jeditaskid'], days, force)
        reply = json.loads(urlopen(req).read().decode('utf-8'))
        jobs = [j['metastruct'] for j in reply['jobs'] if j]
    sum_data = {}
    for j in jobs:
        try:
            meat = j['user_job_metadata']
        except KeyError:
            meat = j
        for k, v in meat.items():
            if k not in sum_data:
                sum_data[k] = v
            else:
                sum_data[k] += v
    string = ', '.join(['{}:{}'.format(k, v) for k, v in sum_data.items()])
    return '{t}  {f}'.format(t=task['taskname'], f=string)


def stdin_iter(args):
    for line in sys.stdin:
        task = line.strip()
        if task[-1] not in '/*':
            task = task + '*'
        req = get_request(task, args.user, args.days, args.metadata)
        for ds in json.loads(urlopen(req).read().decode('utf-8')):
            yield ds


def main():
    args = get_args()

    taskname = args.taskname
    # try to search
    if taskname != '-':
        # append a wildcard if I forgot
        if args.taskname[-1] not in '/*':
            taskname = taskname + '*'
        use_json = not args.print_browser_string
        req = get_request(
            taskname, args.user, args.days, use_json, args.force, args.metadata
        )
        if args.print_browser_string:
            sys.stdout.write(req.get_full_url() + '\n')
            return 0
        reply = urlopen(req).read().decode('utf-8')
        if args.print_json_reply:
            sys.stdout.write(reply)
            return 0
        datasets = json.loads(reply)
    else:
        # otherwise read from stdin
        datasets = stdin_iter(args)

    if args.filt:
        datasets = [ds for ds in datasets if ds['status'] in args.filt]

    if args.rnge:
        r = args.rnge.split('-')
        if args.rnge[0] == '-':
            datasets = [
                ds for ds in datasets if int(ds['jeditaskid']) <= int(r[1])
            ]
        elif args.rnge[-1] == '-':
            datasets = [
                ds for ds in datasets if int(ds['jeditaskid']) >= int(r[0])
            ]
        else:
            datasets = [
                ds
                for ds in datasets
                if int(ds['jeditaskid']) in range(int(r[0]), int(r[1]))
            ]

    if args.metadata and datasets and 'jobs_metadata' not in datasets[0]:
        sys.stderr.write(
            'WARNING: hit batch metadata limit (ATLASPANDA-492)'
            ' running the slow way instead\n'
        )

    # loop over tasks
    for task in datasets:
        if args.stream:
            for ds in get_ds_stream(task, args.stream):
                sys.stdout.write(ds + '\n')
        elif args.metadata:
            sys.stdout.write(format_meta(task, args.days, args.force) + '\n')
        elif args.grid_site:
            ds = get_ds_site(task)
            sys.stdout.write(ds + '\n')
        else:
            sys.stdout.write(getstatus(task, args) + '\n')


if __name__ == "__main__":
    main()
