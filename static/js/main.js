/**
 * Set of functions that are executed whenever the document is loaded.
 * They make requests to the server for all the routes and city data
 * and properly renders them in the current DOM.
 */
$(document).ready(function() {
    updateAndRenderCityTable();
    updateAndRenderRouteTable();
});


/**
 * Counter used to properly place the route links the route map table.
 * Allows to show the last 9 random route map requests.
 */
var counter = 0;


/**
 * Function used to generate the route url that is used to render the route
 * map in the route map modal.
 */
function getFlightMapURL() {
    var routesToQuery = $("#flightMap").val().toUpperCase();
    var routesArr = routesToQuery.split(',');
    var URLSuffix = '';
    for (var x = 0; x < routesArr.length; x++) {
        URLSuffix = URLSuffix + '+' + routesArr[x].trim() + ',';
    }

    if (counter == 9) {
        counter = 0;
    }

    var tagID = "#flightMapURL" + counter;
    var completeTag = "<a href='#' id=" + tagID +">View Map for Routes: " + routesToQuery + "</a>";

    $("#putFlightMapURL" + counter).empty();
    $("#putFlightMapURL" + counter).append(completeTag);
    $(tagID).attr('onclick', 'showMapInModal("' + URLSuffix + '", "wls")');
    counter++;
};


/**
 * Shows the route view and hides other elements from the DOM.
 */
function showRouteView() {
    $("#cityInfoForm").hide();
    $("#cityInfoData").hide();
    $("#cityTableDiv").hide();

    $("#downloadFileDiv").hide();

    $("#analyticsDiv").hide();

    $("#routeMapForm").show();
    $("#routeMapURL").show();
    $("#routeTableDiv").show();
};


/**
 * Shows the city view and hides other elements from the DOM.
 */
function showCityView() {
    $("#routeMapForm").hide();
    $("#routeTableDiv").hide();
    $("#routeMapURL").hide();

    $("#downloadFileDiv").hide();

    $("#analyticsDiv").hide();

    $("#cityInfoForm").show();
    $("#cityInfoData").show();
    $("#cityTableDiv").show();
};


/**
 * Shows the analytics view and hides other elements from the DOM.
 */
function showAnalyticsView() {
    $("#routeMapForm").hide();
    $("#routeTableDiv").hide();
    $("#routeMapURL").hide();

    $("#downloadFileDiv").hide();

    $("#cityInfoForm").hide();
    $("#cityInfoData").hide();
    $("#cityTableDiv").hide();

    getNetworkMetrics();
    $("#analyticsDiv").show();
};


/**
 * Shows the export view and hides other elements from the DOM.
 */
function showExportView() {
    $("#routeMapForm").hide();
    $("#routeTableDiv").hide();
    $("#routeMapURL").hide();

    $("#cityInfoForm").hide();
    $("#cityInfoData").hide();
    $("#cityTableDiv").hide();

    $("#analyticsDiv").hide();

    $("#downloadFileDiv").show();
};


/**
 *  Shows the active tag in the sidebar city view navigation button.
 */
$("#showCityView").click(function (event) {
    event.preventDefault();
    removeAndAddActiveClass("showCityViewList");
    showCityView();
});


/**
 * Shows the active tag in the sidebar route view navigation button.
 */
$("#showRouteView").click(function (event) {
    event.preventDefault();
    removeAndAddActiveClass("showRouteViewList");
    showRouteView();
});


/**
 * Shows the active tag in the sidebar analytics view navigation button.
 */
$("#showAnalyticsView").click(function (event) {
    event.preventDefault();
    removeAndAddActiveClass("showAnalyticsViewList");
    showAnalyticsView();
});


/**
 * Shows the active tag in the sidebar export view navigation button.
 */
$("#showExportView").click(function (event) {
    event.preventDefault();
    removeAndAddActiveClass("showExportViewList");
    showExportView();
});


/**
 * Removes the active tag from the sidebar current navigation button.
 */
function removeAndAddActiveClass(id) {
    $("li").removeClass("active");
    $("#" + id).addClass("active");
};


/**
 * Function that requests the server for the city information of the current
 * selected city from the drop-down select tag.
 * If the request is successful, it calls the rendering function to render the
 * city information on the view.
 * Otherwise, it will alert the user of the error.
 *
 * NOTE: Propagate the server side error message to the user, or use the response
 *      code to better inform the user of the issue.
 */
