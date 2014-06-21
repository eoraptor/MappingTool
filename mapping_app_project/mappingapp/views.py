from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from mappingapp.forms import UploadFileForm

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

    if request.method == 'POST':
        form = UploadFileForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = UploadFileForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('mappingapp/upload.html', {'form': form}, context)


@login_required
def edit(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/edit.html', context_dict, context)


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
