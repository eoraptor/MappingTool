from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

# view for the About page
def about(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    return render_to_response('mappingapp/about.html', {'is_member': is_member}, context)

