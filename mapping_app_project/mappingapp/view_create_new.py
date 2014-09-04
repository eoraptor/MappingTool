from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory

from mappingapp.forms import CoreDetailsForm, PhotographForm, CoordinatesForm, EditCoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm, HiddenSiteForm, EditSampleSiteForm
from mappingapp.forms import SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form, EditTCNForm
from mappingapp.forms import Location_PhotoForm, PhotoOfForm, SelectSampleForm, ExistingSitesForm, EditSampleForm,\
    EditBIForm, SampleTypeForm, AgeRangeForm, KeywordForm, CodeForm, MarkersForm, EditOSLSampleForm, EditRadiocarbonForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination, OSL_Sample, Core_Details, Radiocarbon_Sample
from mappingapp.conversion import get_transect
from mappingapp.is_member import is_member
from mappingapp.view_home import index


@login_required
@user_passes_test(is_member)
def create_new(request, sample_type_url):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    sample_type = sample_type_url.upper()

    if sample_type == 'TCN':
        BearingsFormSet = formset_factory(BearingInclinationForm, extra=40)

    tcnForm = None
    oslForm = None
    coreForm = None
    bearingsFormSet = None
    c14Form = None

    # A HTTP POST?
    if request.method == 'POST':

        sampForm = SampleForm(request.POST)
        samplecoordForm = CoordinatesForm(request.POST, prefix='sample')
        siteForm = SampleSiteForm(request.POST)
        sitecoordForm = CoordinatesForm(request.POST)
        tranForm = TransectForm(request.POST)
        retForm = RetreatForm(request.POST)
        sitechoicesForm = ExistingSitesForm(request.POST, prefix='main')
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')

        if sample_type == 'TCN':
            tcnForm = EditTCNForm(request.POST)
            bearingsFormSet = BearingsFormSet(request.POST, request.FILES)

        elif sample_type == 'OSL':
            oslForm = EditOSLSampleForm(request.POST)
            coreForm = CoreDetailsForm(request.POST)

        elif sample_type == 'C14':
            coreForm = CoreDetailsForm(request.POST)
            c14Form = EditRadiocarbonForm(request.POST)

        # Have we been provided with a complete set of valid forms?  If yes save forms sequentially in order to supply
        # foreign key values where required
        if sampForm.is_valid and samplecoordForm.is_valid() and tranForm.is_valid() and retForm.is_valid() and\
                hiddensiteForm.is_valid():

            sample = None
            sample = sampForm.save(commit=False)

            # prevent second save of existing form if user presses back on browser
            existing = None
            if sample.sample_code is not None:
                try:
                    existing = Sample.objects.get(sample_code=sample.sample_code)
                except:
                    pass

            if existing is not None:
                pass
            else:
                sample_coords = samplecoordForm.save()

                transect = tranForm.save()

                retreat = retForm.save()

                site_selected = hiddensiteForm.save()

                sample.transect = transect
                sample.retreat = retreat
                sample.sample_coordinates = sample_coords
                sample.sample_site = site_selected
                sample.save()

                core = None

                if sample_type == 'OSL' or sample_type == 'C14':
                    core = coreForm.save()

                if sample_type == 'C14':
                    c14 = c14Form.save(commit=False)
                    if c14 is not None:
                        c14.c14_sample = sample
                        c14.c14_core = core
                        c14.save()

                if sample_type == 'OSL':
                    osl = oslForm.save(commit=False)
                    if osl is not None:
                        osl.osl_sample = sample
                        osl.osl_core = core
                        osl.save()

                if sample_type == 'TCN':
                    tcn = tcnForm.save(commit=False)
                    if tcn is not None:
                        tcn.tcn_sample = sample
                        tcn.save()

                        for form in bearingsFormSet.forms:
                                bear_inc = form.save()
                                if bear_inc is not None:
                                    sample_bearing = Sample_Bearing_Inclination.objects.create(sample_with_bearing=tcn,
                                                                                             bear_inc=bear_inc)

                if sample is not None:
                    request.session['new_markers'] = sample.sample_code

                # all samples checked, return to home page
                return HttpResponseRedirect(reverse('index'))
        else:
            # The supplied form contained errors
            print sampForm.errors

    else:
        sampForm = SampleForm()
        samplecoordForm = CoordinatesForm(prefix='sample')
        siteForm = SampleSiteForm()
        sitecoordForm = CoordinatesForm(prefix='site')
        tranForm = TransectForm()
        retForm = RetreatForm()
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        fillsiteForm = ExistingSitesForm(prefix='fill')

        if sample_type == 'TCN':
            tcnForm = EditTCNForm()
            bearingsFormSet = BearingsFormSet()

        elif sample_type == 'OSL':
            oslForm = EditOSLSampleForm()
            coreForm = CoreDetailsForm()

        elif sample_type == 'C14':
            coreForm = CoreDetailsForm()
            c14Form = EditRadiocarbonForm()


    return render_to_response('mappingapp/create_new.html', {'c14form':c14Form,
                                                                 'coreform':coreForm,
                                                                 'tranform': tranForm, 'hiddensiteform':hiddensiteForm,
                                                                 'sitechoices':sitechoicesForm,
                                                                 'samplecoordform':samplecoordForm,
                                                                 'siteform': siteForm, 'sitecoordform':sitecoordForm,
                                                                 'sampform':sampForm, 'fillsiteform':fillsiteForm,
                                                                 'is_member':is_member,  'retform': retForm,
                                                                 'sample_type':sample_type,
                                                                 'bearingformset':bearingsFormSet,  'tcnform':tcnForm,
                                                                 'oslform':oslForm}, context)


