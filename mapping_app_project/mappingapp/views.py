from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, modelformset_factory
from django.db.models import Q
import json
import csv
import datetime, time

from mappingapp.forms import UploadFileForm, CoreDetailsForm, PhotographForm, CoordinatesForm, EditCoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm, HiddenSiteForm, EditSampleSiteForm
from mappingapp.forms import SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form, EditTCNForm
from mappingapp.forms import Location_PhotoForm, PhotoOfForm, SelectSampleForm, ExistingSitesForm, EditSampleForm,\
    EditBIForm, SampleTypeForm, AgeRangeForm, KeywordForm, CodeForm, MarkersForm, EditOSLSampleForm, EditRadiocarbonForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination, OSL_Sample, Core_Details, Radiocarbon_Sample
from mappingapp.extract import process_file
from mappingapp.conversion import get_transect



def is_member(user):
    return user.groups.filter(name='Consortium Super User')

def markers(request):
    context = RequestContext(request)

    sample_details = None

    if request.method == 'GET':
        samples = Sample.objects.all()
        samples_with_coordinates = []

        for sample in samples:
            if sample.sample_coordinates is not None:

                sample_type = None
                type = None

                try:
                    type = TCN_Sample.objects.get(tcn_sample=sample)
                except:
                    pass
                if type is not None:
                    sample_type = 'tcn'

                if sample_type is None:
                    try:
                        type = OSL_Sample.objects.get(osl_sample=sample)
                    except:
                        pass
                    if type is not None:
                        sample_type = 'osl'

                if sample_type is None:
                    try:
                        type = Radiocarbon_Sample.objects.get(c14_sample=sample)
                    except:
                        pass
                    if type is not None:
                        sample_type = 'c14'

                data = {'latitude': sample.sample_coordinates.latitude,
                        'longitude': sample.sample_coordinates.longitude,
                        'code': sample.sample_code, 'type':sample_type}

                samples_with_coordinates.append(data)

        if len(samples_with_coordinates) != 0:
            sample_details = json.dumps(samples_with_coordinates)

    return HttpResponse(sample_details, mimetype='application/json')


# check to see if sample exists in database
def check_sample(request):
    context = RequestContext(request)

    if request.method == 'GET':
        sample_code = request.GET['sample_code']

    sample = None
    existing = False

    try:
        sample = Sample.objects.get(sample_code=sample_code)
    except:
        pass

    if sample is not None:
        existing = True

    result = json.dumps([{'exists': existing}])

    return HttpResponse(result, mimetype='application/json')


# search functionality
def query(request):
    context = RequestContext(request)

    results = []
    transect_object = None
    type = None
    type_samples = None
    code_samples = None
    age_samples = None
    keyword_samples = None
    samples = None


    if request.method == 'GET':
        transect = request.GET['transect']
        type = request.GET['type']
        sample_code = request.GET['code']
        start_age = request.GET['start']
        end_age = request.GET['end']
        keyword = request.GET['keyword']

    # search for samples belonging to one transect
    if transect != '':
        try:
            transect_object = Transect.objects.get(transect_number=transect)
        except:
            pass

    if transect_object is not None:
        samples = Sample.objects.filter(transect=transect_object)

    # search for samples of one type
    if type != '' and type is not None:
        type_samples = []
        sample_list = None
        if type == 'TCN':
            sample_list = TCN_Sample.objects.values_list('tcn_sample', flat=True)
        elif type == 'OSL':
            sample_list = OSL_Sample.objects.values_list('osl_sample', flat=True)
        elif type == 'C14':
            sample_list = Radiocarbon_Sample.objects.values_list('c14_sample', flat=True)

        if sample_list is not None:
            for pk in sample_list:
                type_samples.append(Sample.objects.get(pk=pk))

    if samples is not None and type_samples is not None:
        samples = set(samples).intersection(type_samples)
    elif samples is None and type_samples is not None:
        samples = type_samples

    #search using sample code/code fragment
    if sample_code is not None and sample_code != '':
        code_samples = []
        if ',' in sample_code:
            codes = [code.strip() for code in sample_code.split(',')]
            for code in codes:
                code_samples.append(Sample.objects.get(sample_code=code))
        else:
            code_samples = Sample.objects.filter(Q(sample_code__startswith=sample_code))

    if samples is not None and code_samples is not None:
        samples = set(samples).intersection(code_samples)
    elif samples is None and code_samples is not None:
        samples = code_samples

    #search using sample age
    if start_age is not None and start_age != '':

        if end_age is None or end_age == '':
            end_age = 0

        age_samples = Sample.objects.filter(calendar_age__lte=start_age, calendar_age__gte=end_age)

    if samples is not None and age_samples is not None:
        samples = set(samples).intersection(age_samples)
    elif samples is None and age_samples is not None:
        samples = age_samples

    # search using keywords
    if keyword is not None and keyword != '':
        keyword_samples = []
        if ',' in keyword:
            words = [word.strip() for word in keyword.split(',')]
            for word in words:
                keyword_samples.extend(Sample.objects.filter(Q(sample_notes__icontains=word)))
        else:
            keyword_samples = Sample.objects.filter(Q(sample_notes__icontains=keyword))

    if samples is not None and keyword_samples is not None:
        samples = set(samples).intersection(keyword_samples)
    elif samples is None and keyword_samples is not None:
        samples = keyword_samples

    # return values for display
    if samples is not None:
        for sample in samples:
            site = ''
            latitude = None
            longitude = None

            if sample.sample_site is not None:
                site = sample.sample_site.site_name
            if sample.sample_coordinates is not None:
                latitude = sample.sample_coordinates.latitude
                longitude = sample.sample_coordinates.longitude
                elevation = sample.sample_coordinates.elevation
            data = {'code': sample.sample_code, 'latitude':latitude, 'longitude':longitude, 'elevation':elevation,
            'site':site, 'notes':sample.sample_notes, 'age':sample.calendar_age,
            'age_error':sample.calendar_error}


            results.append(data)

    results = json.dumps(results)

    return HttpResponse(results, content_type='application/json')


