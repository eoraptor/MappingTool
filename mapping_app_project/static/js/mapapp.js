 $('#modalbutton').click(function(){
    var site = $('#id_sites option:selected').text();

     $.getJSON('/mappingapp/sites/', {site_name: site}, function(data){
         var items = [];
         $.each(data, function( key, val) {
         $('#id_site_name').text(val.name, true);
         if (val.county == null) {
             val.county = ''
         }
         $('#id_county').text(val.county, true);
         $('#id_site_date').text(val.date, true);
         $('#id_site_location').text(val.loc, true);
         if (val.operator == null) {
             val.operator = ''
         }
         $('#id_operator').text(val.operator, true);
         $('#id_photographs').text(val.photographs, true);
         $('#id_site_notes').text(val.notes, true);
         $('#id_geomorph_setting').text(val.geomorph, true);

         $('#id_sample_type_collected').text(val.type, true);
         if (val.photos_taken == True) {
             val.photos_taken = 'Yes'
         }else if (val.photos_taken == False) {
             val.photos_taken = 'No'
         }else {
             val.photos_taken = 'Unknown'
         }
         $('#id_photos_taken').text(val.photos_taken, true);
           });
     });
});
