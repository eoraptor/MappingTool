from django.db import models


class Core_Details(models.Model):
    exposure_core = models.IntegerField()
    core_number = models.IntegerField()

    def __unicode__(self):
        return self.core_number



class Photograph(models.Model):
    photo_time_stamp = models.DateTimeField()
    photo_label = models.CharField(max_length=128)

    def __unicode__(self):
        return self.photo_label



class Coordinates(models.Model):
    grid_reference = models.CharField(max_length=12)
    easting = models.IntegerField()
    northing = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.CharField(max_length=50)
    site_id = models.IntegerField()

    def __unicode__(self):
        return self.coordinate_id



class Transect(models.Model):
    transect_number = models.CharField(max_length=3)

    def __unicode__(self):
        return self.transect_number



class Retreat_Zone(models.Model):
    zone_number = models.IntegerField()

    def __unicode__(self):
        return self.zone_number



class Sample(models.Model):
    code = models.CharField(max_length=20)
    collection_date = models.DateField()
    collector = models.CharField(max_length=20)
    notes = models.CharField(max_length=200)
    age = models.IntegerField()
    age_error = models.IntegerField()
    calendar_age = models.IntegerField()
    calendar_error = models.IntegerField()
    lab_code = models.CharField(max_length=50)
    location = models.ForeignKey(Coordinates)
    site = models.ForeignKey('Sample_Site')

    def __unicode__(self):
        return self.code



class Photo_Of(models.Model):
    sample = models.ForeignKey(Sample)
    photo = models.ForeignKey(Photograph)

    def __unicode__(self):
        return self.sample



class Radiocarbon_Sample(models.Model):
    depth_below_SL = models.IntegerField()
    material = models.CharField(max_length=45)
    geological_setting = models.CharField(max_length=45)
    stratigraphic_position_depth = models.IntegerField()
    sample_weight = models.IntegerField()
    pot_contamination = models.CharField(max_length=100)
    calibration_curve = models.CharField(max_length=20)
    core = models.ForeignKey(Core_Details)
    sample = models.ForeignKey(Sample)

    def __unicode__(self):
        return self.sample



class Sample_Site(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    location = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    geomorph_setting = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    photograph = models.NullBooleanField()
    notes = models.CharField(max_length=300)
    transect = models.ForeignKey(Transect)
    retreat = models.ForeignKey(Retreat_Zone)
    coordinates = models.ForeignKey(Coordinates)

    def __unicode__(self):
        return self.name



class Location_Photo(models.Model):
    location_number = models.ForeignKey(Sample_Site)
    photo = models.ForeignKey(Photograph)

    def __unicode__(self):
        return self.photo




class OSL_Sample(models.Model):
    stratigraphic_position = models.CharField(max_length=20)
    lithofacies = models.CharField(max_length=50)
    burial_depth_history = models.CharField(max_length=50)
    pot_perturb_water_table = models.CharField(max_length=50)
    pot_perturb_burial_depth = models.CharField(max_length=50)
    gamma_dose = models.CharField(max_length=50)
    sample = models.ForeignKey(Sample)
    core = models.ForeignKey(Core_Details)

    def __unicode__(self):
        return self.sample_id




class TCN_Sample(models.Model):
    quartz_content = models.CharField(max_length=20)
    sample_setting = models.CharField(max_length=50)
    sampled_material = models.CharField(max_length=50)
    boulder_dimensions = models.CharField(max_length=50)
    sample_surface_strike_dip = models.CharField(max_length=50)
    sample_thickness = models.CharField(max_length=50)
    grain_size = models.IntegerField()
    lithology = models.CharField(max_length=50)
    sample = models.ForeignKey(Sample)

    def __unicode__(self):
        return self.sample



class Bearing_Inclination(models.Model):
    bearing = models.IntegerField()
    inclination = models.IntegerField()

    def __unicode__(self):
        return self.bearing



class Sample_Bearing_Inclination(models.Model):
    sample = models.ForeignKey(TCN_Sample)
    bear_inc = models.ForeignKey(Bearing_Inclination)

    def __unicode__(self):
        return self.bear_inc