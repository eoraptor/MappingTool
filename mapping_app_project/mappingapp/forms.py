import datetime, time
from django import forms

from mappingapp.models import Core_Details, Photograph, Coordinates, Transect, Retreat_Zone, Sample, Photo_Of
from mappingapp.models import Radiocarbon_Sample, Sample_Site, Location_Photo, OSL_Sample, TCN_Sample
from mappingapp.models import Bearing_Inclination, Sample_Bearing_Inclination

# Form for Edit Sample code selection page
class SelectSampleForm(forms.Form):
    samp_code = forms.CharField(help_text='Enter sample code:', required=True,
                                  widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 30}))


# File upload page
class UploadFileForm(forms.Form):
    file = forms.FileField()


# Model: Core_Details.   Edit, Create New and Validate pages - OSL and C14 types only.
class CoreDetailsForm(forms.ModelForm):
    exposure_core = forms.CharField(help_text='Exposure/Core', required=False,
                              widget=forms.Textarea())
    core_number = forms.CharField(help_text='Core Number', required=False,
                              widget=forms.Textarea())

    class Meta:
        model = Core_Details


# Model: Photographs
class PhotographForm(forms.ModelForm):
    photo_time_stamp = forms.DateTimeField(help_text='Photo Time Stamp', required=False)
    photo_label = forms.CharField(max_length=128, help_text='Photo Label', required=False)

    class Meta:
        model = Photograph


# Model: Coordinates.   Edit, Create New and Validate pages.
class EditCoordinatesForm(forms.ModelForm):
    bng_ing = forms.CharField(help_text='BNG/ING', required=False,
                              widget=forms.Textarea(attrs={'class': 'noresize'}))
    grid_reference = forms.CharField(help_text='Grid Reference', required=False,
                                     widget=forms.Textarea(attrs={'class': 'noresize'}))
    easting = forms.IntegerField(help_text='Easting', required=False,
                                 widget=forms.Textarea(attrs={'class': 'noresizenumber'}))
    northing = forms.IntegerField(help_text='Northing', required=False,
                                  widget=forms.Textarea(attrs={'class': 'noresizenumber'}))
    latitude = forms.FloatField(help_text='Latitude', required=False,
                                widget=forms.Textarea(attrs={'class': 'noresizenumber'}))
    longitude = forms.FloatField(help_text='Longitude', required=False,
                                 widget=forms.Textarea(attrs={'class': 'noresizenumber'}))
    elevation = forms.CharField(help_text='Elevation', required=False,
                                widget=forms.Textarea(attrs={'class': 'noresize'}))

    class Meta:
        model = Coordinates


