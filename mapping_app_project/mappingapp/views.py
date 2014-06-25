from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from mappingapp.forms import DocumentForm, CoreDetailsForm, PhotographForm, SiteCoordinatesForm, SampleCoordinatesForm, TransectForm, RetreatForm, SampleForm, RadiocarbonForm,SampleSiteForm, OSLSampleForm, TCNForm, BearingInclinationForm, Sample_BI_Form, Location_PhotoForm, PhotoOfForm
from mappingapp.models import Document, Transect, Coordinates

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
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('/mappingapp/upload')

    else:
        form = DocumentForm() # A empty, unbound form

        # Load documents for the list page
        documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response('mappingapp/upload.html', {'documents': documents, 'form': form}, context)



@login_required
def edit(request):
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        tranForm = TransectForm(request.POST)
        retForm = RetreatForm(request.POST)
        samplecoordForm = SampleCoordinatesForm(request.POST, prefix='sample')
        sitecoordForm = SampleCoordinatesForm(request.POST, prefix='site')
        siteForm = SampleSiteForm(request.POST)
        sampForm = SampleForm(request.POST)
        tcnForm = TCNForm(request.POST)
        bearincForm = BearingInclinationForm(request.POST)
        sampleBIForm = Sample_BI_Form(request.POST)


        # Have we been provided with a complete set of valid forms?
        if tranForm.is_valid() and retForm.is_valid()and sitecoordForm.is_valid() and siteForm.is_valid()\
            and samplecoordForm.is_valid() and sampForm.is_valid()\
            and bearincForm.is_valid() and sampleBIForm.is_valid()\
            and tcnForm.is_valid():

            transect = tranForm.save()
            retForm.save()
            sitecoords = sitecoordForm.save()
            sampcoords = samplecoordForm.save()
            bearinc = bearincForm.save()

            site = siteForm.save(commit=False)
            site.site_transect = transect
            site.site_coordinates = sitecoords
            site.save()

            samp = sampForm.save(commit=False)
            samp.sample_coordinates = sampcoords
            samp.samp_site = site
            samp.save()

            tcnsample = tcnForm.save(commit=False)
            tcnsample.tcn_sample = samp
            tcnsample.save()

            sampleBI = sampleBIForm.save(commit=False)
            sampleBI.sample_with_bearing = tcnsample
            sampleBI.bear_inc = bearinc
            sampleBI.save()

            tcnsample.sample_bearings = sampleBI
            tcnsample.save()

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print 'Error'
    else:
        tranForm = TransectForm()
        retForm = RetreatForm()
        samplecoordForm = SampleCoordinatesForm(prefix='sample')
        sitecoordForm = SiteCoordinatesForm(prefix='site')
        sampForm = SampleForm()
        siteForm = SampleSiteForm()
        tcnForm = TCNForm()
        bearincForm = BearingInclinationForm()
        sampleBIForm = Sample_BI_Form()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/edit.html', {'tcnform':tcnForm, 'bearincform':bearincForm, 'sampleBIform':sampleBIForm, 'sampform':sampForm, 'samplecoordform':samplecoordForm, 'sitecoordform':sitecoordForm, 'siteform': siteForm, 'tranform': tranForm, 'retform': retForm}, context)




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
