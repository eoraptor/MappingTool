# functions for converting date and lat/long fields if incorrect

# take date format with full stops and replace
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

    return day + '/' + month + '/' + year


# convert lat/long in degrees, minutes to decimal format
def convert_lat_long(coord):
    if type(coord) is float:
        return coord
    else:
        result = "".join(i for i in coord if ord(i)<128)

        degrees = float(result[:result.index(' ')])
        minutes = float(result[result.rindex(' ')+1:])
        return degrees + (minutes/60)
