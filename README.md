This project provides a set of tools to test out [proveR](https://github.com/Mbodin/proveR).

It executes R code with both an R and Coq interpreter, and then proceeds to
compare their outputs.

# Setup

Requirements:
- Python 3.5
- R binary (tested on v3.4.2)
- proveR

First of all, Python libraries should be installed. You can do it with the
following command:
```bash
$ pip install -r requirements.txt
or
$ pip3 install -r requirements.txt
```

You may need to provide permissions to install (or install in a virtualenv)

# Scripts

It is possible to either execute the whole process with both interpreters
or to execute different stages of the process separately.

# Run all

Executes the whole process with both interpreters and outputs general
statistics of the process.

It requires a `.env` file next to the run_all script, with the following content:
```
# Contents of .env file
# Without ''

COQ_INTERP=path/to/coq-interpreter
RSCRIPT=path/to/rscript  # Or just name if it's in global scope

# If sending data to server
URL=https://...
TOKEN=token-authentication
```

Doc of the script:
```bash
usage: run_all.py [-h] [-o OUTPUT] [--debug] [-s] [-r] [-t TITLE] src

Run given file with R and Coq interpreters, processes outputs and compares

positional arguments:
  src

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
  --debug
  -s, --server
  -r, --recursive
  -t TITLE, --title TITLE

```

Usage of the script:
```bash
$ ./run_all src -o output

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
$ ./stats.py -g out/result.json

# Case info
$ ./stats.py -status Pass out/result.json
```