class CompareError(object):
    def __init__(self, error_path: str, error_code: str, error_msg: str):
        self.error_path = error_path
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return "\n\terrorPath:\t%s\n\terrorCode:\t%s\n\terrorMsg:\n%s" % (self.error_path, self.error_code, self.error_msg)
