var fields = ['#id_site_name', '#id_county', '#id_site_date', '#id_site_location', '#id_operator', '#id_photographs',
'#id_site_notes', '#id_geomorph_setting', '#id_sample_type_collected', "#id_site-latitude", '#id_site-longitude',
"#id_site-easting", "#id_site-northing", "#id_site-elevation", "#id_site-grid_reference", "#id_site-bng_ing",
    "#id_collected_by"];

var sample_fields = ['#id_sample_thickness', '#id_sample_code', '#id_collection_date', '#id_collector',
'#id_sample_location_name', '#id_sampled_material', '#id_lithology', '#id_quartz_content',
'#id_sample_surface_strike_dip', '#id_boulder_dimensions', '#id_grain_size', '#id_sample_setting',
'#id_sample_notes', '#id_sample-latitude', '#id_sample-longitude', '#id_sample-easting', '#id_sample-northing',
'#id_sample-elevation', '#id_sample-bng_ing', "#id_exposure_core", "#id_core_number"];

var $table;
var bear_inc_errors = false;
var bearing_errors = [];
var form_errors = [];



// check numerical fields in Edit and Validate pages match expected type
// prevent saving if non-numerical
function check_number(field, value) {
    if (!jQuery.isNumeric(value) && value != '') {
        var found = false;
        for (var i = 0; i < form_errors.length; i++){
            if (field == form_errors[i]){
                found = true;
            }
        }if (!found){
            if (field.indexOf('form') != -1 && bearing_errors.indexOf(field) === -1) {
                bearing_errors.push(field);
                if (bear_inc_errors === false) {
                    bear_inc_errors = true;
                    form_errors.push(field);
                }
            }else if (field.indexOf('form') === -1) {
                form_errors.push(field);
            }
        }
        // change field background colour and disable save buttons
        $('#'+field).css("background-color", "#E6760C");
        $('#validatebutton').attr("disabled", true);
        $('#editbutton').attr("disabled", true);
        if (field.indexOf('site') != -1){
            $('#savebutton').attr("disabled", true);
        }


    }else if(jQuery.isNumeric(value) || value == ''){

        if (bearing_errors.indexOf(field) != -1) {
            var index1 = bearing_errors.indexOf(field);
            removed = bearing_errors.splice(index1, 1);
            if (bearing_errors.length === 0) {
                bear_inc_errors = false;
                for (var i = 0; i < form_errors.length; i++) {
                    if (form_errors[i].indexOf('form') != -1) {
                        removed = form_errors.splice(i, 1);
                    }
                }
            }
        }else{
            for (var i = 0; i < form_errors.length; i++) {
                if (field === form_errors[i]) {
                removed = form_errors.splice(i, 1);
        }}}
        // revert background colour to white and enable saving if all errors fixed
        $('#'+field).css("background-color", "");
        if (form_errors.length == 0) {
            $('#editbutton').attr("disabled", false);
            $('#validatebutton').attr("disabled", false);
            $('#savebutton').attr("disabled", false);
        }else {
            var site_errors = false;
            for (var i = 0; i < form_errors.length; i++) {
                if (form_errors[i].indexOf('site') != -1) {
                    site_errors = true;
            }
        }
            if (site_errors == false){
                // if site errors fixed - enable site saving again
                $('#savebutton').attr("disabled", false);
            }
    }}}


// Populate and open the field error dialogue on Validate and Edit sample pages
function openerrordialogue() {
        var insert = '<ul>';
        for (var i=0; i<form_errors.length; i++){
            var field = form_errors[i];
            if (field.indexOf('sample-latitude') != -1){
                field = 'Sample Latitude - field must be numerical';
            }else if (field.indexOf('sample-longitude') != -1){
                field = 'Sample Longitude - field must be numerical';
            }else if (field.indexOf('sample-easting') != -1){
                field = 'Sample Easting - field must be numerical';
            }else if (field.indexOf('sample-northing') != -1){
                field = 'Sample Northing - field must be numerical';
            }else if (field.indexOf('calendar_age') != -1){
                field = 'Calendar Age - field must be numerical';
            }else if (field.indexOf('calendar_error') != -1){
                field = 'Calendar Error - field must be numerical';
            }else if (field.indexOf('age_error') != -1){
                field = 'Sample Age Error - field must be numerical';
            }else if (field.indexOf('age') != -1) {
                field = 'Sample Age - field must be numerical';
            }else if (field.indexOf('site-latitude') != -1){
                field = 'Site Latitude - field must be numerical';
            }else if (field.indexOf('site-longitude') != -1){
                field = 'Site Longitude - field must be numerical';
            }else if (field.indexOf('site-easting') != -1){
                field = 'Site Easting - field must be numerical';
            }else if (field.indexOf('site-northing') != -1) {
                field = 'Site Northing - field must be numerical';
            }else if (field.indexOf('form') != -1) {
                field = 'Bearing and Inclination - all fields must be numerical';
            }else{
                field = 'Sample Code - must be non null and unique';
            }
            insert = insert + '<li>'+ field + '</li>'
        }
        if (insert == '<ul>'){
            insert = insert + 'None</ul>'
            }
        $('#errorfields').html(insert);
        $("#errordialog").dialog("open");
        }

