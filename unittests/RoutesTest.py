__author__ = 'rgirish2'

import unittest
from Model.Route import Route

source = 'NYC'
destination = 'CHI'
distance = '700'


class RoutesTest(unittest):

    ########################################################
    #   Unittest for the get_distance() method
    ########################################################
    def get_distance_test(self):
        a = Route(source, destination, distance)
        self.assertEquals(a.get_distance(), distance)

    ########################################################
    #   Unittest for the get_source() method
    ########################################################
    def get_source_test(self):
        a = Route(source, destination, distance)
        self.assertEquals(a.get_source(), source)

    ########################################################
    #   Unittest for the get_destination() method
    ########################################################
    def get_destination_test(self):
        a = Route(source, destination, distance)
        self.assertEquals(a.get_destination(), destination)