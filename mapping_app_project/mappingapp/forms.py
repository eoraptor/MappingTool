from django import forms
from django.utils.safestring import mark_safe
from mappingapp.models import Core_Details, Photograph, Coordinates, Transect, Retreat_Zone, Sample, Photo_Of
from mappingapp.models import Radiocarbon_Sample, Sample_Site, Location_Photo, OSL_Sample, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination

class SelectSampleForm(forms.Form):
    sample_code = forms.CharField(help_text='Enter sample code:', required=True)


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


class CoordinatesForm(forms.ModelForm):
    bng_ing = forms.CharField(help_text='BNG/ING', required=False,
                              widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 20}))
    grid_reference = forms.CharField(help_text='Grid Reference', required=False,
                                     widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    easting = forms.IntegerField(help_text='Easting', required=False,
                                 widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    northing = forms.IntegerField(help_text='Northing', required=False,
                                  widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    latitude = forms.FloatField(help_text='Latitude', required=False,
                                widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    longitude = forms.FloatField(help_text='Longitude', required=False,
                                 widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    elevation = forms.CharField(help_text='Elevation', required=False,
                                widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 4}))

    class Meta:
        model = Coordinates

    def save(self, commit=True):
        coords = super(CoordinatesForm, self).save(commit=False)
        if coords.bng_ing == '' and coords.grid_reference == '' and\
            coords.easting is None and coords.northing is None and\
            coords.latitude is None and coords.longitude is None and coords.elevation == '':
            return None
        else:

            return Coordinates.objects.create(bng_ing=coords.bng_ing, grid_reference=coords.grid_reference,
                                              easting=coords.easting, northing=coords.northing,
                                              latitude=coords.latitude, longitude=coords.longitude,
                                              elevation=coords.elevation)


class TransectForm(forms.ModelForm):

    TRANSECT_CHOICES = (('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('T4', 'T4'), ('T5', 'T5'), ('T6', 'T6'),
                        ('T7', 'T7'), ('T8', 'T8'))
    transect_number = forms.ChoiceField(help_text='Transect', required=False, choices=TRANSECT_CHOICES)

    class Meta:
        model = Transect

    def save(self, commit=True):
        transect = super(TransectForm, self).save(commit=False)
        if transect.transect_number != '':
            return Transect.objects.get_or_create(transect_number=transect.transect_number)[0]


class RetreatForm(forms.ModelForm):
    ZONE_CHOICES = (('1', ''), ('2', '1'), ('3', '2'), ('4', '3'), ('5', '4'), ('6', '5'), ('7', '6'), ('8', '7'))
    zone_number = forms.ChoiceField(help_text='Retreat Zone', required=False, choices=ZONE_CHOICES)

    class Meta:
        model = Retreat_Zone

    def save(self, commit=True):
        retreat = super(RetreatForm, self).save(commit=False)
        if retreat.zone_number != '':
            return Retreat_Zone.objects.get_or_create(zone_number=retreat.zone_number)[0]


class SampleForm(forms.ModelForm):
    sample_code = forms.CharField(help_text='Sample Code', required=True,
                                  widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_location_name = forms.CharField(help_text='Sample Location Name', required=False,
                                           widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 45}))
    collection_date = forms.DateField(help_text='Collection Date', required=False,
                                      widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    collector = forms.CharField(help_text='Collector(s)', required=False,
                                widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 25}))
    sample_notes = forms.CharField(help_text='Notes', required=False,
                                   widget=forms.Textarea(attrs={'rows': 4, 'cols': 69}))
    dating_priority = forms.CharField(help_text='Dating Priority', required=False,
                                      widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    age = forms.IntegerField(help_text='Sample Age', required=False,
                             widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    age_error = forms.IntegerField(help_text='Age Error', required=False,
                                   widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    calendar_age = forms.IntegerField(help_text='Calendar Age', required=False,
                                      widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    calendar_error = forms.IntegerField(help_text='Calendar Error', required=False,
                                        widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    lab_code = forms.CharField(help_text='Lab Code', required=False,
                               widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(),
                                                widget=forms.HiddenInput(), required=False)
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
    site_name = forms.CharField(help_text='Name', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 35}))
    site_location = forms.CharField(help_text='Location', required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 44}))
    county = forms.CharField(help_text='County', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 20}))
    site_date = forms.DateField(help_text='Date', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    operator = forms.CharField(help_text='Operator', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 20}))
    geomorph_setting = forms.CharField(help_text='Geomorph Setting', required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}))
    sample_type_collected = forms.CharField(help_text='Sample Type', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 30}))
    photos_taken = forms.NullBooleanField(help_text='Photos Taken', required=False)
    photographs = forms.CharField(help_text='Photograph Labels/Time Stamps', required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 44}))
    site_notes = forms.CharField(help_text='Notes', required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 100}))
    site_coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sample_Site

    def save(self, commit=True):
        site = super(SampleSiteForm, self).save(commit=False)
        if site.site_name == '' and site.site_location == '' and site.county == '' and\
            site.site_date == '' and site.operator == '' and site.geomorph_setting == '' and\
            site.sample_type_collected == '' and site.photos_taken == 1 and site.photographs == '' and\
            site.site_notes == '' and site.site_coordinates is None:
                return None
        else:
            site.save()




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
    quartz_content = forms.CharField(help_text='Quartz Content', required=False,
                                     widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    sample_setting = forms.CharField(help_text='Sample Setting', required=False,
                                     widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    sampled_material = forms.CharField(help_text='Sampled Material', required=False,
                                       widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    boulder_dimensions = forms.CharField(help_text='Boulder Dimensions', required=False,
                                         widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 14}))
    sample_surface_strike_dip = forms.CharField(help_text='Surface Strike/Dip', required=False,
                                                widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 8}))
    sample_thickness = forms.CharField(help_text='Thickness', required=False,
                                       widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 5}))
    grain_size = forms.CharField(help_text='Grain Size', required=False,
                                 widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 10}))
    lithology = forms.CharField(help_text='Lithology', required=False,
                                widget=forms.Textarea(attrs={'rows':3, 'cols':40}))
    tcn_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = TCN_Sample

    def save(self, commit=True):
        tcn = super(TCNForm, self).save(commit=False)
        if tcn.quartz_content == '' and tcn.sample_setting == '' and tcn.sampled_material == '' and\
            tcn.boulder_dimensions == '' and tcn.sample_surface_strike_dip == '' and tcn.sample_thickness == '' and\
            tcn.grain_size == '' and tcn.lithology == '' and tcn.tcn_sample is None:
                return None
        else:
            tcn.save()



class BearingInclinationForm(forms.ModelForm):
    bearing = forms.IntegerField(help_text='Bearing', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 1, 'resize':'none'}))
    inclination = forms.IntegerField(help_text='Inclination', required=False, widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 1, 'resize':'none'}))

    class Meta:
        model = Bearing_Inclination

    def save(self, commit=True):
        bearinc = super(BearingInclinationForm, self).save(commit=False)
        if bearinc.bearing is None and bearinc.inclination is None:
            return None
        else:
            bearinc.save()


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




class ExistingSitesForm(forms.Form):

    sites = forms.ModelChoiceField(help_text="Select from existing sites:",
                                   queryset=Sample_Site.objects.values_list('site_name', flat=True), required=False)



class HiddenSiteForm(forms.ModelForm):

    site_name = forms.CharField(max_length=500, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Sample_Site


    def save(self, commit=True):
        site = super(HiddenSiteForm, self).save(commit=False)
        if site.site_name is None:
            return None
        else:
            site_choice = Sample_Site.objects.get(site_name=site.site_name)
            return site_choice