function getCityInfo() {
    var cityname = $("#cityQueryField").val();

    $.ajax({
        url : '/cityinfo',
        data : {cityname : cityname},
        type : 'GET',
        datatype : 'jsonp',
        success : function (response) {
            retval = response;

            $.ajax({
                url : '/cityconnections',
                data : {cityname : cityname},
                type : 'GET',
                datatype : 'jsonp',
                success : function (response) {
                    setCityValue(retval, response);
                },
                error : function (response) {
                    alert('Connections information could not be retrieved.')
                    setCityValue(retval, 0);
                }
            })
        },
        error : function(response) {
            alert('No such city exists.');
        }
    })
};


/**
 * Function used to render all the city information on the view.
 * @param information The dictionary containing all the generic information about a city.
 * @param connections An array containing all the connections of the city.
 */
function setCityValue(information, connections) {
    var name = information['_Metros__name'];
    var code = information['_Metros__code'];
    var continent = information['_Metros__continent'];
    var region = information['_Metros__region'];
    var country = information['_Metros__country'];
    var population = information['_Metros__population'];
    var timezone = information['_Metros__timezone'];
    var coordinates = information['_Metros__coordinates'];

    $("#codeline").empty();
    $("#nameline").empty();
    $("#continentline").empty();
    $("#regionline").empty();
    $("#countryline").empty();
    $("#populationline").empty();
    $("#timezoneline").empty();
    $("#coordinatesline").empty();
    $("#connectionsline").empty();

    $("#nameline").append("Name: " + name);
    $("#codeline").append("Code: " + code);
    $("#continentline").append("Continent: " + continent);
    $("#regionline").append("Region: " + region);
    $("#countryline").append("Country: " + country);
    $("#populationline").append("Population: " + population);
    $("#timezoneline").append("Time Zone: " + timezone);
    $("#coordinatesline").append("Coordinates: " + JSON.stringify(coordinates));

    if (connections == 0) {
        $("#connectionsline").append('Unable to retrieve any.')
    } else {
        var appendStuff = '';
        for (var i = 0; i < connections.length; i++) {
            appendStuff = appendStuff + connections[i] + ' ';
        }
        $("#connectionsline").append("Connections: " + appendStuff);
    }
};


/**
 * Shows the user the modal that allows them to edit the current information
 * about any city in the CSAir network.
 * @param value The index of the city that needs to be edited. Used to grab their
 *              current value from the view and render that in the generic modal.
 */
function editCityView(value) {
    var code = $("#code" + value).text();
    var name = $("#name" + value).text();
    var country = $('#country' + value).text();
    var timezone = $('#timezone' + value).text();
    var continent = $('#continent' + value).text();
    var coordinates = $('#coordinates' + value).text();
    var population = $('#population' + value).text();
    var region = $('#region' + value).text();

    $("#editCityCode").attr('value', code);
    $("#editCityName").attr('value', name);
    $("#editCityCountry").attr('value', country);
    $("#editCityTimeZone").attr('value', timezone);
    $("#editCityContinent").attr('value', continent);
    $("#editCityCoordinates").attr('value', coordinates);
    $("#editCityPopulation").attr('value', population);
    $("#editCityRegion").attr('value', region);

    $("#editCityDeleteButton").attr('onclick', 'deleteCity("' + code + '")');

    $("#editCityModal").modal('show');
    return;
};


/**
 * Makes the request to the server to update the values of a current city in the
 * CSAir network. If the request is successful, it clears and updates the current
 * cities tables. Otherwise, it informs the user of the failure of their request.
 *
 * NOTE: It would be better to propagate the server side error message to the user.
 *      But, it might be a security vulnerability too. Look more into it.
 */
function editCity() {
    // Make ajax request to the server to update the values of the current city.
    var cityname = $('#editCityName').val();
    var code = $('#editCityCode').val();
    var country = $('#editCityCountry').val();
    var timezone = $('#editCityTimeZone').val();
    var continent = $('#editCityContinent').val();
    var coordinates = $('#editCityCoordinates').val();
    var population = $('#editCityPopulation').val();
    var region = $('#editCityRegion').val();

    $.ajax({
        url : '/editCity',
        type: 'POST',
        data : {
            cityname : cityname,
            code : code,
            country : country,
            timezone : timezone,
            continent : continent,
            coordinates : coordinates,
            population : population,
            region : region
        },
        success : function(response) {
            updateAndRenderCityTable();
            updateAndRenderRouteTable();
        },
        error : function(response) {
            alert('Unable to update the city information. Please try again.');
        }
    });

    $("#editCityModal").modal('hide');
    return;
};


