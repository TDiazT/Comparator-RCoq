import re

from Comparator.Constants import CASE_INVISIBLE, CASE_ERROR, SEQ_TOKEN, NULL


class ROutputProcessor:
    vec_res_regex = re.compile('\[\d+\]')
    error_regex = re.compile('Error:*')
    flag = False

    def process(self, output):
        result = []
        splitlines = [row.split() for row in output.splitlines()]
        if not splitlines:
            result.append(CASE_INVISIBLE)
            return result

        for line in splitlines:
            for word in line:
                if self.error_regex.match(word):
                    result.append(CASE_ERROR)
                    self.flag = False
                    break
                elif self.vec_res_regex.match(word) is not None:
                    if self.vec_res_regex.match(word).group() == '[1]':
                        if line[1] == '"%s"' % SEQ_TOKEN:
                            if not self.flag:
                                self.flag = True
                            else:
                                result.append(CASE_INVISIBLE)
                        else:
                            result.append(line)
                            self.flag = False
                    else:
                        result[-1].extend(line)
                        self.flag = False
                    break
                elif word == NULL:
                    result.append(NULL)
                    break
                elif word == SEQ_TOKEN:
                    if not self.flag:
                        self.flag = True
                    else:
                        result.append(CASE_INVISIBLE)
                    break
                else:
                    break

        return result