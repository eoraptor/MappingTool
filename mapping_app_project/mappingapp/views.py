from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, modelformset_factory
import json
import datetime, time

from mappingapp.forms import UploadFileForm, CoreDetailsForm, PhotographForm, CoordinatesForm, EditCoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm, HiddenSiteForm, EditSampleSiteForm
from mappingapp.forms import SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form, EditTCNForm
from mappingapp.forms import Location_PhotoForm, PhotoOfForm, SelectSampleForm, ExistingSitesForm, EditSampleForm,\
    EditBIForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination, OSL_Sample, Core_Details, Radiocarbon_Sample
from mappingapp.extract import process_file



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
                samples_with_coordinates.append(sample)

        if len(samples_with_coordinates) != 0:
            sample_details = json.dumps([{'latitude': sample.sample_coordinates.latitude,
                                        'longitude': sample.sample_coordinates.longitude,
                                        'code': sample.sample_code} for sample in samples_with_coordinates])

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

    return render_to_response('mappingapp/index.html', {'is_member':is_member}, context)


@login_required
def search(request):

    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/search.html', context_dict, context)


def results(request):
   context = RequestContext(request)

   context_dict = {}

   return render_to_response('mappingapp/results.html', context_dict, context)


@login_required
@user_passes_test(is_member)
def upload(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            sample_data = process_file(request.FILES['file'])

            for k, v in sample_data.iteritems():
                request.session[k] = v

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('validatesample'))

    else:
        form = UploadFileForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('mappingapp/upload.html', {'is_member':is_member, 'form': form}, context)


@login_required
@user_passes_test(is_member)
def edit(request):
    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    if request.method == 'POST':
        sample_code = request.POST['sample_code']

        if sample_code is not None:

            request.session['sample'] = sample_code

            return HttpResponseRedirect(reverse('editsample'))

        else:
            print 'Error'

    else:
       selectsampleform = SelectSampleForm()

    return render_to_response('mappingapp/edit.html', {'is_member':is_member, 'selectsampleform':selectsampleform}, context)



