from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test

from mappingapp.is_member import is_member
from mappingapp.models import Sample


# view for File Summary page
@login_required
@user_passes_test(is_member)
def nercfilesummary(request):

    context = RequestContext(request)

    is_member = request.user.groups.filter(name='Consortium Super User')

    # retrieve file data from session dictionary
    file_name = request.session['nerc_file_name']
    sample_count = request.session['sample_count']

    # set counter in session to 1 - used to ensure all samples in file checked
    request.session['counter'] = 1

    counter = 1

    samples = []
    samples_unique = True
    samples_in_db = []
    exist_in_db = False
    samples_seen = set()
    errors = []
    missing_key_list = []

    # perform checks on each sample in file
    while counter <= sample_count:
        # add sample code to list of sample codes
        sample = request.session['sample_code'+str(counter)]
        samples.append(sample)

        # add sample errors with their sample code to list of errors
        sample_errors = request.session['errors'+str(counter)]
        if len(sample_errors) != 0:
            for error in sample_errors:
                errors.append((sample, error))

        # add missing keys and their sample code to list of errors
        missing_keys = request.session['missing_keys'+str(counter)]

        if len(missing_keys) != 0:
            for key in missing_keys:
                missing_key_list.append((sample, key))

        counter += 1

    # check sample code list for duplicates
    if len(samples) != 0:
        for sample in samples:
            samples_seen.add(sample)

        if len(samples_seen) != len(samples):
            samples_unique = False

    # check samples codes against those in database
    if len(samples_seen) > 0:
        existing = None
        for sample in samples_seen:
            try:
                existing = Sample.objects.get(sample_code=sample)
            except:
                pass

            if existing is not None:
                samples_in_db.append(existing)
                existing = None

    if len(samples_in_db) > 0:
        exist_in_db = True

    return render_to_response('mappingapp/nercfilesummary.html',
                              {'is_member': is_member, 'file_name': file_name, 'errors': errors,
                              'samples': samples, 'count': sample_count, 'samples_unique': samples_unique,
                              'exist_in_db': samples_in_db, 'existing': exist_in_db,
                              'missing_keys': missing_key_list}, context)


