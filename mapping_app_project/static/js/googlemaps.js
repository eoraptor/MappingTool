var map;
var markers = [];
var infowindow = null;
var mapicons = [];

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

    $.getJSON('/mappingapp/markers/', function (data) {
        $.each(data, function (key, val) {
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(val.latitude, val.longitude),
                map: map,
                icon: mapicons[val.type],
                title: val.code
            });
            markers.push(marker);
        });
    });

    var infowindow = new google.maps.InfoWindow({
        maxWidth: 120,
        content: "sss"
    });

    for (var i = 0; i < markers.length; i++) {
        var marker = markers[i];
        google.maps.event.addListener(marker, 'click', function () {
            alert(this.html)
            infowindow.setContent(this.html);
            infowindow.open(map, this);
        });
    }

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

    var legend = document.getElementById('map-legend');

    for (var key in icons) {
        var type = icons[key];
        var name = type.name;
        var icon = type.icon;
        var div = document.createElement("row");
        div.innerHTML = name + '<img src="' + icon + '" height="15px">';
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
}



