# -*- coding: utf-8 -*-
from openpyxl import load_workbook
from mappingapp.conversion import convert_date, convert_lat_long, missing_keys
import datetime

# column headings
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# iterate over the tcn sheet to determine which cells to extract data from
def get_tcn_cell_positions(ws):

    # dictionary of field names
    positions = {'Date: ': '', 'Location:': '', 'Latitude (if different from site info)': '',
                 'Unique Sample Identifier': '', 'BNG or ING': '', 'Northing': '', 'Easting': '',
                 'Elevation': '', 'Longtitude': '', 'Lithology': '', 'Boulder dimensions [cm] (LxWxH)': '',
                 'Transect:': '', 'Est Quartz content': '', 'Sample setting': '', 'Sample surface strike/dip ': '',
                 'Sampled material (eg:boulder)': '', 'sample thickness': '', 'Grain Size:': '',
                 'Collector: ': '', 'Notes (inc.weathering and erosion rate est)': '', 'Bearing': '',
                 'Inclination': '', 'Sample Thickness :': '', 'Boulder dimensions [cm] (LxBxH)': ''}

    # iterate over sheet and retrieve positions of value cells
    for row in ws.iter_rows():
        for cell in row:
            val = cell.value
            # remove newlines from strings
            if val is not None and isinstance(val, basestring):
                val = val.replace('\n', '')

                if val in positions:
                    # cells with values one row below
                    if val == 'Notes (inc.weathering and erosion rate est)' or val == 'Bearing' or val == 'Inclination':
                        positions[val] = cell.column + str(cell.row+1)
                    else:
                        # cells with values one cell to the right
                        col = columns.index(cell.column)
                        val_col = columns[col+1]
                        positions[val] = val_col + str(cell.row)

    # fix cell locations for alternate spreadsheet format
    if positions['sample thickness'] == '':
        positions['sample thickness'] = positions['Sample Thickness :']

    # alternative Boulder dimensions cell split in three - return list of positions
    if positions['Boulder dimensions [cm] (LxWxH)'] == '' and positions['Boulder dimensions [cm] (LxBxH)'] != '':
        cellA = positions['Boulder dimensions [cm] (LxBxH)']
        row = cellA[1:]
        col = columns.index(cellA[0])
        cellB = columns[col+1] + row
        cellC = columns[col+2] + row
        positions['Boulder dimensions [cm] (LxWxH)'] = [cellA, cellB, cellC]

    # alternative Surface strike cell split in two - return list of positions
    surface_strike_cell = positions['Sample surface strike/dip ']
    row = surface_strike_cell[1:]
    col = columns.index(surface_strike_cell[0])
    cellB = columns[col+1] + row
    positions['Sample surface strike/dip '] = [surface_strike_cell, cellB]

    # Cover for potential cell merging - retrieve cell past expected value cell
    longitude_cell = positions['Longtitude']
    row = longitude_cell[1:]
    col = columns.index(longitude_cell[0])
    cellB = columns[col+1] + row
    positions['Longtitude'] = [longitude_cell, cellB]

    # Cover for potential cell merging - retrieve cell past expected value cell
    easting_cell = positions['Easting']
    row = easting_cell[1:]
    col = columns.index(easting_cell[0])
    cellB = columns[col+1] + row
    positions['Easting'] = [easting_cell, cellB]

    # Cover for potential cell merging - retrieve cell past expected value cell
    bng_cell = positions['BNG or ING']
    row = bng_cell[1:]
    col = columns.index(bng_cell[0])
    cellB = columns[col+1] + row
    positions['BNG or ING'] = [bng_cell, cellB]

    return positions


