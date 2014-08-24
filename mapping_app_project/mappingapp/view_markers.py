from django.http import HttpResponse
from django.template import RequestContext
from mappingapp.models import Sample, Sample_Site, TCN_Sample, OSL_Sample, Radiocarbon_Sample, Coordinates
import json


# view for processing Ajax requests for marker data
def markers(request):
    context = RequestContext(request)

    sample_details = None
    samples_with_coordinates = []

    if request.method == 'GET':
        samples = Sample.objects.all()

        for sample in samples:
            if sample.sample_coordinates is not None:

                sample_type = None
                type = None
                site_name = ''

                # get site name
                if sample.sample_site is not None:
                    site_name = sample.sample_site.site_name

                # get sample type
                try:
                    type = TCN_Sample.objects.get(tcn_sample=sample)
                except:
                    pass
                if type is not None:
                    sample_type = 'tcn'

                if sample_type is None:
                    try:
                        type = OSL_Sample.objects.get(osl_sample=sample)
                    except:
                        pass
                    if type is not None:
                        sample_type = 'osl'

                if sample_type is None:
                    try:
                        type = Radiocarbon_Sample.objects.get(c14_sample=sample)
                    except:
                        pass
                    if type is not None:
                        sample_type = 'c14'

                # get sample age
                sample_age = sample.calendar_age
                if sample_age is None:
                    sample_age = ''


                data = {'latitude': sample.sample_coordinates.latitude,
                        'longitude': sample.sample_coordinates.longitude, 'code': sample.sample_code,
                        'type':sample_type, 'age': sample_age, 'site':site_name}

                samples_with_coordinates.append(data)

        if len(samples_with_coordinates) != 0:
            sample_details = json.dumps(samples_with_coordinates)

    return HttpResponse(sample_details, content_type='application/json')

