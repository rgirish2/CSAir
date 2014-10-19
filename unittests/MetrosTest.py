__author__ = 'rgirish2'

import unittest
from Model.Metros import Metros

code = 'NYC'
name = 'New York City'
country = 'United States of America'
continent = 'North Americas'
timezone = 'Eastern'
coordinates = '{"W" : 50, "S" : 30}'
population = 8000000
region = 1


class MetrosTest(unittest.TestCase):

    ########################################################
    #   Unittest for the get_name() method
    ########################################################
    def test_get_name(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEquals(a.get_name(), name)

    ########################################################
    #   Unittest for the get_code() method
    ########################################################
    def test_get_code(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEquals(a.get_code(), code)

    ########################################################
    #   Unittest for the get_country() method
    ########################################################
    def test_get_country(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEquals(a.get_country(), country)

    ########################################################
    #   Unittest for the get_continent() method
    ########################################################
    def test_get_continent(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEquals(a.get_continent(), continent)

    ########################################################
    #   Unittest for the get_timezone() method
    ########################################################
    def test_get_timezone(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEqauls(a.get_timezone(), timezone)

    ########################################################
    #   Unittest for the get_coordinates() method
    ########################################################
    def test_get_coordinates(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEquals(a.get_coordinates(), coordinates)

    ########################################################
    #   Unittest for the get_population() method
    ########################################################
    def test_get_population(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEqauls(a.get_population(), population)

    ########################################################
    #   Unittest for the get_region() method
    ########################################################
    def test_get_region(self):
        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.assertEqauls(a.get_region(), region)