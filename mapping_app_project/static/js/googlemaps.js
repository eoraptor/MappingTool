var markers = [];

(function() {
    window.onload = function() {
        var mapDiv = document.getElementById('map-canvas');

        var map_options = {
                    center: new google.maps.LatLng(55.8720, -4.2921),
                    zoom: 5,
                    mapTypeId: google.maps.MapTypeId.SATELLITE,
                    panControl: false,
                    mapTypeControl: false,
                    streetViewControl: false,
                    zoomControl: true,
                    zoomControlOptions: {
                        style: google.maps.ZoomControlStyle.SMALL
                }};

        var map = new google.maps.Map(mapDiv, map_options);

    var iconBase = 'http://labs.google.com/ridefinder/images/';
        var icons = {
          parking: {
            name: 'OSL  ',
            icon: iconBase + 'mm_20_red.png'
          },
          library: {
            name: '  TCN  ',
            icon: iconBase + 'mm_20_green.png'
          },
          info: {
            name: '  C14  ',
            icon: iconBase + 'mm_20_yellow.png'
          }
        };

   var legend = document.getElementById('map-legend');

        for (var key in icons) {
          var type = icons[key];
          var name = type.name;
          var icon = type.icon;
          var div = document.createElement("row");
          div.innerHTML = name + '<img src="' + icon + '">';
          legend.appendChild(div);
        }
   map.controls[google.maps.ControlPosition.BOTTOM].push(legend);

  var center;
  function calculateCenter() {
  center = map.getCenter();
}
    google.maps.event.addDomListener(map, 'idle', function() {
        calculateCenter();
    });
    google.maps.event.addDomListener(window, 'resize', function() {
        map.setCenter(center);
    });
  }
})();

