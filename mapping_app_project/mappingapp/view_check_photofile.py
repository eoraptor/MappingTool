from django.http import HttpResponse
from django.template import RequestContext
from mappingapp.models import Photograph
import json


# view for processing Ajax requests to check if photograph filename exists in database
def check_photofile(request):

    context = RequestContext(request)

    photo_filename = None

    if request.method == 'GET':
        photo_filename = 'photographs/' + request.GET['filename']

    photo = None

    # variable to return
    existing = False

    # does the sample exist?
    try:
        photo = Photograph.objects.get(photo_filename=photo_filename)
    except:
        pass

    if photo is not None:
        existing = True

    result = json.dumps([{'exists': existing}])

    return HttpResponse(result, content_type='application/json')

