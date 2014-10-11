from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from mappingapp.is_member import is_member
from mappingapp.forms import PhotographForm, Location_PhotoForm, PhotoOfForm
from mappingapp.models import Photo_Of, Sample, Photograph


@login_required
@user_passes_test(is_member)
# view for the file selection page
def manage_photographs(request, photo_id):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    photograph = None
    photo_file = None

    try:
        photograph = Photograph.objects.get(pk=photo_id)

    except:
        pass

    if photograph is not None:
        photo_file = photograph.photo_filename.name[12:]


    # Handle edited data
    if request.method == 'POST':
        photo_form = PhotographForm(data=request.POST)
        site_form = Location_PhotoForm(data=request.POST)
        sample_form = PhotoOfForm(data=request.POST)

        if photo_form.is_valid() and sample_form.is_valid():

            photo = photo_form.save(commit=False)
            site_photo = site_form.save(commit=False)

            sample_list = sample_form.cleaned_data.get('sample_pictured')

            photo.save()
            site_photo.photo_ident = photo
            site_photo.save()

            try:
                for sample in sample_list:
                    samp = Photo_Of.objects.get_or_create(sample_pictured=Sample.objects.get(pk=sample),
                                                          photo_idno=photo)

            # handle exceptions ----> show error page
            except:
                return HttpResponseRedirect(reverse('error'))

            # Redirect to summary of file contents after upload
            # return HttpResponseRedirect(reverse('upload_photograph'))

    else:

        photo_form = PhotographForm(instance=photograph)
        site_form = Location_PhotoForm()
        sample_form = PhotoOfForm()


    # Render list page with the documents and the form
    return render_to_response('mappingapp/manage_photos.html', {'is_member': is_member, 'photo_form': photo_form,
                                                                    'site_form': site_form, 'sample_form': sample_form,
                                                                    'photo':photograph, 'file':photo_file}, context)



