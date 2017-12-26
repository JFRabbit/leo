import re
import datetime

from jsonCompare.data import *
from jsonCompare.compareConstant import *
from jsonCompare.compareData import *
from jsonCompare.compareError import *
from jsonCompare.ruleEnum import *


class Comparator(object):
    def __init__(self):
        self.is_same = True
        self.error_msg = ""
        self.__path = ""
        self.__rule_dict = {}  # type: dict

    def __str__(self):
        if self.is_same:
            return "\nIsSame:\n\t%s" % (self.is_same)
        return "\nIsSame:\n\t%s\nErrorMsg:%s\n" % (self.is_same, self.error_msg)

    def set_rule(self, key: str, rule: Rule, regex=None):
        """
        Set Compare Rule
        :param key: key of json, default use "root"
        :param rule: Rule Enum
        :param regex: if Rule is MATCH_REGEX
        :return:
        """
        if regex == None:
            self.__rule_dict[key] = rule
        else:
            self.__rule_dict[key] = rule + regex

    def compare(self, expect: CompareData, actual: CompareData):
        """
        :param expect: 预期
        :param actual: 实际
        :return: True False
        """

        print(expect)
        print(actual)

        self.__path += PATH_ROOT

        # 判断Response Code

        if expect.code != actual.code:
            self.is_same = False
            self.__set_error(
                CompareError(self.__path, RESPONSE_CODE_DIFF, self.__set_error_msg(expect.code, actual.code)))
            return self

        self.__compare_json(expect.data, actual.data)

        if len(self.error_msg) != 0:
            self.is_same = False
            pass

        print(self)
        return self

    def __compare_json(self, expect: dict, actual: dict):

        # 对比json object
        self.__compare_obj(PATH_ROOT, expect, actual)

        pass

    def __compare_obj(self, key: str, expect: dict, actual: dict):
        if self.__rule_dict.get(key) == Rule.IGNORE_VALUE or self.__rule_dict.get(key) == Rule.IS_JSON_OBJECT:
            return

        self.__path += PATH_OBJECT

        # 判断Response 的json字段长度
        if self.__rule_dict.get(key) == Rule.IGNORE_OBJECT_KEY_MISS_MATCH:
            pass
        else:
            if expect.keys() != actual.keys():
                print(key)
                self.__set_error(
                    CompareError(self.__path, KEY_NOT_MATCH, self.__set_error_msg(expect.keys(), actual.keys())))
                return

        # 遍历
        index = -1
        current_path = self.__path

        for (k, v) in expect.items():
            index += 1
            self.__path = current_path

            if self.__is_primitive(v):
                if self.__compare_primitive(v, actual.get(k), self.__rule_dict.get(k)):
                    pass
                else:
                    self.__path += "[%d][%s]" % (index, k)
                    self.__set_error(CompareError(self.__path, VALUE_DIFF, self.__set_error_msg(v, actual.get(k))))
                continue

            if isinstance(v, dict):
                self.__compare_obj(k, v, actual.get(k))
                continue

            if isinstance(v, list):
                self.__path += PATH_ARRAY + "[%s]" % k
                self.__compare_list(k, v, actual.get(k))
                continue

        pass

    def __compare_list(self, key: str, expect: list, actual: list, isCheckOne=False):
        if self.__rule_dict.get(key) == Rule.IS_JSON_ARRAY or self.__rule_dict.get(key) == Rule.IGNORE_VALUE:
            return

        # key += PATH_ROOT

        if isCheckOne or self.__rule_dict.get(key) == Rule.IGNORE_ARRAY_SIZE:
            self.__path += "[0]"
            i = expect[0]
            if isinstance(i, dict):
                key += SUB_OBJ
                self.__compare_obj(key, i, actual[0])
                return

            if isinstance(i, list):
                self.__path += PATH_ARRAY
                self.__compare_list(key, i, actual[0])
                return

        else:
            if len(expect) != len(actual):
                self.__set_error(
                    CompareError(self.__path, ARRAY_SIZE_DIFF, self.__set_error_msg(len(expect), len(actual))))
                return

        current_path = self.__path
        for i in expect:
            self.__path = current_path
            self.__path += "[%d]" % (expect.index(i))

            if isinstance(i, dict):
                key += SUB_OBJ
                self.__compare_obj(key, i, actual[expect.index(i)])
                continue

            if isinstance(i, list):
                self.__path += PATH_ARRAY
                self.__compare_list(key, i, actual[expect.index(i)])
                continue

        pass

    def __compare_primitive(self, expect, actual, regex):
        if expect == Rule.IS_JSON_PRIMITIVE.value or expect == Rule.IGNORE_VALUE.value:
            return True

        if expect != actual:
            if expect == Rule.IS_ANY_INTEGER.value and isinstance(actual, int):
                return True

            if expect == Rule.IS_ANY_FLOAT.value and isinstance(actual, float):
                return True

            if expect == Rule.IS_ANY_STRING.value and isinstance(actual, str):
                return True

            if expect == Rule.IS_TIMESTEMP.value:
                try:
                    datetime.datetime.strptime(actual, '%Y-%m-%d %H:%M:%S')
                    return True
                except ValueError:
                    pass

            if str(expect).startswith(str(Rule.MATCH_REGEX.value)):
                # pattern = re.compile(expect[len(str(Rule.MATCH_REGEX.value)):])
                # return pattern.match(actual) != None
                return re.search(expect[len(str(Rule.MATCH_REGEX.value)):], actual)

            return False
        else:
            return True

    def __set_error_msg(self, expect, actual):
        return "\t\tExpect: %s\n\t\tActual: %s" % (expect, actual) + DEBUG_LINE

    def __set_error(self, compareError: CompareError):
        self.error_msg += compareError.__str__()

    def __is_primitive(self, value):
        if isinstance(value, int):
            return True
        if isinstance(value, str):
            return True
        if isinstance(value, bool):
            return True

        return False


if __name__ == '__main__':
    e_data = CompareData(200, expect, True)
    a_data = CompareData(200, actual, False)
    print(e_data)
    print(a_data)

    comparator = Comparator()
    comparator.set_rule(PATH_ROOT, Rule.IGNORE_OBJECT_KEY_MISS_MATCH)
    # comparator.set_rule(PATH_ROOT, Rule.IS_JSON_OBJECT)

    comparator.set_rule("result", Rule.IGNORE_ARRAY_SIZE)
    comparator.set_rule("result" + SUB_OBJ, Rule.IGNORE_OBJECT_KEY_MISS_MATCH)
    # comparator.set_rule("result", Rule.IS_JSON_ARRAY)


    result = comparator.compare(e_data, a_data)
    print(result)
