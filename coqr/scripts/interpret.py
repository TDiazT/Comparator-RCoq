#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time

from coqr.interpreters.CoqInterpreter import CoqInterpreter
from coqr.interpreters.FileInterpreter import FileInterpreter
from coqr.interpreters.RInterpreter import RInterpreter
from coqr.utils.file import write_to_file

parser = argparse.ArgumentParser(description='Run every expression in a file with named interpreter')

parser.add_argument('input')
parser.add_argument('-o', '--output', help="Creates a JSON file with the results in the given path.")
parser.add_argument('--line', action='store_true')


def get_interpreter():
    RSCRIPT = os.environ.get('RSCRIPT')
    COQ_INTERP = os.environ.get('COQ_INTERP')
    if RSCRIPT:
        return RInterpreter(RSCRIPT)
    elif COQ_INTERP:
        return CoqInterpreter(COQ_INTERP, os.environ.get('COQR_INITIAL_STATE'))
    else:
        sys.exit("No valid interpreter set in environment. Define either 'RSCRIPT' or 'COQ_INTERP' variables.")


def obj_dict(obj):
    return obj.__dict__


if __name__ == '__main__':
    options = parser.parse_args()

    interpreter = get_interpreter()
    file_interpreter = FileInterpreter(interpreter)

    print('Interpreting file %s with %s interpreter' % (options.input, interpreter.name))
    current_time = time.time()
    if not options.line:
        reports = file_interpreter.interpret_multiline(options.input)
    else:
        reports = file_interpreter.interpret_line_by_line(options.input)

    print('Done! It took %f' % (time.time() - current_time))
    if options.output:
        print('You may find the results in %s' % options.output)
        write_to_file(options.output, reports)
    else:
        print(json.dumps(reports, indent=2, default=obj_dict))
