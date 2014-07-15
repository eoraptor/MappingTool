var fields = ['#id_site_name', '#id_county', '#id_site_date', '#id_site_location', '#id_operator', '#id_photographs',
'#id_site_notes', '#id_geomorph_setting', '#id_sample_type_collected', "#id_site-latitude", '#id_site-longitude',
"#id_site-easting", "#id_site-northing", "#id_site-elevation", "#id_site-grid_reference", "#id_site-bng_ing"]


$(document).ready(function(){
    $('#savebutton').hide();
})

$('#myModal').on('hidden.bs.modal', function (e) {
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).val('');
    }
    $("#id_photos_taken").val(1);
     $( "#savebutton" ).hide();
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

        });
    });
});


$('#modalbutton2').click(function(){

    $('#id_site_name').val($('#id_hidden-site_name').text());
    $('#id_county').val($('#id_hidden-county').text());
    $('#id_site_date').val($('#id_hidden-site_date').text());
    $('#id_site_location').val($('#id_hidden-site_name').text());
    $('#id_operator').val($('#id_hidden-operator').text());
    $('#id_photographs').val($('#id_hidden-photographs').text());
    $('#id_site_notes').val($('#id_hidden-site_notes').text());
    $('#id_geomorph_setting').val($('#id_hidden-geomorph_setting').text());
    $('#id_sample_type_collected').val($('#id_hidden-sample_type_collected').text());
    $("#id_photos_taken").val($('#id_hidden-photos_taken option:selected').val());

    $("#id_site-latitude").val($('#id_hidden_coords-latitude').text());
    $("#id_site-longitude").val($('#id_hidden_coords-longitude').text());
    $("#id_site-easting").val($('#id_hidden_coords-easting').text());
    $("#id_site-northing").val($('#id_hidden_coords-northing').text());
    $("#id_site-elevation").val($('#id_hidden_coords-elevation').text());
    $("#id_site-grid_reference").val($('#id_hidden_coords-grid_reference').text());
    $("#id_site-bng_ing").val($('#id_hidden_coords-bng_ing').text());

    $( "#savebutton" ).show();
});


$('#savebutton').click(function(){
    var site = $('#id_site_name').val();

    var county = $('#id_county').val();
//    var date = $('#id_site_date').val();
    var location = $('#id_site_location').val();
    var operator = $('#id_operator').val();
    var photographs = $('#id_photographs').val();
    var site_notes = $('#id_site_notes').val();
    var sample_type = $('#id_sample_type_collected').val();
    var geomorph = $('#id_geomorph_setting').val();
    var photos_taken = $('#id_photos_taken option:selected').val();

    var latitude = $("#id_site-latitude").text();
    var longitude = $("#id_site-longitude").text();
    var easting = $("#id_site-easting").text();
    var northing = $("#id_site-northing").text();
    var elevation = $("#id_site-elevation").text();
    var grid = $("#id_site-grid_reference").text();
    var bng = $("#id_site-bng_ing").text();

//      , date:date,

    $.getJSON('/mappingapp/create_site/', {site_name: site, photographs:photographs, site_operator:operator,
        site_county:county, site_location:location, notes:site_notes, type:sample_type, photos_taken:photos_taken,
        geomorph:geomorph, latitude:latitude, longitude:longitude, easting:easting, northing:northing,
        elevation:elevation, grid:grid, bng:bng}, function(data){

        $.each(data, function( key, val) {
            if ((val.created) == true) {
            $('#id_sites').append(new Option(site))
            alert('Site Saved')
            }else if ((val.created) == false) {
                alert('Site Already Exists')
            }
        });
    $("#id_sites").val(site);
  });

    $('#myModal').hide()
});


$('#modalbutton2').click(function(){
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).prop( "disabled", false );
    }

    $("#id_photos_taken").prop( "disabled", false );
    $( "#savebutton" ).show();
 });


$('#modalbutton3').click(function(){
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).prop( "disabled", false );
    }

    $("#id_photos_taken").prop( "disabled", false );
    $( "#savebutton" ).show();
 });


// $(function() {
//$( document ).tooltip();
//});

