from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

# view for the Contact page
def contact(request):
    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # get list of users to populate email links
    user_list = User.objects.filter(groups__name='Consortium Super User')
    users = []

    for user in user_list:
        data = {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}
        users.append(data)

    return render_to_response('mappingapp/contact.html', {'is_member': is_member, 'user_data': users}, context)


