# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from mappingapp.conversion import convert_date, convert_lat_long

columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_C14_cell_positions(ws):

    positions = {'Date: ': '', 'Location:': '', 'Latitude (if different from site info)': '',
                 'Unique Sample Identifier': '', 'BNG or ING': '', 'Northing:': '', 'Easting:': '',
                 'Elevation:': '', 'Longtitude:': '', 'Depth below SL:': '', 'Transect:': '', 'Exposure/Core:': '',
                 'Core number:': '', 'Material:': '', 'Geological Setting/ In Situ enivronment:': '',
                 'Stratigraphic position (depth):': '', 'Sample weight (g):': '', 'Collector: ': '', 'Notes': '',
                 'Potential contamination sources:': '', '8/6 Figure ref.':''}

    merged_cells = {'BNG or ING': '', 'Easting:': '', 'Longtitude:': '', 'Core number:': ''}

    for row in ws.iter_rows():
        for cell in row:
            val = cell.value
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

                if val in positions:
                    if val not in merged_cells:
                        col = columns.index(cell.column)
                        val_col = columns[col+1]
                        positions[val] = val_col + str(cell.row)
                    else:
                        col = columns.index(cell.column)
                        val_col = columns[col+2]
                        positions[val] = val_col + str(cell.row)

    return positions


# extract the data from a tcn sample sheet
def get_C14_sample_info(sample_sheet, sample_count):
    positions = get_C14_cell_positions(sample_sheet)

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
        date = str(sample_date)
        if '.' in date:
            sample_date = convert_date(date)

    # convert latitude and longitude if format incorrect
    if latitude is not None:
        latitude = convert_lat_long(latitude)

    if longitude is not None:
        longitude = convert_lat_long(longitude)

    # add T to transect if missing
    if transect is not None:
        if isinstance(transect, (int, float)):
            transect = 'T'+ str(int(transect))

    counter = str(sample_count)

    # set sample type
    sample_type = 'C14'

    sample_details = {'sample_bng_ing'+counter:bng_ing, 'sample_grid_reference'+counter:None,
                      'sample_easting'+counter:sample_easting, 'sample_northing'+counter:sample_northing,
                      'sample_latitude'+counter:latitude, 'sample_longitude'+counter:longitude,
                      'sample_elevation'+counter:elevation, 'grid_reference'+counter:grid,
                      'sample_code'+counter:sample_code,
                      'sample_location_name'+counter:sample_location_name, 'sample_date'+counter:None,
                      'collector'+counter:collector, 'sample_notes'+counter:notes, 'transect'+counter:transect,
                      'exposure_core'+counter:exposure_core, 'core_number'+counter:core_number,
                      'position'+counter:position, 'depth'+counter:depth,
                      'material'+counter:material, 'setting'+counter:setting, 'weight'+counter:weight,
                      'contamination'+counter:contamination, 'sample_type'+counter:sample_type}

    return sample_details


