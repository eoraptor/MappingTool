from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import json
import pickle
from django.core import serializers


from mappingapp.forms import UploadFileForm, CoreDetailsForm, PhotographForm, CoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm, HiddenSiteForm
from mappingapp.forms import SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form
from mappingapp.forms import Location_PhotoForm, PhotoOfForm, SelectSampleForm, ExistingSitesForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination
from mappingapp.extract import process_file


def markers(request):
    context = RequestContext(request)

    sample_details = None

    if request.method == 'GET':
        samples = Sample.objects.all()
        if samples is not None:

            sample_details = json.dumps( [{'latitude': sample.sample_coordinates.latitude,
                                       'longitude': sample.sample_coordinates.longitude,
                                       'code': sample.sample_code} for sample in samples])

    return HttpResponse(sample_details, mimetype='application/json')


def create_site(request):
    context = RequestContext(request)

    site_name = None

    if request.method == 'GET':
        site_name = request.GET['site_name']
        site_county = request.GET['site_county']
        site_location = request.GET['site_location']
        # site_date = request.GET['date']
        site_operator = request.GET['site_operator']
        photographs = request.GET['photographs']
        notes = request.GET['notes']
        type = request.GET['type']
        geomorph = request.GET['geomorph']
        photos_taken = request.GET['photos_taken']

        latitude = request.GET['latitude']
        longitude = request.GET['longitude']
        easting = request.GET['easting']
        northing = request.GET['northing']
        elevation = request.GET['elevation']
        grid = request.GET['grid']
        bng = request.GET['bng']



        site = Sample_Site.objects.get_or_create(site_name=site_name, county=site_county,
                                                    site_location=site_location, photographs=photographs,
                                                    operator=site_operator, geomorph_setting=geomorph,
                                                    photos_taken=photos_taken, sample_type_collected=type,
                                                    site_notes=notes)
                                            # , site_date=site_date

        #if site[1] is True:
        if easting == '':
            easting = None
        if northing == '':
            northing = None


        coordinates = Coordinates.objects.create(latitude=latitude, longitude=longitude, easting=easting,
                                                 elevation=elevation, northing=northing, bng_ing=bng,
                                                 grid_reference=grid)

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

    # date = site.site_date.strftime('%d/%m/%Y')
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
                                    'grid':coordinates.grid_reference, 'easting':coordinates.easting,
                                    'northing':coordinates.northing, 'latitude':coordinates.latitude,
                                    'longitude':coordinates.longitude,'elevation':coordinates.elevation}])
    else:
        site_details = json.dumps([{'name':site.site_name, 'loc':site.site_location, 'county':site.county,
                                    'operator':site.operator, 'type':site.sample_type_collected,
                                    'geomorph':site.geomorph_setting, 'photographs':site.photographs,
                                    'notes':site.site_notes, 'photos_taken':photos_taken}])

                                # 'date':date,

    return HttpResponse(site_details, mimetype='application/json')


def index(request):

    context = RequestContext(request)

    return render_to_response('mappingapp/index.html', {}, context)


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
def upload(request):

    context = RequestContext(request)

    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            sample_data = process_file(request.FILES['file'])
            for k, v in sample_data.iteritems():
                request.session[k] = v

            request.session['source'] = 'file'

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('edittcn'))

    else:
        form = UploadFileForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('mappingapp/upload.html', {'form': form}, context)


@login_required
def edit(request):
    context = RequestContext(request)

    if request.method == 'POST':
        sample_code = request.POST['sample_code']

        if sample_code is not None:

            request.session['sample'] = sample_code
            request.session['source'] = 'code'
            return HttpResponseRedirect(reverse('edittcn'))

        else:
            print 'Error'

    else:
       selectsampleform = SelectSampleForm()

    return render_to_response('mappingapp/edit.html', {'selectsampleform':selectsampleform}, context)



