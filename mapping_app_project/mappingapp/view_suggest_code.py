from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from mappingapp.models import Sample


# helper function - performs query to get list of suggestions
def get_sample_code_list(starts_with=''):

    code_list = []
    code_samples = None

    if starts_with:
        code_samples = Sample.objects.filter(Q(sample_code__istartswith=starts_with))

    else:
        code_samples = Sample.objects.all()

    if code_samples is not None:
        for sample in code_samples:
            code_list.append(sample.sample_code)
            code_list.sort()

    if len(code_list) > 50:
        code_list = code_list[:50]

    return code_list


# view to populate suggestions list as user types into the sample code input on the Edit Sample code selection page
def suggest_code(request):
    context = RequestContext(request)
    code_list = []
    starts_with = ''

    if request.method == 'GET':

        starts_with = request.GET['suggestion']

        code_list = get_sample_code_list(starts_with)

    return render_to_response('mappingapp/code_list.html', {'code_list': code_list }, context)


