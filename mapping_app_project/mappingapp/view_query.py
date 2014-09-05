from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Q
import json

from mappingapp.models import Document, Transect, Coordinates, Sample, Retreat_Zone, Sample_Site, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination, OSL_Sample, Core_Details, Radiocarbon_Sample


# Ajax search functionality - called from Search page.  Gets data to populate tablesorter table
def query(request):

    context = RequestContext(request)

    # variables
    results = []
    transect = ''
    transect_object = None
    sample_code = None
    start_age = None
    end_age = None
    keyword = None
    type = None
    type_samples = None
    code_samples = None
    age_samples = None
    keyword_samples = None
    samples = None

    # retrieve the search criteria
    if request.method == 'GET':
        transect = request.GET['transect']
        type = request.GET['type']
        sample_code = request.GET['code']
        start_age = request.GET['start']
        end_age = request.GET['end']
        keyword = request.GET['keyword']

    # search for samples belonging to one transect
    if transect != '':
        try:
            transect_object = Transect.objects.get(transect_number=transect)
        except:
            pass

    if transect_object is not None:
        samples = Sample.objects.filter(transect=transect_object)

    # search for samples of one type
    if type != '' and type is not None:
        type_samples = []
        sample_list = None
        if type == 'TCN':
            sample_list = TCN_Sample.objects.values_list('tcn_sample', flat=True)
        elif type == 'OSL':
            sample_list = OSL_Sample.objects.values_list('osl_sample', flat=True)
        elif type == 'C14':
            sample_list = Radiocarbon_Sample.objects.values_list('c14_sample', flat=True)

        if sample_list is not None:
            for pk in sample_list:
                type_samples.append(Sample.objects.get(pk=pk))

    # reduce search results to include only those matching all search criteria at this stage
    if samples is not None and type_samples is not None:
        samples = set(samples).intersection(type_samples)
    elif samples is None and type_samples is not None:
        samples = type_samples

    #search using sample code/code fragment
    if sample_code is not None and sample_code != '':
        code_samples = []
        if ',' in sample_code:
            codes = [code.strip() for code in sample_code.split(',')]
            for code in codes:
                code_samples.append(Sample.objects.get(sample_code=code))
        else:
            code_samples = Sample.objects.filter(Q(sample_code__startswith=sample_code))

    # reduce search results to include only those matching all search criteria at this stage
    if samples is not None and code_samples is not None:
        samples = set(samples).intersection(code_samples)
    elif samples is None and code_samples is not None:
        samples = code_samples

    #search using sample age: check integers, reverse values if wrong way round
    if start_age is not None and start_age != '' and end_age is not None and end_age != '':
        try:
            start_age = int(start_age)
            end_age = int(end_age)
        except:
            pass

        if isinstance(start_age, int) and isinstance(end_age, int):
            if start_age > end_age:
                start = end_age
                end_age = start_age
                start_age = start

            age_samples = Sample.objects.filter(calendar_age__gte=start_age, calendar_age__lte=end_age)

    # reduce search results to include only those matching all search criteria at this stage
    if samples is not None and age_samples is not None:
        samples = set(samples).intersection(age_samples)
    elif samples is None and age_samples is not None:
        samples = age_samples

    # search using keywords
    if keyword is not None and keyword != '':
        keyword_samples = []
        if ',' in keyword:
            words = [word.strip() for word in keyword.split(',')]
            for word in words:
                keyword_samples.extend(Sample.objects.filter(Q(sample_notes__icontains=word)))
        else:
            keyword_samples = Sample.objects.filter(Q(sample_notes__icontains=keyword))

    # reduce search results to include only those matching all search criteria at this stage
    if samples is not None and keyword_samples is not None:
        samples = set(samples).intersection(keyword_samples)
    elif samples is None and keyword_samples is not None:
        samples = keyword_samples

    # return values for display
    if samples is not None:
        for sample in samples:
            site = ''
            latitude = None
            longitude = None
            elevation = None
            type = None
            type_found = None
            transect = None
            retreat = None

            # get sample type
            try:
                type_found = TCN_Sample.objects.get(tcn_sample=sample.pk)
            except:
                pass
            if type_found is not None:
                type = 'TCN'

            if type is None:
                try:
                    type_found = OSL_Sample.objects.get(osl_sample=sample.pk)
                except:
                    pass
                if type_found is not None:
                    type = 'OSL'

            if type is None:
                try:
                    type_found = Radiocarbon_Sample.objects.get(c14_sample=sample.pk)
                except:
                    pass
                if type_found is not None:
                    type = 'C14'

            # get sample site
            if sample.sample_site is not None:
                site = sample.sample_site.site_name

            # get location details
            if sample.sample_coordinates is not None:
                latitude = sample.sample_coordinates.latitude
                longitude = sample.sample_coordinates.longitude
                elevation = sample.sample_coordinates.elevation

            # get transect
            if sample.transect is not None:
                transect = sample.transect.transect_number

            # get retreat zone
            if sample.retreat is not None:
                retreat = sample.retreat.zone_number

            # get data specific to type - for other samples set to N/A
            if type == 'C14':
                c14_data = None
                try:
                    c14_data = Radiocarbon_Sample.objects.get(c14_sample=sample)
                except:
                    pass
                if c14_data is not None:
                    c14Depth = c14_data.depth_below_SL
                    c14Material = c14_data.material
                    c14Setting = c14_data.geological_setting
                    c14Pos = c14_data.stratigraphic_position_depth
                    c14Weight = c14_data.sample_weight
                    c14Contam = c14_data.pot_contamination
                    c14Curve = c14_data.calibration_curve

                    core = c14_data.c14_core
                    if core is not None:
                        expcore = core.exposure_core
                        core = core.core_number

                else:
                    c14Depth = None
                    c14Material = None
                    c14Setting = None
                    c14Pos = None
                    c14Weight = None
                    c14Contam = None
                    c14Curve = None
                    expcore = None
                    core = None

            else:
                c14Depth = 'N/A'
                c14Material = 'N/A'
                c14Setting = 'N/A'
                c14Pos = 'N/A'
                c14Weight = 'N/A'
                c14Contam = 'N/A'
                c14Curve = 'N/A'

            if type == 'OSL':
                osl_data = None
                try:
                    osl_data = OSL_Sample.objects.get(osl_sample=sample)
                except:
                    pass

                if osl_data is not None:
                    oslPosition = osl_data.stratigraphic_position
                    oslLithofacies = osl_data.lithofacies
                    oslDepth = osl_data.burial_depth
                    oslLithology = osl_data.lithology
                    oslGamma = osl_data.gamma_spec
                    oslEquip = osl_data.equipment_number
                    oslProbe = osl_data.probe_serial_no
                    oslFile = osl_data.filename
                    oslTime = osl_data.sample_time
                    oslDuration = osl_data.sample_duration
                    oslPotassium = osl_data.potassium
                    oslThorium = osl_data.thorium
                    oslUranium = osl_data.uranium

                    core = osl_data.osl_core
                    if core is not None:
                        expcore = core.exposure_core
                        core = core.core_number

                else:
                    oslPosition = None
                    oslLithofacies = None
                    oslDepth = None
                    oslLithology = None
                    oslGamma = None
                    oslEquip = None
                    oslProbe = None
                    oslFile = None
                    oslTime = None
                    oslDuration = None
                    oslPotassium = None
                    oslThorium = None
                    oslUranium = None
                    expcore = None
                    core = None


            else:
                oslPosition = 'N/A'
                oslLithofacies = 'N/A'
                oslDepth = 'N/A'
                oslLithology = 'N/A'
                oslGamma = 'N/A'
                oslEquip = 'N/A'
                oslProbe = 'N/A'
                oslFile = 'N/A'
                oslTime = 'N/A'
                oslDuration = 'N/A'
                oslPotassium = 'N/A'
                oslThorium = 'N/A'
                oslUranium = 'N/A'


            if type == 'TCN':
                tcn_data = None
                expcore = 'N/A'
                core = 'N/A'
                try:
                    tcn_data = TCN_Sample.objects.get(tcn_sample=sample)
                except:
                    pass

                if tcn_data is not None:
                    tcnQuartz = tcn_data.quartz_content
                    tcnSetting = tcn_data.sample_setting
                    tcnMaterial = tcn_data.sampled_material
                    tcnBoulder = tcn_data.boulder_dimensions
                    tcnStrike = tcn_data.sample_surface_strike_dip
                    tcnThickness = tcn_data.sample_thickness
                    tcnGrain = tcn_data.grain_size
                    tcnLithology = tcn_data.lithology
                    bearIncList = Sample_Bearing_Inclination.objects.filter(sample_with_bearing=tcn_data)
                    tcnBearInc = None
                    data = ''
                    counter = 1
                    for item in bearIncList:
                         values = item.bear_inc
                         if values is not None:
                             bearing = values.bearing
                             inclination = values.inclination
                             bear = 'B'+str(counter)
                             inc = 'I'+str(counter)
                             data += ("(%s: %s, %s: %s), " %(bear, bearing, inc, inclination))
                             counter += 1
                    if len(data) != 0:
                         data = data[0:-2]
                         tcnBearInc = data

                else:
                    tcnQuartz = None
                    tcnSetting = None
                    tcnMaterial = None
                    tcnBoulder = None
                    tcnStrike = None
                    tcnThickness = None
                    tcnGrain = None
                    tcnLithology = None


            else:
                tcnQuartz = 'N/A'
                tcnSetting = 'N/A'
                tcnMaterial = 'N/A'
                tcnBoulder = 'N/A'
                tcnStrike = 'N/A'
                tcnThickness = 'N/A'
                tcnGrain = 'N/A'
                tcnLithology = 'N/A'
                tcnBearInc = 'N/A'

            data = {'code': sample.sample_code, 'sampletype':type, 'latitude':latitude, 'longitude':longitude,
                    'elevation':elevation, 'site':site, 'notes':sample.sample_notes, 'cal_age':sample.calendar_age,
            'cal_age_error':sample.calendar_error, 'age':sample.age, 'age_error':sample.age_error,
            'lab_code':sample.lab_code, 'transect':transect, 'retreat':retreat, 'c14Depth':c14Depth,
            'c14Material':c14Material, 'c14Setting':c14Setting, 'c14Pos':c14Pos, 'c14Weight':c14Weight,
            'c14Contam':c14Contam, 'c14Curve':c14Curve, 'oslPosition':oslPosition, 'oslLithofacies':oslLithofacies,
            'oslDepth':oslDepth, 'oslLithology':oslLithology, 'oslGamma':oslGamma, 'oslEquip':oslEquip,
            'oslProbe':oslProbe, 'oslFile':oslFile, 'oslTime':oslTime, 'oslDuration':oslDuration,
            'oslPotassium':oslPotassium, 'oslThorium':oslThorium, 'oslUranium':oslUranium, 'expcore':expcore,
            'core':core, 'tcnQuartz':tcnQuartz, 'tcnSetting':tcnSetting, 'tcnMaterial':tcnMaterial,
            'tcnBoulder':tcnBoulder, 'tcnStrike':tcnStrike, 'tcnThickness':tcnThickness, 'tcnGrain':tcnGrain,
            'tcnLithology':tcnLithology, 'tcnBearInc':tcnBearInc}

            results.append(data)

    results = json.dumps(results)

    return HttpResponse(results, content_type='application/json')
