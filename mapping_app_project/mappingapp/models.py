from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


class CoreDetailsManager(models.Manager):
    def create_core_details(self, exposure, number):
        core_details = self.create(exposure_core=exposure, core_number=number)
        return core_details

class Core_Details(models.Model):
    exposure_core = models.CharField(max_length=255, null=True, blank=True)
    core_number = models.CharField(max_length=255, null=True, blank=True)

    objects = CoreDetailsManager()

    def __unicode__(self):
        return self.core_number


class PhotographManager(models.Manager):
    def create_photograph(self, time, label):
        photo = self.create(photo_time_stamp=time,photo_label=label)
        return photo

class Photograph(models.Model):
    photo_time_stamp = models.DateTimeField(null=True, blank=True)
    photo_label = models.CharField(max_length=128, null=True, blank=True)

    objects = PhotographManager()

    def __unicode__(self):
        return self.photo_label



class CoordinatesManager(models.Manager):
    def create_coordinates(self, bng_ing, grid_ref, east, north, lat, long, ele):
        coordinates = self.create(bng_ing=bng_ing, grid_reference=grid_ref, easting=east,
                                  northing=north, latitude=lat, longitude=long, elevation=ele)
        return coordinates

class Coordinates(models.Model):
    bng_ing = models.CharField(max_length=255, null=True, blank=True)
    grid_reference = models.CharField(max_length=20, null=True, blank=True)
    easting = models.IntegerField(null=True, blank=True)
    northing = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    elevation = models.CharField(max_length=255, null=True, blank=True)

    objects = CoordinatesManager()

    def __unicode__(self):
        return self.grid_reference

    def as_json(self):
        return dict(input_lat=self.latitude, input_long=self.longitude)


class TransectManager(models.Manager):
    def create_transect(self, transect_number):
        transect = self.create(transect_number=transect_number)
        return transect


