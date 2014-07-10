var map;

(function() {
    var mapicons = [];
    mapicons['tcn'] = new google.maps.MarkerImage(
    '/static/imgs/ylw-circle.png',
    null,
    null,
    null,
    new google.maps.Size(28, 28)
    );



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

        map = new google.maps.Map(mapDiv, map_options);

    for (var i = 0; i < coordinates.coords.length; i++) {
        var coord = coordinates.coords[i];
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(coord.lat, coord.lng),
            map: map,
            icon: mapicons['tcn']
        });}


    var iconBase = "/static/imgs/"
    var icons = {
            osl: {
            name: 'OSL  ',
            icon: iconBase + 'grn-circle.png'
          },
            tcn: {
            name: '  TCN  ',
            icon: iconBase + 'ylw-circle.png'
          },
            c14: {
            name: '  C14  ',
            icon: iconBase + 'purple-circle.png'
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
    google.maps.event.addDomListener(map, 'idle', function() {
        calculateCenter();
    });
    google.maps.event.addDomListener(window, 'resize', function() {
        map.setCenter(center);
    });
  }
})();




