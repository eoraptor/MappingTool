# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from mappingapp.models import Sample_Site, Coordinates, Sample, TCN_Sample, Bearing_Inclination, Sample_Bearing_Inclination, Transect


# iterate over the site sheet to determine which cells to extract data from
def get_site_cell_positions(ws):

    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    positions = {'Site Name: ': '', 'Location (inc. Transect no.)': '', 'Latitude(decimal deg)': '',
                 'Longtitude(decimal deg)(West is -ve)': '', 'BNG/ING?': '', 'Northing:': '', 'Easting:': '',
                 'Elevation             (m ASL)': '', 'Date Sampled:': '', 'Geomorph Setting:': '',
                 'Type of Samples collected (TCN/14C/OSL)': '', 'Collected by:': '', 'Photographs Taken (Y/N):': '',
                 'Photo labels/Time stamps:': '', 'Notes': ''}

    for row in ws.iter_rows():
        for cell in row:
            val = cell.value
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

                if val in positions:
                    col = columns.index(cell.column)
                    val_col = columns[col+1]
                    positions[val] = val_col + str(cell.row)

    return positions


# extract the data from the site sheet
def get_site_info(wb):
    site_sheet = wb["Site Info"]
    positions = get_site_cell_positions(site_sheet)

    site_name = site_sheet[positions['Site Name: ']].value
    site_location = site_sheet[positions['Location (inc. Transect no.)']].value
    site_latitude = site_sheet[positions['Latitude(decimal deg)']].value
    site_longitude = site_sheet[positions['Longtitude(decimal deg)(West is -ve)']].value
    bng_ing = site_sheet[positions['BNG/ING?']].value
    site_northing = site_sheet[positions['Northing:']].value
    site_easting = site_sheet[positions['Easting:']].value
    site_elevation = site_sheet[positions['Elevation             (m ASL)']].value
    sample_date = site_sheet[positions['Date Sampled:']].value
    geomorph = site_sheet[positions['Geomorph Setting:']].value
    type = site_sheet[positions['Type of Samples collected (TCN/14C/OSL)']].value
    collector = site_sheet[positions['Collected by:']].value
    photographs = site_sheet[positions['Photographs Taken (Y/N):']].value
    photo_labels = site_sheet[positions['Photo labels/Time stamps:']].value
    site_notes = site_sheet[positions['Notes']].value

    if photographs is not None:
        photographs = photographs.lower()
        if photographs.startswith('y'):
            photographs = True
        else:
            photographs = False

    if sample_date is not None:
        date = str(sample_date)
        if '.' in date:
            sample_date = convert_date(date)

    if site_latitude is not None:
        site_latitude = convert_lat_long(site_latitude)

    if site_longitude is not None:
        site_longitude = convert_lat_long(site_longitude)

    if all(ele is None for ele in [site_name, site_location, site_latitude, site_longitude, bng_ing, site_northing,
                                   site_easting, site_elevation, sample_date, geomorph, type, collector, photographs,
                                   photo_labels, site_notes]):
        return None
    else:
        coords = Coordinates.objects.create_coordinates(bng_ing, None, site_easting, site_northing, site_latitude,
                                    site_longitude, site_elevation)
        coords.save()
        site = Sample_Site.objects.create_site(site_name, site_location, None, None, sample_date, None, geomorph, type,
                                          photographs, photo_labels, site_notes, None, None, coords)
        site.save()
        return site


# iterate over the tcn sheet to determine which cells to extract data from
def get_tcn_cell_positions(ws):
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    positions = {'Date: ': '', 'Location:': '', 'Latitude (if different from site info)': '',
                 'Unique Sample Identifier': '', 'BNG or ING': '', 'Northing': '', 'Easting': '',
                 'Elevation': '', 'Longtitude': '', 'Lithology': '', 'Boulder dimensions [cm] (LxWxH)': '',
                 'Transect:': '', 'Est Quartz content': '', 'Sample setting': '', 'Sample surface strike/dip ': '',
                 'Sampled material (eg:boulder)': '', 'sample thickness': '', 'Grain Size:': '',
                 'Collector: ': '', 'Notes (inc.weathering and erosion rate est)': '', 'Bearing': '',
                 'Inclination': ''}

    for row in ws.iter_rows():
        for cell in row:
            val = cell.value
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

                if val in positions:
                    if val == 'Notes (inc.weathering and erosion rate est)' or val == 'Bearing' or val == 'Inclination':
                        positions[val] = cell.column + str(cell.row+1)
                    else:
                        col = columns.index(cell.column)
                        val_col = columns[col+1]
                        positions[val] = val_col + str(cell.row)

    return positions


