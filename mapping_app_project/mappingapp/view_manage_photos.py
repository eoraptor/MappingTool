from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from mappingapp.is_member import is_member
from mappingapp.forms import PhotographForm, Location_PhotoForm, PhotoOfForm
from mappingapp.models import Photo_Of, Sample, Photograph, Location_Photo, Sample_Site


@login_required
@user_passes_test(is_member)
# view for the file selection page
def manage_photographs(request, photo_id):

    is_member = request.user.groups.filter(name='Consortium Super User')

    context = RequestContext(request)

    photograph = None
    photo_file = None
    photo_site = None
    photo_samples = None

    try:
        photograph = Photograph.objects.get(pk=photo_id)

    except:
        pass

    if photograph is not None:
        photo_file = photograph.photo_filename.name[12:]

        try:
            photo_samples = Photo_Of.objects.filter(photo_idno=photograph)

        except:
            pass

        try:
            photo_site = Location_Photo.objects.filter(photo_ident=photograph)
        except:
            pass


    # Handle edited data
    if request.method == 'POST':
        photo_form = PhotographForm(data=request.POST, instance=photograph)
        site_form = Location_PhotoForm(data=request.POST)
        sample_form = PhotoOfForm(data=request.POST)

        if photo_form.is_valid() and sample_form.is_valid() and site_form.is_valid():

            photo = photo_form.save()
            site = site_form.cleaned_data.get('photo_site')
            sample_list = sample_form.cleaned_data.get('sample_pictured')

            if site is not None:
                site_photo = site_form.save(commit=False)
                site_photo.photo_ident = photo
                site_photo.save()

            sample_to_remove = request.POST['remove_sample']
            site_to_remove = request.POST['remove_site']


            if sample_to_remove != u'' and sample_to_remove is not None:
                sample = None
                try:
                    sample = Sample.objects.get(sample_code=sample_to_remove)
                    if sample is not None:
                        record = Photo_Of.objects.get(photo_idno=photograph, sample_pictured=sample)
                        record.delete()

                except:
                    return HttpResponseRedirect(reverse('error'))

            if site_to_remove != u'' and site_to_remove is not None:
                site = None
                try:
                    site = Sample_Site.objects.get(site_name=site_to_remove)
                    if site is not None:
                        record = Location_Photo.objects.get(photo_ident=photograph, photo_site=site)
                        record.delete()

                except:
                    return HttpResponseRedirect(reverse('error'))

            if len(sample_list) != 0:
                try:
                    for sample in sample_list:
                        samp = Photo_Of.objects.get_or_create(sample_pictured=Sample.objects.get(pk=sample),
                                                              photo_idno=photo)

                # handle exceptions ----> show error page
                except:
                    return HttpResponseRedirect(reverse('error'))

            # Redirect to summary of file contents after upload
            return HttpResponseRedirect(reverse('manage_photographs', args=(photo_id,)))

    else:

        photo_form = PhotographForm(instance=photograph)
        site_form = Location_PhotoForm()
        sample_form = PhotoOfForm()


    # Render list page with the documents and the form
    return render_to_response('mappingapp/manage_photos.html', {'is_member': is_member, 'photo_form': photo_form,
                                                                'site_form': site_form, 'sample_form': sample_form,
                                                                'photo':photograph, 'file':photo_file,
                                                                'sites':photo_site, 'samples':photo_samples}, context)



