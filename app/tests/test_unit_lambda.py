import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

import lambda_function
import unittest
import json


class LambdaFunctionUnitTests(unittest.TestCase):
    def test_all_indexes_of_hyphen_in_string(self):
        self.assertEqual(lambda_function.all_indexes_of_hyphen_in_string("0-2345-7-9"),[1,6,8])

if __name__ == '__main__':
    unittest.main()