# Copyright (c) 2013-2015, Yahoo Inc.
# Copyrights licensed under the Apache 2.0 License
# See the accompanying LICENSE.txt file for terms.
"""
ServicePing Utility functioins
"""
import logging
import math


LOG = logging.getLogger(__name__)


class StatsList(object):
    """
    A list object that can do statistics on the values
    """
    count = 0
    old_m = 0
    new_m = 0
    old_s = 0
    new_s = 0

    def __init__(self, values=None):
        if values:
            for value in values:
                self.append(value)

    def reset(self):
        """
        Reset the counter
        """
        self.count = 0

    def append(self, value):
        """
        Append a value to the stats list

        Parameters
        ----------
        value : float
            The value to add
        """
        self.count += 1

        if self.count == 1:
            self.old_m = self.new_m = value
            self.old_s = 0
        else:
            self.new_m = self.old_m + (value - self.old_m) / self.count
            self.new_s = self.old_s + (value - self.old_m) * (value - self.new_m)

            self.old_m = self.new_m
            self.old_s = self.new_s

    def mean(self):
        """
        Calculate the mean of the elements

        Returns
        -------
        float
            The mean of the list elements
        """
        if self.count:
            return self.new_m
        return 0.0

    def variance(self):
        """
        Calculate the variance of the elements

        Returns
        -------
        float
            The variance of the list elements
        """
        if self.count > 1:
            return self.new_s / (self.count - 1)
        return 0.0

    def standard_deviation(self):
        """
        Calculate the standard deviation of the elements

        Returns
        -------
        float
            The standard deviation of the list elements
        """
        return math.sqrt(self.variance())


def calc_deviation1(values, average):
    """
    Calculate the standard deviation of a list of values
    @param values: list(float)
    @param average:
    @return:
    """
    # pylint: disable=unused-argument
    status = StatsList(values)
    return status.standard_deviation()


def calc_deviation(values, average):
    """
    Calculate the standard deviation of a list of values
    @param values: list(float)
    @param average:
    @return:
    """
    size = len(values)
    if size < 2:
        return 0
    calc_sum = 0.0

    for number in range(0, size):
        calc_sum += math.sqrt((values[number] - average) ** 2)
    return math.sqrt((1.0 / (size - 1)) * (calc_sum / size))
