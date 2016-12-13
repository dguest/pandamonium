Pandamonium
===========

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
> cat tasks.txt | awk '$1 ~ /broken/ {print $3}' | pandamon - -s IN
```

Testimonials
------------

"I like colors" -- Chase Schimmin

"I tried to use it but it's python 3" -- also Chase

(I added python 2 support, and that's all that's currently supported)

I'll add other stuff too, if you want.
