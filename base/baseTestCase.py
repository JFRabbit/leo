from httpUtils.httpUtil import *
from jsonCompare.compare import CompareData, Comparator


class BaseTestCase(object):
    def do_compare(self, request_items: RequestItems, expect_code: int, expect_json: dict, comparator=None):
        print("\n", "=" * 100, "\n", request_items)
        self.res = do_request(request_items)
        print(self.res)

        expect = CompareData(expect_code, expect_json, True)
        actual = CompareData(self.res.status, self.res.json, False)
        print(expect)
        print(actual)

        if comparator is None:
            result = Comparator().compare(expect, actual)
        else:
            result = comparator.compare(expect, actual)
        print(result)

        if result.is_same is False:
            raise Exception("Run Fail!")
        else:
            print("Run Success!")

        import time
        time.sleep(1)