# Model: Transect.  Edit, Create New and Validate pages.
class TransectForm(forms.ModelForm):

    TRANSECT_CHOICES = (('', ''), ('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('T4', 'T4'), ('T5', 'T5'), ('T6', 'T6'),
                        ('T7', 'T7'), ('T8', 'T8'))

    transect_number = forms.ChoiceField(help_text='Transect', required=False, choices=TRANSECT_CHOICES)

    class Meta:
        model = Transect

    def save(self, commit=True):
        transect = super(TransectForm, self).save(commit=False)
        if transect.transect_number is not None:
            return Transect.objects.get_or_create(transect_number=transect.transect_number)[0]


# Model: Retreat Zone.  Edit, Create New and Validate pages.
class RetreatForm(forms.ModelForm):
    ZONE_CHOICES = (('1', ''), ('2', '1'), ('3', '2'), ('4', '3'), ('5', '4'), ('6', '5'), ('7', '6'), ('8', '7'))
    zone_number = forms.ChoiceField(help_text='Retreat', required=False, choices=ZONE_CHOICES)

    class Meta:
        model = Retreat_Zone

    def save(self, commit=True):
        retreat = super(RetreatForm, self).save(commit=False)
        if retreat.zone_number != '' and retreat.zone_number != '1' and retreat.zone_number is not None:
            return Retreat_Zone.objects.get_or_create(zone_number=int(retreat.zone_number)-1)[0]


# Model: Sample - Edit Sample page - all types.
class EditSampleForm(forms.ModelForm):
    sample_code = forms.CharField(help_text='Sample Code', required=True,
                                  widget=forms.Textarea(attrs={'class':'noresize'}))
    sample_location_name = forms.CharField(help_text='Sample Location Name', required=False,
                                           widget=forms.Textarea(attrs={'class':'noresize'}))
    collection_date = forms.DateField(help_text='Collection Date', input_formats=['%d/%m/%Y'], required=False,
                                      widget=forms.DateInput(format='%d/%m/%Y'))
    collector = forms.CharField(help_text='Collector(s)', required=False,
                                widget=forms.Textarea(attrs={'class':'noresize'}))
    sample_notes = forms.CharField(help_text='Notes', required=False,
                                   widget=forms.Textarea())
    dating_priority = forms.CharField(help_text='Dating Priority', required=False,
                                      widget=forms.Textarea(attrs={'class':'noresize'}))
    age = forms.IntegerField(help_text='Sample Age', required=False,
                             widget=forms.Textarea(attrs={'class':'noresizenumber'}))
    age_error = forms.IntegerField(help_text='Age Error', required=False,
                                   widget=forms.Textarea(attrs={'class':'noresizenumber'}))
    calendar_age = forms.IntegerField(help_text='Calendar Age', required=False,
                                      widget=forms.Textarea(attrs={'class':'noresizenumber'}))
    calendar_error = forms.IntegerField(help_text='Calendar Error', required=False,
                                        widget=forms.Textarea(attrs={'class':'noresizenumber'}))
    lab_code = forms.CharField(help_text='Lab Code', required=False,
                               widget=forms.Textarea(attrs={'class':'noresize'}))
    sample_coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(),
                                                widget=forms.HiddenInput(), required=False)
    samp_site = forms.ModelChoiceField(queryset=Sample_Site.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sample


# Model: Radiocarbon_Sample - Edit C14 Sample page.
class EditRadiocarbonForm(forms.ModelForm):
    depth_below_SL = forms.CharField(help_text='Depth', required=False,
                                     widget=forms.Textarea(attrs={'class':'noresize'}))
    material = forms.CharField(help_text='Material', required=False,
                               widget=forms.Textarea())
    geological_setting = forms.CharField(help_text='Geological Setting', required=False,
                                         widget=forms.Textarea())
    stratigraphic_position_depth = forms.CharField(help_text='Stratigraphic Position Depth', required=False,
                                                   widget=forms.Textarea())
    sample_weight = forms.CharField(help_text='Weight (g)', required=False,
                                    widget=forms.Textarea(attrs={'class':'noresize'}))
    pot_contamination = forms.CharField(help_text='Potential Contamination', required=False,
                                        widget=forms.Textarea())
    calibration_curve = forms.CharField(help_text='Calibration Curve', required=False,
                                        widget=forms.Textarea(attrs={'class':'noresize'}))
    c14_core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput(), required=False)
    c14_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Radiocarbon_Sample


