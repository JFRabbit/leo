import unittest
import time


class BaseSuite(object):
    def __init__(self, run_classes):
        self.run_classes = run_classes  # type: dict

    def run(self):
        print("\n\n Test Start \n ------------------------------------------------------------> ")

        suite = unittest.TestSuite()
        for case, is_run in self.run_classes.items():

            test = unittest.TestLoader().loadTestsFromTestCase(case)
            if is_run == 1:
                suite.addTest(test)
                print("Run Case: %s", test)
            elif is_run == 0:
                print("Not Run Case: %s", test)
                pass
            else:
                raise Exception("Wrong Arguments! 0:not run, 1:run")

        unittest.TextTestRunner().run(suite)
        time.sleep(1)
        print("\n\n <------------------------------------------------------------ \nTest End\n\n\n ")