/**
 * Function used to delete a current city in the CSAir network.
 * Upon successful deletion of the city, it calls the table update
 * method that updates the data in the city table.
 * If unsuccessful, it will alert the user about the failure.
 * @param code The code of the city that needs to be deleted.
 *
 * NOTE: Would be better to inform the user about exact error that occurred.
 */
function deleteCity(code) {
    // Make an ajax call to the server to delete the requested city from current instance.
    $.ajax({
        url : "/removeCity",
        type : "DELETE",
        data : {
            city : code
        },
        success : function(response) {
            updateAndRenderCityTable();
            updateAndRenderRouteTable();
        },
        error : function(response) {
            alert('Unable to delete the route. Please try again.');
        }
    });

    $("#editCityModal").modal('hide');
    return;
};


/**
 * Function that shows the modal that allows the user to edit the
 * current routes in the CSAir network.
 * @param index The index of the route in the table that needs to be edited.
 */
function editRouteView(index) {
    var origin = $('#routeOriginCode' + index).text();
    var destination = $('#routeDestinationCode' + index).text();
    var distance = $('#routeDistance' + index).text();

    $('#editRouteOrigin').attr('value', origin);
    $('#editRouteDestination').attr('value', destination);
    $('#editRouteDistance').attr('value', distance);

    $("#editRouteModal").modal('show');
    return;
};


/**
 * Edit the values of the current selected route in the CSAir network.
 */
function editRoute() {
    $.ajax({

    });

    updateAndRenderRouteTable ();
    $("#editRouteModal").modal('hide');
};


/**
 * Delete the current selected route from the CSAir network.
 */
function deleteRoute() {
    $.ajax({

    });

    updateAndRenderRouteTable ();
    $("#editRouteModal").modal('hide');
}

/**
 * Function used to show that modal that allows the user to add
 * a new city to the CSAir network.
 */
function addCityView() {
    $("#addCityModal").modal('show');
    return;
};


/**
 * Function that is called whenever the user adds a new city
 * to the CSAir network.
 */
function addCity() {
    var code = $("#addCityCode").val();
    var name = $("#addCityName").val();
    var country = $('#addCityCountry').val();
    var timezone = $('#addCityTimeZone').val();
    var continent = $('#addCityContinent').val();
    var coordinates = $('#addCityCoordinates').val();
    var population = $('#addCityPopulation').val();
    var region = $('#addCityRegion').val();

    $.ajax({
        url : "/addCity",
        type : "POST",
        data : {
            code : code,
            name : name,
            country : country,
            timezone : timezone,
            continent : continent,
            coordinates : coordinates,
            population : population,
            region : region
        },
        success : function(response) {
            updateAndRenderCityTable();
            updateAndRenderRouteTable();
        },
        error : function (response) {
            alert('Unfortunately city cannot be added. Please try again.');
        }
    });

    $("#addCityModal").modal('hide');
};


/**
 * Function used to show the modal that allows the user to add a new route.
 */
function addRouteView() {
    $("#addRouteModal").modal('show');
    return;
};


/**
 * Function that is called whenever the user tries to add a new route
 * to the current CSAir network.
 */
function addRoute() {
    var originCode = $("#addRouteOriginCode").val();
    var destinationCode = $("#addRouteDestinationCode").val();
    var distance = $("#addRouteDistance").val();
    var direction = $("#addRouteDirection").val();

    $.ajax({
        url : "/addRoute",
        type : "POST",
        data : {
            originCode : originCode,
            destinationCode : destinationCode,
            distance : distance,
            direction : direction
        },
        success : function(response) {
            updateAndRenderRouteTable();
        },
        error : function (response) {
            alert('Unfortunately route cannot be added. Please try again.');
        }
    });

    $("#addRouteModal").modal('hide');
};


/**
 * Function that requests route information from the server about the given route.
 * @param origin The origin of the route being queried.
 * @param destination The destination of the route being queried.
 */
