__author__ = 'rgirish2'

from flask import Flask, render_template, request, Response, make_response
from GraphBuilder.GraphBuilder import GraphBuilder
from Graph.RouteGraph import RouteGraph
from pprint import pprint
import json

UPLOAD_FOLDER = '../uploadedFiles/'
MAX_CONTENT_LENGTH = 1024 * 1024 * 5
ALLOWED_EXTENSIONS = set(['json'])
FILENAME = '../map_data.json'

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

GRAPH = GraphBuilder(FILENAME)
GRAPH.buildgraph()
ROUTEGRAPH = GRAPH.get_route_graph()
ALL_CITIES = ROUTEGRAPH.get_all_cities()
ALL_CITIES_DATA = ROUTEGRAPH.get_metros()
ALL_ROUTES_DATA = ROUTEGRAPH.get_routes()

###############################################################
#   Primary controller to render the homepage of the application.
#
###############################################################
@app.route('/', methods=['GET'])
def maybe():
    initApp(FILENAME)
    return render_template('info.html', cities=ALL_CITIES, allcities=ALL_CITIES_DATA, allroutes=ALL_ROUTES_DATA)


###############################################################
#   Method to verify if the uploaded file is in the 
#   allowed formats or not.
###############################################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


###############################################################
#   Controller to allow the users to upload their own json
#   files and use the app. Otherwise they can use the default
#   data set.
###############################################################
@app.route('/upload', methods=['POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(UPLOAD_FOLDER)
        return render_template('info.html')
    else:
        return 'Wrong upload method. Use POST.'


###############################################################
#   Method to initialize all the variables and other metrics
#   used by the application at runtime.
###############################################################
def initApp(filename):
    a = GraphBuilder(filename)
    a.buildgraph()
    b = a.get_route_graph()
    if isinstance(b, RouteGraph):
        return b
    else:
        raise Exception('incorrect type.')


###############################################################
#   Controller to get all the city data inside the default 
#   data-set.
###############################################################
@app.route('/allcitydata', methods=['GET'])
def getAllCityData():
    allCityData = ROUTEGRAPH.get_all_metros_jsonlist()
    return Response(json.dumps(allCityData, default=lambda o: o.__dict__), mimetype='application/json')


###############################################################
#   Controller to get all the routes data inside the default
#   data-set.
###############################################################
@app.route('/allroutedata', methods=['GET'])
def getAllRouteData():
    allRouteData = ROUTEGRAPH.get_all_routes_jsonlist()
    return Response(json.dumps(allRouteData), mimetype='application/json')


###############################################################
#   Controller to respond to request for more information about
#   a particular city from the user.
###############################################################
@app.route('/cityinfo', methods=['GET'])
def getCityInfo():
    cityName = request.args.get('cityname')
    cityInfo = ROUTEGRAPH.get_city_info(cityName)
    return Response(json.dumps(cityInfo, default=lambda o: o.__dict__), mimetype='application/json')


###############################################################
#   Controller to respond to request about further connections
#   from a city by the user.
###############################################################
@app.route('/cityconnections', methods=['GET'])
def getcityconnections():
    cityName = request.args.get('cityname')
    cityConnections = ROUTEGRAPH.get_reachable_cities(cityName)
    return Response(json.dumps(cityConnections), mimetype='application/json')


###############################################################
#   Controller to respond to the download requests from the
#   user.
###############################################################
@app.route('/download', methods=['GET'])
def downloadAsJson():
    data = ROUTEGRAPH.getCompleteJson()
    response = make_response(data)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=flights.json"
    return response


###############################################################
#   Method that allows the user to write the complete CSAir
#   network to disk.
###############################################################
@app.route('/writeToDisk', methods=['POST'])
def writeToDisk():
    result = ROUTEGRAPH.getCompleteJson()
    filename = request.form.get('filename')
    f = open(filename, 'w')
    f.write(result)
    f.close()
    return 'OK'


###############################################################
#   Method that allows the user to infer details about a route
#   in the CSAIR network.
###############################################################
@app.route('/routeDetails', methods=['GET'])
def getRouteDetails():
    originCode = request.args.get('origin')
    destinationCode = request.args.get('destination')
    cities = list()
    cities.append(originCode)
    cities.append(destinationCode)
    details = ROUTEGRAPH.inferRouteInformation(cities)
    return Response(json.dumps(details), mimetype='application/json')


###############################################################
#   Method that allows the user to add a new city to the CS-AIR
#   network.
###############################################################
@app.route('/addCity', methods=['POST'])
def addNewCity():
    code = request.form.get('code')
    name = request.form.get('name')
    country = request.form.get('country')
    timezone = int(request.form.get('timezone'))                    # Check the value is an int before performing the conversion.
    continent = request.form.get('continent')
    coordinates = request.form.get('coordinates')
    population = int(request.form.get('population'))                # Check the value is an int before performing the conversion.
    region = int(request.form.get('region'))                        # Check the value is an int before performing the conversion.
    ROUTEGRAPH.addNewCity(code, name, country, timezone, continent, coordinates, population, region)
    return 'OK'


###############################################################
#   Method that allows the user to add a new route to the CSAIR
#   network.
###############################################################
@app.route('/addRoute', methods=['POST'])
def addNewRoute():
    source = request.form.get('originCode')
    destination = request.form.get('destinationCode')
    distance = float(request.form.get('distance'))                    # Check the value is a float before performing the conversion.
    direction = request.form.get('direction')
    ROUTEGRAPH.addNewRoute(source, destination, distance, direction)
    return 'OK'


###############################################################
#   Method that allows the user to remove an existing city from
#   the CSAIR network.
###############################################################
@app.route('/removeCity', methods=['DELETE'])
def removeExistingCity():
    city = request.form.get('city')
    ROUTEGRAPH.removeExistingCity(city)
    return 'OK'


###############################################################
#   Method that allows the user to edit an existing city from
#   the CSAIR network.
###############################################################
@app.route('/editCity', methods=['POST'])
def editExistingCity():
    code = request.form.get('code')
    country = request.form.get('country')
    timezone = request.form.get('timezone')
    continent = request.form.get('continent')
    coordinates = request.form.get('coordinates')
    population = int(request.form.get('population'))                # Check the value is an int before performing the conversion.
    region = int(request.form.get('region'))                        # Check the value is an int before performing the conversion.
    ROUTEGRAPH.editExistingCity(code, country, timezone, continent, coordinates, population, region)
    return 'OK'


###############################################################
#   Method that runs the app.
#   You know what it is.
###############################################################
if __name__ == '__main__':
    app.run(debug='false')      # Set to true when doing local development and testing.
