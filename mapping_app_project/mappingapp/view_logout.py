from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# log user out in response to logout button press
@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/briticechrono/')



