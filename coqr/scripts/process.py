import argparse
import json
import sys

import time

from collections import namedtuple

from coqr.processors.CoqOutputProcessor import CoqOutputProcessor
from coqr.processors.ROutputProcessor import ROutputProcessor
from coqr.reports.processing import report_from_dict, reports_from_list
from coqr.utils.file import write_to_file, read_json_to_processed_report

parser = argparse.ArgumentParser(description='Processes output and returns a new standard one')

parser.add_argument('interp')
parser.add_argument('input')
parser.add_argument('-output')


def read_json_file(filename):
    with open(filename) as file_:
        data = file_.read()
        return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


if __name__ == '__main__':
    options = parser.parse_args()

    if options.interp == 'R':
        processor = ROutputProcessor()
    elif options.interp == 'Coq':
        processor = CoqOutputProcessor()
    else:
        sys.exit('"%s" is not a valid interpreter (either "R" or "Coq")' % options.interp)

    print("Processing file %s" % options.input)
    current_time = time.time()
    previous_reports = read_json_to_processed_report(options.input)
    new_reports = processor.process_reports(previous_reports)

    print("Done in %f seconds" % (time.time() - current_time))
    if options.output:
        print('Results may be found in %s' % options.output)
        write_to_file(options.output, new_reports)

    else:
        print("-------------------------------")
        print(json.dumps(new_reports, indent=2))
