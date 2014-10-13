from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from mappingapp.is_member import is_member
from mappingapp.forms import PhotographForm, Location_PhotoForm, PhotoOfForm
from mappingapp.models import Photo_Of, Sample, Photograph
from mappingapp.view_manage_photos import manage_photographs


@login_required
@user_passes_test(is_member)
# view for the photo edit selection page
def photo_select(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    photolist = []
    photo_files = Photograph.objects.values_list('photo_filename', flat=True).order_by('photo_filename')
    for photo in photo_files:
        filename = photo[12:]
        photolist.append(filename)

    # Handle edited data
    if request.method == 'POST':
        photo_file = request.POST['photo_selected']

        filename = 'photographs/' + photo_file

        try:
            photograph = Photograph.objects.get(photo_filename=filename)

            # Redirect to summary of file contents after upload
            return HttpResponseRedirect(reverse('manage_photographs', args=(photograph.id,)))

        except:
            return HttpResponseRedirect(reverse('error', args=('photo_error',)))

        # handle exceptions ----> show error page

    else:

        # Render list page with the documents and the form
        return render_to_response('mappingapp/photo_select.html', {'is_member': is_member, 'photos':photolist}, context)




