function HomeControl(controlDiv, map) {

  // Set CSS styles for the DIV containing the control
  // Setting padding to 5 px will offset the control
  // from the edge of the map.
  controlDiv.style.padding = '5px';

  // Set CSS for the control border.
  var controlUI = document.createElement('div');
  controlUI.style.backgroundColor = 'white';
  controlUI.style.borderStyle = 'solid';
  controlUI.style.borderWidth = '1px';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Sample Type';
  controlDiv.appendChild(controlUI);

  // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.fontFamily = 'Arial,sans-serif';
  controlText.style.fontSize = '12px';
  controlText.style.paddingLeft = '4px';
  controlText.style.paddingRight = '4px';
  controlText.innerHTML = '<strong>Sample Type:  TCN  OSL  C14</strong>';
  controlUI.appendChild(controlText);
}


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
        var chicago = new google.maps.LatLng(41.850033, -87.6500523);

        var homeControlDiv = document.createElement('div');
        var homeControl = new HomeControl(homeControlDiv, map);

  homeControlDiv.index = 1;
  map.controls[google.maps.ControlPosition.BOTTOM].push(homeControlDiv);

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

