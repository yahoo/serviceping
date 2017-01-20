#!/usr/bin/env python
# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
"""
test serviceping network scan
"""
from __future__ import print_function
from serviceping.network import scan, ScanFailed
import unittest


# Any methods of the class below that begin with "test" will be executed
# when the the class is run (by calling unittest.main()
class TestServicepingScan(unittest.TestCase):

    def test_serviceping_scan_exception(self):
        with self.assertRaises(ScanFailed):
            result = scan('localhost', port=65500)
            print(result) 
        

if __name__ == '__main__':
    unittest.main()
