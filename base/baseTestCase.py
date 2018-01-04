import unittest

from httpUtil.httpUtil import *
from jsonCompare.compare import CompareData, Comparator


class BaseTestCase(unittest.TestCase):
    def do_compare(self, request_items: RequestItems, expect_code: int, expect_json: dict):
        print(request_items)
        self.res = do_request(request_items)
        print(self.res)

        expect = CompareData(expect_code, expect_json, True)
        actual = CompareData(self.res.status, self.res.json, False)
        print(expect)
        print(actual)

        result = Comparator().compare(expect, actual)
        print(result)

        if result.is_same is False:
            raise Exception("Run Fail!")
        else:
            print("Run Success!")
