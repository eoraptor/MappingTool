from django import forms
from mappingapp.models import Core_Details, Photograph, Coordinates, Transect, Retreat_Zone, Sample, Photo_Of, Radiocarbon_Sample, Sample_Site, Location_Photo, OSL_Sample, TCN_Sample, Bearing_Inclination, Sample_Bearing_Inclination


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file:')


class CoreDetailsForm(forms.ModelForm):
    exposure_core = forms.IntegerField(help_text='Exposure Core')
    core_number = forms.IntegerField(help_text='Core Number')

    class Meta:
        model = Core_Details

class PhotographForm(forms.ModelForm):
    photo_time_stamp = forms.DateTimeField(help_text='Photo Time Stamp')
    photo_label = forms.CharField(max_length=128, help_text='Photo Label')

    class Meta:
        model = Photograph


class CoordinatesForm(forms.ModelForm):
    grid_reference = forms.CharField(max_length=12, help_text='Grid Reference')
    easting = forms.IntegerField(help_text='Easting')
    northing = forms.IntegerField(help_text='Northing')
    latitude = forms.FloatField(help_text='Latitude')
    longitude = forms.FloatField(help_text='Longitude')
    elevation = forms.CharField(max_length=50, help_text='Elevation')

    class Meta:
        model = Coordinates


class TransectForm(forms.ModelForm):
    transect_number = forms.CharField(max_length=3, help_text='Transect')

    class Meta:
        model = Transect


class RetreatForm(forms.ModelForm):
    zone_number = forms.IntegerField(help_text='Retreat Zone')

    class Meta:
        model = Retreat_Zone


class SampleForm(forms.ModelForm):
    code = forms.CharField(max_length=20, help_text='Sample Code')
    collection_date = forms.DateField(help_text='Collection Date')
    collector = forms.CharField(max_length=20, help_text='Collector(s)')
    notes = forms.CharField(max_length=200, help_text='Notes')
    age = forms.IntegerField(help_text='Sample Age')
    age_error = forms.IntegerField(help_text='Age Error')
    calendar_age = forms.IntegerField(help_text='Calendar Age')
    calendar_error = forms.IntegerField(help_text='Calendar Error')
    lab_code = forms.CharField(max_length=50, help_text='Lab Code')
    location = forms.ModelChoiceField(queryset=Coordinates.objects.all(),
                                      widget=forms.HiddenInput())
    site = forms.ModelChoiceField(queryset=Sample_Site.objects.all(),
                                         widget=forms.HiddenInput())

    class Meta:
        model = Sample


class RadiocarbonForm(forms.ModelForm):
    depth_below_SL = forms.IntegerField(help_text='Depth Below Sea Level')
    material = forms.CharField(max_length=45, help_text='Material')
    geological_setting = forms.CharField(max_length=45, help_text='Geological Setting')
    stratigraphic_position_depth = forms.IntegerField(help_text='Stratigraphic Position Depth')
    sample_weight = forms.IntegerField(help_text='Sample Weight')
    pot_contamination = forms.CharField(max_length=100, help_text='Potential Contamination')
    calibration_curve = forms.CharField(max_length=20, help_text='Calibration Curve')
    core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput())
    sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Radiocarbon_Sample



class SampleSiteForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Site Name')
    number

