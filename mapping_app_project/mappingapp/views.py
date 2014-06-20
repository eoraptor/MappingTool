from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/index.html', context_dict, context)



def search(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/search.html', context_dict, context)



def results(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/results.html', context_dict, context)


def upload(request):
    context = RequestContext(request)

    context_dict = {}

    return render_to_response('mappingapp/upload.html', context_dict, context)


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