function getRouteDetails(origin, destination) {
    $.ajax({
        url : '/routeDetails',
        data : {origin : origin, destination: destination},
        type : 'GET',
        datatype : 'jsonp',
        success: function (response) {
            var cost = response['totalCost'];
            var time = response['totalTime'];

            $("#routeDetailsModalTitle").empty();
            $("#routeDetailsModalTitle").append('Route Details: ' + origin + ' -- ' + destination);

            $("#routeDetailsModalCost").empty();
            $("#routeDetailsModalCost").append('Cost: ' + cost + ' USD');

            $("#routeDetailsModalTime").empty();
            $("#routeDetailsModalTime").append('Time: ' + time + ' hours');

            $("#routeDetailsModal").modal('show');
        },
        error : function(response) {
            alert('No such city exists.');
        }
    })
};


/**
 * Function that is called whenever the user requests to view a route map.
 * @param route The route for which the map is being requested.
 * @param type  The type of map to view. Only 3 possible values:
 *               {'wls->plain view', 'wls2->light plain view', 'bm->blue marble view'}
 *               If any value other than {'wls2', 'bm'} is provided, it defaults to 'wls'.
 */
function showMapInModal(route, type) {
    var imageBaseURL = 'http://www.gcmap.com//map?P=';

    // Choose the correct image end URL based on the type of request from the user.
    var imageEndURL = '';
    if (type === 'wls2') {
        imageEndURL = '&amp;MS=wls2&amp;MR=900&amp;MX=720x360&amp;PM=*';
    } else if (type === 'bm') {
        imageEndURL = '&amp;MS=bm&amp;MR=900&amp;MX=720x360&amp;PM=*';
    } else {
        imageEndURL = '&amp;MS=wls&amp;MR=900&amp;MX=720x360&amp;PM=*';
    }

    var completeURL = imageBaseURL + route + imageEndURL;

    var imageTag = '<img src=' + completeURL + ' alt="map" id="map_image" class="map-image" width="100%" height="100%">';

    // Adding title to the route map modal.
    $("#routeMapModalTitle").empty();
    $("#routeMapModalTitle").append("Route Map for: " + route);

    // Adding the image tab to the image div within the modal content section.
    $("#modalMapDiv").empty();
    $("#modalMapDiv").append(imageTag);

    // Adding the requests to change the map view on the buttons in the modal footer.
    $("#requestPlainViewMap").attr('onclick', 'showMapInModal("' + route + '", "wls")');
    $("#requestLightViewMap").attr('onclick', 'showMapInModal("' + route + '", "wls2")');
    $("#requestBlueMarbleMap").attr('onclick', 'showMapInModal("' + route + '", "bm")');

    $("#routeMapModal").modal('show');
};


/**
 *  Function that is called whenever the data in the cities table is altered. It cleans up
 *  all the current city table data and makes a ajax request for the updated data and
 *  renders it on the view.
 */
function updateAndRenderCityTable() {
    $.ajax({
        url : '/allcitydata',
        type : 'GET',
        datatype : 'jsonp',
        success : function (response) {
            var data = response;

            cleanupCityTable();
            $("#cityQueryField").empty();

            for (var i = 0; i < data.length; i++) {
                var information = $.parseJSON(data[i]);

                var name = '<th id=' + 'name' + i + '>' + information['_Metros__name'] + '</th>';
                var code = '<th id=' + 'code' + i + '>' + information['_Metros__code'] + '</th>';
                var continent = '<th id=' + 'continent' + i + '>' + information['_Metros__continent'] + '</th>';
                var region = '<th id=' + 'region' + i + '>' + information['_Metros__region'] + '</th>';
                var country = '<th id=' + 'country' + i + '>' + information['_Metros__country'] + '</th>';
                var population = '<th id=' + 'population' + i + '>' + information['_Metros__population'] + '</th>';
                var timezone = '<th id=' + 'timezone' + i + '>' + information['_Metros__timezone'] + '</th>';
                var coordinates = '<th id=' + 'coordinates' + i + '>' + JSON.stringify(information['_Metros__coordinates']) + '</th>';
                var editButton = '<th><button type="button" onclick="editCityView(' + i + ')" class="btn btn-sm btn-default">Edit City</button></th>';

                var oneEntry = '<tr>' + code + name + country + continent + timezone + coordinates + population + region + editButton + '</tr>';

                var cityQueryOption = '<option value="' + information['_Metros__name'] + '">' + information['_Metros__name'] + '</option>' ;

                $("#cityDataTableBody").append(oneEntry);
                $("#cityQueryField").append(cityQueryOption);
            }

            $("#cityTable").dataTable();
        },
        error : function(response) {
            alert('City data could not be retrieved. Please try again.');
        }
    });
};


/**
 *  Function to empty the current cities tables data and add all the skeleton
 *  tags for the city table.
 */
