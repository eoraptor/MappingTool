from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from mappingapp.is_member import is_member
from mappingapp.forms import PhotographForm, Location_PhotoForm, PhotoOfForm
from mappingapp.models import Photo_Of, Sample


@login_required
@user_passes_test(is_member)
# view for the file selection page
def upload_photograph(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    photos_saved = None
    if 'photos_saved' in request.session:
        photos_saved = request.session['photos_saved']

    # Handle file upload
    if request.method == 'POST':
        photo_form = PhotographForm(data=request.POST)
        site_form = Location_PhotoForm(request.POST)
        sample_form = PhotoOfForm(data=request.POST)


        if photo_form.is_valid() and sample_form.is_valid() and site_form.is_valid():

            photo = photo_form.save(commit=False)


            site = None
            site = site_form.cleaned_data.get('photo_site')

            sample_list = None
            sample_list = sample_form.cleaned_data.get('sample_pictured')

            if 'photo_filename' in request.FILES:
                photo.photo_filename = request.FILES['photo_filename']
            photo.save()

            if site is not None:
                site_photo = site_form.save(commit=False)
                site_photo.photo_ident = photo
                site_photo.save()

            # add file to files saved list in session dictionary
            photo_file = request.FILES['photo_filename'].name.replace('photographs/', '')

            if 'photos_saved' in request.session:
                if photo_file not in request.session['photos_saved']:
                    request.session['photos_saved'] = request.session['photos_saved'] + ', ' + photo_file
            else:
                request.session['photos_saved'] = photo_file

            if sample_list is not None:
                try:
                    for sample in sample_list:
                        samp = Photo_Of.objects.create(sample_pictured=Sample.objects.get(pk=sample), photo_idno=photo)
                        samp.save()

                # handle exceptions ----> show error page
                except:

                     return HttpResponseRedirect(reverse('error'))


            # Redirect to summary of file contents after upload
            return HttpResponseRedirect(reverse('upload_photograph'))

    else:

        photo_form = PhotographForm() # A empty, unbound form
        site_form = Location_PhotoForm()
        sample_form = PhotoOfForm()


    # Render list page with the documents and the form
    return render_to_response('mappingapp/upload_photograph.html', {'is_member': is_member, 'photo_form': photo_form,
                                                                    'site_form': site_form, 'sample_form': sample_form,
                                                                    'photos_saved':photos_saved}, context)


