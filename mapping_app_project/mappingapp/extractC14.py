# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from mappingapp.conversion import convert_date, convert_lat_long, missing_keys
import datetime

# list of column headings
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_C14_cell_positions(ws):

    # the cell field names
    positions = {'Date: ': '', 'Location:': '', 'Latitude (if different from site info)': '',
                 'Unique Sample Identifier': '', 'BNG or ING': '', 'Northing:': '', 'Easting:': '',
                 'Elevation:': '', 'Longtitude:': '', 'Depth below SL:': '', 'Transect:': '', 'Exposure/Core:': '',
                 'Core number:': '', 'Material:': '', 'Geological Setting/ In Situ enivronment:': '',
                 'Stratigraphic position (depth):': '', 'Sample weight (g):': '', 'Collector: ': '', 'Notes': '',
                 'Potential contamination sources:': '', '8/6 Figure ref.':''}

    # fields in which the cell is a merged cell
    merged_cells = {'BNG or ING': '', 'Easting:': '', 'Longtitude:': '', 'Core number:': ''}

    # get positions of cells containing the corresponding values
    for row in ws.iter_rows():
        for cell in row:
            val = cell.value

            # remove newlines from strings
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

                if val in positions:
                    # if not a merged cell, get cell coordinates of adjacent cell
                    if val not in merged_cells:
                        col = columns.index(cell.column)
                        val_col = columns[col+1]
                        positions[val] = val_col + str(cell.row)

                    else:
                        # for merged cells, move column across by 2
                        col = columns.index(cell.column)
                        val_col = columns[col+2]
                        positions[val] = val_col + str(cell.row)

    return positions


# extract the data from a tcn sample sheet
def get_C14_sample_info(sample_sheet, sample_count):

    # get dictionary of field name, value cell positions
    positions = get_C14_cell_positions(sample_sheet)

    # populate list with keys which were not found
    missing_key_list = missing_keys(positions)

    # list to contain fields for which type errors were found
    errors = []

    # create variables from the spreadsheet values
    sample_date = sample_sheet[positions['Date: ']].value
    sample_location_name = sample_sheet[positions['Location:']].value
    sample_code = sample_sheet[positions['Unique Sample Identifier']].value
    sample_northing = sample_sheet[positions['Northing:']].value
    sample_easting = sample_sheet[positions['Easting:']].value
    transect = sample_sheet[positions['Transect:']].value
    latitude = sample_sheet[positions['Latitude (if different from site info)']].value
    longitude = sample_sheet[positions['Longtitude:']].value
    elevation = sample_sheet[positions['Elevation:']].value
    bng_ing = sample_sheet[positions['BNG or ING']].value
    grid = sample_sheet[positions['8/6 Figure ref.']].value
    depth = sample_sheet[positions['Depth below SL:']].value
    exposure_core = sample_sheet[positions['Exposure/Core:']].value
    core_number = sample_sheet[positions['Core number:']].value
    material = sample_sheet[positions['Material:']].value
    notes = sample_sheet[positions['Notes']].value
    setting = sample_sheet[positions['Geological Setting/ In Situ enivronment:']].value
    position = sample_sheet[positions['Stratigraphic position (depth):']].value
    collector = sample_sheet[positions['Collector: ']].value
    weight = sample_sheet[positions['Sample weight (g):']].value
    contamination = sample_sheet[positions['Potential contamination sources:']].value

    # remove newlines and excess whitespace from notes
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

        # is it a date object, if yes reformat to desired output
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            sample_date = date.strftime('%d/%m/%Y')

        # if not a date object try to convert or add to notes if conversion fails
        except:
            if '.' in date:
                try:
                    sample_date = convert_date(date)
                    if sample_date == 'Error' and notes is not None:
                        notes = notes + ' ' + date + '. '
                        sample_date = None
                        errors.append('Sample Date')
                    elif sample_date == 'Error' and notes is None:
                        notes = date + '. '
                        sample_date = None
                        errors.append('Sample Date')
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
    if latitude is not None and not isinstance(latitude, (float,int)):
        latitude = convert_lat_long(latitude)
        if latitude == 'Error':
            errors.append('Sample latitude')
            latitude = None

    if longitude is not None and not isinstance(longitude, (float, int)):
        longitude = convert_lat_long(longitude)
        if longitude == 'Error':
            errors.append('Sample longitude')
            longitude = None
        else:
            longitude = -1 * longitude

    # convert easting and northing to integers if possible
    if sample_easting is not None:
        try:
            sample_easting = int(sample_easting)
        except:
            errors.append('Sample Easting')
            sample_easting = None

    if sample_northing is not None:
        try:
            sample_northing = int(sample_northing)
        except:
            errors.append('Sample Northing')
            sample_northing = None

    # add T to transect if missing
    if transect is not None:
        if isinstance(transect, (int, float)):
            transect = 'T'+ str(int(transect))

    # counter passed to function which is used to uniquely identify multiple sample values from same file
    counter = str(sample_count)

    # set sample type
    sample_type = 'C14'

    # create dictionary of field name keys concatenated with the counter and with their associated values
    sample_details = {'sample_bng_ing'+counter:bng_ing, 'sample_grid_reference'+counter:grid,
                      'sample_easting'+counter:sample_easting, 'sample_northing'+counter:sample_northing,
                      'sample_latitude'+counter:latitude, 'sample_longitude'+counter:longitude,
                      'sample_elevation'+counter:elevation,
                      'sample_code'+counter:sample_code, 'errors'+counter:errors,
                      'sample_location_name'+counter:sample_location_name, 'sample_date'+counter:sample_date,
                      'collector'+counter:collector, 'sample_notes'+counter:notes, 'transect'+counter:transect,
                      'exposure_core'+counter:exposure_core, 'core_number'+counter:core_number,
                      'position'+counter:position, 'depth'+counter:depth,
                      'material'+counter:material, 'setting'+counter:setting, 'weight'+counter:weight,
                      'contamination'+counter:contamination, 'sample_type'+counter:sample_type,
                      'missing_keys'+counter:missing_key_list}

    return sample_details


