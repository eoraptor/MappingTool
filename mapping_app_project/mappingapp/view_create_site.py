from django.http import HttpResponse
from django.template import RequestContext
import json
import datetime

from mappingapp.models import Coordinates, Sample_Site


# View to create site in response to Ajax request from Sample Validate & Edit pages
def create_site(request):

    context = RequestContext(request)

    # variable to return - True if new site created, False if not
    new_site = False

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

        # create date or set to None
        if site_date == '':
            date = None
        else:
            date = datetime.datetime.strptime(site_date, '%d/%m/%Y').date()

        # set Photograph values
        if photos_taken == '1':
            photos_taken = None
        elif photos_taken == '2':
            photos_taken = True
        else:
            photos_taken = False

        # values for site coordinates
        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        easting = request.GET['easting']
        northing = request.GET['northing']
        elevation = request.GET['elevation']
        grid = request.GET['grid']
        bng = request.GET['bng']

        # does site with that name already exist?
        sample_site = None
        try:
            sample_site = Sample_Site.objects.get(site_name=site_name)

        except:
            pass

        # no name match - create site
        if sample_site is None and site_name != '' and site_name is not None:
            sample_site = Sample_Site.objects.create(site_name=site_name, county=site_county,
                                                 site_location=site_location, site_notes=notes,
                                                 photographs=photographs, operator=site_operator,
                                                 photos_taken=photos_taken, collected_by=collected_by,
                                                 geomorph_setting=geomorph, sample_type_collected=type,
                                                 site_date=date)

            # if new site created ---> create set of coordinates.  Begin by setting empty number fields to None
            if sample_site is not None:
                if easting == '':
                    easting = None
                if northing == '':
                    northing = None
                if latitude == '':
                    latitude = None
                if longitude == '':
                    longitude = None

                # if all fields null or None don't create a coordinates instance
                if bng == '' and grid == '' and easting is None and northing is None and latitude is None and\
                        longitude is None and elevation == '':
                    coordinates = None

                else:
                    coordinates = Coordinates.objects.create(elevation=elevation, latitude=latitude,
                                                             longitude=longitude, grid_reference=grid, bng_ing=bng,
                                                             easting=easting, northing=northing,)

                # add coordinates to site
                sample_site.site_coordinates = coordinates
                sample_site.save()
                new_site = True

        # return boolean to show if site created or not
        reply = json.dumps([{'created':new_site}])

        return HttpResponse(reply, content_type='application/json')
