from openpyxl import load_workbook
import datetime

columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_osl_cell_positions(ws):

    positions = {'Date: ': '', 'Location:': '', 'Latitude': '', 'National grid reference':'',
                 'Unique Sample Identifier': '', 'Elevation': '', 'Longtitude': '', 'Lithology': '',
                 'Exposure/Core': '', 'Exposure/Core No.': '', 'Stratigraphic Position': '',
                 'Lithofacies': '', 'Burial Depth (i.e. from section /deposit top)': '', 'Collector: ': '',
                 'Notes': '', 'Gamma-Spec Model':'', 'Equip. No. (if applicable)':'', 'Probe Serial No.':'',
                 'Filename':'', 'Time of sample':'', 'Sample duration':'', 'K':'', 'Th':'', 'U':''}

    for row in ws.iter_rows():
        for cell in row:
            val = cell.value
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

            if val in positions:
                if val == 'Notes':
                    positions[val] = cell.column + str(cell.row+1)
                else:
                    col = columns.index(cell.column)
                    val_col = columns[col+1]
                    positions[val] = val_col + str(cell.row)

    return positions


# extract the data from a tcn sample sheet
def get_osl_sample_info(sample_sheet, sample_count):
    positions = get_osl_cell_positions(sample_sheet)

    sample_date = sample_sheet[positions['Date: ']].value
    sample_location_name = sample_sheet[positions['Location:']].value
    grid = sample_sheet[positions['National grid reference']].value
    sample_code = sample_sheet[positions['Unique Sample Identifier']].value
    latitude = sample_sheet[positions['Latitude']].value
    longitude = sample_sheet[positions['Longtitude']].value
    elevation = sample_sheet[positions['Elevation']].value
    lithofacies = sample_sheet[positions['Lithofacies']].value
    lithology = sample_sheet[positions['Lithology']].value
    exposure_core = sample_sheet[positions['Exposure/Core']].value
    core_number = sample_sheet[positions['Exposure/Core No.']].value
    position = sample_sheet[positions['Stratigraphic Position']].value
    notes = sample_sheet[positions['Notes']].value
    burial_depth = sample_sheet[positions['Burial Depth (i.e. from section /deposit top)']].value
    collector = sample_sheet[positions['Collector: ']].value
    gamma_spec = sample_sheet[positions['Gamma-Spec Model']].value
    equipment_number = sample_sheet[positions['Equip. No. (if applicable)']].value
    probe_serial_number = sample_sheet[positions['Probe Serial No.']].value
    filename = sample_sheet[positions['Filename']].value
    sample_time = sample_sheet[positions['Time of sample']].value
    sample_duration = sample_sheet[positions['Sample duration']].value
    potassium = sample_sheet[positions['K']].value
    thorium = sample_sheet[positions['Th']].value
    uranium = sample_sheet[positions['U']].value

    # remove newlines from notes
    if notes is not None:
        notes = notes.replace('\n', ' ')
        notes = ' '.join(notes.split())

    # convert date if format incorrect
    if sample_date is not None:
        date = str(sample_date)
        if '.' in date:
            sample_date = convert_date(date)

    # convert latitude and longitude if format incorrect
    if latitude is not None:
        latitude = convert_lat_long(latitude)

    if longitude is not None:
        longitude = convert_lat_long(longitude)

    counter = str(sample_count)

    # convert date if format incorrect
    if sample_date is not None:
        date = str(sample_date)
        if '.' in date:
            sample_date = convert_date(date)
        else:
            sample_date = sample_date.strftime("%d/%m/%Y")

    # convert sample time to string
    if sample_time is not None and isinstance(sample_time, datetime.time):
        sample_time = sample_time.strftime("%H:%M")

    sample_details = {'sample_grid_reference'+counter:grid, 'lithology'+counter:lithology,
                      'sample_latitude'+counter:latitude, 'sample_longitude'+counter:longitude,
                      'sample_elevation'+counter:elevation, 'sample_code'+counter:sample_code,
                      'sample_location_name'+counter:sample_location_name, 'sample_date'+counter:sample_date,
                      'collector'+counter:collector, 'sample_notes'+counter:notes,
                      'exposure_core'+counter:exposure_core, 'core_number'+counter:core_number,
                      'position'+counter:position, 'lithofacies'+counter:lithofacies,
                      'burial_depth'+counter:burial_depth, 'gamma_spec'+counter:gamma_spec,
                      'equipment_number'+counter:equipment_number, 'probe_number'+counter:probe_serial_number,
                      'filename'+counter:filename, 'sample_time'+counter:sample_time,
                      'sample_duration'+counter:sample_duration, 'potassium'+counter:potassium,
                      'thorium'+counter:thorium, 'uranium'+counter:uranium, 'sample_bng_ing'+counter:None,
                      'sample_easting'+counter:None, 'sample_northing'+counter:None}

    return sample_details


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


# convert lat/long in degrees, minutes to decimal format
def convert_lat_long(coord):
    if type(coord) is float:
        return coord
    else:
        result = "".join(i for i in coord if ord(i)<128)

        degrees = float(result[:result.index(' ')])
        minutes = float(result[result.rindex(' ')+1:])
        return degrees + (minutes/60)

