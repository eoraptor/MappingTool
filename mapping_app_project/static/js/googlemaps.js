var map;
var markers = [];
var infowindow = null;
var drawingManager;
var mapicons = [];
var selectedShape;
var iconBase = "/static/imgs/";
var coordinates;
var newShape;

     function clearSelection() {
        if (selectedShape) {
          selectedShape.setEditable(false);
          selectedShape = null;
        }
      }

      function setSelection(shape) {
        clearSelection();
        selectedShape = shape;
        shape.setEditable(true);
      }

      function deleteSelectedShape() {
        if (newShape) {
          newShape.setMap(null);
          $('#id_sample_codes').empty();

        }
      }

        var opendialogue = function() {
        $("#dialog").dialog("open");
        };


       // filter markers based on age
        function markeragefilter() {
            var start = $('#startagefilter').val();
            var end = $('#endagefilter').val();


            for (var i = 0; i < markers.length; i++) {
                var marker = markers[i];
                if ((marker.age > start && marker.age < end) || marker.age == null) {
                    marker.setMap(null);
                }
            }
        }


function getCoordinates() {

           coordinates = (selectedShape.getPath().getArray());

            var poly = new google.maps.Polygon ({
                paths: coordinates
            });
            var in_bounds = [];

            for (var i = 0; i < markers.length; i++) {
                if (google.maps.geometry.poly.containsLocation(markers[i].position, poly)) {
                    in_bounds.push(markers[i].title);
            }
           }
            $('#id_sample_codes').empty().val(in_bounds);
            if (in_bounds.length > 0) {
                $('#submit_markers').click();
            }
        }


var icons = {
    osl: {
        name: 'OSL  ',
        icon: iconBase + 'pink-circle.png'
    },
    tcn: {
        name: '  TCN  ',
        icon: iconBase + 'ylw-circle.png'
    },
    c14: {
        name: '  C14  ',
        icon: iconBase + 'ltblu-circle.png'
    }
};

function initialize() {

        make_icons();

        $("#dialog").dialog({
               autoOpen: false
            });

        var mapDiv = document.getElementById('map-canvas');

        var map_options = {
            center: new google.maps.LatLng(56, -4.2921),
            zoom: 5,
            mapTypeId: google.maps.MapTypeId.SATELLITE,
            panControl: false,
            mapTypeControl: false,
            streetViewControl: false,
            zoomControl: true,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL
            }
        };


        map = new google.maps.Map(mapDiv, map_options);

        var oms = new OverlappingMarkerSpiderfier(map);

        drawingManager = new google.maps.drawing.DrawingManager({
            drawingControl: true,
            drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
            google.maps.drawing.OverlayType.POLYGON
          ]
        },
        polygonOptions: {
            fillColor: '#ffff00',
            fillOpacity: 0.4,
            strokeWeight: 2,
            clickable: true,
            zIndex: 1,
            editable: true,
            draggable:true
        }
        });

        var markerfilterDiv = document.createElement('div');
             var markerfilter = new MarkerFilterButton(markerfilterDiv, map);
             markerfilterDiv.index = 1;
             map.controls[google.maps.ControlPosition.TOP_LEFT].push(markerfilterDiv);

         if ($('#viewastable').length > 0) {
             drawingManager.setMap(map);

             var drawingControlDiv = document.createElement('div');
             var drawingControl = new MarkerSelectControl(drawingControlDiv, map);
             drawingControlDiv.index = 1;
             map.controls[google.maps.ControlPosition.TOP_CENTER].push(drawingControlDiv);

             var helpDiv = document.createElement('div');
             var help = new MarkerSelectHelp(helpDiv, map);
             helpDiv.index = -1;
             map.controls[google.maps.ControlPosition.TOP_CENTER].push(helpDiv);

         }

        google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
            coordinates = (polygon.getPath().getArray());
