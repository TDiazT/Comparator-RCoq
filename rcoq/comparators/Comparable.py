from abc import ABC, abstractmethod

from rcoq.constants.Cases import Cases
from rcoq.constants.Status import Status


class Comparable(ABC):
    def __init__(self, case=Cases.UNKNOWN) -> None:
        self.case = case

    @abstractmethod
    def compare_to(self, other):
        pass


class NotImplementedComparable(Comparable):
    def __init__(self, case=Cases.NOT_IMPLEMENTED) -> None:
        super().__init__(case)
        self.case = Cases.NOT_IMPLEMENTED

    def compare_to(self, other):
        return Status.NOT_IMPLEMENTED


class ErrorComparable(Comparable):
    def __init__(self, case=Cases.ERROR) -> None:
        super().__init__(case)
        self.case = Cases.ERROR

    def compare_to(self, other):
        if other.case == Cases.UNKNOWN:
            return Status.UNKNOWN
        elif self.case == other.case:
            return Status.PASS
        else:
            return Status.FAIL


class ImpossibleComparable(Comparable):
    def __init__(self, case=Cases.IMPOSSIBLE) -> None:
        super().__init__(case)
        self.case = Cases.IMPOSSIBLE

    def compare_to(self, other):
        return Status.IMPOSSIBLE


class OtherComparable(Comparable):
    def __init__(self, case) -> None:
        super().__init__(case)

    def compare_to(self, other):
        if other.case == Cases.UNKNOWN:
            return Status.UNKNOWN
        elif other.case == Cases.INVISIBLE:
            return Status.PASS
        else:
            if self.case == other.case:
                return Status.PASS
            else:
                return Status.FAIL


class UnknownComparable(Comparable):
    def __init__(self, case=Cases.UNKNOWN) -> None:
        super().__init__(case)
        self.case = Cases.UNKNOWN

    def compare_to(self, other):
        return Status.UNKNOWN


class PrimitiveComparable(Comparable):
    def __init__(self, case=Cases.UNKNOWN) -> None:
        super().__init__(case)
        self.case = Cases.PRIMITIVE

    def compare_to(self, other):
        if self.case == other.case:
            return Status.PASS
        elif other.case == Cases.UNKNOWN:
            return Status.UNKNOWN
        elif other.case == Cases.FUNCTION:
            return Status.PASS
        else:
            return Status.FAIL