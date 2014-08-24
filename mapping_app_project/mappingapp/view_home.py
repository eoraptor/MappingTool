from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from mappingapp.forms import MarkersForm


# the main map page and home of the app
def index(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # get newly saved markers
    new_markers = None

    if 'markers' in request.session:
        del request.session['markers']
        request.session.modified = True

    if 'new_markers' in request.session:
       new_markers = request.session['new_markers']

    # form to submit markers from users drawing on the map
    if request.method == 'POST':
        form = MarkersForm(request.POST)

        if form.is_valid():
            markers = form.cleaned_data['sample_codes']

            request.session['markers'] = markers

            # Redirect to search page with marker data
            return HttpResponseRedirect(reverse('search'))
    else:
        form = MarkersForm()

    return render_to_response('mappingapp/index.html', {'form':form, 'is_member':is_member, 'new_markers':new_markers},
                              context)

