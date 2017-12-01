# Scripts

## Expression runner
It runs an expression with given interpreter and prints output in console.

```bash

# R
python expression-runner.py R "expression"

# Coq
COQ_INTERP=/path/to/proveR/ python expression-runner.py a "expression"


```

[See also](#run-exp)


## Runner
It runs every command in a file, line by line, with the given interpreter and outputs
a file with a JSON-style result.

Example: 
```bash
# Running R on a file
$ python runner.py R input.R output.json

# Running proveR 
$ COQ_INTERP=/path/to/proveR/ python runner.py asdf input.R output.json
```

Arguments:
1. Interpreter: Either "R" or anything
1. R file: File with R expressions to be run
1. Output: name of the output file (Ideally .json)

Output:
A file with the results in the following format:
```javascript
[
    {
       "interpreter": "",
        "execution_time": ,
        "expression": "",
        "output": "",
        "line":  
    },
    ...
]
```

## Cleaner
Reads a file (in JSON format), "cleans" the output and returns a file with a new
"cleaned_output" field.

```bash
$ python cleaner.py R input.json output.json

```

Arguments:
1. Input file: Ideally the one from the runner phase or with the same format.
1. Output file: Where to write the resulting "cleaned" version.

Output:
A file with the same results as in the input file but with a new field:
```javascript
[
    {
       ...,
       "clean_output": [],
    },
    ...
]
```

## Comparator
Reads two files, Coq's output first and then R's output, compares the values and 
outputs a file with the resulting comparison.
```bash
$ python comparator.py coq.json r.json output.json
```

Arguments:
1. First input: Ideally Coq's cleaned output
1. Second input: Ideally R's cleaned output
1. Output file: Where to print resulting comparison

Output:
A file with the results in the following format:

```javascript
[
  {
    "clean_coq_output": [],
    "status_code": "",
    "expression": "",
    "clean_r_output": [],
    "coq_output": "",
    "r_output": ""
  },
  ...
 ]
```


## Run-exp
Runs an expression with R and Coq interpreter.

```bash
$ ./run-exp.sh "exp"
```

Arguments:
1. Expression to be run



## Run

This runs all the previous ones sequentially and outputs everything to the
`out` directory.

```bash
$ ./run.sh input.R
# This will generate in ../out, the files:
# - r.json
# - coq.json
# - r-clean.json
# - coq-clean.json
# - comparison.json
```


Arguments:
1. Input file: R file with expressions to be run
2. R output (optional): Particular name for the R output file
3. Coq output (optional): Particular name for the Coq output file

Output:
All files mentioned in previous scripts:
- r.json
- coq.json
- r-clean.json
- coq-clean.json
- comparison.json