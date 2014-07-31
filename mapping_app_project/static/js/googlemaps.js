var map;
var markers = [];
var infowindow = null;
var mapicons = [];
var iconBase = "/static/imgs/";
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

(function() {
    window.onload = function() {

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
})();




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
