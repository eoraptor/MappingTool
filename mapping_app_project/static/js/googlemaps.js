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
    }
})();