@login_required
def edittcn(request):

    context = RequestContext(request)

    # retrieve objects to populate form fields
    sample = None

    request.session['counter'] = 1

    if request.session['source'] == 'code':
        sample_code = request.session['sample']
        sample = Sample.objects.get(sample_code=sample_code)

    elif request.session['source'] == 'file':

        site_name = request.session['site_name']

        counter = str(request.session['counter'])
        sample_coords = Coordinates(bng_ing=request.session['sample_bng_ing'+counter],
                                    grid_reference=request.session['sample_grid_reference'+counter],
                                    easting=request.session['sample_easting'+counter],
                                    northing=request.session['sample_northing'+counter],
                                    latitude=request.session['sample_latitude'+counter],
                                    longitude=request.session['sample_longitude'+counter],
                                    elevation=request.session['sample_elevation'+counter])

        sample = Sample(sample_code=request.session['sample_code'+counter],
                        sample_location_name=request.session['sample_location_name'+counter],
                        collection_date=request.session['sample_date'+counter],
                        collector=request.session['collector'+counter],
                        sample_notes=request.session['sample_notes'+counter],
                        dating_priority=None, age=None, age_error=None, calendar_age=None, calendar_error=None,
                        lab_code=None, sample_coordinates=None, sample_site=None, transect=None, retreat=None)

        tcn = TCN_Sample(quartz_content=request.session['quartz_content'+counter],
                         sample_setting=request.session['sample_setting'+counter],
                         sampled_material=request.session['sampled_material'+counter],
                         boulder_dimensions=request.session['boulder_dimensions'+counter],
                         sample_surface_strike_dip=request.session['sample_surface_strike_dip'+counter],
                         sample_thickness=request.session['sample_thickness'+counter],
                         grain_size=request.session['grain_size'+counter],
                         lithology=request.session['lithology'+counter], tcn_sample=None)

        transect = Transect(transect_number=request.session['transect'+counter])

        retreat = None

    # A HTTP POST?
    if request.method == 'POST':

        sampForm = SampleForm(request.POST, instance=sample)
        samplecoordForm = CoordinatesForm(request.POST, prefix='sample', instance=sample_coords)
        siteForm = SampleSiteForm(request.POST)
        sitecoordForm = CoordinatesForm(request.POST, prefix='site')
        tranForm = TransectForm(request.POST, instance=transect)
        retForm = RetreatForm(request.POST, instance=retreat)
        tcnForm = TCNForm(request.POST, instance=tcn)
        sitechoicesForm = ExistingSitesForm(request.POST)
        hiddensiteForm = HiddenSiteForm(request.POST, prefix='hidden')

        #
        # bearincForm = BearingInclinationForm(request.POST)
        # sampleBIForm = Sample_BI_Form(request.POST)

        # Have we been provided with a complete set of valid forms?  If yes save forms sequentially in order to supply
        # foreign key values where required
        if siteForm.is_valid():

        # if sampForm.is_valid() and tcnForm.is_valid() and tranForm.is_valid() and retForm.is_valid() and\
        #     samplecoordForm.is_valid() and sitecoordForm.is_valid() and siteForm.is_valid() and\
        #     bearincForm.is_valid():

            sample_coords = samplecoordForm.save()

            transect = tranForm.save()

            retreat = retForm.save()

            site_selected = hiddensiteForm.save()

            sample = sampForm.save(commit=False)
            sample.transect = transect
            sample.retreat = retreat
            sample.sample_coordinates = sample_coords
            sample.sample_site = site_selected
            sample.save()

            # tcnForm.save()

            # sampleBI = sampleBIForm.save(commit=False)
            # sampleBI.sample_with_bearing = tcnsample
            # sampleBI.bear_inc = bearinc
            # sampleBI.save()
            #
            # tcnsample.sample_bearings = sampleBI
            # tcnsample.save()
            # bearincForm.save()



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
        tranForm = TransectForm(instance=transect)
        retForm = RetreatForm(instance=retreat)
        tcnForm = TCNForm(instance=tcn)
        sitechoicesForm = ExistingSitesForm()
        hiddensiteForm = HiddenSiteForm(prefix='hidden')


        # bearincForm = BearingInclinationForm()
        # sampleBIForm = Sample_BI_Form()


    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/edittcn.html', {'hiddensiteform':hiddensiteForm, 'site_name':site_name, 'sitechoices':sitechoicesForm,
                                                          'retform': retForm,'tranform': tranForm, 'tcnform':tcnForm,
                                                          'samplecoordform':samplecoordForm, 'siteform': siteForm,
                                                          'sitecoordform':sitecoordForm, 'sampform':sampForm}, context)


                              #  , 'bearincform':bearincForm,
                              #  'sampleBIform':sampleBIForm, }


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
