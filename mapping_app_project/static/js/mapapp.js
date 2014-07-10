 $('#modalbutt').click(function(){
    var site = $('#id_sites option:selected').text();

     $.getJSON('/mappingapp/sites/', {site_name: site}, function(data){
         var items = [];
         $.each(data, function( key, val) {
         $('#site-name').text(val.name, true);
           });
     });
});
