var fields = ['#id_site_name', '#id_county', '#id_site_date', '#id_site_location', '#id_operator', '#id_photographs',
'#id_site_notes', '#id_geomorph_setting', '#id_sample_type_collected', "#id_site-latitude", '#id_site-longitude',
"#id_site-easting", "#id_site-northing", "#id_site-elevation", "#id_site-grid_reference", "#id_site-bng_ing",
    "#id_collected_by"];

var sample_fields = ['#id_sample_thickness', '#id_sample_code', '#id_collection_date', '#id_collector',
'#id_sample_location_name', '#id_sampled_material', '#id_lithology', '#id_quartz_content',
'#id_sample_surface_strike_dip', '#id_boulder_dimensions', '#id_grain_size', '#id_sample_setting',
'#id_sample_notes', '#id_sample-latitude', '#id_sample-longitude', '#id_sample-easting', '#id_sample-northing',
'#id_sample-elevation', '#id_sample-bng_ing'];

var $table;

$(document).ready(function(){
    $('#savebutton').hide();

    if ($('#site_option').text() == 'None') {
        $('#modalbutton1').attr("disabled", true);
    }

    $('.td').click(function() {
    var text = $(this).text();
    $('#id_samp_code').val(text);
    });

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
                widgets: ['zebra', 'filter', 'columnSelector','output'],
                widgetOptions : {
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
      // see http://view.jquerymobile.com/1.3.2/dist/demos/widgets/table-column-toggle/#Applyingapresetbreakpoint
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

    $('textarea[name=sample_code]').keyup(function() {
    $('#id_sample_code').text($(this).val());
    });

    var site_name = $('#site_option').text();
    if (site_name != 'None') {
        $('#id_main-sites').val(site_name);
    }
    $('#site_selected').text(site_name);
    $('#id_hidden-site_name').val(site_name);

    // check if TCN spreadsheet has incorrect field names.  Will need similar checks for OSL and C14
    for (var i = 0 ; i < sample_fields.length ; i++) {
        if ($(sample_fields[i]).val() == "TCN Sample Sheet") {
            $(sample_fields[i]).val('');
            $(sample_fields[i]).css("border-color", 'red');
        }
    }

    if ($('#validate').length > 0) {
        var sample = $('#id_sample_code').text();

        $.getJSON('/mappingapp/check_sample/', {sample_code: sample}, function (data) {
            $.each(data, function (key, val) {
                var response = val.exists;
                if (response == true) {
                    $('#id_sample_code').css("background", '#FF7F50');
                    $('#validatebutton').attr("disabled", true);
                    alert('Sample Code already exists.');
                }

            });
        });
    }
});



$('#id_main-sites').change(function() {
    var selected = $('#id_main-sites option:selected').val();
    $('#id_hidden-site_name').val(selected);
    if (selected == '') {
        $('#modalbutton1').attr("disabled", true);
    }else{
        $('#modalbutton1').attr("disabled", false);
    }
});


$('#myModal').on('hidden.bs.modal', function (e) {
    for (var i = 0; i < fields.length ; i++) {
        $(fields[i]).val('');
    }
    $("#id_photos_taken").val(1);
     $( "#savebutton" ).hide();
});



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

    $.getJSON('/mappingapp/create_site/', {site_name: site, site_county:county, site_location:location,
        geomorph:geomorph, type:sample_type, photographs:photographs, notes:site_notes, site_operator:operator,
        photos_taken:photos_taken, collected_by:collected_by, date:stringdate, latitude:latitude,
         northing:northing, easting:easting, longitude:longitude, elevation:elevation, grid:grid, bng:bng}, function(data){

        $.each(data, function( key, val) {
            if ((val.created) == true) {
            $('#id_main-sites').append(new Option(site))
            $('#id_fill-sites').append(new Option(site))
            alert('Site Saved')
            }else if ((val.created) == false) {
                alert('Site Already Exists')
            }
        });
    $("#id_main-sites").val(site);
  });
    $('#myModal').hide()
});


$('#modalbutton2').click(function(){
    enable();
    $( "#savebutton" ).show();
    $('#id_fill-sites').val('');
    $('.site-info').css('visibility','visible');
    $('.sitech').css('visibility','visible');

 });


$('[data-toggle="tooltip"]').tooltip({
    'placement': 'top'
});


$(document).ready(function() {
    $('#id_sample_code').keyup(function () {
        var sample1 = $('#id_sample_code').text();
    if ($('#validate').length > 0) {
        var sample = $('#id_sample_code').text();

        $.getJSON('/mappingapp/check_sample/', {sample_code: sample1}, function (data) {
            $.each(data, function (key, val) {
                var response = val.exists;
                if (response == true) {
                    $('#id_sample_code').css("background", '#FF7F50');
                    $('#validatebutton').attr("disabled", true);
                }
                else {
                    $('#id_sample_code').css("background", 'white');
                    $('#validatebutton').attr("disabled", false);
                }
            });
        });
        }
    });
});


var enable = function() {
    for (var i = 0 ; i < fields.length ; i++) {
    $(fields[i]).prop( "disabled", false );
    $("#id_photos_taken").prop( "disabled", false );
    }
};

var disable = function() {
    for (var i = 0 ; i < fields.length ; i++) {
    $(fields[i]).prop( "disabled", true );
    $("#id_photos_taken").prop( "disabled", true );
    }
};


var getsites = function(element) {
    var site = $(element + ' option:selected' ).val();

   $.getJSON('/mappingapp/sites/', {site_name: site}, function(data){
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



$( "#id_fill-sites" ).change(function () {
    getsites("#id_fill-sites");
});


$( "#modalbutton1" ).click(function () {
    getsites("#id_main-sites");
    disable();
    $('.site-info').css('visibility','hidden');
    $('.sitech').css('visibility','hidden');
});


$( "#skipbutton" ).click(function () {
    var sample = $('#id_sample_code').text();

    $.getJSON('/mappingapp/incrementcounter/', {sample_code: sample}, function (data) {
        $.each(data, function (key, val) {
            var response = val.done;
            if (response == false) {
                location.reload();
                $('#validatebutton').attr("disabled", false);
            }else{
//          !!!!      This must be changed when not on local machine !!!
                window.location.replace("http://127.0.0.1:8000/mappingapp/");
            }
        });
    });
});


$( "#searchbutton" ).click(function () {
    $('#resultstable').empty();
    var transect = $('#transectsearch option:selected').text();
    var type = $('#sampletype option:selected').text();
    var code = $('#searchcode').val();
    var start = $('#startage').val();
    var end = $('#endage').val();
    var keyword = $('#searchkeyword').val();

    $.getJSON('/mappingapp/query/', {keyword:keyword, start:start, end:end, code:code, transect: transect, type:type},
        function (data) {
        $.each(data, function (key, val) {

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
                val.tcnLithology+"</td></tr>")
        });
    $("table").trigger('update').trigger("appendCache");
    });
});

// function to retrieve sample code suggestions in Enter Sample Code (Edit Sample) page
$('#id_samp_code').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/mappingapp/suggest_code/', {suggestion: query}, function(data) {
                $('#suggestion').html(data);
        });
});


// function to add sample code from suggestions to sample code input box in Enter Sample Code (Edit Sample) page
$('#suggestion').on('click', '#sugg', function() {
  var text = $(this).text();
    $('#id_samp_code').val(text);
    });


