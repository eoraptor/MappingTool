from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse

from mappingapp.forms import CoreDetailsForm, CoordinatesForm, EditCoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm, HiddenSiteForm, EditSampleSiteForm
from mappingapp.forms import SampleSiteForm, SelectSampleForm, ExistingSitesForm, EditSampleForm,\
    EditBIForm, SampleTypeForm, AgeRangeForm, KeywordForm, CodeForm, MarkersForm, EditOSLSampleForm, EditRadiocarbonForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site
from mappingapp.models import Core_Details, Radiocarbon_Sample
from mappingapp.is_member import is_member
from mappingapp.view_home import index


@login_required
@user_passes_test(is_member)
def validate_nerc_samples(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    sample = None

    # retrieve the counter from the session dictionary
    counter = str(request.session['counter'])

    # retrieve the total number of samples from the session dictionary
    num_samples = request.session['sample_count']

    # retrieve sample's errors from session dictionary
    errors = request.session['errors'+str(counter)]

    # retrieve sample's missing fields from session dictionary
    missing_keys = request.session['missing_keys'+str(counter)]

    # set sample save boolean to false in session dictionary
    if 'sample_saved' in request.session:
        sample_saved = request.session['sample_saved']
    else:
        sample_saved = False

    # have all samples been saved or skipped?  If yes return to index page
    if request.session['counter'] > num_samples:
        del request.session['counter']
        del request.session['sample_count']
        return index(request)

    # retrieve objects to populate form fields
    latitude = request.session['sample_latitude'+counter]

    longitude = request.session['sample_longitude'+counter]

    # create sample coordinates object
    try:
        sample_coords = Coordinates(latitude=latitude, longitude=longitude)
    except:
        sample_coords = None

    # create sample object
    sample = Sample(sample_code=request.session['sample_code'+counter],
                    sample_location_name=request.session['sample_location_name'+counter],
                    collection_date=request.session['sample_date'+counter],
                    collector=request.session['collector'+counter],
                    sample_notes=request.session['sample_notes'+counter])


    # create object instances specific to sample type
    radiocarbon = Radiocarbon_Sample(material=request.session['material'+counter],
                             geological_setting=request.session['setting'+counter],
                             stratigraphic_position_depth=request.session['position'+counter],
                             pot_contamination=request.session['contamination'+counter])

    # A HTTP POST?
    if request.method == 'POST':

        sampForm = SampleForm(request.POST, instance=sample)
        samplecoordForm = CoordinatesForm(request.POST, prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm(request.POST)
        sitecoordForm = CoordinatesForm(request.POST, prefix='site')
        tranForm = TransectForm(request.POST)
        retForm = RetreatForm(request.POST)
        sitechoicesForm = ExistingSitesForm(request.POST, prefix='main')
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')
        coreForm = CoreDetailsForm(request.POST)
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
                # sample exists - do not save
                request.session['sample_saved'] = False
                pass

            else:
                sample_coords = samplecoordForm.save()

                transect = tranForm.save()

                retreat = retForm.save()

                site_selected = hiddensiteForm.save()

                # set sample foreign keys
                sample.transect = transect
                sample.retreat = retreat
                sample.sample_coordinates = sample_coords
                sample.sample_site = site_selected
                sample.save()

                # add saved samples to new marker list in session dictionary - used to show newly added samples on map
                marker_list = None
                if 'new_markers' in request.session:
                    marker_list = request.session['new_markers']
                    if marker_list is not None:
                        request.session['new_markers'] = marker_list + ',' + sample.sample_code
                    else:
                        request.session['new_markers'] = sample.sample_code
                else:
                    request.session['new_markers'] = sample.sample_code

                # save C14 type data
                c14 = c14Form.save(commit=False)
                c14.c14_sample = sample
                core = coreForm.save(commit=False)
                if core.exposure_core is not None and core.exposure_core != '' and core.core_number is not None and\
                            core.core_number != '':
                    core.save()
                    c14.c14_core = core
                c14.save()

            # add file to files saved list in session dictionary
            if 'nerc_files_saved' in request.session:
                if request.session['nerc_file_name'] not in request.session['nerc_files_saved']:
                    request.session['nerc_files_saved'] = request.session['nerc_files_saved'] + ', ' +\
                                                          request.session['nerc_file_name']
            else:
                request.session['nerc_files_saved'] = request.session['nerc_file_name']

            request.session['sample_saved'] = True

            # Process remaining samples
            if request.session['counter'] < num_samples:
                counter = request.session['counter']
                request.session['counter'] = counter+1
                return HttpResponseRedirect(reverse('validate_nerc_samples'))

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
        tranForm = TransectForm()
        retForm = RetreatForm()
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        fillsiteForm = ExistingSitesForm(prefix='fill')
        coreForm = CoreDetailsForm()
        c14Form = EditRadiocarbonForm(instance=radiocarbon)


    return render_to_response('mappingapp/validate_nerc_samples.html', {'c14form': c14Form,
                                                                 'coreform': coreForm, 'missing_keys': missing_keys,
                                                                 'tranform': tranForm, 'hiddensiteform': hiddensiteForm,
                                                                 'sitechoices': sitechoicesForm,
                                                                 'samplecoordform': samplecoordForm,
                                                                 'siteform': siteForm, 'sitecoordform': sitecoordForm,
                                                                 'sampform': sampForm, 'fillsiteform': fillsiteForm,
                                                                 'is_member': is_member,  'retform': retForm,
                                                                 'sample_type': 'C14', 'errors': errors,
                                                                 'count': counter,
                                                                 'num_samples': num_samples,
                                                                 'sample_saved': sample_saved}, context)