$(document).ready(function(){

       // slider plugin for Age Filter on map page
    $("#ex2").slider();
        $(this).on('slide', function(slideEvt) {
	    var range = slideEvt.value;
        $('#startagefilter').val(range[0]);
        $('#endagefilter').val(range[1]);
});

    // hide Site modal save button on page launch (shown if Create New Site option selected)
    $('#savebutton').hide();

    // initialise and hide error dialogue on Edit, Validate & Create New pages
    $("#errordialog").dialog({
               autoOpen: false
            });

    // has sample been saved on Validate page?
    var sample_saved = $('#sample_saved').text();
    if (sample_saved == 'True') {
        $("#samp_saved").css('visibility', 'visible');
        $("#saveAlert").fadeOut(6000);
    }else{
        $("#saveAlert").hide();
    }

    // open error dialogue on error button click
    $('#errorbutton').click(openerrordialogue);

    // check file is of correct type
    $('#id_file').change(function(){
    var filename = $('#id_file').val();
    var fileparts = filename.split('.');
    var filetype = fileparts[fileparts.length - 1];
    if (filetype != 'xlsx'){
        $('#uploadbutton').attr('disabled', true);
        alert('Files must be of type .xlsx');
    }else{
        $('#uploadbutton').attr('disabled', false)
    }
    });


    // check if site name was loaded with sample in Edit, Validate & Create New pages
    var site_name = $('#site_option').text();

    // if no site, disable show details button in site panel - stop empty modal launching
    if (site_name == 'None' || site_name == '') {
        $('#modalbutton1').attr("disabled", true);
    }else{
        $('#id_main-sites').val(site_name);
    }
    // add selected site to hidden site form - will be used to set sample site when sample is saved
    $('#site_selected').text(site_name);
    $('#id_hidden-site_name').val(site_name);

    // transfer selected sample code to code input in Edit Sample code selection page
    $('.td').click(function() {
    var text = $(this).text();
    $('#id_samp_code').val(text);
    });

    // round the Lat/Long values in the sample form
    var lat = $('#id_sample-latitude').val();
    var long = $('#id_sample-longitude').val();
    if (lat != '') {
        var latitude = Math.round(lat * Math.pow(10, 5)) / Math.pow(10, 5);
        $('#id_sample-latitude').val(latitude);
        }
    if (long != '') {
    var longitude = Math.round(long * Math.pow(10, 5)) / Math.pow(10, 5);
    $('#id_sample-longitude').val(longitude);
    }


    // setup for tablesorter plugin on Search page
    $(function(){

    $table = $('table');

        $('#getcsv').click(function(){
    // get delivery type
        $table.trigger('outputTable');
    });
        $table
        .tablesorter({
                theme: 'green',
                widthFixed: true,
                widgets: ['zebra', 'filter', 'columnSelector','output', 'resizable'],
                widgetOptions : {

                    resizable: true,

                    // These are the default column widths which are used when the table is
                    // initialized or resizing is reset; note that the "Age" column is not
                    // resizable, but the width can still be set to 40px here
                    resizable_widths : [ '10%', '10%', '40px', '10%', '100px' ],
                    // target the column selector markup
                    columnSelector_container : $('#columnSelector'),
                    // column status, true = display, false = hide
                    // disable = do not display on list
                    columnSelector_columns : {
                        0: 'disable' /* set to disabled; not allowed to unselect it */
                    },
                    // remember selected columns (requires $.tablesorter.storage)
                    columnSelector_saveColumns: false,

                    // container layout
                    columnSelector_layout : '<div class="col-md-4"><label><input type="checkbox"> {name}</label></div>',
                    // data attribute containing column name to use in the selector container
                    columnSelector_name  : 'data-selector-name',

                    /* Responsive Media Query settings */
                    // enable/disable mediaquery breakpoints
                    columnSelector_mediaquery: true,
                    // toggle checkbox name
                    columnSelector_mediaqueryName: 'Select All',
                    // breakpoints checkbox initial setting
                    columnSelector_mediaqueryState: false,
                    // responsive table hides columns with priority 1-6 at these breakpoints
                    // see http://view.jquerymobile.com/1.3.2/dist/demos/widgets/table-column-toggle/
                    // #Applyingapresetbreakpoint
                    // *** set to false to disable ***
                    columnSelector_breakpoints : [ '20em', '30em', '40em', '50em', '60em', '70em' ],
                    // data attribute containing column priority
                    // duplicates how jQuery mobile uses priorities:
                    // http://view.jquerymobile.com/1.3.2/dist/demos/widgets/table-column-toggle/
                    columnSelector_priority : 'data-priority'
                }
            })
        .tablesorterPager({container: $("#pager")});
    });




    // register changes to sample code input box in Edit, Validate & Create New pages - used to check against database
    $('textarea[name=sample_code]').keyup(function() {
    $('#id_sample_code').text($(this).val());
    });

    // respond to typing in number fields in Edit, Validate & Create New pages - checks if numerical type
    $('textarea[class=noresizenumber]').keyup(function(){
        var field = this.id;
        var value = this.value;
        check_number(field, value);
    });

    // respond to typing in numerical Bearing and Inclination fields in Edit, Validate & Create New pages - check type
    $('textarea[class=bearinc]').keyup(function(){
        var field = this.id;
        var value = this.value;
        check_number(field, value);
    });


    // add datepicker to datefields in sample and site forms
     $(function() {
      $('#id_collection_date').datepicker({dateFormat: 'dd/mm/yy'});
});

     $(function() {
    $('#id_site_date').datepicker({dateFormat: 'dd/mm/yy'});
});

    // Test for missing keys - if key missing A1 cell contents appear - Validate Sample page
    for (var i = 0 ; i < sample_fields.length ; i++) {
        if ($(sample_fields[i]).val() == "TCN Sample Sheet" || $(sample_fields[i]).val() == "14C Sample Sheet" ||
            $(sample_fields[i]).val() == "Section B: OSL Sample Sheet") {
            $(sample_fields[i]).val('');
            $(sample_fields[i]).css("background-color", '#fff8b3');
        }
    }

    // stop saving of empty or duplicate sample code fields - Validate, Edit and Create New pages
    if ($('#validate').length > 0) {
        var sample = $('#id_sample_code').text();
        if (sample === '') {
            $('#id_sample_code').css("background-color", "#E6760C");
                    $('#validatebutton').attr("disabled", true);
                    form_errors.push('sample_code');
        }else {

            $.getJSON('/briticechrono/check_sample/', {sample_code: sample}, function (data) {
                $.each(data, function (key, val) {
                    var response = val.exists;
                    if (response == true) {
                        $('#id_sample_code').css("background-color", "#E6760C");
                        $('#validatebutton').attr("disabled", true);
                        form_errors.push('sample_code');
                    }
                });
            });
        }
    }

    // trigger a sample code search using the codes from the markers selected on the map page either from drawing
    // or the age filter
    if ($('#marker_codes').text() != 'None') {
        var sample_codes = $('#marker_codes').text().slice(0,-1);
        $('#searchcode').val(sample_codes);
        $('#searchbutton').trigger( "click" );
        $('#searchcode').val('');
    }

});

    // reset the search fields - Search Page
    $('#clearsearchfields').click(function(){
        $('#searchcode').val('');
        $('#searchkeyword').val('');
        $('#endage').val('');
        $('#startage').val('');
        $('#sampletype').val('');
        $('#transectsearch').val('');
    });



