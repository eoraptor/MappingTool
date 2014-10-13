from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse

from mappingapp.is_member import is_member
from mappingapp.models import Sample
from mappingapp.forms import SelectSampleForm


# view for sample selection page of edit sample process
@login_required
@user_passes_test(is_member)
def edit(request):
    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # get complete list of sample codes to display
    samplecodelist = Sample.objects.values_list('sample_code', flat=True).order_by('sample_code')

    # get sample code from form
    if request.method == 'POST':
        sample_code = request.POST['samp_code']

        if sample_code is not None:

            # add sample code to session dictionary
            request.session['sample'] = sample_code

            # does sample exist?
            try:
                Sample.objects.get(sample_code=sample_code)
                return HttpResponseRedirect(reverse('editsample'))
            # if not
            except:
                return HttpResponseRedirect(reverse('error', args=('sample_error',)))

    else:
        # an empty form
       selectsampleform = SelectSampleForm()

    return render_to_response('mappingapp/edit.html', {'sample_codes': samplecodelist, 'is_member': is_member,
                                                       'selectsampleform': selectsampleform}, context)


