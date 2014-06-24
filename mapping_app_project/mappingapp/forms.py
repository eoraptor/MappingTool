from django import forms
from mappingapp.models import Core_Details, Photograph, Coordinates, Transect, Retreat_Zone, Sample, Photo_Of, Radiocarbon_Sample, Sample_Site, Location_Photo, OSL_Sample, TCN_Sample, Bearing_Inclination, Sample_Bearing_Inclination


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file:')


class CoreDetailsForm(forms.ModelForm):
    exposure_core = forms.IntegerField(help_text='Exposure Core', required=False)
    core_number = forms.IntegerField(help_text='Core Number', required=False)

    class Meta:
        model = Core_Details

class PhotographForm(forms.ModelForm):
    photo_time_stamp = forms.DateTimeField(help_text='Photo Time Stamp', required=False)
    photo_label = forms.CharField(max_length=128, help_text='Photo Label', required=False)

    class Meta:
        model = Photograph


class CoordinatesForm(forms.ModelForm):
    grid_reference = forms.CharField(max_length=12, help_text='Grid Reference', required=False)
    easting = forms.IntegerField(help_text='Easting', required=False)
    northing = forms.IntegerField(help_text='Northing', required=False)
    latitude = forms.FloatField(help_text='Latitude', required=False)
    longitude = forms.FloatField(help_text='Longitude', required=False)
    elevation = forms.CharField(max_length=50, help_text='Elevation', required=False)

    class Meta:
        model = Coordinates


class TransectForm(forms.ModelForm):
    transect_number = forms.CharField(max_length=3, help_text='Transect', required=False)

    class Meta:
        model = Transect


class RetreatForm(forms.ModelForm):
    zone_number = forms.IntegerField(help_text='Retreat Zone', required=False)

    class Meta:
        model = Retreat_Zone


class SampleForm(forms.ModelForm):
    code = forms.CharField(max_length=20, help_text='Sample Code', required=False)
    collection_date = forms.DateField(help_text='Collection Date', required=False)
    collector = forms.CharField(max_length=20, help_text='Collector(s)', required=False)
    notes = forms.CharField(max_length=200, help_text='Notes', required=False)
    age = forms.IntegerField(help_text='Sample Age', required=False)
    age_error = forms.IntegerField(help_text='Age Error', required=False)
    calendar_age = forms.IntegerField(help_text='Calendar Age', required=False)
    calendar_error = forms.IntegerField(help_text='Calendar Error', required=False)
    lab_code = forms.CharField(max_length=50, help_text='Lab Code', required=False)
    location = forms.ModelChoiceField(queryset=Coordinates.objects.all(),
                                      widget=forms.HiddenInput())
    site = forms.ModelChoiceField(queryset=Sample_Site.objects.all(),
                                         widget=forms.HiddenInput())

    class Meta:
        model = Sample


class RadiocarbonForm(forms.ModelForm):
    depth_below_SL = forms.IntegerField(help_text='Depth Below Sea Level', required=False)
    material = forms.CharField(max_length=45, help_text='Material', required=False)
    geological_setting = forms.CharField(max_length=45, help_text='Geological Setting', required=False)
    stratigraphic_position_depth = forms.IntegerField(help_text='Stratigraphic Position Depth', required=False)
    sample_weight = forms.IntegerField(help_text='Sample Weight', required=False)
    pot_contamination = forms.CharField(max_length=100, help_text='Potential Contamination', required=False)
    calibration_curve = forms.CharField(max_length=20, help_text='Calibration Curve', required=False)
    core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput())
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Radiocarbon_Sample



class SampleSiteForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Site Name', required=False)
    location = forms.CharField(max_length=50, help_text='Location', required=False)
    county = forms.CharField(max_length=50, help_text='County', required=False)
    geomorph_setting = forms.CharField(max_length=50, help_text='Geomorph Setting', required=False)
    type = forms.CharField(max_length=50, help_text='Type', required=False)
    photograph = forms.NullBooleanField(help_text='Photographs Taken?', required=False)
    notes = forms.CharField(max_length=300, help_text='Site Notes', required=False)
    transect = forms.ModelChoiceField(queryset=Transect.objects.all(), widget=forms.HiddenInput())
    coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Sample_Site


class OSLSampleForm(forms.ModelForm):
    stratigraphic_position = forms.CharField(max_length=20, help_text='Stratigraphic Position', required=False)
    lithofacies = forms.CharField(max_length=50, help_text='Lithofacies', required=False)
    burial_depth_history = forms.CharField(max_length=50, help_text='Burial Depth History', required=False)
    pot_perturb_water_table = forms.CharField(max_length=50, help_text='Potential Perturb of Water Table', required=False)
    pot_perturb_burial_depth = forms.CharField(max_length=50, help_text='Potential Perturb of Burial Depth', required=False)
    gamma_dose = forms.CharField(max_length=50, help_text='Gamma Dose', required=False)
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput())
    core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = OSL_Sample


class TCNForm(forms.ModelForm):
    quartz_content = forms.CharField(max_length=20, help_text='Quartz Content', required=False)
    sample_setting = forms.CharField(max_length=50, help_text='Sample Setting', required=False)
    sampled_material = forms.CharField(max_length=50, help_text='Sampled Material', required=False)
    boulder_dimensions = forms.CharField(max_length=50, help_text='Boulder Dimensions', required=False)
    sample_surface_strike_dip = forms.CharField(max_length=50, help_text='Sample Surface Strike Dip', required=False)
    sample_thickness = forms.CharField(max_length=50, help_text='Sample Thickness', required=False)
    grain_size = forms.IntegerField(help_text='Grain Size', required=False)
    lithology = forms.CharField(max_length=50, help_text='Lithology', required=False)
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = TCN_Sample


class BearingInclinationForm(forms.ModelForm):
    bearing = forms.IntegerField(help_text='Bearing', required=False)
    inclination = forms.IntegerField(help_text='Inclination', required=False)

    class Meta:
        model = Bearing_Inclination


class Sample_BI_Form(forms.ModelForm):
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput())
    bear_inc = forms.ModelChoiceField(queryset=Bearing_Inclination.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Sample_Bearing_Inclination


class Location_PhotoForm(forms.ModelForm):
    location_number = forms.ModelChoiceField(queryset=Sample_Site.objects.all(), widget=forms.HiddenInput())
    photo = forms.ModelChoiceField(queryset=Photograph.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Location_Photo

class PhotoOfForm(forms.ModelForm):
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput())
    photo = forms.ModelChoiceField(queryset=Photograph.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Photo_Of




