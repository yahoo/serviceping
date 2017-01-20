#!/usr/bin/env python
# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.

"""
test_serviceping
----------------------------------

Tests for `serviceping` module.
"""
import serviceping
import unittest


# Any methods of the class below that begin with "test" will be executed
# when the the class is run (by calling unittest.main()
class TestServiceping(unittest.TestCase):

    def test_serviceping_calc_deviation(self):
        times = [24.913, 25.120, 25.266, 26.371, 25.237, 24.833, 26.465, 25.053, 25.857, 25.121]
        avg_time = sum(times) / float(len(times))
        print(avg_time)
        print(len(times))
        print(serviceping.StatsList(times).standard_deviation())
        result = serviceping.calc_deviation(times, avg_time)
        self.assertAlmostEqual(result, 0.232, places=3)

    def test_serviceping_calc_deviation_single_item(self):
        times = [24.913]
        avg_time = sum(times) / float(len(times))
        print(avg_time)
        print(len(times))
        print(serviceping.StatsList(times).standard_deviation())
        result = serviceping.calc_deviation(times, avg_time)
        self.assertAlmostEqual(result, 0, places=3)

 
if __name__ == '__main__':
    unittest.main()
