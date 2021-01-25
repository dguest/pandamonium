Pandamonium
===========

Cause panda and rucio don't work too good

This tells you if your jobs are done. And stuff like that.

 - No login required
 - Colors! (when you want them)
 - Gets input / output dataset names
 - Works with piping, other unix nice things

Like badges? We have the best badges:

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/dguest/pandamonium)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4019463.svg)](https://doi.org/10.5281/zenodo.4019463)

[![PyPI version](https://badge.fury.io/py/pandamonium.svg)](https://badge.fury.io/py/pandamonium)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pandamonium.svg)](https://pypi.org/project/pandamonium/)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/dguest/pandamonium/master.svg)](https://results.pre-commit.ci/latest/github/dguest/pandamonium/master)


Installation
------------

### Install from PyPI

You can install [`pandamonium` from PyPI][pandamonium_PyPI] into any Python
environment by running

```
python -m pip install pandamonium
```

### Install oldschool way

If you can't get `pip` working you can just put the scripts you need
in your path. Note that this is **deprecated** (but still works for
now).

1. Clone the repository
```
git clone git@github.com:dguest/pandamonium.git
```
2. Add the directory to your `PATH`.

Maybe with something like the following in your `.bashrc`

```
# Add pandamonium to PATH
if [ -d "your/path/stuff/goes/here/pandamonium" ]; then
    PATH="your/path/stuff/goes/here/pandamonium${PATH:+:${PATH}}"
    export PATH
fi
```

[pandamonium_PyPI]: https://pypi.org/project/pandamonium/


Use
---

1. Run `pandamon`
```
pandamon [user.<your user name>]
```
2. See the output of your current GRID jobs with **pretty colors!**

You can add more of the task name if you want, and use wildcards
(`*`). Wildcards are automatically appended to names that don't end in
`*` or `/`.

Without any arguments the task name defaults to `user.$RUCIO_ACCOUNT*`.

Also try `pandamon -h`.


Other tricks
------------

#### Get input/output dataset names ####

```
> pandamon -s IN <task name>
> pandamon -s OUT <task name>
```

#### Filter by user name ####

This is useful if you're running with group privileges. Set the
environment variable `GRID_USER_NAME` to your full user name (the one
that shows up on the top of the bigpanda page). Or specify one with
`--user`.

#### Find input datasets for jobs in the `broken` state ####

You can do more useful stuff by piping through standard Unix utilities

```sh
> pandamon your.tasks > tasks.txt
> cat tasks.txt | awk '$1 ~ /broken/ {print $2}' | pandamon - -s IN
```

or (faster)

```sh
pandamon your.tasks -i broken -s IN
```

#### Filter by taskid range ####

Use to only display jobs in a specific range.
This is useful for when you inevitably submit jobs with wrong parameters that
you don't want to retry.

```sh
pandamon -r 12000-12100
```

#### Read the job user metadata ####

Now panda supports a `userMetadata.json` file for additional information in your
job.
Print it with

```sh
pandamon your.tasks -m
```

See [this JIRA ticket][1] where they plan to make it faster.

[1]: https://its.cern.ch/jira/browse/ATLASPANDA-492


Additional Technical Information
--------------------------------

### Deprecation Warning

You can currently just clone the repository and have `master` work the
same way as [`v0.1`][tag_v0.1] on LXPLUS or ATLAS Connect, but this
will be deprecated in the future in favor of installing `pandamonium`
as a Python library.

The motivation for this is that `pandamonium`
does have hard requirements on other libraries, and it is better to
fully contain them through the installation of the library through
PyPI.

If you really need the old behaviour forever, you can always use

```
git clone git@github.com:dguest/pandamonium.git --branch v0.1
```

[tag_v0.1]: https://github.com/dguest/pandamonium/releases/tag/v0.1


### Install development release from TestPyPI

You can install the latest development release of
[`pandamonium` from TestPyPI][pandamonium_TestPyPI] into any Python virtual
environment by running

```
python -m pip install --extra-index-url https://test.pypi.org/simple/ --pre pandamonium
```

> **Note:** This adds TestPyPI as [an additional package index to search][additional_package_index]
when installing `pandamonium` specifically.
PyPI will still be the default package index `pip` will attempt to install from
for all dependencies.

[pandamonium_TestPyPI]: https://test.pypi.org/project/pandamonium/
[additional_package_index]: https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-extra-index-url

### Notes if working on a remote server

If you are working from a remote server where you do not have control over your
Python runtimes (e.g. LXPLUS, ALTAS Connect login nodes) it is recommended that
you bootstrap `virtualenv` and a default Python virtual environment by adding
the following to your `.bashrc` or `.bashrc_user`

```
# Ensure local virtualenv setup
if [ ! -f "${HOME}/opt/venv/bin/virtualenv" ]; then
    curl -sL --location --output /tmp/virtualenv.pyz https://bootstrap.pypa.io/virtualenv.pyz
    python /tmp/virtualenv.pyz ~/opt/venv # Change this to python3 if available
    ~/opt/venv/bin/pip install --upgrade pip
    ~/opt/venv/bin/pip install virtualenv
    mkdir -p ~/bin  # Ensure exists if new machine
    ln -s ~/opt/venv/bin/virtualenv ~/bin/virtualenv
fi

# default venv from `virtualenv "${HOME}/.venvs/base"`
if [ -d "${HOME}/.venvs/base" ]; then
    source "${HOME}/.venvs/base/bin/activate"
fi
```

After that source your `.profile` or `.bash_profile` and then if you want to
create a default Python virtual environment run

```
virtualenv "${HOME}/.venvs/base"
```

You will now be dropped into a virtual environment named `base` each time you login.
The virtual environment is not special in anyway, so you should treat it as you
would any other.


Testimonials
------------

"I like colors" -- Chase Schimmin

"I found a bug" -- Danny Antrim (Fixed! Thanks Danny!)

"I tried to use it but it's python 3" -- also Chase

(I added Python 2 support, but `pandamonium` is also Python 3 compliant)

"I made a merge request. It was approved!" -- Alex

"It needs to use [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)" -- Matthew Feickert

(Hey man, whatever floats your boat!)

I'll add other stuff too, if you want.