# Model: Sample_Site - Edit Page.
class EditSampleSiteForm(forms.ModelForm):
    collected_by = forms.CharField(help_text='Collector(s)', required=False, widget=forms.Textarea())
    site_name = forms.CharField(help_text='Name', required=False, widget=forms.Textarea(attrs={'class': 'noresize'}))
    site_location = forms.CharField(help_text='Location', required=False, widget=forms.Textarea())
    county = forms.CharField(help_text='County', required=False, widget=forms.Textarea(attrs={'class': 'noresize'}))
    site_date = forms.DateField(help_text='Date', input_formats=['%d/%m/%Y'], required=False,
                                                widget=forms.DateInput(format='%d/%m/%Y'))
    operator = forms.CharField(help_text='Operator', required=False, widget=forms.Textarea())
    geomorph_setting = forms.CharField(help_text='Geomorph Setting', required=False, widget=forms.Textarea())
    sample_type_collected = forms.CharField(help_text='Sample Type', required=False,
                                            widget=forms.Textarea(attrs={'class': 'noresize'}))
    photos_taken = forms.NullBooleanField(help_text='Photos Taken', required=False)
    photographs = forms.CharField(help_text='Photograph Labels/Time Stamps', required=False, widget=forms.Textarea())
    site_notes = forms.CharField(help_text='Notes', required=False,widget=forms.Textarea())
    site_coordinates = forms.ModelChoiceField(queryset=Coordinates.objects.all(),
                                              widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Sample_Site


# Model: OSL_Sample.  Edit OSL Sample page.
class EditOSLSampleForm(forms.ModelForm):
    stratigraphic_position = forms.CharField(help_text='Stratigraphic Position', required=False,
                                             widget=forms.Textarea())
    lithofacies = forms.CharField(help_text='Lithofacies', required=False,
                                  widget=forms.Textarea(attrs={'class': 'noresize'}))
    burial_depth = forms.CharField(help_text='Burial Depth', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    lithology = forms.CharField(help_text='Lithology', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    gamma_spec = forms.CharField(help_text='Gamma Spec Model', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    equipment_number = forms.CharField(help_text='Equip No.', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    probe_serial_no = forms.CharField(help_text='Probe Serial Number', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    filename = forms.CharField(help_text='Filename', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    sample_time = forms.CharField(help_text='Time', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    sample_duration = forms.CharField(help_text='Duration', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    potassium = forms.CharField(help_text='Potassium', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    thorium = forms.CharField(help_text='Thorium', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    uranium = forms.CharField(help_text='Uranium', required=False,
                                           widget=forms.Textarea(attrs={'class': 'noresize'}))
    osl_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)
    osl_core = forms.ModelChoiceField(queryset=Core_Details.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = OSL_Sample


# Model: TCN_Sample. Validate, Edit & Create New Pages - TCN Samples only.
class EditTCNForm(forms.ModelForm):
    quartz_content = forms.CharField(help_text='Quartz Content', required=False,
                                     widget=forms.Textarea(attrs={'class':'noresize'}))
    sample_setting = forms.CharField(help_text='Sample Setting', required=False,
                                     widget=forms.Textarea())
    sampled_material = forms.CharField(help_text='Sampled Material', required=False,
                                       widget=forms.Textarea())
    boulder_dimensions = forms.CharField(help_text='Boulder Dimensions', required=False,
                                         widget=forms.Textarea(attrs={'class':'noresize'}))
    sample_surface_strike_dip = forms.CharField(help_text='Surface Strike/Dip', required=False,
                                                widget=forms.Textarea(attrs={'class':'noresize'}))
    sample_thickness = forms.CharField(help_text='Thickness', required=False,
                                       widget=forms.Textarea(attrs={'class':'noresize'}))
    grain_size = forms.CharField(help_text='Grain Size', required=False,
                                 widget=forms.Textarea(attrs={'class':'noresize'}))
    lithology = forms.CharField(help_text='Lithology', required=False,
                                widget=forms.Textarea())
    tcn_sample = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = TCN_Sample


# Model: Bearing_Inclination.  Validate, Edit & Create New Pages - Bearing & Inclination Modal.
class EditBIForm(forms.ModelForm):
    bearing = forms.IntegerField(help_text='Bearing', required=False,
                                 widget=forms.Textarea(attrs={'class':'bearinc', 'resize':'none'}))
    inclination = forms.IntegerField(help_text='Inclination',
                                     required=False, widget=forms.Textarea(attrs={'class':'bearinc', 'resize':'none'}))

    class Meta:
        model = Bearing_Inclination


# Model: Sample_Bearing_Inclination.  Validate, Edit & Create New Pages.
class Sample_BI_Form(forms.ModelForm):
    sample_with_bearing = forms.ModelChoiceField(queryset=TCN_Sample.objects.all(), widget=forms.HiddenInput(),
                                                 required=False)
    bear_inc = forms.ModelChoiceField(queryset=Bearing_Inclination.objects.all(), widget=forms.HiddenInput(),
                                      required=False)

    class Meta:
        model = Sample_Bearing_Inclination


# Model: Location_Photo
class Location_PhotoForm(forms.ModelForm):
    photo_site = forms.ModelChoiceField(queryset=Sample_Site.objects.all(), widget=forms.HiddenInput(), required=False)
    photo_ident = forms.ModelChoiceField(queryset=Photograph.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Location_Photo

# Model: Photo_Of
class PhotoOfForm(forms.ModelForm):
    sample_pictured = forms.ModelChoiceField(queryset=Sample.objects.all(), widget=forms.HiddenInput(), required=False)
    photo_idno = forms.ModelChoiceField(queryset=Photograph.objects.all(), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Photo_Of


# Form for Site selection on Validate, Edit & Create New Pages.
class ExistingSitesForm(forms.Form):
    sites = forms.ModelChoiceField(help_text="Select from existing sites:",
                                   queryset=Sample_Site.objects.values_list('site_name',
                                   flat=True).order_by('site_name'), required=False)


# Edit, Create New and Validate pages - used for submission of selected site name.
class HiddenSiteForm(forms.ModelForm):

    site_name = forms.CharField(max_length=500, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Sample_Site

    def save(self, commit=True):
        site = super(HiddenSiteForm, self).save(commit=False)
        site_choice = None
        try:
            site_choice = Sample_Site.objects.get(site_name=site.site_name)
        except:
            pass
        return site_choice


# forms for creating new instances which overwrite the default save method - do not save empty instances
class SampleForm(EditSampleForm):
    def save(self, commit=True):

        sample = None
        form_data = super(SampleForm, self).save(commit=False)
        sample_date = form_data.collection_date
        if sample_date is not None and not isinstance(sample_date, datetime.date):
             sample_date = time.strptime(sample_date, '%d/%m/%Y')

        try:
            sample = Sample.objects.get(sample_code=form_data.sample_code)
        except:
            pass

        if sample is None:
            sample = Sample(sample_code=form_data.sample_code,
                                           sample_location_name=form_data.sample_location_name,
                                           collection_date=sample_date,
                                           collector=form_data.collector, sample_notes=form_data.sample_notes,
                                           dating_priority=form_data.dating_priority, age=form_data.age,
                                           age_error=form_data.age_error, calendar_age=form_data.calendar_age,
                                           calendar_error=form_data.calendar_error, lab_code=form_data.lab_code)

        return sample


class CoordinatesForm(EditCoordinatesForm):
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


class SampleSiteForm(EditSampleSiteForm):
    def save(self, commit=True):
        site = super(SampleSiteForm, self).save(commit=False)
        if site.site_name == '' and site.site_location == '' and site.county == '' and\
            site.site_date == '' and site.operator == '' and site.geomorph_setting == '' and\
            site.sample_type_collected == '' and site.photos_taken == 1 and site.photographs == '' and\
            site.site_notes == '' and site.collected_by == '' and site.site_coordinates is None:
                return None
        else:
            site.save()


class TCNForm(EditTCNForm):
    def save(self, commit=True):
        tcn = super(TCNForm, self).save(commit=False)
        if tcn.quartz_content == '' and tcn.sample_setting == '' and tcn.sampled_material == '' and\
            tcn.boulder_dimensions == '' and tcn.sample_surface_strike_dip == '' and tcn.sample_thickness == '' and\
            tcn.grain_size == '' and tcn.lithology == '' and tcn.tcn_sample is None:
                return None
        else:
            return TCN_Sample.objects.create(quartz_content=tcn.quartz_content, sample_setting=tcn.sample_setting,
                                             sampled_material=tcn.sampled_material,
                                             boulder_dimensions=tcn.boulder_dimensions,
                                             sample_surface_strike_dip=tcn.sample_surface_strike_dip,
                                             sample_thickness=tcn.sample_thickness,
                                             grain_size=tcn.grain_size, lithology=tcn.lithology,
                                             tcn_sample=tcn.tcn_sample)


class OSLSampleForm(EditOSLSampleForm):
    def save(self, commit=True):
        osl = super(OSLSampleForm, self).save(commit=False)
        if osl.stratigraphic_position == '' and osl.lithofacies == '' and osl.burial_depth == '' and\
            osl.lithology == '' and osl.gamma_spec == '' and osl.equipment_number == '' and\
            osl.probe_serial_no == '' and osl.filename == '' and osl.sample_time == '' and\
            osl.sample_duration == '' and osl.potassium == '' and osl.thorium == '' and osl.uranium == '' and\
            osl.osl_sample is None and osl.osl_core is None:
            return None

        else:
            return OSL_Sample.objects.create(stratigraphic_position=osl.stratigraphic_position,
                                             lithofacies=osl.lithofacies, burial_depth=osl.burial_depth,
                                             lithology=osl.lithology, gamma_spec=osl.gamma_spec,
                                             equipment_number=osl.equipment_number,
                                             probe_serial_no=osl.probe_serial_no, filename=osl.filename,
                                             sample_time=osl.sample_time, sample_duration=osl.sample_duration,
                                             potassium=osl.potassium, thorium=osl.thorium, uranium=osl.uranium,
                                             osl_sample=osl.osl_sample, osl_core=osl.osl_core)


class RadiocarbonForm(EditRadiocarbonForm):
    def save(self, commit=True):
        c14 = super(RadiocarbonForm, self).save(commit=False)
        if c14.depth_below_SL == '' and c14.material == '' and c14.geological_setting == '' and\
            c14.stratigraphic_position_depth == '' and c14.sample_weight == '' and c14.pot_contamination == '' and\
            c14.calibration_curve == '' and c14.c14_core is None and c14.c14_sample is None:

            return None

        else:
            return Radiocarbon_Sample.objects.create(depth_below_SL=c14.depth_below_SL, material=c14.material,
                                                     geological_setting=c14.geological_setting,
                                                     stratigraphic_position_depth=c14.stratigraphic_position_depth,
                                                     sample_weight=c14.sample_weight,
                                                     pot_contamination=c14.pot_contamination,
                                                     calibration_curve=c14.calibration_curve, c14_core=c14.c14_core,
                                                     c14_sample=c14.c14_sample)


class BearingInclinationForm(EditBIForm):
    def save(self, commit=True):
        bearinc = super(BearingInclinationForm, self).save(commit=False)
        if bearinc.bearing is None and bearinc.inclination is None:
            return None
        else:
            return Bearing_Inclination.objects.create(bearing=bearinc.bearing, inclination=bearinc.inclination)



# Search Page forms
class MarkersForm(forms.Form):
    sample_codes = forms.CharField(max_length=5000, required=False, widget=forms.HiddenInput())


class SampleTypeForm(forms.Form):
    SAMPLE_CHOICES = ((None, ''), ('TCN', 'TCN'), ('OSL', 'OSL'), ('C14', 'C14'))

    types = forms.ChoiceField(help_text='Sample Type', required=False, choices=SAMPLE_CHOICES)


class AgeRangeForm(forms.Form):
    start = forms.IntegerField(help_text='From', required=False,
                               widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 9}))
    end = forms.IntegerField(help_text='To', required=False,
                             widget=forms.Textarea(attrs={'class':'noresize', 'rows': 1, 'cols': 9}))


class KeywordForm(forms.Form):
    string = forms.CharField(help_text='Keyword', required=False,
                             widget=forms.Textarea(attrs={'rows': 2, 'cols': 31}))

class CodeForm(forms.Form):
    code = forms.CharField(required=False,
                             widget=forms.Textarea(attrs={'rows': 2, 'cols': 31}))

