from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from mappingapp.forms import UploadFileForm
from mappingapp.extractNERC import process_nerc_file
from mappingapp.is_member import is_member


@login_required
@user_passes_test(is_member)
# view for the file selection page
def upload_nerc(request):

    is_member = request.user.groups.filter(name='Consortium Super User')

    sample_data = None

    context = RequestContext(request)

    # empty the session dictionary of all keys except two to keep user logged in and one for files uploaded so far
    for k in request.session.keys():
        if k != u'_auth_user_backend' and k != u'_auth_user_id' and k !=u'files_saved' and k !=u'photos_saved' and\
                        k != u'nerc_files_saved':
            del request.session[k]

    # get files already uploaded in session to display on page
    files = None
    if 'nerc_files_saved' in request.session:
        files = request.session['nerc_files_saved']

    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                sample_data = process_nerc_file(request.FILES['file'])

            # handle exceptions ----> show error page
            except:
                return HttpResponseRedirect(reverse('error', args=('file_error',)))

            request.session['nerc_file_name'] = request.FILES['file'].name

            if sample_data is None:
                return HttpResponseRedirect(reverse('error', args=('file_error',)))

            else:
                # extraction ok - add data to session dictionary
                for k, v in sample_data.iteritems():
                    request.session[k] = v
                    request.session.modified = True

                # Redirect to summary of file contents after upload
                return HttpResponseRedirect(reverse('nerc_file_summary'))

    else:

        form = UploadFileForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response('mappingapp/uploadnerc.html', {'files':files, 'is_member':is_member, 'form': form},
                              context)

