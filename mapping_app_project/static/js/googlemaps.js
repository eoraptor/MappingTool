var map;
var markers = [];
var infowindow = null;
var drawingManager;
var mapicons = [];
var selectedShape;
var iconBase = "/static/imgs/";

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
        if (selectedShape) {
          selectedShape.setMap(null);
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

        drawingManager = new google.maps.drawing.DrawingManager({
            drawingControl: true,
            drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
            drawingModes: [
            google.maps.drawing.OverlayType.CIRCLE,
            google.maps.drawing.OverlayType.POLYGON,
            google.maps.drawing.OverlayType.RECTANGLE
          ]
        },
        polygonOptions: {
            fillColor: '#ffff00',
            fillOpacity: 0.4,
            strokeWeight: 3,
            clickable: true,
            zIndex: 1,
            editable: true,
            draggable:true
        },
        circleOptions: {
            fillColor: '#ffff00',
            fillOpacity: 0.4,
            strokeWeight: 3,
            clickable: true,
            zIndex: 1,
            editable: true,
            draggable:true
        },
        rectangleOptions: {
            fillColor: '#ffff00',
            fillOpacity: 0.4,
            strokeWeight: 3,
            clickable: true,
            zIndex: 1,
            editable: true,
            draggable:true
        },
            map: map
        });

        google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
            var coordinates = (polygon.getPath().getArray());
            console.log(coordinates);
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

        var clearButtonDiv = document.createElement('div');
        var clear = new clearButton(clearButtonDiv, map);

        clearButtonDiv.index = 1;
        map.controls[google.maps.ControlPosition.RIGHT_TOP].push(clearButtonDiv);

        google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {

        // Switch back to non-drawing mode after drawing a shape.
        drawingManager.setDrawingMode(null);

        // Add an event listener that selects the newly-drawn shape when the user
        // mouses down on it.
        var newShape = e.overlay;
        newShape.type = e.type;
        google.maps.event.addListener(newShape, 'click', function() {
          setSelection(newShape);
        });
        setSelection(newShape);

        // Clear the current selection when clear button clicked
        google.maps.event.addDomListener(document.getElementById("clearbutton"), 'click', deleteSelectedShape);
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
                sample_data = {'lat': val.latitude, 'long': val.longitude, 'type': val.type, 'code': val.code};
                marker_data.push(sample_data);
            });



        for (var i = 0; i < marker_data.length; i++) {
            sample_data = marker_data[i];
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(sample_data['lat'], sample_data['long']),
                map: map,
                icon: mapicons[sample_data['type']],
                title: sample_data['code']
            });

        (function (i, marker) {
            google.maps.event.addListener(marker, 'click', function() {
                if (!infowindow) {
                    infowindow = new google.maps.InfoWindow({
                        width: 120
                    });
                    }
                infowindow.setContent(marker.title);
                infowindow.open(map, marker);
                });
                })(i,marker);
            }
    })();

//        bottom of function
};


google.maps.event.addDomListener(window, 'load', initialize);

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


function clearButton(controlDiv, map) {

  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map
  controlDiv.style.padding = '5px';

  // Set CSS for the control border
  var controlUI1 = document.createElement('div');
  controlUI1.id = "clearbutton";
  controlUI1.style.backgroundColor = 'white';
  controlUI1.style.borderStyle = 'solid';
  controlUI1.style.borderWidth = '1px';
  controlUI1.style.cursor = 'pointer';
  controlUI1.style.textAlign = 'center';
  controlUI1.title = 'Click to delete shape';
  controlDiv.appendChild(controlUI1);

  // Set CSS for the control interior
  var controlText1 = document.createElement('div');
  controlText1.style.fontFamily = 'Arial,sans-serif';
  controlText1.style.fontSize = '12px';
  controlText1.style.paddingLeft = '4px';
  controlText1.style.paddingRight = '4px';
  controlText1.innerHTML = '<b>Delete Shape</b>';
  controlUI1.appendChild(controlText1);
}
