from datetime import datetime
from django.db import models

class myData(models.Model):
    debug_mode = models.BooleanField(default=False)
    nmod_nav_ok = models.BooleanField(default=False)
    nmod_gps_ok = models.BooleanField(default=False)
    set_polaris_ok = models.BooleanField(default=False)
    gps_latitude = models.FloatField(default=0)
    gps_longitude = models.FloatField(default=0)
    gps_altitude = models.FloatField(default=0)
    gps_time = models.DateTimeField(default=datetime.fromisoformat('1970-01-01'))
    # Data for motors not copied

    def __str__(self):
        return '%s %s %s' % (self.debug_mode, self.nmod_nav_ok, self.nmod_gps_ok)

class myStatus(models.Model):
    observe = models.CharField(default='None', max_length=50) # don't know what goes here…
    read_sensor_data = models.BooleanField(default=False)

# 3 star alignment data
class myTarget(models.Model):
    target = models.CharField(default='None', max_length=25) # was None originally, which doesn't work in a database
    star1 = models.CharField(default='Star1', max_length=25)
    star2 = models.CharField(default='Star2', max_length=25)
    star3 = models.CharField(default='Star3', max_length=25)
    star1_ok = models.CharField(default='incomplete', max_length=25)
    star2_ok = models.CharField(default='incomplete', max_length=25)
    star3_ok = models.CharField(default='incomplete', max_length=25)

class myCalc(models.Model):
    LMST = models.FloatField(default=0)
    ra_sv = models.FloatField(default=0)        # start value
    ra_sp = models.FloatField(default=0)        # set point
    ra_deg = models.FloatField(default=0)        # result of motor_ra.get_degree()
    ra_av = models.FloatField(default=0)        # actual value steps
    ra_sp_steps = models.FloatField(default=0)  # set point steps
    ra_dir = models.CharField(default='None', max_length=10)    # direction
    dec_sv = models.FloatField(default=0)  # start value
    dec_sp = models.FloatField(default=0)
    dec_deg = models.FloatField(default=0)        # result of motor_dec.get_degree()
    dec_av = models.FloatField(default=0)
    dec_sp_steps = models.FloatField(default=0)
    dec_dir = models.CharField(default='None', max_length=10)
    
class stargate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(primary_key=True, default='sg1', max_length=10)
    mydata = models.ForeignKey('myData', on_delete=models.CASCADE)
    mycalc = models.ForeignKey('myCalc', on_delete=models.CASCADE)
    mytarget = models.ForeignKey('myTarget', on_delete=models.CASCADE)
    mystatus = models.ForeignKey('myStatus', on_delete=models.CASCADE)
