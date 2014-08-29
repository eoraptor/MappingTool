from django.http import HttpResponse
from django.template import RequestContext
import json

# increments the session counter when uploading multiple samples from the same file
def incrementcounter(request):

    context = RequestContext(request)

    done = True

    if request.method == 'GET':

        counter = request.session['counter'] + 1
        request.session['counter'] = counter
        num_samples = request.session['sample_count']
        request.session['sample_saved'] = False
        if counter <= num_samples:
            done = False

    sample_details = json.dumps([{'done': done}])

    return HttpResponse(sample_details, content_type='application/json')
