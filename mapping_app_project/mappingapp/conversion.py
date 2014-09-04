from mappingapp.models import Transect, Sample_Site

# functions for converting date and lat/long fields if incorrect and to get
# transect number from site location

# take date format with full stops and replace
def convert_date(date):

    first_point = date.find('.')
    last_point = date.rfind('.')

    day = date[:first_point].strip(' ')
    month = date[first_point+1:last_point].strip(' ')
    year = date[last_point+1:].strip(' ')

    if isinstance(day, int) and isinstance(month, int) and isinstance(year, int):

        if len(day) == 1:
            day = '0' + day

        if len(month) == 1:
            month = '0' + month

        if len(year) == 2:
            year = '20' + year

        return day + '/' + month + '/' + year

    else:
        return 'Error'



# convert lat/long in degrees, minutes to decimal format
def convert_lat_long(coord):
    try:
        result = "".join(i for i in coord if ord(i)<128)

        degrees = float(result[:result.index(' ')])
        minutes = float(result[result.rindex(' ')+1:])/60
        value = degrees + minutes
    except:
        value = 'Error'

    return value


# get transect number from site location if not on sample form
def get_transect(site_name):
    transect = None
    site = None

    try:
        site = Sample_Site.objects.get(site_name=site_name)
    except:
        pass

    if site is not None:
        location = site.site_location

        if location is not None:

            if 'T1' in location:
                transect = Transect.objects.get_or_create(transect_number='T1')[0]
            elif 'T2' in location:
                transect = Transect.objects.get_or_create(transect_number='T2')[0]
            elif 'T3' in location:
                transect = Transect.objects.get_or_create(transect_number='T3')[0]
            elif 'T4' in location:
                transect = Transect.objects.get_or_create(transect_number='T4')[0]
            elif 'T5' in location:
                transect = Transect.objects.get_or_create(transect_number='T5')[0]
            elif 'T6' in location:
                transect = Transect.objects.get_or_create(transect_number='T6')[0]
            elif 'T7' in location:
                transect = Transect.objects.get_or_create(transect_number='T7')[0]
            elif 'T8' in location:
                transect = Transect.objects.get_or_create(transect_number='T8')[0]

    return transect


# create list of missing keys
def missing_keys(positions):
    missing_keys = []
    for key, value in positions.iteritems():
        if value == '':
            missing_keys.append(key)
    return missing_keys