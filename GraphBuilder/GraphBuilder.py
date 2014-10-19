__author__ = 'Neo'

import json
from Model.Metros import Metros
from Model.Route import Route
from Graph.RouteGraph import RouteGraph
from pprint import pprint

METROS_IDENTIFIER = 'metros'
METROS_CODE_IDENTIFIER = 'code'
METROS_NAME_IDENTIFIER = 'name'
METROS_COUNTRY_IDENTIFIER = 'country'
METROS_TIMEZONE_IDENTIFIER = 'timezone'
METROS_CONTINENT_IDENTIFIER = 'continent'
METROS_COORDINATES_IDENTIFIER = 'coordinates'
METROS_POPULATION_IDENTIFIER = 'population'
METROS_REGION_IDENTIFIER = 'region'

ROUTES_IDENTIFIER = 'routes'
ROUTES_PORT_IDENTIFIER = 'ports'
ROUTES_DISTANCE_IDENTIFIER = 'distance'


class GraphBuilder(object):

    ###############################################################
    #   Explicit constructor for the metros.
    #   @fileName The file used to construct this graph.
    ###############################################################
    def __init__(self, fileName):
        self.__fileNameList = []
        self.__fileName = fileName
        self.__routeGraph = None
        self.__fileNameList.append(fileName)

    ###############################################################
    #   Method used to actually build the graph all the internal
    #   data structures used to represent a graph.
    ###############################################################
    def buildgraph(self):
        if self is not None:
            json_data = open(self.__fileName)
            data = json.load(json_data)

            given_metros_list = data[METROS_IDENTIFIER]
            given_routes_list = data[ROUTES_IDENTIFIER]

            self.__routeGraph = RouteGraph()

            for x in given_metros_list:
                a = Metros(x['code'], x['name'], x['country'], x['continent'], x['timezone'], x['coordinates'], x['population'], x['region'])
                self.__routeGraph.add_metros(a)

            for x in given_routes_list:
                ports_list = x['ports']
                distance = x['distance']
                a = Route(ports_list[0], ports_list[1], distance)
                self.__routeGraph.add_route(a)

            self.__routeGraph.generate_metric()
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Method used to extract the route graph that is built in the
    #   previous method.
    ###############################################################
    def get_route_graph(self):
        if self is not None:
            if self.__routeGraph is not None:
                return self.__routeGraph
            else:
                raise Exception('Route graph not create. Please call buildGraph() on this instance.')
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Method used to add more json content to the current instance
    #   of the route graph.
    ###############################################################
    def add_json_content(self, fileName):
        if self is not None:
            self.__fileNameList.append(fileName)

            json_data = open(fileName)
            data = json.load(json_data)

            given_metros_list = data[METROS_IDENTIFIER]
            given_routes_list = data[ROUTES_IDENTIFIER]

            if self.__routeGraph is None:
                self.__routeGraph = RouteGraph()

            for x in given_metros_list:
                a = Metros(x['code'], x['name'], x['country'], x['continent'], x['timezone'], x['coordinates'], x['population'], x['region'])
                self.__routeGraph.add_metros(a)

            for x in given_routes_list:
                ports_list = x['ports']
                distance = x['distance']
                a = Route(ports_list[0], ports_list[1], distance)
                self.__routeGraph.add_route(a)

            self.__routeGraph.generate_metric()
        else:
            raise Exception('Uninitialized instance.')


def main():
    a = GraphBuilder('../map_data.json')
    a.buildgraph()
    initial = a.get_route_graph().get_all_cities()
    a.get_route_graph().removeExistingCity('BOG')
    final = a.get_route_graph().get_all_cities()
    print (initial)
    print (final)
    cities = ['LON', 'NyC', 'maD', 'par']
    result = a.get_route_graph().inferRouteInformation(cities)
    print (result)
    allMeteros = a.get_route_graph().get_all_metros_jsonlist()
    print (allMeteros)

if __name__ == '__main__':
    main()