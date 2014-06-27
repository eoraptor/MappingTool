from openpyxl import load_workbook

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

# extract the data
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

    photographs = photographs.lower()
    if photographs.startswith('y'):
        photographs = True
    else:
        photographs = False

    print site_name, '\n', site_location, '\n', site_latitude, '\n', site_longitude, '\n', bng_ing, '\n', site_northing
    print site_easting, '\n', site_elevation, '\n', sample_date, '\n', geomorph, type, '\n', collector
    print photographs, '\n', photo_labels, '\n', site_notes



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
def get_tcn_sample_info(sample_sheet):
    positions = get_tcn_cell_positions(sample_sheet)

    sample_date = sample_sheet[positions['Date: ']].value
    sample_location = sample_sheet[positions['Location:']].value
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

    print sample_date, '\n', sample_location, '\n', sample_code, '\n', bng_ing, '\n', sample_northing, '\n', sample_easting, '\n', transect, '\n', latitude
    print longitude, '\n', elevation, '\n', lithology, '\n', quartz, '\n', setting, '\n', material, boulder_dim, '\n', surface_strike, '\n', notes, '\n', thickness, '\n', grain_size, '\n', collector
    for b in bearing:
            print b[0],b[1]
    print '\n'



# extract all bearing and inclination data from tcn sheets
def get_bearing(sample_sheet, start_cell):
    data = []
    done = False
    start = int(start_cell[1:])
    while not done:
        start_str = str(start)
        bearing = sample_sheet['A' + start_str].value
        inclination = sample_sheet['B' + start_str].value

        if bearing is not None or inclination is not None:
            data.append((int(bearing), int(inclination)))
            start += 1
        else:
            return data


# process a complete file
def process_file(filename):
    # need error handling
    wb = load_workbook(filename, use_iterators=True)

    sheet_names = wb.get_sheet_names()

    for sheet in sheet_names:
        if sheet != 'Site Info':
            ws = wb[sheet]
            get_tcn_sample_info(ws)




#process_file("C:\\Users\\fstev_000\\Documents\\T1 sample info.xlsx")
