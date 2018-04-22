#!/usr/bin/env python3

import argparse
import os
import re
import subprocess

import time

from requests import HTTPError

import stats
import settings

from coqr.comparators.Comparator import Comparator
from coqr.constants.Status import Status
from coqr.interpreters.CoqInterpreter import CoqInterpreter
from coqr.interpreters.FileInterpreter import FileInterpreter
from coqr.interpreters.RInterpreter import RInterpreter
from coqr.network.calls import send_reports
from coqr.processors.AbstractOutputProcessor import AbstractOutputProcessor
from coqr.processors.CoqOutputProcessor import CoqOutputProcessor
from coqr.processors.ROutputProcessor import ROutputProcessor
from coqr.utils.file import write_to_file

COQ_DEFAULT_FILE = 'coq.json'

R_DEFAULT_FILE = 'r.json'

parser = argparse.ArgumentParser(
    description='Run given file with R and Coq interpreters, processes outputs and compares')

parser.add_argument('src')
parser.add_argument('-o', '--output')
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-s', '--server', action='store_true')
parser.add_argument('-r', '--recursive', action='store_true')
parser.add_argument('-t', '--title', default='')
parser.add_argument('-m', '--message', default='')


def interpret_file(src, interpreter, debug=False, out=None):
    reports = interpreter.interpret_file(src)

    if debug:
        write_to_file(out, reports)

    return reports


def interpret_directory(src, interpreter: FileInterpreter, recursive=False, debug=False, out=None):
    reports = interpreter.interpret_directory(src, recursive=recursive)

    if debug:
        write_to_file(out, reports)

    return reports


def process_outputs(output, processor: AbstractOutputProcessor, debug=False, out=None):
    processed = processor.process_reports(output)

    if debug:
        write_to_file(out, processed)

    return processed


def compare_processed_outputs(processed_r, processed_coq):
    print("Comparing")
    comparator = Comparator()
    return comparator.compare_results(processed_coq, processed_r)


def print_general_stats(reports):
    print("")
    print("---------- GENERAL STATS ----------")
    stats_ = stats.get_general_stats(reports)
    for k, v in stats_.most_common():
        print("%s : %d" % (str(Status(k)), v))


def get_coqr_version():
    git_process = subprocess.Popen(["git", "--git-dir", os.path.join(os.environ.get("COQ_INTERP"), '.git'),
                                    "rev-parse", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True)
    (res, err) = git_process.communicate()
    return re.sub(r'\n', '', res)


if __name__ == '__main__':
    options = parser.parse_args()

    print("Interpreting tests in %s" % options.src)
    print("Running R interpreter...")
    delta = time.time()
    r_interpreter = RInterpreter(os.environ.get("RSCRIPT"))
    if os.path.isfile(options.src):
        r_results = interpret_file(options.src, FileInterpreter(r_interpreter))
    else:
        r_results = interpret_directory(options.src, FileInterpreter(r_interpreter),
                                        recursive=options.recursive)
    print("Finished in %f seconds" % (time.time() - delta))

    print("Running Coq interpreter...")
    delta = time.time()
    coqr = CoqInterpreter(os.environ.get("COQ_INTERP"))
    if os.path.isfile(options.src):
        coq_results = interpret_file(options.src, FileInterpreter(coqr))
    else:
        coq_results = interpret_directory(options.src, FileInterpreter(coqr),
                                          recursive=options.recursive)

    print("Finished in %f seconds" % (time.time() - delta))

    if options.debug:
        if options.output:
            directory = os.path.dirname(options.output)
            write_to_file(os.path.join(directory, R_DEFAULT_FILE), r_results)
            write_to_file(os.path.join(directory, COQ_DEFAULT_FILE), coq_results)
        else:
            print("Debug set but no output directory specified")

    print("Processing R output")
    r_process = process_outputs(r_results, ROutputProcessor())
    print("Processing Coq output")
    coq_process = process_outputs(coq_results, CoqOutputProcessor())

    if options.debug:
        if options.output:
            directory = os.path.dirname(options.output)
            write_to_file(os.path.join(directory, 'processed-r.json'), r_process)
            write_to_file(os.path.join(directory, 'processed-coq.json'), coq_process)
        else:
            print("Debug set but no output directory specified")

    comparison = compare_processed_outputs(r_process, coq_process)
    (sysname, nodename, release, version, machine) = os.uname()
    final_report = {
        "r_interpreter_version": "3.4.2",
        "coq_interpreter_version": get_coqr_version(),
        "system": sysname,
        "os_node_name": nodename,
        "os_release": release,
        "os_version": version,
        "hardware": machine,
        "title": options.title,
        "description": options.message,
        "expression_reports": comparison
    }

    if options.output:
        write_to_file(options.output, final_report)

    if options.server:
        print('Sending results to server')
        try:
            send_reports(final_report, os.environ.get("URL"), os.environ.get("TOKEN"))
            print('Sent successfully')
        except HTTPError:
            print('There was an error sending the report to server')

    if options.output:
        print("Done, you may find the results in %s" % options.output)
    else:
        print("Done!")

    print_general_stats(comparison)
