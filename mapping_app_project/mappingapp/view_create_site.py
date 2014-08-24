from django.http import HttpResponse
from django.template import RequestContext
import json
import datetime

from mappingapp.models import Coordinates, Sample_Site


# View to create site in response to Ajax request from Sample Validate & Edit pages
def create_site(request):

    context = RequestContext(request)

    site_name = None

    if request.method == 'GET':
        site_name = request.GET['site_name']
        site_county = request.GET['site_county']
        site_location = request.GET['site_location']
        site_date = request.GET['date']
        site_operator = request.GET['site_operator']
        photographs = request.GET['photographs']
        notes = request.GET['notes']
        type = request.GET['type']
        geomorph = request.GET['geomorph']
        photos_taken = request.GET['photos_taken']
        collected_by = request.GET['collected_by']

        if site_date == '':
            date = None
        else:
            date = datetime.datetime.strptime(site_date, '%d/%m/%Y').date()

        if photos_taken == '1':
            photos_taken = None
        elif photos_taken == '2':
            photos_taken = True
        else:
            photos_taken = False

        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        easting = request.GET['easting']
        northing = request.GET['northing']
        elevation = request.GET['elevation']
        grid = request.GET['grid']
        bng = request.GET['bng']

        site = Sample_Site.objects.get_or_create(site_name=site_name, county=site_county,site_location=site_location,
                                                 site_notes=notes, photographs=photographs, operator=site_operator,
                                                 photos_taken=photos_taken, collected_by=collected_by,
                                                 geomorph_setting=geomorph, sample_type_collected=type,
                                                 site_date=date)

        # new site created ---> create set of coordinates.  Being by setting empty number fields to None
        if site[1] is True:
            if easting == '':
                 easting = None
            if northing == '':
                northing = None
            if latitude == '':
                latitude = None
            if longitude == '':
                longitude = None

            coordinates = Coordinates.objects.create(elevation=elevation, latitude=latitude, longitude=longitude,
                                                 grid_reference=grid, bng_ing=bng, easting=easting, northing=northing,)

            sample_site = site[0]
            sample_site.site_coordinates = coordinates
            sample_site.save()

        reply = json.dumps([{'created':site[1]}])

        return HttpResponse(reply, content_type='application/json')
