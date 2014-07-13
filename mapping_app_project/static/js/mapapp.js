var fields = ['#id_site_name', '#id_county', '#id_site_date', '#id_site_location', '#id_operator', '#id_photographs',
'#id_site_notes', '#id_geomorph_setting', '#id_sample_type_collected', "#id_site-latitude", '#id_site-longitude',
"#id_site-easting", "#id_site-northing", "#id_site-elevation", "#id_site-grid_reference", "#id_site-bng_ing"]


$('#myModal').on('hidden.bs.modal', function (e) {
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).val('');
    }
    $("#id_photos_taken").val(1);
});


$('#modalbutton1').click(function(){
    var site = $('#id_sites option:selected').text();

    $.getJSON('/mappingapp/sites/', {site_name: site}, function(data){
        var items = [];
        $.each(data, function( key, val) {
        $('#id_site_name').val(val.name, true).prop( "disabled", true );
        if (val.county == null) {
            val.county = ''
        }
        $('#id_county').val(val.county, true).prop( "disabled", true );
        $('#id_site_date').val(val.date, true).prop( "disabled", true );
        $('#id_site_location').val(val.loc, true).prop( "disabled", true );

        if (val.operator == null) {
            val.operator = ''
        }
        $('#id_operator').val(val.operator, true).prop( "disabled", true );
        $('#id_photographs').val(val.photographs, true).prop( "disabled", true );
        $('#id_site_notes').val(val.notes, true).prop( "disabled", true );
        $('#id_geomorph_setting').val(val.geomorph, true).prop( "disabled", true );
        $('#id_sample_type_collected').val(val.type, true).prop( "disabled", true );
        $("#id_photos_taken").val(val.photos_taken).prop( "disabled", true );

        $("#id_site-latitude").val(val.latitude).prop( "disabled", true );
        $("#id_site-longitude").val(val.longitude).prop( "disabled", true );
        $("#id_site-easting").val(val.easting).prop( "disabled", true );
        $("#id_site-northing").val(val.northing).prop( "disabled", true );
        $("#id_site-elevation").val(val.elevation).prop( "disabled", true );
        $("#id_site-grid_reference").val(val.grid).prop( "disabled", true );
        $("#id_site-bng_ing").val(val.bng).prop( "disabled", true );

        $( "#savebutton" ).hide();
        });
    });
});


$('#modalbutton2').click(function(){
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).prop( "disabled", false );
    }

    $("#id_photos_taken").prop( "disabled", false );
    $( "#savebutton" ).show();
 });




