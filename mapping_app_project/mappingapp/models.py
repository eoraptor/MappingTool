from django.db import models
from django.contrib.auth.models import User


class Core_Details(models.Model):
    exposure_core = models.IntegerField(null=True, blank=True)
    core_number = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.core_number



class Photograph(models.Model):
    photo_time_stamp = models.DateTimeField(null=True, blank=True)
    photo_label = models.CharField(max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.photo_label



class Coordinates(models.Model):
    grid_reference = models.CharField(max_length=12, null=True, blank=True)
    easting = models.IntegerField(null=True, blank=True)
    northing = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    elevation = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.coordinate_id



class Transect(models.Model):
    transect_number = models.CharField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return self.transect_number



class Retreat_Zone(models.Model):
    zone_number = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.zone_number



class Sample(models.Model):
    code = models.CharField(max_length=20, null=True, blank=True)
    collection_date = models.DateField(null=True, blank=True)
    collector = models.CharField(max_length=20, null=True, blank=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    age_error = models.IntegerField(null=True, blank=True)
    calendar_age = models.IntegerField(null=True, blank=True)
    calendar_error = models.IntegerField(null=True, blank=True)
    lab_code = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey(Coordinates, null=True, blank=True)
    site = models.ForeignKey('Sample_Site', null=True, blank=True)

    def __unicode__(self):
        return self.code



class Photo_Of(models.Model):
    sample = models.ForeignKey(Sample, null=True, blank=True)
    photo = models.ForeignKey(Photograph, null=True, blank=True)

    def __unicode__(self):
        return self.sample



class Radiocarbon_Sample(models.Model):
    depth_below_SL = models.IntegerField(null=True, blank=True)
    material = models.CharField(max_length=45, null=True, blank=True)
    geological_setting = models.CharField(max_length=45, null=True, blank=True)
    stratigraphic_position_depth = models.IntegerField(null=True, blank=True)
    sample_weight = models.IntegerField(null=True, blank=True)
    pot_contamination = models.CharField(max_length=100, null=True, blank=True)
    calibration_curve = models.CharField(max_length=20, null=True, blank=True)
    core = models.ForeignKey(Core_Details, null=True, blank=True)
    sample = models.ForeignKey(Sample, null=True, blank=True)

    def __unicode__(self):
        return self.sample



class Sample_Site(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    geomorph_setting = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    photograph = models.NullBooleanField(null=True, blank=True)
    notes = models.CharField(max_length=300, null=True, blank=True)
    transect = models.ForeignKey(Transect, null=True, blank=True)
    retreat = models.ForeignKey(Retreat_Zone, null=True, blank=True)
    coordinates = models.ForeignKey(Coordinates, null=True, blank=True)

    def __unicode__(self):
        return self.name



class Location_Photo(models.Model):
    location_number = models.ForeignKey(Sample_Site, null=True, blank=True)
    photo = models.ForeignKey(Photograph, null=True, blank=True)

    def __unicode__(self):
        return self.photo




class OSL_Sample(models.Model):
    stratigraphic_position = models.CharField(max_length=20, null=True, blank=True)
    lithofacies = models.CharField(max_length=50, null=True, blank=True)
    burial_depth_history = models.CharField(max_length=50, null=True, blank=True)
    pot_perturb_water_table = models.CharField(max_length=50, null=True, blank=True)
    pot_perturb_burial_depth = models.CharField(max_length=50, null=True, blank=True)
    gamma_dose = models.CharField(max_length=50, null=True, blank=True)
    sample = models.ForeignKey(Sample, null=True, blank=True)
    core = models.ForeignKey(Core_Details, null=True, blank=True)

    def __unicode__(self):
        return self.sample_id




class TCN_Sample(models.Model):
    quartz_content = models.CharField(max_length=20, null=True, blank=True)
    sample_setting = models.CharField(max_length=50, null=True, blank=True)
    sampled_material = models.CharField(max_length=50, null=True, blank=True)
    boulder_dimensions = models.CharField(max_length=50, null=True, blank=True)
    sample_surface_strike_dip = models.CharField(max_length=50, null=True, blank=True)
    sample_thickness = models.CharField(max_length=50, null=True, blank=True)
    grain_size = models.IntegerField(null=True, blank=True)
    lithology = models.CharField(max_length=50, null=True, blank=True)
    sample = models.ForeignKey(Sample, null=True, blank=True)

    def __unicode__(self):
        return self.sample



class Bearing_Inclination(models.Model):
    bearing = models.IntegerField(null=True, blank=True)
    inclination = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.bearing



class Sample_Bearing_Inclination(models.Model):
    sample = models.ForeignKey(TCN_Sample, null=True, blank=True)
    bear_inc = models.ForeignKey(Bearing_Inclination, null=True, blank=True)

    def __unicode__(self):
        return self.bear_inc


class UserProfile(models.Model):
    # link UserProfile to a User model
    user = models.OneToOneField(User)

    # additional custom attributes
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