def create_site(request):
    context = RequestContext(request)

    site_name = None

    if request.method == 'GET':
        site_name = request.GET['site_name']
        site_county = request.GET['site_county']
        site_location = request.GET['site_location']
        site_date = request.GET['date']
        site_operator = request.GET['site_operator']
        photographs = request.GET['photographs']
        notes = request.GET['notes']
        type = request.GET['type']
        geomorph = request.GET['geomorph']
        photos_taken = request.GET['photos_taken']
        collected_by = request.GET['collected_by']

        if site_date == '':
            date = None
        else:
            date = datetime.datetime.strptime(site_date, '%d/%m/%Y').date()

        if photos_taken == '1':
            photos_taken = None
        elif photos_taken == '2':
            photos_taken = True
        else:
            photos_taken = False

        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        easting = request.GET['easting']
        northing = request.GET['northing']
        elevation = request.GET['elevation']
        grid = request.GET['grid']
        bng = request.GET['bng']

        site = Sample_Site.objects.get_or_create(site_name=site_name, county=site_county,site_location=site_location,
                                                 site_notes=notes, photographs=photographs, operator=site_operator,
                                                 photos_taken=photos_taken, collected_by=collected_by,
                                                 geomorph_setting=geomorph, sample_type_collected=type,
                                                 site_date=date)

        if site[1] is True:
            if easting == '':
                 easting = None
            if northing == '':
                northing = None
            if latitude == '':
                latitude = None
            if longitude == '':
                longitude = None

            coordinates = Coordinates.objects.create(elevation=elevation, latitude=latitude, longitude=longitude,
                                                 grid_reference=grid, bng_ing=bng, easting=easting, northing=northing,)

            sample_site = site[0]
            sample_site.site_coordinates = coordinates
            sample_site.save()

        reply = json.dumps([{'created':site[1]}])
        return HttpResponse(reply, mimetype='application/json')



def sites(request):
    context = RequestContext(request)

    site_details = None

    if request.method == 'GET':
        site_name = request.GET['site_name']

    site = Sample_Site.objects.get(site_name=site_name)
    coordinates = site.site_coordinates


    date = site.site_date
    if date is not None:
        date = date.strftime("%d/%m/%Y")

    photos_taken = 1
    if site.photos_taken is True:
         photos_taken = 2
    elif site.photos_taken is False:
         photos_taken = 3

    if coordinates is not None:
        site_details = json.dumps([{'name':site.site_name, 'loc':site.site_location, 'county':site.county,
                                    'operator':site.operator, 'type':site.sample_type_collected,
                                    'geomorph':site.geomorph_setting, 'photographs':site.photographs,
                                    'notes':site.site_notes, 'photos_taken':photos_taken, 'bng':coordinates.bng_ing,
                                    'grid':coordinates.grid_reference, 'collected_by':site.collected_by,
                                    'easting':coordinates.easting, 'northing':coordinates.northing,
                                    'latitude':coordinates.latitude, 'longitude':coordinates.longitude,
                                    'elevation':coordinates.elevation, 'date':date}])
    else:
        site_details = json.dumps([{'name':site.site_name, 'loc':site.site_location, 'county':site.county,
                                    'operator':site.operator, 'type':site.sample_type_collected,
                                    'geomorph':site.geomorph_setting, 'photographs':site.photographs,
                                    'notes':site.site_notes, 'photos_taken':photos_taken,
                                    'date':date, 'collected_by':site.collected_by}])

    return HttpResponse(site_details, mimetype='application/json')