class Transect(models.Model):

    TRANSECT_CHOICES = (('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('T4', 'T4'), ('T5', 'T5'), ('T6', 'T6'),
                        ('T7', 'T7'), ('T8', 'T8'))

    transect_number = models.CharField(max_length=2, choices=TRANSECT_CHOICES,
                                       null=True, blank=True)

    objects = TransectManager()

    def __unicode__(self):
        return self.transect_number



class RetreatZoneManager(models.Manager):
    def create_retreat_zone(self, zone_number):
        retreat = self.create(zone_number=zone_number)
        return retreat

class Retreat_Zone(models.Model):
    zone_number = models.CharField(max_length=3, null=True, blank=True)

    objects = RetreatZoneManager()

    def __unicode__(self):
        return self.zone_number



class SampleManager(models.Manager):
    def create_sample(self, code, location, date, collector, notes, priority, age, age_error,
                      cal_age, cal_error, lab_code, coords, site, transect, retreat):
        sample = self.create(sample_code=code, sample_location_name=location, collection_date=date, collector=collector,
                             sample_notes=notes, dating_priority=priority, age=age, age_error=age_error,
                             calendar_age=cal_age, calendar_error=cal_error, lab_code=lab_code,
                             sample_coordinates=coords, sample_site=site, transect=transect, retreat=retreat)
        return sample

class Sample(models.Model):
    sample_code = models.CharField(max_length=100, null=True, blank=True)
    sample_location_name = models.CharField(max_length=255, null=True, blank=True)
    collection_date = models.DateField(null=True, blank=True)
    collector = models.CharField(max_length=255, null=True, blank=True)
    sample_notes = models.TextField(null=True, blank=True)
    dating_priority = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    age_error = models.IntegerField(null=True, blank=True)
    calendar_age = models.IntegerField(null=True, blank=True)
    calendar_error = models.IntegerField(null=True, blank=True)
    lab_code = models.CharField(max_length=255, null=True, blank=True)
    sample_coordinates = models.ForeignKey(Coordinates, null=True, blank=True)
    sample_site = models.ForeignKey('Sample_Site', null=True, blank=True)
    transect = models.ForeignKey(Transect, null=True, blank=True)
    retreat = models.ForeignKey(Retreat_Zone, null=True, blank=True)


    objects = SampleManager()

    def __unicode__(self):
        return self.sample_code





class PhotoOfManager(models.Manager):
    def create_photo_of(self, sample, id):
        photo_of = self.create(sample_pictured=sample, photo_idno=id)
        return photo_of


class Photo_Of(models.Model):
    sample_pictured = models.ForeignKey(Sample, null=True, blank=True)
    photo_idno = models.ForeignKey(Photograph, null=True, blank=True)

    objects = PhotoOfManager()

    def __unicode__(self):
        return self.sample_pictured


class RadiocarbonManager(models.Manager):
    def create_radiocarbon(self, depth, material, setting, position, weight, contam,
                           cal_curve, core, sample):
        radiocarbon = self.create(depth_below_SL=depth, material=material, geological_setting=setting,
                                  stratigraphic_position_depth=position, sample_weight=weight,
                                  pot_contamination=contam, calibration_curve=cal_curve, c14_core=core,
                                  c14_sample=sample)
        return radiocarbon


class Radiocarbon_Sample(models.Model):
    depth_below_SL = models.CharField(max_length=255, null=True, blank=True)
    material = models.CharField(max_length=1000, null=True, blank=True)
    geological_setting = models.CharField(max_length=1500, null=True, blank=True)
    stratigraphic_position_depth = models.CharField(max_length=255, null=True, blank=True)
    sample_weight = models.CharField(max_length=255, null=True, blank=True)
    pot_contamination = models.CharField(max_length=1500, null=True, blank=True)
    calibration_curve = models.CharField(max_length=255, null=True, blank=True)
    c14_core = models.ForeignKey(Core_Details, null=True, blank=True)
    c14_sample = models.ForeignKey(Sample, null=True, blank=True)

    objects = RadiocarbonManager()

    def __unicode__(self):
        return Sample.sample_code



class SiteManager(models.Manager):
    def create_site(self, collected, name, location, county, date, operator, setting, type, photos_taken, photographs, notes,
                    coords):
        site = self.create(collected_by=collected, site_name=name, site_location=location, county=county,
                           site_date=date, operator=operator, geomorph_setting=setting, sample_type_collected=type,
                           photos_taken=photos_taken, photographs=photographs, site_notes=notes, site_coordinates=coords)
        return site


class Sample_Site(models.Model):
    collected_by = models.CharField(max_length=255, null=True, blank=True)
    site_name = models.CharField(max_length=255, null=True, blank=True)
    site_location = models.CharField(max_length=255, null=True, blank=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    site_date = models.DateField(null=True, blank=True)
    operator = models.CharField(max_length=255, null=True, blank=True)
    geomorph_setting = models.TextField(null=True, blank=True)
    sample_type_collected = models.CharField(max_length=255, null=True, blank=True)
    photos_taken = models.NullBooleanField(null=True, blank=True)
    photographs = models.CharField(max_length=255, null=True, blank=True)
    site_notes = models.TextField(null=True, blank=True)
    site_coordinates = models.ForeignKey(Coordinates, null=True, blank=True)

    objects = SiteManager()

    def __unicode__(self):
        return self.site_name


class LocationPhotoManager(models.Manager):
    def create_location_manager(self, site, id):
        loc_photo = self.create(photo_site=site, photo_ident=id)

        return loc_photo

class Location_Photo(models.Model):
    photo_site = models.ForeignKey(Sample_Site, null=True, blank=True)
    photo_ident = models.ForeignKey(Photograph, null=True, blank=True)

    objects = LocationPhotoManager()

    def __unicode__(self):
        return self.photo_ident



class OSLManager(models.Manager):
    def create_osl(self, position, lithofacies, depth, lithology, gamma, equip_no, probe_no, file, time, duration,
                   potassium, thorium, uranium, sample, core):
        osl = self.create(stratigraphic_postion=position, lithofacies=lithofacies, burial_depth=depth,
                          lithology=lithology, gamma_spec=gamma, equipment_number=equip_no, probe_serial_no=probe_no,
                          filename=file, sample_time=time, sample_duration=duration, potassium=potassium,
                          thorium=thorium, uranium=uranium, osl_sample=sample, osl_core=core)
        return osl


class OSL_Sample(models.Model):
    stratigraphic_position = models.CharField(max_length=255, null=True, blank=True)
    lithofacies = models.CharField(max_length=255, null=True, blank=True)
    burial_depth = models.CharField(max_length=255, null=True, blank=True)
    lithology = models.CharField(max_length=255, null=True, blank=True)
    gamma_spec = models.CharField(max_length=255, null=True, blank=True)
    equipment_number = models.CharField(max_length=255, null=True, blank=True)
    probe_serial_no = models.CharField(max_length=255, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)
    sample_time = models.CharField(max_length=255, null=True, blank=True)
    sample_duration = models.CharField(max_length=255, null=True, blank=True)
    potassium = models.CharField(max_length=255, null=True, blank=True)
    thorium = models.CharField(max_length=255, null=True, blank=True)
    uranium = models.CharField(max_length=255, null=True, blank=True)
    osl_sample = models.ForeignKey(Sample, null=True, blank=True)
    osl_core = models.ForeignKey(Core_Details, null=True, blank=True)

    objects = OSLManager()

    def __unicode__(self):
        return Sample.sample_code



class TCNManager(models.Manager):
    def create_tcn(self, quartz, setting, material, boulder, strike, thickness, grain, litho, sample):
        tcn = self.create(quartz_content=quartz, sample_setting=setting, sampled_material=material,
                          boulder_dimensions=boulder, sample_surface_strike_dip=strike,
                          sample_thickness=thickness, grain_size=grain, lithology=litho,
                          tcn_sample=sample)
        return tcn

class TCN_Sample(models.Model):
    quartz_content = models.CharField(max_length=255, null=True, blank=True)
    sample_setting = models.CharField(max_length=255, null=True, blank=True)
    sampled_material = models.CharField(max_length=255, null=True, blank=True)
    boulder_dimensions = models.CharField(max_length=255, null=True, blank=True)
    sample_surface_strike_dip = models.CharField(max_length=255, null=True, blank=True)
    sample_thickness = models.CharField(max_length=255, null=True, blank=True)
    grain_size = models.CharField(max_length=255, null=True, blank=True)
    lithology = models.CharField(max_length=255, null=True, blank=True)
    tcn_sample = models.ForeignKey(Sample, null=True, blank=True)

    objects = TCNManager()

    def __unicode__(self):
        return Sample.sample_code



class BIManager(models.Manager):
    def create_bearing_inclination(self, bearing, inc):
        bi = self.create(bearing=bearing, inclination=inc)
        return bi


class Bearing_Inclination(models.Model):
    bearing = models.IntegerField(null=True, blank=True)
    inclination = models.IntegerField(null=True, blank=True)

    objects = BIManager()

    def __unicode__(self):
        return self.bearing



class SampleBIManager(models.Manager):
    def create_sampleBI(self, sample, bearing):
        samplebi = self.create(sample_with_bearing=sample, bear_inc=bearing)

        return samplebi

class Sample_Bearing_Inclination(models.Model):
    sample_with_bearing = models.ForeignKey(TCN_Sample, null=True, blank=True)
    bear_inc = models.ForeignKey(Bearing_Inclination, null=True, blank=True)

    objects = SampleBIManager()

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