@login_required
@user_passes_test(is_member)
def validatesample(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # retrieve objects to populate form fields
    sample = None

    request.session['counter'] = 1

    site_name = request.session['site_name']

    counter = str(request.session['counter'])

    latitude = request.session['sample_latitude'+counter]
    longitude = request.session['sample_longitude'+counter]

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

    radiocarbon = Radiocarbon_Sample(depth_below_SL=request.session['depth'+counter],
                             material=request.session['material'+counter],
                             geological_setting=request.session['setting'+counter],
                             stratigraphic_position_depth=request.session['position'+counter],
                             sample_weight=request.session['weight'+counter],
                             pot_contamination=request.session['contamination'+counter])

    y = radiocarbon.depth_below_SL

        # ,
        #                      material='xxx',
        #                      geological_setting='xxx',
        #                      stratigraphic_position_depth='xxx',
        #                      sample_weight='xxx',
        #                      pot_contamination='xxx')



    # osl = OSL_Sample(stratigraphic_position=request.session['position'+counter],
    #                  lithofacies=request.session['lithofacies'+counter],
    #                  burial_depth=request.session['burial_depth'+counter],
    #                  lithology=request.session['lithology'+counter],
    #                  gamma_spec=request.session['gamma_spec'+counter],
    #                  equipment_number=request.session['equipment_number'+counter],
    #                  probe_serial_no=request.session['probe_number'+counter],
    #                  filename=request.session['filename'+counter],
    #                  sample_time=request.session['sample_time'+counter],
    #                  sample_duration=request.session['sample_duration'+counter],
    #                  potassium=request.session['potassium'+counter],
    #                  thorium=request.session['thorium'+counter],
    #                  uranium=request.session['uranium'+counter])

    core = Core_Details(exposure_core=request.session['exposure_core'+counter],
                        core_number=request.session['core_number'+counter])

    # tcn = TCN_Sample(quartz_content=request.session['quartz_content'+counter],
    #                  sample_setting=request.session['sample_setting'+counter],
    #                  sampled_material=request.session['sampled_material'+counter],
    #                  boulder_dimensions=request.session['boulder_dimensions'+counter],
    #                  sample_surface_strike_dip=request.session['sample_surface_strike_dip'+counter],
    #                  sample_thickness=request.session['sample_thickness'+counter],
    #                  grain_size=request.session['grain_size'+counter],
    #                  lithology=request.session['lithology'+counter])

    # transect = Transect(transect_number=request.session['transect'+counter])

    retreat = None

    # bearings = None
    #
    # if 'bearings'+counter in request.session:
    #     bearings = request.session['bearings'+counter]
    #
    # data = []
    # if bearings is not None:
    #     for item in bearings:
    #         dict = {}
    #         dict['bearing'] = item[0]
    #         dict['inclination'] = item[1]
    #         data.append(dict)
    #
    # BearingsFormSet = formset_factory(BearingInclinationForm, extra=5)

    # A HTTP POST?
    if request.method == 'POST':

        sampForm = SampleForm(request.POST, instance=sample)
        samplecoordForm = CoordinatesForm(request.POST, prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm(request.POST)
        sitecoordForm = CoordinatesForm(request.POST, prefix='site')
        # tranForm = TransectForm(request.POST, instance=transect)
        retForm = RetreatForm(request.POST, instance=retreat)
        # tcnForm = TCNForm(request.POST, instance=tcn)
        sitechoicesForm = ExistingSitesForm(request.POST, prefix='main')
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')
        # bearingsFormSet = BearingsFormSet(request.POST, request.FILES)

        #oslForm = OSLSampleForm(request.POST, instance=osl)
        coreForm = CoreDetailsForm(request.POST, instance=core)
        c14Form = RadiocarbonForm(request.POST, instance=radiocarbon)

        # Have we been provided with a complete set of valid forms?  If yes save forms sequentially in order to supply
        # foreign key values where required
        if sampForm.is_valid():

            # and tcnForm.is_valid() and samplecoordForm.is_valid() and\
            # siteForm.is_valid() and     tranForm.is_valid() and retForm.is_valid():

            sample_coords = samplecoordForm.save()

            # transect = tranForm.save()
            #
            retreat = retForm.save()

            site_selected = hiddensiteForm.save()
            sample_site = None
            try:
                 sample_site = Sample_Site.objects.get(site_name=site_selected)
            except:
                 pass

            sample = sampForm.save(commit=False)
            #sample.transect = transect
            sample.retreat = retreat
            sample.sample_coordinates = sample_coords
            sample.sample_site = sample_site
            sample.save()

            core = coreForm.save()

            # osl = oslForm.save(commit=False)
            # osl.osl_sample = sample
            # osl.osl_core = core
            # osl.save()
            # tcn = tcnForm.save(commit=False)
            # tcn.tcn_sample = sample
            # tcn.save()
            #
            # for form in bearingsFormSet.forms:
            #     bear_inc = form.save()
            #     if bear_inc is not None:
            #         sample_bearing = Sample_Bearing_Inclination.objects.get_or_create(sample_with_bearing=tcn,
             #                                                                     bear_inc=bear_inc)
            # The user will be returned to the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print sample.errors
    else:
        sampForm = SampleForm(instance=sample)
        samplecoordForm = CoordinatesForm(prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm()
        sitecoordForm = CoordinatesForm(prefix='site')
        # tranForm = TransectForm(instance=transect)
        retForm = RetreatForm(instance=retreat)
        # tcnForm = TCNForm(instance=tcn)
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        # bearingsFormSet = BearingsFormSet(initial=data)
        fillsiteForm = ExistingSitesForm(request.POST, prefix='fill')

        #oslForm = OSLSampleForm(instance=osl)
        coreForm = CoreDetailsForm(instance=core)
        c14Form = RadiocarbonForm(instance=radiocarbon)

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/validatesample.html', {'c14form':c14Form, 'coreform':coreForm,
                                                                 'hiddensiteform':hiddensiteForm, 'site_name':site_name,
                                                                 'sitechoices':sitechoicesForm,                                                                 'samplecoordform':samplecoordForm,
                                                                 'siteform': siteForm, 'sitecoordform':sitecoordForm,
                                                                 'sampform':sampForm, 'fillsiteform':fillsiteForm,
                                                                 'is_member':is_member,  'retform': retForm}, context)

    # 'bearingformset':bearingsFormSet, 'tranform': tranForm, 'tcnform':tcnForm, 'oslform':oslForm,



def editsample(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # retrieve objects to populate form fields
    sample = None

    request.session['counter'] = 1

    sample_code = request.session['sample']
    try:
        sample = Sample.objects.get(sample_code=sample_code)
    except:
        pass

    site_name = None
    tcn_data = None
    transect = None
    retreat_zone = None
    sample_coordinates = None

    if sample is not None:
        if sample.sample_site is not None:
            site_name = sample.sample_site.site_name
        sample_coordinates = sample.sample_coordinates
        transect = sample.transect
        retreat_zone = sample.retreat
        tcn_data = None
        try:
            tcn_data = TCN_Sample.objects.get(tcn_sample=sample)

        except:
            pass

    BearingsFormSet = formset_factory(EditBIForm, extra=5)

    bearings = Sample_Bearing_Inclination.objects.filter(sample_with_bearing=tcn_data)

    data = []
    for item in bearings:
        values = item.bear_inc
        if values is not None:
            data.append({'bearing':values.bearing, 'inclination':values.inclination})

    # A HTTP POST?
    if request.method == 'POST':

        sampleForm = EditSampleForm(request.POST, instance=sample)
        samplecoordForm = EditCoordinatesForm(request.POST, prefix='sample', instance=sample_coordinates)
        siteForm = EditSampleSiteForm(request.POST)
        sitecoordForm = EditCoordinatesForm(request.POST, prefix='site')
        tranForm = TransectForm(request.POST, instance=transect)
        retForm = RetreatForm(request.POST, instance=retreat_zone)
        tcnForm = EditTCNForm(request.POST, instance=tcn_data)
        sitechoicesForm = ExistingSitesForm(request.POST, prefix='main')
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')
        bearingsFormSet = BearingsFormSet(request.POST, request.FILES)

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
                            Sample_Bearing_Inclination.objects.create(sample_with_bearing=tcn_data, bear_inc=bear_inc)

            # The user will be returned to the homepage.
            return index(request)
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
        tcnForm = EditTCNForm(instance=tcn_data)
        sitechoicesForm = ExistingSitesForm(prefix='main')
        hiddensiteForm = HiddenSiteForm(prefix='hidden')
        fillsiteForm = ExistingSitesForm(request.POST, prefix='fill')



        bearingsFormSet = BearingsFormSet(initial=data)


    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/editsample.html', {'sitecoordform':sitecoordForm,'siteform': siteForm,
                                                            'samplecoordform':samplecoordForm,'sampform':sampleForm,
                                                            'tranform': tranForm, 'hiddensiteform':hiddensiteForm,
                                                            'sitechoices':sitechoicesForm, 'retform': retForm,
                                                            'fillsiteform':fillsiteForm,'is_member':is_member,
                                                            'bearingformset':bearingsFormSet, 'tcnform':tcnForm,
                                                            'site_name':site_name}, context)



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


