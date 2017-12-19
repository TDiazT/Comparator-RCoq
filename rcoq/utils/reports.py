from rcoq.constants import ReportKeys
from rcoq.utils import exp_extract


def generate_report(expression, output: list, interpreter, exec_time=-1, filename="", line=-1):
    sub_report = __generate_sub_report(expression, output)

    return {
        ReportKeys.EXPRESSION: expression,
        ReportKeys.FILENAME: filename,
        ReportKeys.INTERPRETER: interpreter,
        ReportKeys.EXEC_TIME: exec_time,
        ReportKeys.LINE: line,
        ReportKeys.SUB_EXPRESSIONS_REPORT: sub_report
    }


def __generate_sub_report(expression, output):
    sub_expressions = exp_extract.extract_expressions(expression)
    result = []
    for i, out in enumerate(output):
        sub_report = {
            ReportKeys.SUB_EXPRESSION: sub_expressions[i],
            ReportKeys.OUTPUT: out
        }

        result.append(sub_report)

    return result