function cleanupCityTable() {
    $("#cityTableDiv").empty();

    var tableTag = '<table id="cityTable" class="display table" cellspacing="0" width="100%"></table>';
    var tableColumns = '<tr><th>Code</th><th>Name</th><th>Country</th><th>Continent</th><th>TimeZone</th><th>Coordinates</th><th>Population</th><th>Region</th><th>Edit City</th></tr>';
    var tableHead = '<thead>' + tableColumns + '</thead>';
    var tableFoot = '<tfoot>' + tableColumns + '</tfoot>';
    var tableBody = '<tbody id="cityDataTableBody"></tbody>';

    $("#cityTableDiv").append(tableTag);
    $("#cityTable").append(tableHead);
    $("#cityTable").append(tableFoot);
    $("#cityTable").append(tableBody);
};


/**
 *  Function that requests all the routes data from the server and updates the view
 *  for the routes table.
 *
 *  NOTE: A better implementation again would be to use dataTable's inherent update
 *          functionality or use a framework rather than doing manual DOM manipulation.
 */
function updateAndRenderRouteTable() {
    $.ajax({
        url : '/allroutedata',
        type : 'GET',
        datatype : 'jsonp',
        success : function (response) {
            var data = response;

            cleanupRouteTable();

            for (var i = 0; i < data.length; i++) {
                var information = $.parseJSON(data[i]);

                var originID = 'routeOriginCode' + i;
                var destinationID = 'routeDestinationCode' + i;
                var distanceID = 'routeDistance' + i;
                var origin = '<th id=' + originID + '>' + information['_Route__source'].toLocaleUpperCase() + '</th>';
                var destination = '<th id=' + destinationID + '>' + information['_Route__destination'].toLocaleUpperCase() + '</th>';
                var distance = '<th id=' + distanceID + '>' + information['_Route__distance'] + '</th>';

                var routeString = "'" + information['_Route__source'] + '-' + information['_Route__destination'] + "', 'wls'";
                var showMapInModalFunction = 'onclick="showMapInModal(' + routeString + ')"';
                var showDetailsRouteString = "'" + information['_Route__source'] + "', '" + information['_Route__destination'] + "'";
                var showRouteDetailsFunction = 'onclick="getRouteDetails(' +  showDetailsRouteString + ')"';

                var routeURL = '<th><a href="#"' + showMapInModalFunction + '>View route map</a></th>';
                var routeDetails = '<th><button type="button" class="btn btn-sm btn-block"' + showRouteDetailsFunction + '>View Details</button></th>';
                var editCurrentRoute = '<th><button type="button" onclick="editRouteView(' + i + ')" class="btn btn-sm btn-default">Edit Route</button></th>';

                var oneEntry = '<tr>' + origin + destination + distance + routeURL + routeDetails + editCurrentRoute + '</tr>';
                $("#routeTableBody").append(oneEntry);
            }

            $("#routeTable").DataTable();
        },

        error : function() {
            alert('Route data could not be retrieved. Please try again.')
        }
    });
};


/**
 *  Function to clean up the contents of the route table so that
 *  it can be populated with new data after any change.
 *
 *  NOTE: A better way to update the table data would be to use
 *  dataTables update function.
 */
function cleanupRouteTable() {
    $('#routeTableDiv').empty();

    var tableTag = ' <table id="routeTable" class="display table" cellspacing="0" width="100%">';
    var tableColumns = '<tr><th>Origin</th><th>Destination</th><th>Distance</th><th>Route URL</th><th>View Route Details</th><th>Edit Route</th></tr>';
    var tableHead = '<thead>' + tableColumns + '</thead>';
    var tableFoot = '<tfoot>' + tableColumns + '</tfoot>';
    var tableBody = '<tbody id="routeTableBody"></tbody>';

    $('#routeTableDiv').append(tableTag);
    $('#routeTable').append(tableHead);
    $('#routeTable').append(tableFoot);
    $('#routeTable').append(tableBody);
};


/**
 * Function used to find the shortest route between two cities in the CSAir network.
 */
function findShortestRoute() {

};


/**
 * Function that is called whenever the user views the analytics view. This would call
 * the server and generate the metrics for the current state of the CSAir network.
 * Also, it calls the renderMetrics() method that shows the metrics on the view.
 */
function getNetworkMetrics() {
    renderMetrics();
}


/**
 * Function used to show the CSAir network metrics on the view.
 */
function renderMetrics() {

}