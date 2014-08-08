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

    function setColour() {
        document.getElementById('clearbutton').style.backgroundColor = 'red';
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

        var oms = new OverlappingMarkerSpiderfier(map);

        drawingManager = new google.maps.drawing.DrawingManager({
            drawingControl: true,
            drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
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

        drawingManager.setMap(map);

        google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
            coordinates = (polygon.getPath().getArray());
//            console.log(coordinates);
            var poly = new google.maps.Polygon ({
                paths: coordinates
            });
        });

        function getCoordinates() {
           coordinates = (selectedShape.getPath().getArray());

            $('#id_sample_codes').empty();
            var poly = new google.maps.Polygon ({
                paths: coordinates
            });
            var in_bounds = [];

            for (var i = 0; i < markers.length; i++) {
                if (google.maps.geometry.poly.containsLocation(markers[i].position, poly)) {
                    in_bounds.push(markers[i].title);
            }
           }
            $('#id_sample_codes').val(in_bounds);
            if (in_bounds.length > 0) {
                $('#submit_markers').click();
            }
        }


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
        google.maps.event.addDomListener(document.getElementById("viewsamples"), 'click', getCoordinates);
        google.maps.event.addDomListener(document.getElementById("clear"), 'mouseover', setColour())

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
            markers.push(marker);
            oms.addMarker(marker);

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
}



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

