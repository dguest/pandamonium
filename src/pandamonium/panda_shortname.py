#!/usr/bin/env python

"""
Crop dataset names. No one cares about your stupid generator tune.

By default expects datasets in the "official" ordering and doesn't
remove any fields. Except the "scope", which seems totally
worthless...
"""

_help_remove = "remove fields that we usually don't care about"
_help_prefix = "prefix file names with this"

import argparse
import re
import sys
import os


def get_args():
    c = ' (with no arg: %(const)s)'
    user = os.environ.get('USER')
    def_prefix = ''
    if user is not None:
        def_prefix = 'user.{}'.format(user)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('ds_names', nargs='*')
    parser.add_argument(
        '-r', '--remove', action='store_true', help=_help_remove
    )
    parser.add_argument(
        '-p', '--prefix', nargs='?', const=def_prefix, help=_help_prefix + c
    )
    parser.add_argument('-s', '--suffix')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def main():
    args = get_args()
    ds_names = args.ds_names
    if not ds_names:
        ds_names = stdin_iter()

    for ds_name in ds_names:
        oname = process_name(ds_name, args.remove, args.prefix, args.suffix)
        if args.verbose:
            prelen, postlen = len(ds_name), len(oname)
            diff = postlen - prelen
            cutdown = 'cut {} to {} ({:+})'.format(prelen, postlen, diff)
            sys.stderr.write(cutdown + '\n')
        sys.stdout.write(oname + '\n')


def stdin_iter():
    for line in sys.stdin:
        yield line.strip()


def process_name(ds_name, remove, prefix=None, suffix=None):
    # throw away the scope
    if ':' in ds_name:
        ds_name = ds_name.split(':', 1)[-1]
    # remove trailing slash
    ds_name = ds_name.rstrip('/')

    res = ds_name.split('.')
    (source, dsid, disc, prodstep, fmt, tags), _ = res[:6], res[6:]

    # sanity checks
    assert dsid.isdigit(), "dsid ({}) not a number".format(dsid)
    assert is_tag(tags), "'{}' doesn't look like a tag".format(tags)
    assert fmt.isupper(), "'{}' doesn't look like a format".format(fmt)

    # replace things
    disc = short_disc(disc)
    prodstep = short_prodstep(prodstep)
    fmt = short_fmt(fmt)

    if remove:
        fields = [dsid, disc, fmt, tags]
    else:
        fields = [source, dsid, disc, prodstep, fmt, tags]
    if prefix is not None:
        fields.insert(0, prefix)
    if suffix is not None:
        fields.append(suffix)
    short_name = '.'.join(fields)
    return short_name


# replace funcs
def short_disc(disc):
    tune_finder = re.compile('[A-Z0-9]{3,}_')
    return tune_finder.sub('', disc)


def short_prodstep(prodstep):
    if '_' in prodstep or not prodstep.islower():
        raise ValueError("{} doesn't look like a prodstep".format(prodstep))
    return prodstep[0]


def short_fmt(fmt):
    removed_pfx = ['DAOD_']
    for pfx in removed_pfx:
        if fmt.startswith(pfx):
            return fmt[len(pfx) :]
    return fmt


# checks
def is_tag(tags):
    tag_finder = re.compile('([a-z][0-9]+_?)+')
    matches = tag_finder.match(tags).group(0)
    return len(matches) == len(tags)


if __name__ == "__main__":
    main()
