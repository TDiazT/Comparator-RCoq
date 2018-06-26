import re

from coqr.processors.AbstractOutputProcessor import AbstractOutputProcessor
from coqr.reports.results import ErrorResult, FunctionResult, NullResult, BooleanVector, StringVector, \
    NumericVector, ListResult


class ROutputProcessor(AbstractOutputProcessor):
    error_regex = re.compile(r'^Error:?.*$', re.MULTILINE)
    function_regex = re.compile(r'^function.*$', re.MULTILINE)
    primitive_regex = re.compile(r'^\.Primitive.*$', re.MULTILINE)
    null_regex = re.compile(r'^ *NULL *$', re.MULTILINE)
    boolean_regex = re.compile(r'^ *\[\d+\](?: +TRUE| +FALSE| +NA)+ *$', re.MULTILINE)
    string_regex = re.compile(r'^ *\[\d+\](?: +\".*\")+ *$', re.MULTILINE)
    number_regex = re.compile(r'^ *\[\d+\](?: +(?:[+-]?(?:(?:[0-9]*[.])?[0-9]+(?:[eE][-+]?[0-9]+)*|Inf)|NA|NaN))+ *$',
                              re.MULTILINE)
    list_regex = re.compile(
        r'^ *(\[\[\d+\]\]|\$\w+).*$',
        re.MULTILINE)

    def __init__(self):
        super().__init__()

    def define_cases_handlers(self):
        return [
            (self.error_regex, lambda x: ErrorResult()),
            (self.function_regex, lambda x: FunctionResult()),
            (self.primitive_regex, lambda x: FunctionResult()),
            (self.null_regex, lambda x: NullResult()),
            (
                self.boolean_regex,
                lambda x: BooleanVector(self._result_to_boolean_vector(self.boolean_regex.findall(x)))),
            (self.string_regex, lambda x: StringVector(self._result_to_string_vector(self.string_regex.findall(x)))),
            (self.number_regex, lambda x: NumericVector(self._result_to_numeric_vector(self.number_regex.findall(x)))),
            (self.list_regex, lambda x: ListResult(self._result_to_list(x)))
        ]

    def _result_to_list(self, result : str) -> dict:
        bracket_regex = re.compile(r'\[\[\d+\]\]')

        lines_aux = result.split("\n")
        lines = list(filter(None, lines_aux))

        res = {}
        aux = res
        index = 1
        for line in lines:
            if self.list_regex.match(line):
                match = bracket_regex.findall(line)
                size = len(match)

                if size > index:
                    last = len(aux)
                    aux[last] = {}
                    aux = aux[last]
                    index = size
                elif size < index:
                    aux = res
                    for i in range(0, size - 1):
                        aux = aux[len(aux) - 1]
                else:
                    continue
            else:
                aux[len(aux)] = self.process_output(line)

        return res