from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
# the search page - accessible to logged in users
def search(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    samples = None

    if 'markers' in request.session:
        sample_codes = request.session['markers']
        samples = [code.strip() for code in sample_codes.split(',')]

        del request.session['markers']
        request.session.modified = True

    return render_to_response('mappingapp/search.html', {'samples':samples, 'is_member':is_member}, context)

