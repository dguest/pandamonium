# Pandamonium

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/dguest/pandamonium)

Cause panda and rucio don't work too good

This tells you if your jobs are done. And stuff like that.

 - No login required
 - Colors! (when you want them)
 - Gets input / output dataset names
 - Works with piping, other unix nice things

## Installation

### Notes if working on a remote server

If you are working from a remote server where you do not have control over your Python runtimes (e.g. LXPLUS, ALTAS Connect login nodes) it is recommended that you bootstrap `virtualenv` and a default Python virtual environment by adding the following to your `.profile` or `.bash_profile`

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

After that source your `.profile` or `.bash_profile` and then if you want to create a default Python virtual environment run

```
virtualenv "${HOME}/.venvs/base"
```

You will now be dropped into a virtual environment named `base` each time you login.
The virtual environment is not special in anyway, so you should treat it as you would any other.

### Install from PyPI

You can install [`pandamonium` from PyPI][pandamonium_PyPI] into any Python virtual environment by simply running

```
python -m pip install pandamonium
```

### Install the old style of global scripts

If you want to install the original version of `pandamonium` before it became a library and was a set of global level Python scripts you can still do that.

1. Clone the repository at tag `v0.0.1`
```
git clone git@github.com:dguest/pandamonium.git --branch v0.0.1
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

## Use

1. Make sure that you have a valid `X509` certificate.
If you are on LXPLUS or ATLAS Connect this can be done with
```
lsetup emi
```
2. Run `pandamon`
```
pandamon [user.<your user name>]
```
3. See the output of your current GRID jobs with **pretty colors!**

You can add more of the task name if you want, and use wildcards
(`*`). Wildcards are automatically appended to names that don't end in
`*` or `/`.

Without any arguments the task name defaults to `user.$RUCIO_ACCOUNT*`.

Also try `pandamon -h`.

## Other tricks

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
This is useful for when you inevitably submit jobs with wrong parameters that you don't want to retry.

```sh
pandamon -r 12000-12100
```

#### Read the job user metadata ####

Now panda supports a `userMetadata.json` file for additional information in your job. Print it with

```sh
pandamon your.tasks -m
```

See [this JIRA ticket][1] where they plan to make it faster.

[1]: https://its.cern.ch/jira/browse/ATLASPANDA-492

## Testimonials

"I like colors" -- Chase Schimmin

"I found a bug" -- Danny Antrim (Fixed! Thanks Danny!)

"I tried to use it but it's python 3" -- also Chase

(I added python 2 support, and that's all that's currently supported)

"I made a merge request. It was approved!" -- Alex

"It needs to use [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)" -- Matthew Feickert

(Hey man, whatever floats your boat!)

I'll add other stuff too, if you want.
