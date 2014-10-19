__author__ = 'rgirish2'

from Model.Metros import Metros
from Model.Route import Route
import jsonpickle


class GraphEntry(object):

    ###############################################################
    #   The default constructor for the GraphEntry.
    #   @param index Represents the index of this object in the
    #                   metros list.
    ###############################################################
    def __init__(self, index):
        self.index = index
        self.connections = []
        self.distances = []
        self.routeIndices = []


class RouteGraph(object):

    ###############################################################
    #   The default constructor for the RouteGraph.
    ###############################################################
    def __init__(self):
        self.__metros = []                      # List of all the metros served in this air network.
        self.__routes = []                      # List of all the routes in this network.

        self.__metrics = {}                     # Dictionary to hold all the metrics information.

        self.__completeGraph = {}               # Dictionary representing the complete network graph as adjacency list.
        self.__metros_dict = {}                 # Dictionary between metro name and metro code.

    ###############################################################
    #   The method to add metros to the current instance of
    #   RouteGraph. Raises exception if the instance is None.
    ###############################################################
    def add_metros(self, metro):
        if isinstance(metro, Metros):
            name = metro.get_name().lower()
            code = metro.get_code().lower()
            index = len(self.__metros)

            self.__metros_dict[name] = code

            oneEntry = GraphEntry(index)
            self.__completeGraph[code] = oneEntry

            self.__metros.append(metro)
        else:
            raise Exception('Incorrect object passed.')

    ###############################################################
    #   The method to add routes to the current instance of
    #   RouteGraph. Raises exception if the instance is None.
    ###############################################################
    def add_route(self, route):
        if isinstance(route, Route):
            source = route.get_source().lower()
            destination = route.get_destination().lower()
            distance = route.get_distance()
            routeIndex = len(self.__routes)

            sourceEntry = self.__completeGraph[source]
            destinationEntry = self.__completeGraph[destination]

            sourceEntry.connections.append(destination)
            sourceEntry.distances.append(distance)
            sourceEntry.routeIndices.append(routeIndex)

            destinationEntry.connections.append(source)
            destinationEntry.distances.append(distance)
            destinationEntry.routeIndices.append(routeIndex)

            self.__routes.append(route)

        else:
            raise Exception('Incorrect object passed.')

    ###############################################################
    #   The method to retrieve metros list from the current instance
    #   of RouteGraph. Raises exception if the instance is None.
    ###############################################################
    def get_metros(self):
        if self is not None:
            return self.__metros
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   The method to retrieve routes list from the current instance
    #   of RouteGraph. Raises exception if the instance is None.
    ###############################################################
    def get_routes(self):
        if self is not None:
            return self.__routes
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   The method to get the count of routes in the current instance
    #   of RouteGraph. Raises exception if the instance is None.
    ###############################################################
    def get_route_count(self):
        if self is not None:
            return len(self.__routes)
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   The method to retrieve information about a specific city
    #   in the current instance of RouteGraph.
    #
    #   @return A string representation of the information about the
    #            queried city.
    #
    #   Raises exception if the instance is None or if the city
    #   being queried for is not available.
    ###############################################################
    def get_city_info(self, cityname):
        if self is not None:
            cityname = cityname.lower()

            if cityname in self.__metros_dict:
                cityname = self.__metros_dict[cityname]

            if cityname in self.__completeGraph:
                cityEntry = self.__completeGraph[cityname]
                index = cityEntry.index
                return self.__metros[index]

            else:
                raise Exception('City does not exist.')
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Get a list of all the cities in the current instance of the
    #   RouteGraph.
    #
    #   @return A list of all the cities in the RouteGraph
    #
    #   Raises exception if the instance is None.
    ###############################################################
    def get_all_cities(self):
        if self is not None:
            return self.__metros_dict.keys()
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Get a list of all the cities in the current instance of the
    #   RouteGraph that are reachable from the given cityname.
    #
    #   @return A list of all the cities in the RouteGraph reachable
    #            from given parameter
    #
    #   Raises exception if the instance is None or city does not
    #   exists.
    ###############################################################
    def get_reachable_cities(self, cityname):
        if self is not None:
            cityname = cityname.lower()

            if cityname in self.__metros_dict:
                cityname = self.__metros_dict[cityname]

            if cityname in self.__completeGraph:
                cityEntry = self.__completeGraph[cityname]
                retval = []
                for x in cityEntry.connections:
                    retval.append(x.upper())
                return retval

            else:
                raise Exception('City does not exist.')

        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Method to generate all the metrics associated with this
    #   instance and store it in the metrics dictionary.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def generate_metric(self):
        if self is not None:
            if self.__routes is not None and self.__metros is not None:
                longestFlightDistance = 0
                longestFlightIndex = 0
                shortestFlightDistance = self.__routes[0].get_distance()
                shortestFlightIndex = 0
                totalDistanceSum = 0
                biggestCityPopulation = 0
                biggestCityIndex = 0
                smallestCityPopulation = self.__metros[0].get_population()
                smallestCityIndex = 0
                totalPopulation = 0
                continentDict = {}
                hubCitySize = 0
                hubCityIndex = list()

                for x in self.__routes:
                    currentDistance = x.get_distance()
                    totalDistanceSum = totalDistanceSum + currentDistance
                    if currentDistance > longestFlightDistance:
                        longestFlightDistance = currentDistance
                        longestFlightIndex = self.__routes.index(x)

                    if currentDistance < shortestFlightDistance:
                        shortestFlightDistance = currentDistance
                        shortestFlightIndex = self.__routes.index(x)

                for x in self.__metros:
                    currentPopulation = x.get_population()
                    totalPopulation = totalPopulation + currentPopulation
                    if currentPopulation > biggestCityPopulation:
                        biggestCityPopulation = currentPopulation
                        biggestCityIndex = self.__metros.index(x)

                    if currentPopulation < smallestCityPopulation:
                        smallestCityPopulation = currentPopulation
                        smallestCityIndex = self.__metros.index(x)

                    currentContinent = x.get_continent()
                    if currentContinent in continentDict:
                        cities = continentDict[currentContinent]
                        cities.append(x.get_name())
                        continentDict[currentContinent] = cities
                    else:
                        cities = list()
                        cities.append(x.get_name())
                        continentDict[currentContinent] = cities

                for oneEntry in self.__completeGraph:
                    x = self.__completeGraph[oneEntry]
                    connectionsSize = len(x.connections)
                    if connectionsSize > hubCitySize:
                        hubCitySize = connectionsSize
                        del hubCityIndex[:]
                        hubCityIndex.append(x.index)
                    elif connectionsSize == hubCitySize:
                        hubCityIndex.append(x.index)

                self.__metrics['longest_flight'] = longestFlightIndex
                self.__metrics['shortest_flight'] = shortestFlightIndex
                self.__metrics['average_distance'] = totalDistanceSum/len(self.__routes)
                self.__metrics['biggest_city'] = biggestCityIndex
                self.__metrics['smallest_city'] = smallestCityIndex
                self.__metrics['avg_population'] = totalPopulation/len(self.__metros)
                self.__metrics['continent_breakdown'] = continentDict
                self.__metrics['hub_cities'] = hubCityIndex
                return

            else:
                raise Exception('Structure is not defined. Try calling add_metros and add_routes.')
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Method to get information about the longest flight in all
    #   the routes in the CSAIR network.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def get_longest_flight(self):
        if 'longest_flight' in self.__metrics:
            longestFlightIndex = self.__metrics['longest_flight']
            return self.__routes[longestFlightIndex]
        else:
            raise Exception('Please call generate_metrics() before calling any specific metrics.')

    ###############################################################
    #   Method to get information about the shortest flight in all
    #   the routes in the CSAIR network.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def get_shortest_flight(self):
        if 'shortest_flight' in self.__metrics:
            shortestFlightIndex = self.__metrics['shortest_flight']
            return self.__routes[shortestFlightIndex]
        else:
            raise Exception('Please call generate_metrics() before calling any specific metrics.')

    ###############################################################
    #   Method to get information about the average flight distance
    #   among all the routes in the CSAIR network.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def get_average_distance(self):
        if 'average_distance' in self.__metrics:
            averageDistance = self.__metrics['average_distance']
            return averageDistance
        else:
            raise Exception('Please call generate_metrics() before calling any specific metrics.')

    ###############################################################
    #   Method to get information about the biggest city by population
    #   among all the cities in the CSAIR network.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def get_biggest_city(self):
        if 'biggest_city' in self.__metrics:
            biggestCityIndex = self.__metrics['biggest_city']
            return self.__metros[biggestCityIndex]
        else:
            raise Exception('Please call generate_metrics() before calling any specific metrics.')

    ###############################################################
    #   Method to get information about the smallest city by population
    #   among all the cities in the CSAIR network.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def get_smallest_city(self):
        if 'smallest_city' in self.__metrics:
            smallestCityIndex = self.__metrics['smallest_city']
            return self.__metros[smallestCityIndex]
        else:
            raise Exception('Please call generate_metrics() before calling any specific metrics.')

    ###############################################################
    #   Method to get information about the average city population
    #   among all the cities in the CSAIR network.
    #
    #   Raises exception if the current instance is uninitialized.
    ###############################################################
    def get_average_population(self):
        if 'avg_population' in self.__metrics:
            avgCityPopulation = self.__metrics['avg_population']
            return avgCityPopulation
        else:
            raise Exception('Please call generate_metrics() before calling any specific metrics.')

    ###############################################################
    #   To get the list of all the metros as metros json rather than
    #   strings.
    #
    #   @return A list of metros object contained in this routeGraph
    ###############################################################
    def get_all_metros_jsonlist(self):
        if self is not None:
            retval = []
            for x in self.__metros:
                retval.append(jsonpickle.encode(x, unpicklable=False))
            return retval
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   To get the list of routes as a routes json rather than
    #   strings.
    #
    #   @return A list of routes object contained in this routeGraph
    ###############################################################
    def get_all_routes_jsonlist(self):
        if self is not None:
            retval = []
            for x in self.__routes:
                retval.append(jsonpickle.encode(x, unpicklable=False))
            return retval
        else:
            raise Exception('Uninitialized instance.')

    ###############################################################
    #   Method to remove an existing city from the CSAir network.
    #
    #   @param cityname The city that needs to be removed.
    ###############################################################
    def removeExistingCity(self, cityname):
        cityname = cityname.lower()

        if cityname in self.__metros_dict:
            cityname = self.__metros_dict[cityname]

        if cityname in self.__completeGraph:
            cityEntry = self.__completeGraph[cityname]

            routes = cityEntry.routeIndices                 # Removed the routes associated with this city from the
            for x in routes:                                # routes list.
                oneRoute = self.__routes[x]
                if oneRoute in self.__routes:
                    self.__routes.remove(oneRoute)

            connections = cityEntry.connections             # Removed the city from the connecting cities entries
            for x in connections:                           # in the completeGraph dictionary.
                if x in self.__completeGraph:
                    x = self.__completeGraph[x]
                    connectionList = x.connections
                    distanceList = x.distances
                    routeIndexList = x.routeIndices
                    if cityname in connectionList:
                        index = connectionList.index(cityname)
                        del connectionList[index]
                        del distanceList[index]
                        del routeIndexList[index]

            index = cityEntry.index                         # Remove the city from the list of metros available to the
            name = self.__metros[index].get_name()          # complete network. Getting the so that we can remove this
            del self.__metros[index]                        # city's entry from the metro_dict.

            self.__completeGraph.pop(cityname, None)        # Remove the city entry from the complete graph dictionary.

            self.__metros_dict.pop(name.lower(), None)      # Remove the entry of this city from the metro_dict.
        else:
            raise Exception('City does not exist.')

    ###############################################################
    #   Method to remove an existing route from the CSAir network.
    #
    #   @param source The city that is the source of the route.
    #   @param destination The city that is the destination of the
    #                       route to be removed.
    ###############################################################
    def removeExistingRoute(self, source, destination):
        source = source.lower()
        destination = destination.lower()
        if source and destination in self.__completeGraph:
            sourceEntry = self.__completeGraph[source]
            destinationEntry = self.__completeGraph[destination]
            routeIndex = 0

            if destination in sourceEntry.connections:
                index = sourceEntry.connections.index(destination)
                del sourceEntry.connections[index]
                del sourceEntry.distances[index]
                del sourceEntry.routeIndices[index]
            else:
                raise Exception('No route between source and destination.')

            if source in destinationEntry.connections:
                index = destinationEntry.connections.index(source)
                routeIndex = destinationEntry.routeIndices[index]
                del destinationEntry.connections[index]
                del destinationEntry.distances[index]
                del destinationEntry.routeIndices[index]
            else:
                raise Exception('No route between source and destination.')

            del self.__routes[routeIndex]
        else:
            raise Exception('Source or destination does not exist.')

    ###############################################################
    #   Method to add a new city to the CSAir network.
    #
    #   @param code The code for the new city.
    #   @param name The name of the city.
    #   @param country The country of the new city.
    #   @param timezone The timezone of the new city.
    #   @param continent The continent of the new city.
    #   @param coordinated The coordinates of the new city.
    #   @param population The population of the new city.
    #   @param region The region of the new city.
    ###############################################################
    def addNewCity(self, code, name, country, timezone, continent, coordinates, population, region):
        code = code.lower()
        name = name.lower()

        if code in self.__completeGraph:
            raise Exception('City already exists.')

        if name in self.__metros_dict:
            raise Exception('City already exists.')

        if population < 0 or region < 0:
            raise Exception('Incorrect population or region field value.')

        a = Metros(code, name, country, continent, timezone, coordinates, population, region)
        self.add_metros(a)

    ###############################################################
    #   Method to add a new route to the CSAir network.
    #
    #   @param source The source for the new route.
    #   @param destination The destination for the new route.
    #   @param distance The distance for the new route.
    ###############################################################
    def addNewRoute(self, source, destination, distance, direction):
        source = source.lower()
        destination = destination.lower()

        if distance <= 0:
            raise Exception('Incorrect value of distance provided.')

        if source == destination:
            raise Exception('Routes between same source and destination not possible')

        if source not in self.__completeGraph:
            raise Exception('Source does not exist in the network.')

        if destination not in self.__completeGraph:
            raise Exception('Destination does not exist in the network.')

        newRoute = Route(source, destination, distance)
        self.add_route(newRoute)

    ###############################################################
    #   Method to edit an existing city in the CSAir network.
    #
    #   @param code The code of the city being edited.
    #   @param country The new country of the city.
    #   @param timezone The new timezone of the city.
    #   @param continent The new continent of the city.
    #   @param coordinates The new coordinates of the city.
    #   @param population The population of the city.
    #   @param region The new region of the city.
    ###############################################################
    def editExistingCity(self, code, country, timezone, continent, coordinates, population, region):
        code = code.lower()
        if code in self.__completeGraph:
            index = self.__completeGraph[code].index
            currentInstance = self.__metros[index]
            currentInstance.edit_values(country, timezone, continent, coordinates, population, region)
        else:
            raise Exception('City could not be found in the current network.')

    ###############################################################
    #   Method to get the complete information the CSAir network.
    #   This returns a json string that could be written to disk
    #   or anything else the user wants to do with it.
    ###############################################################
    def getCompleteJson(self):
        retval = dict()
        retval["metros"] = self.get_all_metros_jsonlist()
        retval["routes"] = self.get_all_routes_jsonlist()
        return jsonpickle.encode(retval)

    ###############################################################
    #   Method to get the shortest route between the origin and
    #   destination cities in the CSAir network. This value is
    #   calculated using the Dijkstra's Algorithm.
    #
    #   @param origin The start of the route.
    #   @param destination The end of the route.
    ###############################################################
    def shortestRoute(self, origin, destination):
        origin = origin.lower()
        destination = destination.lower()
        allNodes = self.__completeGraph.keys()
        allNodesVisited = []
        allNodesDistance = []
        for x in allNodes:
            if x is not origin:
                allNodesDistance.append(-1)
                allNodesVisited.append(False)
            else:
                allNodesDistance.append(0)
                allNodesVisited.append(True)


        return ""

    ###############################################################
    #   Method to evaluate route information about a route of
    #   multiple cities in the CSAir network.
    #
    #   @param cities An ordered list of cities that represents the
    #           route requested by the user.
    ###############################################################
    def inferRouteInformation(self, cities):
        if len(cities) < 2:
            raise Exception('Information could be calculated for empty route.')

        cities = [oneCity.lower() for oneCity in cities]

        x = 0
        y = 1
        totalCost = 0.0
        totalTime = 0.0
        initalFactor = 0.35

        while y < len(cities):
            if cities[x] and cities[y] in self.__completeGraph:
                sourceEntry = self.__completeGraph[cities[x]]
                destinations = sourceEntry.connections
                if cities[y] in destinations:
                    index = destinations.index(cities[y])
                    distance = sourceEntry.distances[index]
                    flyingTime = self.getFlyingTime(cities[x], cities[y])
                    layoverTime = self.getLayoverTime(cities[y])
                    totalTime += flyingTime + layoverTime
                    if initalFactor == 0.0:
                        break
                    else:
                        totalCost += (distance * initalFactor)
                        initalFactor -= 0.05
                        x += 1
                        y += 1
                else:
                    raise Exception('No route between ' + cities[x] + ' and ' + cities[y])
            else:
                raise Exception('Cities not found in network.')

        retval = dict()
        retval['totalCost'] = totalCost
        retval['totalTime'] = totalTime
        return retval

    ###############################################################
    #   Helper function to calculate layover time at the given
    #   airport.
    #
    #   @param city The city at which layover time needs to be calculated.
    ###############################################################
    def getLayoverTime(self, city):
        city = city.lower()
        if city in self.__completeGraph:
            cityEntry = self.__completeGraph[city]
            connections = cityEntry.connections
            outboundCount = len(connections)
            if outboundCount <= 0:
                return 0
            elif outboundCount == 1:
                return 2
            else:
                result = 2.0 - (outboundCount * (1/6))
                if result < 0:
                    return 0
                else:
                    return result
        else:
            raise Exception('City not found in the network.')

    ###############################################################
    #   Helper function to calculate the flying time between the
    #   given pair of cities.
    #
    #   @param origin The starting city.
    #   @param destination The ending city.
    ###############################################################
    def getFlyingTime(self, origin, destination):
        origin = origin.lower()
        destination = destination.lower()
        if origin and destination in self.__completeGraph:
            sourceEntry = self.__completeGraph[origin]
            if destination in sourceEntry.connections:
                index = sourceEntry.connections.index(destination)
                distance = sourceEntry.distances[index]
                if distance <= 400:
                    return (distance/750.0) * 2.0
                else:
                    initialTime = (8.0/15.0) * 2.0
                    cruiseTime = (distance - 400.0)/750.0
                    return initialTime + cruiseTime
            else:
                raise Exception('Not path found between source and destination.')
        else:
            raise Exception('Cities could not be found in the route network.')