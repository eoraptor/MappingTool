from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from mappingapp.is_member import is_member


@login_required
@user_passes_test(is_member)
# File upload & sample edit code selection failure page
def error(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    return render_to_response('mappingapp/error.html', {'is_member':is_member}, context)

