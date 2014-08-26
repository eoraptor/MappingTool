from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response


# login view to process login from the navbar
def userlogin(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If User object, the details are correct.
        if user:
            # Is the account active?
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/briticechrono/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your BRITICE CHRONO account is disabled.")
        else:
            # Bad login details were provided.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:

        return render_to_response('mappingapp/index.html', {}, context_instance=RequestContext(request))

