from django.http import HttpResponse
from django.template import RequestContext
from mappingapp.models import Sample
import json


# view for processing Ajax requests to check if sample exists in database
def check_sample(request):

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
        existing = True

    result = json.dumps([{'exists': existing}])

    return HttpResponse(result, content_type='application/json')
