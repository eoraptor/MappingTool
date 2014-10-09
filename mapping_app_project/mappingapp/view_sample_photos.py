from django.http import HttpResponse
from django.template import RequestContext
from mappingapp.models import Sample, Photo_Of, Photograph
import json


# view for processing Ajax requests to return all photographs for a sample
def sample_photos(request):

    context = RequestContext(request)

    sample_code = None

    if request.method == 'GET':
        sample_code = request.GET['sample_code']

    sample = None

    # variable to return
    existing = False

    # does the sample exist?
    try:
        sample = Sample.objects.get(sample_code=sample_code)
    except:
        pass

    if sample is not None:
        photos = ''
        photo_list = []
        try:
            photo_list = Photo_Of.objects.filter(sample_pictured=sample)
            if len(photo_list) != 0:
                for photo in photo_list:
                    photo_url = '/media/' + photo.photo_idno.photo_filename.name
                    photos += photo_url + ', '
        except:
            pass

    result = json.dumps([{'photos': photos}])

    return HttpResponse(result, content_type='application/json')

