from django.http import HttpResponse
from django.template import RequestContext
import json
import datetime
from mappingapp.models import Coordinates, Sample_Site


# View to get site details in response to Ajax request from Sample Validate/Edit pages - populates Modal fields
def sites(request):

    context = RequestContext(request)

    site_details = None
    site_name = None
    site = None
    coordinates = None
    date = None
    photos_taken = 1

    if request.method == 'GET':
        site_name = request.GET['site_name']

    try:
        site = Sample_Site.objects.get(site_name=site_name)
        coordinates = site.site_coordinates
    except:
        pass

    if site is not None:
        date = site.site_date
        if date is not None:
            date = date.strftime("%d/%m/%Y")

        if site.photos_taken is True:
             photos_taken = 2
        elif site.photos_taken is False:
             photos_taken = 3

    if coordinates is not None and site is not None:
        site_details = json.dumps([{'name':site.site_name, 'loc':site.site_location, 'county':site.county,
                                    'operator':site.operator, 'type':site.sample_type_collected,
                                    'geomorph':site.geomorph_setting, 'photographs':site.photographs,
                                    'notes':site.site_notes, 'photos_taken':photos_taken, 'bng':coordinates.bng_ing,
                                    'grid':coordinates.grid_reference, 'collected_by':site.collected_by,
                                    'easting':coordinates.easting, 'northing':coordinates.northing,
                                    'latitude':coordinates.latitude, 'longitude':coordinates.longitude,
                                    'elevation':coordinates.elevation, 'date':date}])
    elif site is not None:
        site_details = json.dumps([{'name':site.site_name, 'loc':site.site_location, 'county':site.county,
                                    'operator':site.operator, 'type':site.sample_type_collected,
                                    'geomorph':site.geomorph_setting, 'photographs':site.photographs,
                                    'notes':site.site_notes, 'photos_taken':photos_taken,
                                    'date':date, 'collected_by':site.collected_by}])

    return HttpResponse(site_details, content_type='application/json')
