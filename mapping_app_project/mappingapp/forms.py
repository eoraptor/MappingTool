from django import forms
from mappingapp.models import Core_Details, Photograph, Coordinates, Transect, Retreat_Zone, Sample, Photo_Of, Radiocarbon_Sample, Sample_Site, Location_Photo, OSL_Sample, TCN_Sample, Bearing_Inclination, Sample_Bearing_Inclination


class UploadFileForm(forms.Form):
    file = forms.FileField()


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


class SampleCoordinatesForm(forms.ModelForm):
    bng_ing = forms.CharField(help_text='BNG/ING', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    grid_reference = forms.CharField(help_text='Grid Reference', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    easting = forms.IntegerField(help_text='Easting', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    northing = forms.IntegerField(help_text='Northing', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    latitude = forms.FloatField(help_text='Latitude', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    longitude = forms.FloatField(help_text='Longitude', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    elevation = forms.CharField(help_text='Elevation', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 4}))

    class Meta:
        model = Coordinates


class SiteCoordinatesForm(forms.ModelForm):
    bng_ing = forms.CharField(help_text='BNG/ING', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    grid_reference = forms.CharField(help_text='Grid Reference', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    easting = forms.IntegerField(help_text='Easting', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    northing = forms.IntegerField(help_text='Northing', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    latitude = forms.FloatField(help_text='Latitude', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    longitude = forms.FloatField(help_text='Longitude', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    elevation = forms.CharField(help_text='Elevation', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 4}))

    class Meta:
        model = Coordinates


class TransectForm(forms.ModelForm):
    transect_number = forms.CharField(help_text='Transect', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 2, 'resize':'none'}))

    class Meta:
        model = Transect


class RetreatForm(forms.ModelForm):
    zone_number = forms.CharField(help_text='Retreat Zone', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 2, 'resize':'none'}))

    class Meta:
        model = Retreat_Zone


class SampleForm(forms.ModelForm):
    sample_code = forms.CharField(help_text='Sample Code', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_location_name = forms.CharField(help_text='Sample Location Name', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 30}))
    collection_date = forms.DateField(help_text='Collection Date', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    collector = forms.CharField(help_text='Collector(s)', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 25}))
    sample_notes = forms.CharField(help_text='Notes', required=False, widget=forms.Textarea(attrs={'rows': 7, 'cols': 35}))
    dating_priority = forms.CharField(help_text='Dating Priority', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    age = forms.IntegerField(help_text='Sample Age', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    age_error = forms.IntegerField(help_text='Age Error', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    calendar_age = forms.IntegerField(help_text='Calendar Age', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    calendar_error = forms.IntegerField(help_text='Calendar Error', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    lab_code = forms.CharField(help_text='Lab Code', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(), widget=forms.HiddenInput(), required=False)
    samp_site = forms.ModelChoiceField(queryset=Sample_Site.objects.all(), widget=forms.HiddenInput(), required=False)

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
    c14_core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput(), required=False)
    c14_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Radiocarbon_Sample


class SampleSiteForm(forms.ModelForm):
    site_name = forms.CharField(help_text='Name', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    site_location = forms.CharField(help_text='Location', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    site_number = forms.CharField(help_text='Site Number', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 2, 'resize':'none'}))
    county = forms.CharField(help_text='County', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    site_date = forms.DateField(help_text='Date', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    operator = forms.CharField(help_text='Operator', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    geomorph_setting = forms.CharField(help_text='Geomorph Setting', required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 35}))
    sample_type_collected = forms.ChoiceField(help_text='Sample Type', required=False, choices=(('1', 'Select'), ('2', 'C14'), ('3', 'OSL'), ('4', 'TCN')))
    photos_taken = forms.NullBooleanField(help_text='Photos Taken', required=False)
    photographs = forms.CharField(help_text='Photograph Labels/Time Stamps', required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 35}))
    site_notes = forms.CharField(help_text='Notes', required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 35}))
    site_transect = forms.ModelChoiceField(queryset=Transect.objects.all(), widget=forms.HiddenInput(), required=False)
    site_retreat = forms.ModelChoiceField(queryset=Retreat_Zone.objects.all(), widget=forms.HiddenInput(), required=False)
    site_coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sample_Site


class OSLSampleForm(forms.ModelForm):
    stratigraphic_position = forms.CharField(max_length=20, help_text='Stratigraphic Position', required=False)
    lithofacies = forms.CharField(max_length=50, help_text='Lithofacies', required=False)
    burial_depth_history = forms.CharField(max_length=50, help_text='Burial Depth History', required=False)
    pot_perturb_water_table = forms.CharField(max_length=50, help_text='Potential Perturb of Water Table', required=False)
    pot_perturb_burial_depth = forms.CharField(max_length=50, help_text='Potential Perturb of Burial Depth', required=False)
    gamma_dose = forms.CharField(max_length=50, help_text='Gamma Dose', required=False)
    osl_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)
    osl_core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = OSL_Sample


class TCNForm(forms.ModelForm):
    quartz_content = forms.CharField(help_text='Quartz Content', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    sample_setting = forms.CharField(help_text='Sample Setting', required=False, widget=forms.Textarea(attrs={'rows':3, 'cols':35}))
    sampled_material = forms.CharField(help_text='Sampled Material', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows':1, 'cols':40}))
    boulder_dimensions = forms.CharField(help_text='Boulder Dimensions', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_surface_strike_dip = forms.CharField(help_text='Surface Strike/Dip', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_thickness = forms.CharField(help_text='Thickness', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    grain_size = forms.CharField(help_text='Grain Size', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    lithology = forms.CharField(help_text='Lithology', required=False, widget=forms.Textarea(attrs={'rows':3, 'cols':35}))
    tcn_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = TCN_Sample


class BearingInclinationForm(forms.ModelForm):
    bearing = forms.IntegerField(help_text='Bearing', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 2, 'resize':'none'}))
    inclination = forms.IntegerField(help_text='Inclination', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 2, 'resize':'none'}))

    class Meta:
        model = Bearing_Inclination


class Sample_BI_Form(forms.ModelForm):
    sample_with_bearing = forms.ModelChoiceField(queryset=TCN_Sample.objects.all(), widget=forms.HiddenInput(), required=False)
    bear_inc = forms.ModelChoiceField(queryset=Bearing_Inclination.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sample_Bearing_Inclination


class Location_PhotoForm(forms.ModelForm):
    photo_site = forms.ModelChoiceField(queryset=Sample_Site.objects.all(), widget=forms.HiddenInput(), required=False)
    photo_ident = forms.ModelChoiceField(queryset=Photograph.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Location_Photo

class PhotoOfForm(forms.ModelForm):
    sample_pictured = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)
    photo_idno = forms.ModelChoiceField(queryset=Photograph.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Photo_Of




