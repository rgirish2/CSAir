__author__ = 'rgirish2'

###############################################################
#   A class representing the metros in the current flight
#   planning application. The metros contains name, code, country
#   continent, timezone, coordinates, population, region.
###############################################################


class Metros (object):

    ###############################################################
    #   Explicit constructor for the metros.
    ###############################################################
    def __init__(self, code, name, country, continent, timezone, coordinates, population, region):
        self.__code = code
        self.__name = name
        self.__continent = continent
        self.__country = country
        self.__timezone = timezone
        self.__coordinates = coordinates                     # Coordinates should be an object in itself
        self.__population = population
        self.__region = region

    ###############################################################
    #   Overriding the __str__ built in method to provide the
    #   correct string representation of the metros instance.
    #   Somewhat equivalent to toString() in Java.
    #   Writing so to make the object json serializable.
    #
    #   @return The string representation of the calling instance
    ###############################################################
    def __str__(self):
        if self is not None:
            self_str = '{"code": ' + str(self.__code)
            self_str += ', "name": ' + str(self.__name)
            self_str += ', "country": ' + str(self.__country)
            self_str += ', "continent": ' + str(self.__continent)
            self_str += ', "timeZone": ' + str(self.__timezone)
            self_str += ', "coordinates": ' + str(self.__coordinates)
            self_str += ', "population": ' + str(self.__population)
            self_str += ', "region": ' + str(self.__region) + '}'

            return self_str
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for code attribute
    #
    #   @return The code of the associated metro object
    ###############################################################
    def get_code(self):
        if self is not None:
            return self.__code
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for name attribute
    #
    #   @return The name of the associated metro object
    ###############################################################
    def get_name(self):
        if self is not None:
            return self.__name
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for country attribute
    #
    #   @return The country of the associated metro object
    ###############################################################
    def get_country(self):
        if self is not None:
            return self.__country
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for continent attribute
    #
    #   @return The continent of the associated metro object
    ###############################################################
    def get_continent(self):
        if self is not None:
            return self.__continent
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for timezone attribute
    #
    #   @return The timezone of the associated metro object
    ###############################################################
    def get_timezone(self):
        if self is not None:
            return self.__timezone
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for coordinates attribute
    #
    #   @return The coordinates of the associated metro object
    ###############################################################
    def get_coordinates(self):
        if self is not None:
            return self.__coordinates
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for population attribute
    #
    #   @return The population of the associated metro object
    ###############################################################
    def get_population(self):
        if self is not None:
            return self.__population
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for region attribute
    #
    #   @return The region of the associated metro object
    ###############################################################
    def get_region(self):
        if self is not None:
            return self.__region
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Method to update the current values of the metro.
    #
    #   @param country
    #   @param timezone
    #   @param continent
    #   @param coordinates
    #   @param population
    #   @param region
    ###############################################################
    def edit_values(self, country, timezone, continent, coordinates, population, region):
        self.__country = country
        self.__timezone = timezone
        self.__continent = continent
        self.__coordinates = coordinates
        self.__population = population
        self.__region = region