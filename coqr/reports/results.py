from abc import ABC, abstractmethod
from typing import List

from coqr.constants.Status import Status
from math import nan, isnan


# noinspection PyMethodMayBeStatic
class ProcessedResult(ABC):
    processed_output = ''

    @abstractmethod
    def compare_to(self, other) -> Status:
        return Status.FAIL

    def compare_to_not_implemented(self, other) -> Status:
        return Status.NOT_IMPLEMENTED

    def compare_to_error(self, other) -> Status:
        return Status.FAIL

    def compare_to_impossible(self, other) -> Status:
        return Status.IMPOSSIBLE

    def compare_to_null(self, other) -> Status:
        return Status.FAIL

    def compare_to_function(self, other) -> Status:
        return Status.FAIL

    def compare_to_unknown(self, other) -> Status:
        return Status.UNKNOWN

    def compare_to_vector(self, other) -> Status:
        return Status.FAIL

    def compare_to_invisible(self, other) -> Status:
        return Status.FAIL

    def compare_to_list(self, other) -> Status:
        return Status.FAIL

    def to_json(self):
        return self.processed_output


class NullResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'NULL'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_null(self)

    def compare_to_null(self, other):
        return Status.PASS


class ImpossibleResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'Impossible'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_impossible(self)

    def compare_to_not_implemented(self, other):
        return Status.IMPOSSIBLE

    def compare_to_error(self, other):
        return Status.IMPOSSIBLE

    def compare_to_null(self, other):
        return Status.IMPOSSIBLE

    def compare_to_function(self, other):
        return Status.IMPOSSIBLE

    def compare_to_unknown(self, other):
        return Status.IMPOSSIBLE

    def compare_to_vector(self, other):
        return Status.IMPOSSIBLE

    def compare_to_invisible(self, other):
        return Status.IMPOSSIBLE

    def compare_to_list(self, other) -> Status:
        return Status.IMPOSSIBLE


class NotImplementedResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'Not Implemented'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_not_implemented(self)

    def compare_to_error(self, other):
        return Status.NOT_IMPLEMENTED

    def compare_to_null(self, other):
        return Status.NOT_IMPLEMENTED

    def compare_to_function(self, other):
        return Status.NOT_IMPLEMENTED

    def compare_to_unknown(self, other):
        return Status.NOT_IMPLEMENTED

    def compare_to_vector(self, other):
        return Status.NOT_IMPLEMENTED

    def compare_to_invisible(self, other):
        return Status.NOT_IMPLEMENTED

    def compare_to_list(self, other) -> Status:
        return Status.NOT_IMPLEMENTED


class ErrorResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'ERROR'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_error(self)

    def compare_to_error(self, other):
        return Status.PASS


class FunctionResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'FUNCTION'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_function(self)

    def compare_to_function(self, other):
        return Status.PASS


class UnknownResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'UNKNOWN'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_unknown(self)

    def compare_to_invisible(self, other) -> Status:
        return Status.UNKNOWN

    def compare_to_function(self, other) -> Status:
        return Status.UNKNOWN

    def compare_to_vector(self, other) -> Status:
        return Status.UNKNOWN

    def compare_to_error(self, other) -> Status:
        return Status.UNKNOWN

    def compare_to_null(self, other) -> Status:
        return Status.UNKNOWN


class VectorResult(ProcessedResult):
    def __init__(self, vector: List) -> None:
        super().__init__()
        self.result = vector
        self.processed_output = 'VECTOR'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_vector(self)

    def compare_to_vector(self, other):
        return Status.PASS if self.result == other.result else Status.FAIL

    def to_json(self):
        return str(self.result)


class BooleanVector(VectorResult):
    def __init__(self, vector: List) -> None:
        super().__init__(vector)
        self.processed_output = 'BOOLEAN_VECTOR'


class StringVector(VectorResult):
    def __init__(self, vector: List) -> None:
        super().__init__(vector)
        self.processed_output = 'STRING_VECTOR'


class NumericVector(VectorResult):
    def __init__(self, vector: List) -> None:
        super().__init__(vector)
        self.processed_output = 'NUMERIC_VECTOR'

    def compare_to_vector(self, other):
        if len(self.result) != len(self.result):
            return Status.FAIL

        for n1, n2 in zip(self.result, other.result):
            if n1 and n2:
                if isnan(n1) and isnan(n2):
                    continue
                elif n1 != n2:
                    return Status.FAIL
            elif not n1 and not n2:
                continue
            else:
                return Status.FAIL
        return Status.PASS


class InvisibleResult(ProcessedResult):
    def __init__(self) -> None:
        super().__init__()
        self.processed_output = 'INVISIBLE'

    def compare_to(self, other: ProcessedResult):
        return other.compare_to_invisible(self)

    def compare_to_invisible(self, other):
        return Status.PASS


class ListResult(ProcessedResult):
    def __init__(self, list_result: dict) -> None:
        super().__init__()
        self.processed_output = 'LIST'
        self.result = list_result

    def compare_to(self, other) -> Status:
        return other.compare_to_list(self)

    def __compare_partial_results(self, res1: dict, res2: dict):
        if not res1.keys() == res2.keys():
            return Status.FAIL

        for k in res1.keys():
            if isinstance(res1[k], dict) and isinstance(res2[k], dict):
                status = self.__compare_partial_results(res1[k], res2[k])
                if status == Status.FAIL or status == Status.UNKNOWN:
                    return status
                else:
                    continue
            elif isinstance(res1[k], dict) or isinstance(res2[k], dict):
                return Status.FAIL

            status = res1[k].compare_to(res2[k])
            if status == Status.FAIL or status == Status.UNKNOWN:
                return status

        return Status.PASS

    def compare_to_list(self, other):
        return self.__compare_partial_results(self.result, other.result)

    def to_json(self):
        return str(self.result)
