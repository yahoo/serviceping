#!/usr/bin/env python
# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.

"""
test_serviceping
----------------------------------

Tests for `serviceping` module.
"""
import serviceping.commandline
import sys
import unittest


# Any methods of the class below that begin with "test" will be executed
# when the the class is run (by calling unittest.main()
class TestServiceping(unittest.TestCase):

    def test_commandline(self):
        sys.argv = ['serviceping', 'yahoo.com']
        options, args = serviceping.commandline.parse_arguments()
        print(options)
        print(args)
        self.assertEqual(args[0], 'yahoo.com')
        self.assertEqual(options.count, 0)


if __name__ == '__main__':
    unittest.main()