//            console.log(coordinates);
            var poly = new google.maps.Polygon ({
                paths: coordinates
            });
        });




        var legend = document.getElementById('map-legend');

        for (var key in icons) {
            var type = icons[key];
            var name = type.name;
            var icon = type.icon;
            var div = document.createElement("row");
            div.innerHTML = name + '<img src="' + icon + '" height="20px">';
            legend.appendChild(div);
        }

        map.controls[google.maps.ControlPosition.BOTTOM].push(legend);

        var center;

        function calculateCenter() {
            center = map.getCenter();
        }

        google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {

        // Switch back to non-drawing mode after drawing a shape.
        drawingManager.setDrawingMode(null);
        clearSelection();

        // Add an event listener that selects the newly-drawn shape when the user
        // mouses down on it.
        newShape = e.overlay;
        newShape.type = e.type;
        google.maps.event.addListener(newShape, 'click', function() {
          setSelection(newShape);
        });
        setSelection(newShape);

        // Clear the current selection when clear button clicked
        google.maps.event.addDomListener(document.getElementById("delshape"), 'click', deleteSelectedShape);
        google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
        google.maps.event.addListener(map, 'click', clearSelection);
        });

        google.maps.event.addDomListener(map, 'idle', function () {
            calculateCenter();
        });

        google.maps.event.addDomListener(window, 'resize', function () {
            map.setCenter(center);
        });

        var infowindow;

        var marker_data = [];

        $.getJSON('/mappingapp/markers/', function (data) {

            $.each(data, function (key, val) {
                sample_data = {'lat': val.latitude, 'long': val.longitude, 'type': val.type, 'code': val.code, 'age':val.age, 'site':val.site};
                marker_data.push(sample_data);
            });

        for (var i = 0; i < marker_data.length; i++) {
            sample_data = marker_data[i];
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(sample_data['lat'], sample_data['long']),
                map: map,
                type: sample_data['type'].toUpperCase(),
                age: sample_data['age'],
                site: sample_data['site'],
                icon: mapicons[sample_data['type']],
                title: sample_data['code']
            });
            markers.push(marker);
            oms.addMarker(marker);

        (function (i, marker) {
            google.maps.event.addListener(marker, 'click', function() {
                if (!infowindow) {
                    infowindow = new google.maps.InfoWindow({
                        width: 120
                    });
                    }
                var latitude = Math.round(marker.position.lat() * Math.pow(10, 5))/Math.pow(10, 5);
                var longitude = Math.round(marker.position.lng() * Math.pow(10, 5))/Math.pow(10, 5);
                infowindow.setContent('<h5>'+marker.title+'</h5>'+'<hr>'+'<b>Lat: </b>'+latitude+'<br />'+
                '<b>Lng: </b>'+longitude+'<br /><b>Calendar Age: </b>'+marker.age+
                    '<br /><b>Type: </b>'+marker.type+'<br /><b>Site: </b>'+marker.site);
                infowindow.open(map, marker);
                });

                })(i,marker);
            }
    })();


//        bottom of function
}

google.maps.event.addDomListener(window, 'load', initialize);

var filterbutton = document.getElementById("filterbutton");
filterbutton.addEventListener("click", markeragefilter, false);

var make_icons = function() {
    mapicons['tcn'] = new google.maps.MarkerImage(
        '/static/imgs/ylw-circle.png',
        null,
        null,
        null,
        new google.maps.Size(28, 28)
    );

    mapicons['osl'] = new google.maps.MarkerImage(
        '/static/imgs/pink-circle.png',
        null,
        null,
        null,
        new google.maps.Size(28, 28)
    );

    mapicons['c14'] = new google.maps.MarkerImage(
        '/static/imgs/ltblu-circle.png',
        null,
        null,
        null,
        new google.maps.Size(28, 28)
    )
};


function MarkerSelectControl(controlDiv, map) {

  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map.
  controlDiv.style.paddingTop = '6px';

  // Set CSS for the control border.
  var clearbutton = document.createElement('button');
  clearbutton.className = 'btn-warning';
  clearbutton.style.height = '25px';
  clearbutton.style.verticalAlign = 'middle';
  clearbutton.title = 'Click to delete the shape';
  clearbutton.innerHTML = 'Clear';
  clearbutton.style.fontSize = '15px';
  controlDiv.appendChild(clearbutton);

  google.maps.event.addDomListener(clearbutton, 'click', deleteSelectedShape);

  var viewbutton = document.createElement('button');
  viewbutton.className = 'btn-success';
  viewbutton.id = 'viewbutton';
  viewbutton.style.height = '25px';
  viewbutton.style.verticalAlign = 'middle';
  viewbutton.title = 'Click to view selected sample data in a table';
  viewbutton.innerHTML = 'View Samples';
  viewbutton.style.fontSize = '15px';
  controlDiv.appendChild(viewbutton);

  google.maps.event.addDomListener(viewbutton, 'click', getCoordinates);

}

function MarkerSelectHelp(controlDiv, map) {

  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map.
  controlDiv.style.paddingTop = '6px';

  // Set CSS for the control border.
  var help = document.createElement('div');
  help.id = 'helplabel';
  help.style.height = '25px';
  help.style.backgroundColor = '#d7e9c6';
  help.style.border = '1px solid';
  help.style.paddingLeft = '4px';
  help.style.paddingRight = '4px';
  help.style.borderColor = 'black';
  help.style.verticalAlign = 'middle';
  help.innerHTML = 'Drawing Controls';
  help.style.fontSize = '15px';
  controlDiv.appendChild(help);
}


function MarkerFilterButton(controlDiv, map) {

    // Set CSS styles for the DIV containing the control
    // Setting padding to 5 px will offset the control
    // from the edge of the map.
    controlDiv.style.paddingTop = '6px';

    // Set CSS for the control border.
    var markerfilter = document.createElement('button');
    markerfilter.className = 'btn-info';
    markerfilter.style.height = '35px';
    markerfilter.style.verticalAlign = 'middle';
    markerfilter.title = 'Click to filter markers by age range';
    markerfilter.innerHTML = 'Age Filter';
    markerfilter.style.fontSize = '18px';
    controlDiv.appendChild(markerfilter);

    google.maps.event.addDomListener(markerfilter, 'click', opendialogue);
}