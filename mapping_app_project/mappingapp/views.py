from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from mappingapp.forms import UploadFileForm, CoreDetailsForm, PhotographForm, CoordinatesForm
from mappingapp.forms import TransectForm, RetreatForm, SampleForm, RadiocarbonForm
from mappingapp.forms import SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form
from mappingapp.forms import Location_PhotoForm, PhotoOfForm, SelectSampleForm
from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination
from mappingapp.extract import process_file


def index(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/index.html', context_dict, context)


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

            samples = process_file(request.FILES['file'])

            request.session['samples'] = samples
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

    if request.session['source'] == 'code':
        sample_code = request.session['sample']
        sample = Sample.objects.get(sample_code=sample_code)

    elif request.session['source'] == 'file':
        sample_codes = request.session['samples']
        sample = Sample.objects.get(sample_code=sample_codes[0])

    site = sample.samp_site
    #tcn = TCN_Sample.objects.get(tcn_sample=sample.pk)


    # A HTTP POST?
    if request.method == 'POST':

        sampForm = SampleForm(request.POST, instance=sample)
        #samplecoordForm = CoordinatesForm(request.POST, prefix='sample', instance=sample.sample_coords)
        siteForm = SampleSiteForm(request.POST, instance=site)
        #sitecoordForm = CoordinatesForm(request.POST, prefix='site', instance=Coordinates.objects.get(pk=site.site_coordinates))
        #tranForm = TransectForm(request.POST, instance=Transect.objects.getsample.samp_site.site_transect)
        #retForm = RetreatForm(request.POST, instance=sample.samp_site.site_retreat)
        #tcnForm = TCNForm(request.POST, instance=tcn)

        #bearincForm = BearingInclinationForm(request.POST)
        #sampleBIForm = Sample_BI_Form(request.POST)

        # Have we been provided with a complete set of valid forms?
        # if yes save forms sequentially in order to supply foreign key values
        # where required
        if sampForm.is_valid():
            # and tcnForm.is_valid() and tranForm.is_valid() and retForm.is_valid() and\
            # samplecoordForm.is_valid() and sitecoordForm.is_valid() and siteForm.is_valid() and\
            # bearincForm.is_valid():


            #samplecoordForm.save()

            # transect = tranForm.save()
            #
            # retreat = retForm.save()

            #site_coords = None
            #sitecoordForm.save()



            # bearinc = bearincForm.save()
            #
            # site = siteForm.save()

            # fix sample type!!!!!!
            #if site is None and (retreat is not None or transect is not None or site_coords is not None):
            #    site = Sample_Site.objects.create_site(None, None, None, None, None, None, None, None, None, None,
            #                                            transect, retreat, sampcoords)
                #site.save()

            #samp = None
            #if sampForm.is_valid():
            samp = sampForm.save(commit=False)
                # samp.sample_coordinates = sampcoords
                # samp.samp_site = site
            samp.save()

            # tcnsample = None
            # if tcnForm.is_valid():
            #     tcnsample = tcnForm.save()
            #
            #     if tcnsample is not None:
            #         tcnsample.tcn_sample = samp
            #         tcnsample.save()
            #
            # if tcnsample is None and samp is not None:
            #     tcnsample = TCN_Sample.objects.create_tcn(None, None, None, None, None, None, None, None, samp)
            #     tcnsample.save()
            #
            # sampleBI = sampleBIForm.save(commit=False)
            # sampleBI.sample_with_bearing = tcnsample
            # sampleBI.bear_inc = bearinc
            # sampleBI.save()
            #
            # tcnsample.sample_bearings = sampleBI
            # tcnsample.save()


            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print sample.errors
    else:
        sampForm = SampleForm(instance=sample)
        #samplecoordForm = CoordinatesForm(prefix='sample', instance=Coordinates.objects.get(pk=sample.sample_coords))
        siteForm = SampleSiteForm(instance=site)
        #sitecoordForm = CoordinatesForm(prefix='site', instance=Coordinates.objects.get(pk=site.site_coordinates))
        #tranForm = TransectForm(instance=Transect.objects.get(pk=site.site_transect))
        #retForm = RetreatForm(instance=Retreat_Zone.objects.get(pk=site.site_retreat))
        #tcnForm = TCNForm(instance=tcn)

        #bearincForm = BearingInclinationForm()
        #sampleBIForm = Sample_BI_Form()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/edittcn.html', {'sampform':sampForm}, context)
    #, 'bearincform':bearincForm, 'sampleBIform':sampleBIForm, 'tcnform':tcnForm, 'samplecoordform':samplecoordForm, 'sitecoordform':sitecoordForm, 'siteform': siteForm, 'tranform': tranForm, 'retform': retForm




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