// set the hidden site form value - used to assign site to sample on saving
$('#id_main-sites').change(function() {
    var selected = $('#id_main-sites option:selected').val();
    $('#id_hidden-site_name').val(selected);
    if (selected == '') {
        $('#modalbutton1').attr("disabled", true);
    }else{
        $('#modalbutton1').attr("disabled", false);
    }
});


// clear site modal fields on close
$('#myModal').on('hidden.bs.modal', function (e) {
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).val('');
    }
    $("#id_photos_taken").val(1);
     $( "#savebutton" ).hide();
});


// Action for save button in Site Modal - creates new site if it doesn't exist
$('#savebutton').click(function(){
    var site = $('#id_site_name').val();

    var county = $('#id_county').val();
    var date = $('#id_site_date').val();
    var location = $('#id_site_location').val();
    var operator = $('#id_operator').val();
    var photographs = $('#id_photographs').val();
    var site_notes = $('#id_site_notes').val();
    var sample_type = $('#id_sample_type_collected').val();
    var geomorph = $('#id_geomorph_setting').val();
    var photos_taken = $('#id_photos_taken option:selected').val();
    var collected_by = $("#id_collected_by").val();

    var stringdate = date.split(' ')[0];

    var latitude = $("#id_site-latitude").val();
    var longitude = $("#id_site-longitude").val();
    var easting = $("#id_site-easting").val();
    var northing = $("#id_site-northing").val();
    var elevation = $("#id_site-elevation").val();
    var grid = $("#id_site-grid_reference").val();
    var bng = $("#id_site-bng_ing").val();

    $.getJSON('/briticechrono/create_site/', {site_name: site, site_county:county, site_location:location,
        geomorph:geomorph, type:sample_type, photographs:photographs, notes:site_notes, site_operator:operator,
        photos_taken:photos_taken, collected_by:collected_by, date:stringdate, latitude:latitude,
         northing:northing, easting:easting, longitude:longitude, elevation:elevation, grid:grid, bng:bng},
        function(data){

        $.each(data, function( key, val) {
            if ((val.created) == true) {
            $('#id_main-sites').append(new Option(site));
            $('#id_fill-sites').append(new Option(site));
            $("#id_main-sites").val(site);
            $('#id_hidden-site_name').val(site);
            alert('Site Saved')
            }else if ((val.created) == false) {
                alert('Site not saved: site name must be unique and non-null')
            }
        });
  });
    $('#myModal').hide()
});

