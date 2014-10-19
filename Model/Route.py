__author__ = 'rgirish2'

###############################################################
#   A class representing the routes in the current flight
#   planning application. The routes contains source,
#   destination and distance between source and destination.
###############################################################


class Route(object):

    ###############################################################
    #   Explicit constructor for the Route.
    ###############################################################
    def __init__(self, source, destination, distance):
        self.__source = source
        self.__destination = destination
        self.__distance = distance

    ###############################################################
    #   Overriding the __str__ built in method to provide the
    #   correct string representation of the route instance.
    #   Somewhat equivalent to toString() in Java.
    #   Writing so to make the object json serializable.
    #
    #   @return The string representation of the calling instance
    ###############################################################
    def __str__(self):
        if self is not None:
            self_str = '{"source": ' + str(self.__source)
            self_str += ', "destination": ' + str(self.__destination)
            self_str += ', "distance:" ' + str(self.__distance) + '}'

            return self_str
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for the source attribute.
    #
    #   @return The source of the current instance.
    ###############################################################
    def get_source(self):
        if self is not None:
            return self.__source
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for the destination attribute.
    #
    #   @return The destination of the current instance.
    ###############################################################
    def get_destination(self):
        if self is not None:
            return self.__destination
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Getter method for the distance attribute.
    #
    #   @return The distance of the current instance.
    ###############################################################
    def get_distance(self):
        if self is not None:
            return self.__distance
        else:
            raise Exception('Uninitialized instance.')