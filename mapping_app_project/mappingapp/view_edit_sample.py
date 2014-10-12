from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory

from mappingapp.forms import CoreDetailsForm, CoordinatesForm, EditCoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm, HiddenSiteForm, EditSampleSiteForm
from mappingapp.forms import SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form, EditTCNForm
from mappingapp.forms import Location_PhotoForm, PhotoOfForm, SelectSampleForm, ExistingSitesForm, EditSampleForm,\
    EditBIForm, SampleTypeForm, AgeRangeForm, KeywordForm, CodeForm, MarkersForm, EditOSLSampleForm, EditRadiocarbonForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination, OSL_Sample, Core_Details, Radiocarbon_Sample, Photo_Of, Photograph

from mappingapp.is_member import is_member

# view for sample editing
@login_required
@user_passes_test(is_member)
def editsample(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    sample = None

    # get sample code from the session dictionary and retrieve sample object
    sample_code = request.session['sample']
    try:
        sample = Sample.objects.get(sample_code=sample_code)
    except:
        pass

    # variables
    site_name = None
    transect = None
    retreat_zone = None
    sample_coordinates = None
    osl_data = None
    c14_data = None
    tcn_data = None
    bearings = None
    num_bearings = None
    sample_type = None
    photos = []

    # determine sample type
    if sample is not None:
        try:
            tcn_data = TCN_Sample.objects.get(tcn_sample=sample)
        except:
            pass
    if tcn_data is None:
        try:
            osl_data = OSL_Sample.objects.get(osl_sample=sample)
        except:
            pass
    if tcn_data is None and osl_data is None:
        try:
            c14_data = Radiocarbon_Sample.objects.get(c14_sample=sample)
        except:
            pass

    # retrieve coordinates, transect and retreat zone instances
    if sample is not None:
        if sample.sample_site is not None:
            site_name = sample.sample_site.site_name
        sample_coordinates = sample.sample_coordinates
        transect = sample.transect
        retreat_zone = sample.retreat

    # for tcn samples retrieve bearings and inclination data and set sample type
    if tcn_data is not None:
        bearings = Sample_Bearing_Inclination.objects.filter(sample_with_bearing=tcn_data)
        sample_type = 'TCN'

        data = []
        for item in bearings:
            values = item.bear_inc
            if values is not None:
                data.append({'bearing':values.bearing, 'inclination':values.inclination})

        num_bearings = len(data)
        BearingsFormSet = formset_factory(EditBIForm, extra=40-num_bearings)

    # if OSL sample get core data and set type to OSL
    if osl_data is not None:
        core = osl_data.osl_core
        sample_type = 'OSL'

    # if C14 sample get core data and set type to C14
    if c14_data is not None:
        core = c14_data.c14_core
        sample_type = 'C14'

    # get the photographs
    if sample is not None:


        photo_list = Photo_Of.objects.filter(sample_pictured=sample)

        if len(photo_list) != 0:
            for photo in photo_list:
                    if photo.photo_idno.photo_filename is not None and photo.photo_idno.photo_filename != '':
                        photos.append(photo.photo_idno)


    # form variable names
    oslForm = None
    c14Form = None
    tcnForm = None
    coreForm = None
    bearingsFormSet = None

    # A HTTP POST?
    if request.method == 'POST':

        sampleForm = EditSampleForm(request.POST, instance=sample)
        samplecoordForm = EditCoordinatesForm(request.POST, prefix='sample', instance=sample_coordinates)
        siteForm = EditSampleSiteForm(request.POST)
        sitecoordForm = EditCoordinatesForm(request.POST, prefix='site')
        tranForm = TransectForm(request.POST, instance=transect)
        retForm = RetreatForm(request.POST, instance=retreat_zone)
        sitechoicesForm = ExistingSitesForm(request.POST, prefix='main')
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')

        # branch depending on sample type
        if tcn_data is not None:
            bearingsFormSet = BearingsFormSet(request.POST, request.FILES)
            tcnForm = EditTCNForm(request.POST, instance=tcn_data)

        elif osl_data is not None:
            oslForm = EditOSLSampleForm(request.POST, instance=osl_data)
            coreForm = CoreDetailsForm(request.POST, instance=core)

        elif c14_data is not None:
            c14Form = EditRadiocarbonForm(request.POST, instance=c14_data)
            coreForm = CoreDetailsForm(request.POST, instance=core)

        # Have we been provided with a complete set of valid forms?  If yes save forms sequentially in order to supply
        # foreign key values where required
        if sampleForm.is_valid and samplecoordForm.is_valid() and tranForm.is_valid() and retForm.is_valid() and\
                hiddensiteForm.is_valid():

            sample = sampleForm.save(commit=False)

            sample_coordinates = samplecoordForm.save()

            site_name = hiddensiteForm.save()
            sample_site = None
            try:
                sample_site = Sample_Site.objects.get(site_name=site_name)
            except:
                pass

            transect = tranForm.save()

            retreat = retForm.save()

            # add the foreign keys to sample and write to database
            sample.transect = transect
            sample.retreat = retreat
            sample.sample_coordinates = sample_coordinates
            sample.sample_site = sample_site
            sample.save()

            # TCN specific actions, including updating the bearing and inclination values.
            if sample_type == 'TCN':
                tcn = tcnForm.save(commit=False)
                tcn.tcn_sample = sample
                tcn.save()

                tracker = 0
                for form in bearingsFormSet.forms:
                    bear_inc = form.save(commit=False)
                    if bear_inc is not None:
                        if tracker < len(bearings):
                            bearings[tracker].bear_inc.bearing = bear_inc.bearing
                            bearings[tracker].bear_inc.inclination = bear_inc.inclination
                            bearings[tracker].bear_inc.save()
                            tracker += 1
                        else:
                            if bear_inc.bearing is not None and bear_inc.inclination is not None:
                                bear_inc.save()
                                Sample_Bearing_Inclination.objects.create(sample_with_bearing=tcn_data,
                                                                          bear_inc=bear_inc)
            # C14 sample type specific actions
            elif sample_type == 'C14':
                core = coreForm.save()
                c14 = c14Form.save(commit=False)
                c14.c14_sample = sample
                c14.c14_core = core
                c14.save()

            # OSL sample type specific actions
            elif sample_type == 'OSL':
                core = coreForm.save()
                osl = oslForm.save(commit=False)
                osl.osl_sample = sample
                osl.osl_core = core
                osl.save()

            # The user will be returned to the homepage.
            return HttpResponseRedirect(reverse('index'))
        else:
            # The supplied form contained errors - just print them to the terminal.
            print sampleForm.errors

    else:
        # create forms filled with instance data
        sampleForm = EditSampleForm(instance=sample)
        samplecoordForm = EditCoordinatesForm(prefix='sample', instance=sample_coordinates)
        siteForm = EditSampleSiteForm()
        sitecoordForm = EditCoordinatesForm(prefix='site')
        tranForm = TransectForm(instance=transect)
        retForm = RetreatForm(instance=retreat_zone)
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        fillsiteForm = ExistingSitesForm(request.POST, prefix='fill')

        if tcn_data is not None:
            bearingsFormSet = BearingsFormSet(initial=data)
            tcnForm = EditTCNForm(instance=tcn_data)

        elif osl_data is not None:
            oslForm = EditOSLSampleForm(instance=osl_data)
            coreForm = CoreDetailsForm(instance=core)

        elif c14_data is not None:
            c14Form = EditRadiocarbonForm(instance=c14_data)
            coreForm = CoreDetailsForm(instance=core)


    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/editsample.html', {'num_bearings': num_bearings,
                                                             'sitecoordform': sitecoordForm, 'siteform': siteForm,
                                                            'samplecoordform': samplecoordForm,'sampform': sampleForm,
                                                            'tranform': tranForm, 'hiddensiteform': hiddensiteForm,
                                                            'sitechoices': sitechoicesForm, 'retform': retForm,
                                                            'fillsiteform': fillsiteForm,'is_member': is_member,
                                                            'bearingformset': bearingsFormSet, 'tcnform': tcnForm,
                                                            'site_name': site_name, 'oslform': oslForm,
                                                            'c14form': c14Form, 'coreform': coreForm,
                                                            'sample_type': sample_type, 'photos':photos}, context)

