# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from mappingapp.conversion import convert_date, convert_lat_long, missing_keys
import datetime

# column headings
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
          'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_osl_cell_positions(ws):
    # dictionary of field name keys
    positions = {'Date: ': '', 'Location:': '', 'Latitude': '', 'National grid reference': '',
                 'Unique Sample Identifier': '', 'Elevation': '', 'Longtitude': '', 'Lithology': '',
                 'Exposure/Core': '', 'Exposure/Core No.': '', 'Stratigraphic Position': '',
                 'Lithofacies': '', 'Burial Depth (i.e. from section /deposit top)': '', 'Collector: ': '',
                 'Notes': '', 'Gamma-Spec Model': '', 'Equip. No. (if applicable)': '', 'Probe Serial No.': '',
                 'Filename': '', 'Time of sample': '', 'Sample duration':'', 'K': '', 'Th': '', 'U': ''}

    # iterate over sheet and add locations of value cells to corresponding keys
    for row in ws.iter_rows():
        for cell in row:
            val = cell.value
            # remove newlines from strings
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

            if val in positions:
                # notes cell is below its field name cell
                if val == 'Notes':
                    positions[val] = cell.column + str(cell.row+1)

                # all others one cell to the right
                else:
                    col = columns.index(cell.column)
                    val_col = columns[col+1]
                    positions[val] = val_col + str(cell.row)

    return positions


# extract the data from a tcn sample sheet
def get_osl_sample_info(sample_sheet, sample_count):

    # get the value cell positions
    positions = get_osl_cell_positions(sample_sheet)

    # populate list of missing keys
    missing_key_list = missing_keys(positions)

    # empty list to which type error fields will be added
    errors = []

    # create variables from the cell values
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
        # convert to string
        date = str(sample_date)

        # remove time
        if ' 00:00:00' in date:
             date = date.replace(' 00:00:00', '')

        # if date object reformat
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            sample_date = date.strftime('%d/%m/%Y')

        # if not date object try to convert, if conversion impossible add to notes
        except:
            if '.' in date:
                try:
                    sample_date = convert_date(date)
                    if sample_date == 'Error' and notes is not None:
                        notes = notes + ' ' + date + '. '
                        errors.append('Sample Date')
                        sample_date = None
                    elif sample_date == 'Error' and notes is None:
                        notes = date + '. '
                        errors.append('Sample Date')
                        sample_date = None
                except:
                    if notes is not None:
                        notes = notes + ' ' + date + '. '
                    else:
                        notes = date + '. '
                    sample_date = None
                    errors.append('Sample Date')
            else:
                if notes is not None:
                    notes = notes + ' ' + date + '. '
                else:
                    notes = date + '. '
                sample_date = None
                errors.append('Sample Date')


    # convert latitude and longitude if format incorrect
    if latitude is not None and not isinstance(latitude, float):
        latitude = convert_lat_long(latitude)
        if latitude == 'Error':
            errors.append('Sample latitude')
            latitude = None

    if longitude is not None and not isinstance(longitude, float):
        longitude = convert_lat_long(longitude)
        if longitude == 'Error':
            errors.append('Sample longitude')
            longitude = None
        else:
            longitude = -1 * longitude

    # counter which is concatenated to variable name keys - uniquely identifies values in multi-sample files
    counter = str(sample_count)

    # convert sample time to string
    if sample_time is not None and isinstance(sample_time, datetime.time):
        sample_time = sample_time.strftime("%H:%M")

    # set sample type
    sample_type = 'OSL'

    # create dictionary with sample values, error list, missing keys and sample type
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
                      'sample_easting'+counter:None, 'sample_northing'+counter:None, 'sample_type'+counter:sample_type,
                      'transect'+counter:None, 'errors'+counter:errors, 'missing_keys'+counter:missing_key_list}

    return sample_details
