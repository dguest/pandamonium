Pandamonium
===========

[![GitHub Project](https://img.shields.io/badge/GitHub--blue?style=social&logo=GitHub)](https://github.com/dguest/pandamonium)

Cause panda and rucio don't work too good

This tells you if your jobs are done. And stuff like that.

 - No login required
 - Colors! (when you want them)
 - Gets input / output dataset names
 - Works with piping, other unix nice things

How I do dat?
-------------

 1. Clone me
 2. Add the directory to your `PATH`
 3. Type `pandamon [user.<your user name>]`
 4. **Pretty colors!!!**

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

Testimonials
------------

"I like colors" -- Chase Schimmin

"I found a bug" -- Danny Antrim (Fixed! Thanks Danny!)

"I tried to use it but it's python 3" -- also Chase

(I added python 2 support, and that's all that's currently supported)

"I made a merge request. It was approved!" -- Alex

"It needs to use [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)" -- Matthew Feickert

(Hey man, whatever floats your boat!)

I'll add other stuff too, if you want.