# extract the data from a tcn sample sheet
def get_tcn_sample_info(sample_sheet, sample_count):

    # retrieve the value cell postitions
    positions = get_tcn_cell_positions(sample_sheet)

    # populate list of missing fields
    missing_key_list = missing_keys(positions)

    # remove duplicate fields with unused keys - both have had their values added to default field name values
    try:
        missing_key_list.remove('Boulder dimensions [cm] (LxBxH)')
    except:
        pass
    try:
        missing_key_list.remove('Sample Thickness :')
    except:
        pass

    # list to add fields with type errors
    errors = []

    # create variables using the cell values
    sample_date = sample_sheet[positions['Date: ']].value
    sample_location_name = sample_sheet[positions['Location:']].value
    sample_code = sample_sheet[positions['Unique Sample Identifier']].value
    sample_northing = sample_sheet[positions['Northing']].value
    transect = sample_sheet[positions['Transect:']].value
    latitude = sample_sheet[positions['Latitude (if different from site info)']].value
    elevation = sample_sheet[positions['Elevation']].value
    lithology = sample_sheet[positions['Lithology']].value
    quartz = sample_sheet[positions['Est Quartz content']].value
    setting = sample_sheet[positions['Sample setting']].value
    material = sample_sheet[positions['Sampled material (eg:boulder)']].value
    notes = sample_sheet[positions['Notes (inc.weathering and erosion rate est)']].value
    thickness = sample_sheet[positions['sample thickness']].value
    grain_size = sample_sheet[positions['Grain Size:']].value
    collector = sample_sheet[positions['Collector: ']].value

    # bearing and inclination values retrieved using separate function
    bearing = get_bearing(sample_sheet, positions['Bearing'])

    # check boulder dimension value - use three columns if cell was split
    boulder_dim = None
    if isinstance(positions['Boulder dimensions [cm] (LxWxH)'], list):
        value1 = sample_sheet[positions['Boulder dimensions [cm] (LxWxH)'][0]].value
        value2 = sample_sheet[positions['Boulder dimensions [cm] (LxWxH)'][1]].value
        value3 = sample_sheet[positions['Boulder dimensions [cm] (LxWxH)'][2]].value

        if isinstance(value1, float) and value1 is not None:
            value1 = int(value1)

        if isinstance(value2, float) and value2 is not None:
            value1 = int(value2)

        if isinstance(value3, float) and value3 is not None:
            value1 = int(value3)

        # create single value by concatenating the three separate ones
        boulder_dim = str(value1) + ' x ' + str(value2) + ' x ' + str(value3)

    # cell not split - use single cell
    elif positions['Boulder dimensions [cm] (LxWxH)'] is not None and\
            positions['Boulder dimensions [cm] (LxWxH)'] != '':
            boulder_dim = sample_sheet[positions['Boulder dimensions [cm] (LxWxH)']].value

    # check to see if sample surface strike dip cell has been split - create concatenated value if true
    surface_strike = None
    if positions['Sample surface strike/dip '] is not None and positions['Sample surface strike/dip '] != '':
        if sample_sheet[positions['Sample surface strike/dip '][1]] is not None:
            surface_strike = sample_sheet[positions['Sample surface strike/dip '][0]].value + ' / ' +\
                sample_sheet[positions['Sample surface strike/dip '][1]].value
        else:
            surface_strike = sample_sheet[positions['Sample surface strike/dip '][0]].value

    # check longitude in correct cell by looking at value in cell after expected value cell
    longitude = None
    if positions['Longtitude'] is not None and positions['Longtitude'] != '':
        if sample_sheet[positions['Longtitude'][0]].value is not None:
            longitude = sample_sheet[positions['Longtitude'][0]].value
        elif sample_sheet[positions['Longtitude'][1]].value is not None and\
            sample_sheet[positions['Longtitude'][1]].value != 'Elevation':
                longitude = sample_sheet[positions['Longtitude'][1]].value

    # check easting in correct cell by looking at value in cell after expected value cell
    sample_easting = None
    if positions['Easting'] is not None and positions['Easting'] != '':
        if sample_sheet[positions['Easting'][0]].value is not None:
            sample_easting = sample_sheet[positions['Easting'][0]].value
        elif sample_sheet[positions['Easting'][1]].value is not None and\
            sample_sheet[positions['Easting'][1]].value != 'Transect:':
                sample_easting = sample_sheet[positions['Easting'][1]].value

    # check bng in correct cell by looking at value in cell after expected value cell
    bng_ing = None
    if positions['BNG or ING'] is not None and positions['BNG or ING'] != '':
        if sample_sheet[positions['BNG or ING'][0]].value is not None:
            bng_ing = sample_sheet[positions['BNG or ING'][0]].value
        elif sample_sheet[positions['BNG or ING'][1]].value is not None:
                bng_ing = sample_sheet[positions['BNG or ING'][1]].value

    # remove newlines from notes
    if notes is not None:
        notes = notes.replace('\n', ' ')
        notes = ' '.join(notes.split())

    # Remove incorrect formats from Bearing & Inclination and add to Notes
    if bearing is not None:
        remove_list = []
        for value in bearing:

            bear = value[0]
            inc = value[1]

            if not isinstance(bear, int) or not isinstance(inc, int):
                remove_list.append(value)
                if notes is not None:
                    notes = notes + ' ' + str(bear) + ' ' + str(inc) + '. '
                else:
                    notes = str(bear) + ' ' + str(inc) + '. '

        for value in remove_list:
            bearing.remove(value)

        if len(bearing) == 0:
            bearing = None


    # convert date if format incorrect
    if sample_date is not None:
        # convert to string
        date = str(sample_date)

        # remove time
        if ' 00:00:00' in date:
             date = date.replace(' 00:00:00', '')

        try:
            # is it a recognised date?
            # spreadsheet format
            date = datetime.datetime.strptime(date, '%Y-%m-%d')

            # convert to Django and database accepted format
            sample_date = date.strftime('%d/%m/%Y')

            # if not, try to convert into date format, add to notes if unable
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

    # check easting and northing are numerical
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

    # counter to uniquely identify sample's values from others in same file
    counter = str(sample_count)

    # set sample type
    sample_type = 'TCN'

    # return dictionary of values
    sample_details = {'sample_bng_ing'+counter:bng_ing, 'sample_grid_reference'+counter:None,
                      'sample_easting'+counter:sample_easting, 'sample_northing'+counter:sample_northing,
                      'sample_latitude'+counter:latitude, 'sample_longitude'+counter:longitude,
                      'sample_elevation'+counter:elevation, 'sample_code'+counter:sample_code,
                      'sample_location_name'+counter:sample_location_name, 'sample_date'+counter:sample_date,
                      'collector'+counter:collector, 'sample_notes'+counter:notes, 'transect'+counter:transect,
                      'quartz_content'+counter:quartz, 'sample_setting'+counter:setting,
                      'sampled_material'+counter:material, 'boulder_dimensions'+counter:boulder_dim,
                      'sample_surface_strike_dip'+counter:surface_strike, 'sample_thickness'+counter:thickness,
                      'grain_size'+counter:grain_size, 'lithology'+counter:lithology, 'bearings'+counter:bearing,
                      'sample_type'+counter:sample_type, 'errors'+counter: errors,
                      'missing_keys'+counter:missing_key_list}


    return sample_details


# extract all bearing and inclination data from tcn sheets
def get_bearing(sample_sheet, start_cell):

    # list for return
    data = []

    # first bearing cell
    start = int(start_cell[1:])

    bearing = ''
    counter = 0
    # cell contents below last bearing row
    end = 'Please complete one sample sheet for each sample'

    # if not at end cell and less than max number get values
    while bearing != end and counter < 40:

        start_str = str(start)
        bearing = sample_sheet['A' + start_str].value
        inclination = sample_sheet['B' + start_str].value

        # convert floats to integers and add tuple to data list for return
        if bearing is not None and bearing is not end and inclination is not None:
            if isinstance(bearing, float) and isinstance(inclination, float):
                bearing = int(bearing)
                inclination = int(inclination)
            data.append((bearing, inclination))

        #increment the starting point and the counter
        start += 1
        counter += 1

    # if no values found, return None, else return the list of tuples
    if len(data) == 0:
        return None
    else:
        return data

