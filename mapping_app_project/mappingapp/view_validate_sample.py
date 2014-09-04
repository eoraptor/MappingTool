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
def validatesample(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    counter = str(request.session['counter'])

    num_samples = request.session['sample_count']

    errors = request.session['errors'+str(counter)]

    missing_keys = request.session['missing_keys'+str(counter)]

    if 'sample_saved' in request.session:
        sample_saved = request.session['sample_saved']
    else:
        sample_saved = False

    num_bearings = None
    if request.session['counter'] > num_samples:
        del request.session['counter']
        del request.session['sample_count']
        return index(request)

    # retrieve objects to populate form fields
    sample = None

    num_bearings = None

    site_name = request.session['site_name']

    latitude = request.session['sample_latitude'+counter]

    longitude = request.session['sample_longitude'+counter]

    # set lat/long to site values if sample has no lat/long values
    if latitude is None or longitude is None:
        site_coordinates = None
        site = None
        try:
            site = Sample_Site.objects.get(site_name=site_name)
        except:
            pass

        if site is not None:
            try:
                site_coordinates = site.site_coordinates
            except:
                pass

        if site_coordinates is not None:
            if latitude is None:
                latitude = site_coordinates.latitude
            if longitude is None:
                longitude = site_coordinates.longitude

    sample_coords = Coordinates(bng_ing=request.session['sample_bng_ing'+counter],
                                grid_reference=request.session['sample_grid_reference'+counter],
                                easting=request.session['sample_easting'+counter],
                                northing=request.session['sample_northing'+counter],
                                latitude=latitude, longitude=longitude,
                                elevation=request.session['sample_elevation'+counter])

    sample = Sample(sample_code=request.session['sample_code'+counter],
                    sample_location_name=request.session['sample_location_name'+counter],
                    collection_date=request.session['sample_date'+counter],
                    collector=request.session['collector'+counter],
                    sample_notes=request.session['sample_notes'+counter])

    sample_type = request.session['sample_type'+counter]

    transect = None
    if request.session['transect'+counter] is not None:
        transect = Transect(transect_number=request.session['transect'+counter])

    if transect is None and site_name is not None:
        transect = get_transect(site_name)

    retreat = None

    if sample_type == 'C14':
        radiocarbon = Radiocarbon_Sample(depth_below_SL=request.session['depth'+counter],
                                 material=request.session['material'+counter],
                                 geological_setting=request.session['setting'+counter],
                                 stratigraphic_position_depth=request.session['position'+counter],
                                 sample_weight=request.session['weight'+counter],
                                 pot_contamination=request.session['contamination'+counter])

        core = Core_Details(exposure_core=request.session['exposure_core'+counter],
                        core_number=request.session['core_number'+counter])

    elif sample_type == 'OSL':
        osl = OSL_Sample(stratigraphic_position=request.session['position'+counter],
                         lithofacies=request.session['lithofacies'+counter],
                         burial_depth=request.session['burial_depth'+counter],
                         lithology=request.session['lithology'+counter],
                         gamma_spec=request.session['gamma_spec'+counter],
                         equipment_number=request.session['equipment_number'+counter],
                         probe_serial_no=request.session['probe_number'+counter],
                         filename=request.session['filename'+counter],
                         sample_time=request.session['sample_time'+counter],
                         sample_duration=request.session['sample_duration'+counter],
                         potassium=request.session['potassium'+counter],
                         thorium=request.session['thorium'+counter],
                         uranium=request.session['uranium'+counter])

        core = Core_Details(exposure_core=request.session['exposure_core'+counter],
                        core_number=request.session['core_number'+counter])

    elif sample_type == 'TCN':
        tcn = TCN_Sample(quartz_content=request.session['quartz_content'+counter],
                         sample_setting=request.session['sample_setting'+counter],
                         sampled_material=request.session['sampled_material'+counter],
                         boulder_dimensions=request.session['boulder_dimensions'+counter],
                         sample_surface_strike_dip=request.session['sample_surface_strike_dip'+counter],
                         sample_thickness=request.session['sample_thickness'+counter],
                         grain_size=request.session['grain_size'+counter],
                         lithology=request.session['lithology'+counter])

        bearings = None

        if 'bearings'+counter in request.session:
            bearings = request.session['bearings'+counter]


        data = []
        if bearings is not None:
            for item in bearings:
                dict = {}
                dict['bearing'] = item[0]
                dict['inclination'] = item[1]
                data.append(dict)

        num_bearings = len(data)
        BearingsFormSet = formset_factory(BearingInclinationForm, extra=40-num_bearings)

    tcnForm = None
    oslForm = None
    coreForm = None
    bearingsFormSet = None
    c14Form = None

    # A HTTP POST?
    if request.method == 'POST':

        sampForm = SampleForm(request.POST, instance=sample)
        samplecoordForm = CoordinatesForm(request.POST, prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm(request.POST)
        sitecoordForm = CoordinatesForm(request.POST, prefix='site')
        tranForm = TransectForm(request.POST, instance=transect)
        retForm = RetreatForm(request.POST, instance=retreat)
        sitechoicesForm = ExistingSitesForm(request.POST, prefix='main')
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')

        if sample_type == 'TCN':
            tcnForm = EditTCNForm(request.POST, instance=tcn)
            bearingsFormSet = BearingsFormSet(request.POST, request.FILES)

        elif sample_type == 'OSL':
            oslForm = EditOSLSampleForm(request.POST, instance=osl)
            coreForm = CoreDetailsForm(request.POST, instance=core)

        elif sample_type == 'C14':
            coreForm = CoreDetailsForm(request.POST, instance=core)
            c14Form = EditRadiocarbonForm(request.POST, instance=radiocarbon)

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
                request.session['sample_saved'] = False
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

                marker_list = None
                if 'new_markers' in request.session:
                    marker_list = request.session['new_markers']
                    if marker_list is not None:
                        request.session['new_markers'] = marker_list + ',' + sample.sample_code
                    else:
                        request.session['new_markers'] = sample.sample_code
                else:
                    request.session['new_markers'] = sample.sample_code


                if sample_type == 'OSL' or sample_type == 'C14':
                    core = coreForm.save()

                if sample_type == 'C14':
                    c14 = c14Form.save(commit=False)
                    c14.c14_sample = sample
                    c14.c14_core = core
                    c14.save()

                if sample_type == 'OSL':
                    osl = oslForm.save(commit=False)
                    osl.osl_sample = sample
                    osl.osl_core = core
                    osl.save()

                if sample_type == 'TCN':
                    tcn = tcnForm.save(commit=False)
                    tcn.tcn_sample = sample
                    tcn.save()


                    for form in bearingsFormSet.forms:
                        bear_inc = form.save()
                        if bear_inc is not None:
                            sample_bearing = Sample_Bearing_Inclination.objects.create(sample_with_bearing=tcn,
                                                                                     bear_inc=bear_inc)



            if 'files_saved' in request.session:
                if request.session['file_name'] not in request.session['files_saved']:
                    request.session['files_saved'] = request.session['files_saved'] + ', ' + request.session['file_name']
            else:
                request.session['files_saved'] = request.session['file_name']

            request.session['sample_saved'] = True

            # Process remaining samples
            if request.session['counter'] < num_samples:
                counter = request.session['counter']
                request.session['counter'] = counter+1
                return HttpResponseRedirect(reverse('validatesample'))

            else:
                # all samples checked, return to home page
                return HttpResponseRedirect(reverse('index'))
        else:
            # The supplied form contained errors
            print sampForm.errors
    else:
        sampForm = SampleForm(instance=sample)
        samplecoordForm = CoordinatesForm(prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm()
        sitecoordForm = CoordinatesForm(prefix='site')
        tranForm = TransectForm(instance=transect)
        retForm = RetreatForm(instance=retreat)
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        fillsiteForm = ExistingSitesForm(prefix='fill')

        if sample_type == 'TCN':
            tcnForm = EditTCNForm(instance=tcn)
            bearingsFormSet = BearingsFormSet(initial=data)

        elif sample_type == 'OSL':
            oslForm = EditOSLSampleForm(instance=osl)
            coreForm = CoreDetailsForm(instance=core)

        elif sample_type == 'C14':
            coreForm = CoreDetailsForm(instance=core)
            c14Form = EditRadiocarbonForm(instance=radiocarbon)


    return render_to_response('mappingapp/validatesample.html', {'num_bearings':num_bearings, 'c14form':c14Form,
                                                                 'coreform':coreForm, 'missing_keys':missing_keys,
                                                                 'tranform': tranForm, 'hiddensiteform':hiddensiteForm,
                                                                 'site_name':site_name, 'sitechoices':sitechoicesForm,
                                                                 'samplecoordform':samplecoordForm,
                                                                 'siteform': siteForm, 'sitecoordform':sitecoordForm,
                                                                 'sampform':sampForm, 'fillsiteform':fillsiteForm,
                                                                 'is_member':is_member,  'retform': retForm,
                                                                 'sample_type':sample_type, 'errors':errors,
                                                                 'bearingformset':bearingsFormSet,  'tcnform':tcnForm,
                                                                 'oslform':oslForm, 'count':counter,
                                                                 'num_samples':num_samples,
                                                                 'sample_saved':sample_saved}, context)