# extract the data from a tcn sample sheet
def get_tcn_sample_info(sample_sheet, site):
    positions = get_tcn_cell_positions(sample_sheet)

    sample_date = sample_sheet[positions['Date: ']].value
    sample_location_name = sample_sheet[positions['Location:']].value
    sample_code = sample_sheet[positions['Unique Sample Identifier']].value
    bng_ing = sample_sheet[positions['BNG or ING']].value
    sample_northing = sample_sheet[positions['Northing']].value
    sample_easting = sample_sheet[positions['Easting']].value
    transect = sample_sheet[positions['Transect:']].value
    latitude = sample_sheet[positions['Latitude (if different from site info)']].value
    longitude = sample_sheet[positions['Longtitude']].value
    elevation = sample_sheet[positions['Elevation']].value
    lithology = sample_sheet[positions['Lithology']].value
    quartz = sample_sheet[positions['Est Quartz content']].value
    setting = sample_sheet[positions['Sample setting']].value
    material = sample_sheet[positions['Sampled material (eg:boulder)']].value
    boulder_dim = sample_sheet[positions['Boulder dimensions [cm] (LxWxH)']].value
    surface_strike = sample_sheet[positions['Sample surface strike/dip ']].value
    notes = sample_sheet[positions['Notes (inc.weathering and erosion rate est)']].value
    thickness = sample_sheet[positions['sample thickness']].value
    grain_size = sample_sheet[positions['Grain Size:']].value
    collector = sample_sheet[positions['Collector: ']].value
    bearing = get_bearing(sample_sheet, positions['Bearing'])

    notes = notes.replace('\n', ' ')

    if sample_date is not None:
        date = str(sample_date)
        if '.' in date:
            sample_date = convert_date(date)

    if latitude is not None:
        latitude = convert_lat_long(latitude)

    if longitude is not None:
        longitude = convert_lat_long(longitude)

    coords = Coordinates.objects.create_coordinates(bng_ing, None, sample_easting, sample_northing, latitude,
                                    longitude, elevation)
    coords.save()

    sample = Sample.objects.create_sample(sample_code, sample_location_name, sample_date, collector, notes,
                                          None, None, None, None, None, None, coords, site)
    sample.save()

    tcn_data = TCN_Sample.objects.create_tcn(quartz, setting, material, boulder_dim, surface_strike,
                                             thickness, grain_size, lithology, sample)
    tcn_data.save()

    for b in bearing:
        bi = Bearing_Inclination.objects.create_bearing_inclination(b[0], b[1])
        bi.save()
        sample_with_bi = Sample_Bearing_Inclination.objects.create_sampleBI(tcn_data, bi)
        sample_with_bi.save()

    trans = Transect.objects.create_transect(transect)
    trans.save()
    return trans


# extract all bearing and inclination data from tcn sheets
def get_bearing(sample_sheet, start_cell):
    data = []
    done = False
    start = int(start_cell[1:])
    while not done:
        start_str = str(start)
        bearing = sample_sheet['A' + start_str].value
        inclination = sample_sheet['B' + start_str].value

        if (bearing is not None or inclination is not None) and bearing != 'Please complete one sample sheet for each sample':
                data.append((int(bearing), int(inclination)))
                start += 1
        else:
            return data


# process a complete file
def process_file(filename):
    # need error handling
    wb = load_workbook(filename, use_iterators=True)
    site = get_site_info(wb)
    transect = None

    sheet_names = wb.get_sheet_names()
    for sheet in sheet_names:
        if sheet != 'Site Info':
            ws = wb[sheet]
            type = get_sample_type(ws)
            if type == 'TCN':
                if transect is None:
                    transect = get_tcn_sample_info(ws, site)
                else:
                    get_tcn_sample_info(ws, site)

    if transect is not None and site is not None:
        Sample_Site.objects.filter(pk=site.pk).update(site_transect=transect)


# take incorrect date format and replace
def convert_date(date):
    first_point = date.find('.')
    last_point = date.rfind('.')

    day = date[:first_point].strip(' ')
    month = date[first_point+1:last_point].strip(' ')
    year = date[last_point+1:].strip(' ')

    if len(day) == 1:
        day = '0' + day

    if len(month) == 1:
        month = '0' + month

    if len(year) == 2:
        year = '20' + year

    return year + '-' + month + '-' + day


# determine what type of sample, if any, is on a worksheet
def get_sample_type(ws):
    if ws['A1'].value == 'TCN Sample Sheet' and ws['B3'].value is not None:
        return 'TCN'

    elif ws['A1'].value == '14C Sample Sheet' and ws['B3'].value is not None:
        return '14C'

    elif ws['A1'].value == 'OSL Sample Sheet' and ws['B3'].value is not None:
        return 'OSL'

    else:
        return None


# convert lat/long in degrees, minutes to decimal format
def convert_lat_long(coord):
    if type(coord) is float:
        return coord
    else:
        result = "".join(i for i in coord if ord(i)<128)

        degrees = float(result[:result.index(' ')])
        minutes = float(result[result.rindex(' ')+1:])
        return degrees + (minutes/60)


