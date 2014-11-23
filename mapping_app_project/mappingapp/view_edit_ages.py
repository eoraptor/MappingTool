from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory

from mappingapp.forms import EditSampleAgesForm
from mappingapp.models import Document, Sample
from mappingapp.is_member import is_member

# view for sample editing
@login_required
@user_passes_test(is_member)
def edit_ages(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # form variable names
    SampleFormSet = modelformset_factory(Sample, form=EditSampleAgesForm, extra=0, fields=['sample_code', 'age', 'age_error',
                                                                          'calendar_age', 'calendar_error', 'lab_code'])

    sampleForms = None

    # A HTTP POST?
    if request.method == 'POST':

        sampleForms = SampleFormSet(request.POST, request.FILES,
                                    queryset=Sample.objects.filter(calendar_age__isnull=True))

        # Have we been provided with a complete set of valid forms?
        if sampleForms.is_valid:

            sampleForms.save()

            # The user will be returned to the homepage.
            return HttpResponseRedirect(reverse('index'))

        else:
            # The supplied form contained errors - just print them to the terminal.
            print sampleForms.errors

    else:
        # create forms filled with instance data
        sampleForms = SampleFormSet(queryset=Sample.objects.filter(calendar_age__isnull=True).order_by('sample_code'))

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/editages.html', {'sampleForms': sampleForms, 'is_member': is_member}, context)


