from openpyxl import load_workbook
from mappingapp.models import Sample_Site, Coordinates

def get_tcn_sample_info(wb, ws):
    sample_sheet = wb[ws]
    sample_date = sample_sheet['D1'].value
    sample_location = sample_sheet['D2'].value
    sample_code = sample_sheet['B3'].value
    bng_ing = sample_sheet['D3'].value
    sample_northing = sample_sheet['B4'].value
    sample_easting = sample_sheet['D4'].value
    transect = sample_sheet['F4'].value
    latitude = sample_sheet['B5'].value
    longitude = sample_sheet['D5'].value
    elevation = sample_sheet['F5'].value
    lithology = sample_sheet['B7'].value
    quartz = sample_sheet['F7'].value
    setting = sample_sheet['B8'].value
    material = sample_sheet['F8'].value
    boulder_dim = sample_sheet['B9'].value
    surface_strike = sample_sheet['F9'].value
    notes = sample_sheet['C11'].value
    thickness = sample_sheet['D24'].value
    grain_size = sample_sheet['F24'].value
    collector = sample_sheet['F31'].value
    bearing = get_bearing(sample_sheet)

    notes = notes.replace('\n', ' ')


def get_bearing(sample_sheet):
    data = []
    done = False
    start = 11
    while not done:
        start_str = str(start)
        bearing = sample_sheet['A' + start_str].value
        inclination = sample_sheet['B' + start_str].value

        if bearing is not None or inclination is not None:
            data.append((bearing, inclination))
            start += 1
        else:
            return data



def get_site_info(wb):
    site_sheet = wb["Site Info"]
    site_name = site_sheet['D1'].value
    site_location = site_sheet['B3'].value
    site_latitude = site_sheet['B4'].value
    site_longitude = site_sheet['D4'].value
    bng_ing = site_sheet['F4'].value
    site_northing = site_sheet['B5'].value
    site_easting = site_sheet['D5'].value
    site_elevation = site_sheet['B6'].value
    sample_date = site_sheet['E6'].value
    geomorph = site_sheet['B7'].value
    type = site_sheet['B8'].value
    collector = site_sheet['E8'].value
    photographs = site_sheet['B9'].value
    photo_labels = site_sheet['D9'].value
    site_notes = site_sheet['B10'].value

    photographs = photographs.lower()
    if photographs.startswith('y'):
        photographs = True
    else:
        photographs = False

    coords = Coordinates.objects.create_coordinates(bng_ing, None, site_easting, site_northing, site_latitude, site_longitude, site_elevation)
    site = Sample_Site.objects.create_site(site_name, site_location, None, geomorph, type, photographs, site_notes, None, None, coords)




def process_file(file_name):
    wb = load_workbook(file_name)
    sheet_names = wb.get_sheet_names()

    for sheet in sheet_names:
        if sheet == 'Site Info':
            get_site_info(wb)

        else:
            get_tcn_sample_info(wb, sheet)



def get_site_cell_positions(wb):
    ws = wb['Site Info']
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

    for k,v in positions.items():
        print k,v


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

    for k,v in positions.items():
        print k,v

#ws = wb['T1FOU02']
#get_tcn_cell_positions(ws)