// open the Create New Site modal
$('#modalbutton2').click(function(){
    enable();
    $( "#savebutton" ).show();
    $('#id_fill-sites').val('');
    $('.site-info').css('visibility','visible');
    $('.sitech').css('visibility','visible');
    $("#ui-datepicker-div").css("z-index", "9999 !important");

 });


// initialise the tooltips
$('[data-toggle="tooltip"]').tooltip({
    'placement': 'top'
});


$(document).ready(function() {
    // check sample codes are unique and non null on page load - Edit, Validate and Create New pages
    $('#id_sample_code').keyup(function () {

    if ($('#validate').length > 0) {
        var sample = $('#id_sample_code').text();

        $.getJSON('/briticechrono/check_sample/', {sample_code: sample}, function (data) {
            $.each(data, function (key, val) {
                var response = val.exists;
                if (response == true) {
                    $('#id_sample_code').css("background-color", '#FF7F50');
                    $('#validatebutton').attr("disabled", true);
                }
                else {
                    $('#id_sample_code').css("background-color", "");
                    for (var i = 0; i < form_errors.length; i++) {
                            if (form_errors[i] = 'sample_code') {
                                removed = form_errors.splice(i, 1);
                            }
                        }
                    if (form_errors.length == 0) {
                            $('#validatebutton').attr("disabled", false);
                        }
                }
            });
        });
        }
    });
});


// enable input fields in site Modal in Edit, Validate & Create New pages
var enable = function() {
    for (var i = 0 ; i < fields.length ; i++) {
    $(fields[i]).prop( "disabled", false );
    $("#id_photos_taken").prop( "disabled", false );
    }
};

// disable input fields in site Modal in Edit, Validate & Create New pages
var disable = function() {
    for (var i = 0 ; i < fields.length ; i++) {
    $(fields[i]).prop( "disabled", true );
    $("#id_photos_taken").prop( "disabled", true );
    }
};


// get site data for Site Modal in Edit, Validate & Create New pages
var getsites = function(element) {
    var site = $(element + ' option:selected' ).val();

   $.getJSON('/briticechrono/sites/', {site_name: site}, function(data){
        var items = [];
        $.each(data, function( key, val) {

        $('#id_site_name').val(val.name, true);
        if (val.county == null) {
            val.county = ''
        }
        $('#id_county').val(val.county, true);
        $('#id_site_date').val(val.date, true);
        $('#id_site_location').val(val.loc, true);

        if (val.operator == null) {
            val.operator = ''
        }
        $('#id_operator').val(val.operator, true);
        $('#id_photographs').val(val.photographs, true);
        $('#id_site_notes').val(val.notes, true);
        $('#id_geomorph_setting').val(val.geomorph, true);
        $('#id_sample_type_collected').val(val.type, true);
        $("#id_photos_taken").val(val.photos_taken);
        $("#id_collected_by").val(val.collected_by);

        $("#id_site-latitude").val(val.latitude);
        $("#id_site-longitude").val(val.longitude);
        $("#id_site-easting").val(val.easting);
        $("#id_site-northing").val(val.northing);
        $("#id_site-elevation").val(val.elevation);
        $("#id_site-grid_reference").val(val.grid);
        $("#id_site-bng_ing").val(val.bng);
        });
    });
};


