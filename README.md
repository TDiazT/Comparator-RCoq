This project provides a set of tools to test out [proveR](https://github.com/Mbodin/proveR).

It executes R code with both an R and Coq interpreter, and then proceeds to
compare their outputs.

# Scripts

It is possible to either execute the whole process with both interpreters
or to execute different stages of the process separately.

# Run all

Executes the whole process with both interpreters and outputs general
statistics of the process.

It requires a `settings.py` file in `coqr` package, with the following content:
```python
# Contents of settings.py file

COQ_INTERP='path/to/coq-interpreter'
RSCRIPT='path/to/rscript'  # Or just name if it's in global scope

```

To execute the script just do the following.

```bash
$ python -m coqr.scripts.run_all r_file output

```

The output will be in the `output` directory specified, with a JSON format.

It will also print general stats about the execution.


## Runner
It runs every expression in a file. It requires that either `RSCRIPT` or
`COQ_INTERP` environmental variables are defined. If both are, it will
prefer the R case.

```bash
# Running R on a file
$ RSCRIPT='rscript' python -m coqr.scripts.runner input.R output.json

# Running proveR 
$ COQ_INTERP=/path/to/proveR/ python -m coqr.scripts.runner input.R output.json
```


## Cleaner
Reads a file (in JSON format), processes the output and returns a file with a new
processed output.

You must indicate which interpreter generated the output, either R or Coq.

```bash
$ python -m coqr.scripts.cleaner R input.json output.json

$ python -m coqr.scripts.cleaner Coq input.json output.json

```


## Stats

It reads a file generated by the comparison ([See 'run all'](#run-all))
and prints stats or info about it.

You can either display general stats (total of Pass, Fail, etc. cases)
or ask for information on a particular case.

```bash
# General stats
$ python -m coqr.stats.stats -g out/result.json

# Case info
$ python -m coqr.stats.stats -status Pass out/result.json
```