def index(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    if 'markers' in request.session:
        del request.session['markers']
        request.session.modified = True

    if request.method == 'POST':
        form = MarkersForm(request.POST)

        if form.is_valid():
            markers = form.cleaned_data['sample_codes']

            request.session['markers'] = markers

            # Redirect to summary of file contents after upload
            return HttpResponseRedirect(reverse('search'))
    else:
        form = MarkersForm()

    return render_to_response('mappingapp/index.html', {'form':form, 'is_member':is_member}, context)


# helper function - remove from views and import!
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


def suggest_code(request):
    context = RequestContext(request)
    code_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

        code_list = get_sample_code_list(starts_with)

    return render_to_response('mappingapp/code_list.html', {'code_list': code_list }, context)



@login_required
@user_passes_test(is_member)
def search(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    samples = None

    if 'markers' in request.session:
        sample_codes = request.session['markers']
        samples = []
        codes = [code.strip() for code in sample_codes.split(',')]

        del request.session['markers']
        request.session.modified = True

        for sample in codes:
            samples.append(Sample.objects.get(sample_code=sample))


    return render_to_response('mappingapp/search.html', {'samples':samples, 'is_member':is_member}, context)


@login_required
@user_passes_test(is_member)
def upload(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    for k in request.session.keys():
        if k != u'_auth_user_backend' and k != u'_auth_user_id':
            del request.session[k]

    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            sample_data = process_file(request.FILES['file'])

            request.session['file_name'] = request.FILES['file'].name

            for k, v in sample_data.iteritems():
                request.session[k] = v

                request.session.modified = True

            # Redirect to summary of file contents after upload
            return HttpResponseRedirect(reverse('filesummary'))

    else:

        form = UploadFileForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('mappingapp/upload.html', {'is_member':is_member, 'form': form}, context)


@login_required
@user_passes_test(is_member)
def edit(request):
    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    samplecodelist = Sample.objects.values_list('sample_code', flat=True).order_by('sample_code')

    if request.method == 'POST':
        sample_code = request.POST['samp_code']

        if sample_code is not None:

            request.session['sample'] = sample_code

            return HttpResponseRedirect(reverse('editsample'))

        else:
            print 'Error'

    else:
       selectsampleform = SelectSampleForm()

    return render_to_response('mappingapp/edit.html', {'sample_codes':samplecodelist, 'is_member':is_member, 'selectsampleform':selectsampleform}, context)


@login_required
@user_passes_test(is_member)
def filesummary(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    file_name = request.session['file_name']
    sample_count = request.session['sample_count']
    request.session['counter'] = 1

    counter = 1

    samples = []

    samples_unique = True
    samples_in_db = []
    exist_in_db = False
    samples_seen = set()

    while counter <= sample_count:
        samples.append(request.session['sample_code'+str(counter)])
        counter += 1

    if len(samples) != 0:
        for sample in samples:
            samples_seen.add(sample)

        if len(samples_seen) != len(samples):
            samples_unique = False

    if len(samples_seen) > 0:
        existing = None
        for sample in samples_seen:
            try:
                existing = Sample.objects.get(sample_code=sample)
            except:
                pass

            if existing is not None:
                samples_in_db.append(existing)
                existing = None

    if len(samples_in_db) > 0:
        exist_in_db = True

    return render_to_response('mappingapp/filesummary.html',
                              {'is_member':is_member, 'file_name':file_name,
                              'samples':samples, 'count':sample_count, 'samples_unique':samples_unique,
                              'exist_in_db':samples_in_db, 'existing':exist_in_db}, context)




@login_required
@user_passes_test(is_member)
def validatesample(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    counter = str(request.session['counter'])

    num_samples = request.session['sample_count']

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
            tcnForm = TCNForm(request.POST, instance=tcn)
            bearingsFormSet = BearingsFormSet(request.POST, request.FILES)

        elif sample_type == 'OSL':
            oslForm = OSLSampleForm(request.POST, instance=osl)
            coreForm = CoreDetailsForm(request.POST, instance=core)

        elif sample_type == 'C14':
            coreForm = CoreDetailsForm(request.POST, instance=core)
            c14Form = RadiocarbonForm(request.POST, instance=radiocarbon)

        # Have we been provided with a complete set of valid forms?  If yes save forms sequentially in order to supply
        # foreign key values where required
        if sampForm.is_valid():

            # and tcnForm.is_valid() and samplecoordForm.is_valid() and\
            # siteForm.is_valid() and     tranForm.is_valid() and retForm.is_valid():

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
                sample_site = None
                try:
                     sample_site = Sample_Site.objects.get(site_name=site_selected)
                except:
                     pass

                sample.transect = transect
                sample.retreat = retreat
                sample.sample_coordinates = sample_coords
                sample.sample_site = sample_site
                sample.save()

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
                            sample_bearing = Sample_Bearing_Inclination.objects.get_or_create(sample_with_bearing=tcn,
                                                                                         bear_inc=bear_inc)

            # Process remaining samples
            if request.session['counter'] < num_samples:
                counter = request.session['counter']
                request.session['counter'] = counter+1
                return HttpResponseRedirect(reverse('validatesample'))

            else:
                # all samples checked, return to home page
                return HttpResponseRedirect(reverse('index'))
        else:
            # The supplied form contained errors - just print them to the terminal.
            print sample.errors
    else:
        sampForm = SampleForm(instance=sample)
        samplecoordForm = CoordinatesForm(prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm()
        sitecoordForm = CoordinatesForm(prefix='site')
        tranForm = TransectForm(instance=transect)
        retForm = RetreatForm(instance=retreat)
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        fillsiteForm = ExistingSitesForm(request.POST, prefix='fill')

        if sample_type == 'TCN':
            tcnForm = TCNForm(instance=tcn)
            bearingsFormSet = BearingsFormSet(initial=data)

        elif sample_type == 'OSL':
            oslForm = OSLSampleForm(instance=osl)
            coreForm = CoreDetailsForm(instance=core)

        elif sample_type == 'C14':
            coreForm = CoreDetailsForm(instance=core)
            c14Form = RadiocarbonForm(instance=radiocarbon)


    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/validatesample.html', {'num_bearings':num_bearings, 'c14form':c14Form,
                                                                 'coreform':coreForm,
                                                                 'tranform': tranForm, 'hiddensiteform':hiddensiteForm,
                                                                 'site_name':site_name, 'sitechoices':sitechoicesForm,
                                                                 'samplecoordform':samplecoordForm,
                                                                 'siteform': siteForm, 'sitecoordform':sitecoordForm,
                                                                 'sampform':sampForm, 'fillsiteform':fillsiteForm,
                                                                 'is_member':is_member,  'retform': retForm,
                                                                 'sample_type':sample_type,
                                                                 'bearingformset':bearingsFormSet,  'tcnform':tcnForm,
                                                                 'oslform':oslForm, 'count':counter,
                                                                 'num_samples':num_samples}, context)

def incrementcounter(request):

    context = RequestContext(request)

    done = True

    if request.method == 'GET':

        counter = request.session['counter'] + 1
        request.session['counter'] = counter
        num_samples = request.session['sample_count']
        if counter <= num_samples:
            done = False

    sample_details = json.dumps([{'done': done}])

    return HttpResponse(sample_details, mimetype='application/json')


def editsample(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # retrieve objects to populate form fields
    sample = None

    num_bearings = None

    sample_code = request.session['sample']
    try:
        sample = Sample.objects.get(sample_code=sample_code)
    except:
        pass

    site_name = None
    transect = None
    retreat_zone = None
    sample_coordinates = None
    osl_data = None
    c14_data = None
    tcn_data = None
    bearings = None
    sample_type = None

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

    if sample is not None:
        if sample.sample_site is not None:
            site_name = sample.sample_site.site_name
        sample_coordinates = sample.sample_coordinates
        transect = sample.transect
        retreat_zone = sample.retreat

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

    if osl_data is not None:
        core = osl_data.osl_core
        sample_type = 'OSL'

    if c14_data is not None:
        core = c14_data.c14_core
        sample_type = 'C14'

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
        if sampleForm.is_valid():
        # if siteForm.is_valid() and sampleForm.is_valid() and tcnForm.is_valid() and samplecoordForm.is_valid() and\
        #         tranForm.is_valid() and retForm.is_valid():


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

            sample.transect = transect
            sample.retreat = retreat
            sample.sample_coordinates = sample_coordinates
            sample.sample_site = sample_site
            sample.save()

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

            elif sample_type == 'C14':
                core = coreForm.save()
                c14 = c14Form.save(commit=False)
                c14.c14_sample = sample
                c14.c14_core = core
                c14.save()

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
            print sample.errors
    else:
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
    return render_to_response('mappingapp/editsample.html', {'num_bearings':num_bearings, 'sitecoordform':sitecoordForm,'siteform': siteForm,
                                                            'samplecoordform':samplecoordForm,'sampform':sampleForm,
                                                            'tranform': tranForm, 'hiddensiteform':hiddensiteForm,
                                                            'sitechoices':sitechoicesForm, 'retform': retForm,
                                                            'fillsiteform':fillsiteForm,'is_member':is_member,
                                                            'bearingformset':bearingsFormSet, 'tcnform':tcnForm,
                                                            'site_name':site_name, 'oslform':oslForm,
                                                            'c14form':c14Form, 'coreform':coreForm,
                                                            'sample_type':sample_type}, context)



def userlogin(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/mappingapp/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your BRITICE CHRONO account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('mappingapp/index.html', {}, context_instance=RequestContext(request))


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/mappingapp/')