// action when fill sites dropdown is altered - Site Modal in Validate, Edit and Create New pages
$( "#id_fill-sites" ).change(function () {
    getsites("#id_fill-sites");
});


// Open site modal showing existing site and disable fields to prevent editing
$( "#modalbutton1" ).click(function () {
    getsites("#id_main-sites");
    disable();
    $('.site-info').css('visibility','hidden');
    $('.sitech').css('visibility','hidden');
});



// action to take when the skip button is pressed - increments counter and checks if all samples processed.
// Create New, Edit and Validate pages
$( "#skipbutton" ).click(function () {
    var sample = $('#id_sample_code').text();

    $.getJSON('/briticechrono/incrementcounter/', {sample_code: sample}, function (data) {
        $.each(data, function (key, val) {
            var response = val.done;

            if (response == false) {
                location.reload();
                $('#validatebutton').attr("disabled", false);
            }else{
                window.location.href = "../";
            }
        });
    });
});


// action to perfom when search button pressed in Search page.  Retrieves search criteria and performs Ajax request.
$( "#searchbutton" ).click(function () {
    $('#resultstable').empty();
    var transect = $('#transectsearch option:selected').text();
    var type = $('#sampletype option:selected').text();
    var code = $('#searchcode').val();
    var start = $('#startage').val();
    var end = $('#endage').val();
    var keyword = $('#searchkeyword').val();

    $.getJSON('/briticechrono/query/', {keyword:keyword, start:start, end:end, code:code, transect: transect, type:type},
        function (data) {
        $.each(data, function (key, val) {
             // Use returned data to populate the tabelsorter table
            $('#resultstable').append("<tr><td>"+val.code+"</td><td>"+val.sampletype+"</td>"+
                "<td>"+val.latitude+"</td><td>"+val.longitude+"</td>" +
            "<td>"+val.elevation+"</td>" + "<td>"+val.site+"</td>" + "<td>"+val.notes+"</td>" +
                "<td>"+val.cal_age+"</td>" + "<td>"+val.cal_age_error+"</td><td>"+val.age+"</td><td>"
                +val.age_error+"</td><td>"+val.lab_code+"</td><td>"+val.transect+"</td><td>"+val.retreat+"</td><td>"+
                val.c14Depth+"</td><td>"+val.c14Material+"</td><td>"+val.c14Setting+"</td><td>"+val.c14Pos+"</td><td>"+
                val.c14Weight+"</td><td>"+val.c14Contam+"</td><td>"+val.c14Curve+"</td><td>"+val.oslPosition+
                "</td><td>"+val.oslLithofacies+"</td><td>"+val.oslDepth+"</td><td>"+val.oslLithology+"</td><td>"+
                val.oslGamma+"</td><td>"+val.oslEquip+"</td><td>"+val.oslProbe+"</td><td>"+val.oslFile+"</td><td>"+
                val.oslTime+"</td><td>"+val.oslDuration+"</td><td>"+val.oslPotassium+"</td><td>"+val.oslThorium+
                "</td><td>"+val.oslUranium+"</td><td>"+val.expcore+"</td><td>"+val.core+"</td><td>"
                +val.tcnQuartz+"</td><td>"+val.tcnSetting+"</td><td>"+val.tcnMaterial+"</td><td>"+val.tcnBoulder+
                "</td><td>"+val.tcnStrike+"</td><td>"+val.tcnThickness+"</td><td>"+val.tcnGrain+"</td><td>"+
                val.tcnLithology+"</td><td>"+val.tcnBearInc+"</td></tr>")
        });
     // update the table for changes to be effected
    $("table").trigger('update').trigger("appendCache");
    });
});

// function to retrieve sample code suggestions in Enter Sample Code (Edit Sample) page
$('#id_samp_code').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/briticechrono/suggest_code/', {suggestion: query}, function(data) {
                $('#suggestion').html(data);
        });
});


// function to add sample code from suggestions to sample code input box in Enter Sample Code (Edit Sample) page
$('#suggestion').on('click', '#sugg', function() {
  var text = $(this).text();
    $('#id_samp_code').val(text);
    });


