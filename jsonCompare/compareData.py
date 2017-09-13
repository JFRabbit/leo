class CompareData(object):
    def __init__(self, code: int, data: dict, is_expect):
        self.code = code
        self.data = data
        self.is_expect = is_expect

    def __str__(self):
        if self.is_expect:
            return "Expect: code:\n\t%s data: %s" % (self.code, self.data)
        return "Actual: code:\n\t%s data: %s" % (self.code, self.data)
