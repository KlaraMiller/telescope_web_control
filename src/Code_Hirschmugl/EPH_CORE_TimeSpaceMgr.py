# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 12:29:28 2018

@author: Admin

==============================================================================
 LICENCE INFORMATION
==============================================================================
This Software uses Code (spg4) provided by "Brandon Rhodes" under
the "MIT License". For more Information see "licence-info.txt".

Diese Software benutzt Code (spg4), welcher von "Brandon Rhodes" unter
der "MIT License" zur Verfuegung gestellt wird. Fuer weitere Information
siehe "licence-info.txt".
==============================================================================

"""

import datetime
import math

import sgp4.ext as sgp4_ext
import EPH_ADD_math_helper as math_helper
from EPH_ADD_wgs72_complete import wgs72_complete
import EPH_SAT_norad_lists as NORAD



class TimeSpaceMgr:
    ''' deals with converting utc time for calculation purposes
        and calculating sidereal (star) time from gps position '''

    ################################################################
    #### STATIC / CLASS VARIABLES

    static_geo_valid_north = ("n","N","north","North")
    static_geo_valid_south = ("s","S","south","South")
    static_geo_valid_west =  ("w","W","west", "West")
    static_geo_valid_east =  ("e","E","east", "East")

    # ratio : sideral to tropical year
    static_sidereal_starPerSol = 366.24219/365.24219      

    static_units_deg = ("deg","DEG","Deg","degree","DEGREE","Degree")
    static_units_rad = ("rad","RAD","Rad")




    ################################################################
    #### INIT

    def __init__(self, utcDateTime=None, lat=0, lon=0, alti=0 ):
        ''' datetimeObject, latitude, longitude, altitude '''

        self._df_init() #initialize Dirty Flag
        self._time_init()

        # set geo position
        self.pos_set_LLA( lat, lon, alti )

        # default time UTCnow
        if(utcDateTime==None): utcDateTime=datetime.datetime.utcnow()
        self.time_set_utcDateTime(utcDateTime)

    # End of Method -----------------------




    ################################################################
    ##### DIRTY FLAG METHODS

    def _df_init(self):
        if not(hasattr(self,"_df_dict")):
            self._df_dict={}


    def _df_check(self,key):
        if not(key in self._df_dict):
            # key existiert noch nicht
            return False
        else:
            #key existiert
            return self._df_dict[key]


    def _df_set(self,key):
        self._df_dict[key] = True

    def _df_clear(self,key):
        self._df_dict[key] = False


    ################################################################
    #### DEALING WITH GLOBAL POSITION

    def norad_get_date(self):
        return NORAD.get_norad_age()

    def norad_get_age_in_days_str(self):
        age = self.norad_get_date()
        if type(age)==str:
            return "Error: {}. Update TLE.".format(age)
        else:
            delta = datetime.datetime.utcnow() - age
            return "{:.3f} days".format(delta.days + delta.seconds/3600/24)
    
        
    def norad_update(self):
        if NORAD.try_connect_to_celestrak():
            # wenn internet connection vorhanden
            NORAD.retrieve_norad_tle_from_url()
    
    
    def norad_update_if_older_than_days(self,days=0.5):
        import datetime
        
        if NORAD.try_connect_to_celestrak():
            # wenn internet connection vorhanden
            
            last = NORAD.get_norad_age()
            update = False
            
            if type(last) == datetime.datetime:
                # berechne tage seit letztem update
                delta = datetime.datetime.utcnow() - last
                delta = delta.days + delta.seconds/3600/24
                
                # update NORAD, wenn mehr als 'days' seit 
                # letztem update vergangen sind
                update = delta >= days
                
            else:
                # kein update file oder anderer feher:
                # versuche zu updaten
                update = True
            
            if update==True:
                NORAD.retrieve_norad_tle_from_url()
            
            


    ################################################################
    #### DEALING WITH GLOBAL POSITION

    def pos_set_LLA(self, lat, lon, alti):
        ''' Latitude: gemessen von sueden (-90°) nach norden (+90°)
            Longitude: gemessen von nullmeridian (0°)
                in Richtung der Bewegung der Sonne (nach Osten)
            Altitude: height above geodesic ellipsoid reference model of 
                earth '''

        self._df_set("pos")    # set DF for new pos entry


        # ALTITUDE ------
        self._geo_alti = float(alti)

        # LATITUDE ------
        if (type(lat) == tuple):
            # wenn tuple eingabe, zB function(("N",38.45),("E",121.54))
            vz = 1  # setze positives vorzeichen

            if(lat[0] in self.static_geo_valid_south):
                # wenn negative Richtung erkannt
                vz = -1
            else:
                # stelle sicher, dass positive richtung
                assert(lat[0] in self.static_geo_valid_north)

            self._geo_lat = float(vz*lat[1])
        else:
            self._geo_lat = float(lat)

        # LONGITUDE ------
        if (type(lon) == tuple):
            # wenn tuple eingabe, zB function(("N",38.45),("E",121.54))
            vz = 1

            if(lon[0] in self.static_geo_valid_west):
                # wenn negative Richtung erkannt
                vz = -1
            else:
                # stelle sicher, dass positive richtung
                assert(lon[0] in self.static_geo_valid_east)

            self._geo_lon = float(vz*lon[1])
        else:
            self._geo_lon = float(lon)

    # End of Method -----------------------

    def pos_get_LLA(self):
        ''' returnes: tuple(Latitude, Longitude, Altitude) '''
        return self._geo_lat, self._geo_lon, self._geo_alti
    # End of Method -----------------------

    def pos_get_LLAlat(self):
        ''' returnes: Latitude '''
        return self._geo_lat
    # End of Method -----------------------

    def pos_get_LLAlon(self):
        ''' returnes: Longitude '''
        return self._geo_lon
    # End of Method -----------------------

    def pos_get_LLAalti(self):
        ''' returnes: Elevation '''
        return self._geo_alti
    # End of Method -----------------------


    def _calc_ECI(self):
        ''' calc position in ECI reference from time:LMST and pos:LLA'''

        self._df_clear("time")  # clear dirty flags
        self._df_clear("pos")


        a =     wgs72_complete["radiusearthkm"]
        e2 =    wgs72_complete["e^2"]

        phi =   self._geo_lat
        lambd = self.sidereal_get_LMST()
        h =     self._geo_alti/1000     # m to km
        
        sin_phi =   math_helper.sin_deg(phi)
        cos_phi =   math_helper.cos_deg(phi)
        sin_lambd = math_helper.sin_deg(lambd)
        cos_lambd = math_helper.cos_deg(lambd)


        # [Günter Seeber, "Satellite Geodesy", 2nd edition] page 24

        # N is the radius of curvature in the prime vertical:
        # N = a / sqrt( 1 - (e^2)*(sin(lat)^2) )
        # EQUATION (2.36)
        N = a / math.sqrt( 1 - e2*(sin_phi**2) )

        # EQUATION (2.35)
        self._eci_x = (N+h) * cos_phi * cos_lambd
        self._eci_y = (N+h) * cos_phi * sin_lambd
        self._eci_z = ( (1-e2)*N + h ) * sin_phi


    def pos_get_ECI(self):
        ''' returns position in ECI reference x,y,z in km '''

        # check for new time or pos entry
        if(self._df_check("time") or self._df_check("pos")):
            self._calc_ECI()

        return self._eci_x, self._eci_y,self._eci_z

    # End of Method -----------------------






    ################################################################
    #### DEALING WITH TIME


    def _time_init(self):
        self._utcTime = datetime.datetime(2000,1,1)
        self._utcTime_prev = datetime.datetime(2000,1,1)
    # End of Method -----------------------


    def time_set_utcNow(self):
        # sets TSMgr to utcNow
        self.time_set_utcDateTime(datetime.datetime.utcnow())
    # End of Method -----------------------


    def time_set_utcDateTime(self, new_utcDateTime=None):
        # set a new UTC time

        self._df_set("time")    # set DF for new time entry

        if(new_utcDateTime==None):
            # wenn keine zeit übergeben wurde, dann immer utcNOW
            new_utcDateTime=datetime.datetime.utcnow()


        if (type(new_utcDateTime) == datetime.datetime):
            # wenn vom typ datetime
            self._utcTime = new_utcDateTime
        else:
            # wenn nicht typ datetime, dann stell sicher,
            #   dass ein tuple eingegeben wurde
            assert (type(new_utcDateTime) == tuple)

            # set default values to 2000-1-1 12:00:00
            Y,M,D,h,m,s,us = 2000,1,1,12,0,0,0

            # wenn in tuple enthalten, dann überschreibe default values
            if (len(new_utcDateTime) > 0):
                Y = new_utcDateTime[0]
            if (len(new_utcDateTime) > 1):
                M = new_utcDateTime[1]
            if (len(new_utcDateTime) > 2):
                D = new_utcDateTime[2]
            if (len(new_utcDateTime) > 3):
                h = new_utcDateTime[3]
            if (len(new_utcDateTime) > 4):
                m = new_utcDateTime[4]
            if (len(new_utcDateTime) > 5):
                s = new_utcDateTime[5]
            if (len(new_utcDateTime) > 6):
                us = new_utcDateTime[6]

            self._utcTime = datetime.datetime(Y,M,D,h,m,s,us)
        # End of ELSE -----------------------

        self.time_calc_julianDateFromUtc()  #update julian date
        self.sidereal_calc_GMST()           #update gmst
        self._calc_ECI()
    # End of Method -----------------------


    def time_get_utcDateTime(self):
        return self._utcTime
    # End of Method -----------------------


    def time_calc_julianDateFromUtc(self):
        #def jday(year, mon, day, hr, minute, sec):
        self._julianDate = sgp4_ext.jday(
                self._utcTime.year, self._utcTime.month, self._utcTime.day,
                self._utcTime.hour, self._utcTime.minute,
                self._utcTime.second+self._utcTime.microsecond*1e-6)

        # CALCULATING JULIAN CENTURIES SINCE EPOCH J2000
        #   julianische jahrhunderte ephemeridenzeit seit der epoche J2000
        self._julianCentJ2000 = (self._julianDate - 2451545.0) / 36525.0

    # End of Method -----------------------


    def time_get_julianDate(self):
        ''' returns Julianisches datum '''
        return self._julianDate
    # End of Method -----------------------

    def time_get_julianCenturiesJ2000(self):
        ''' returns Julianische jahrhunderte seit J2000 '''
        return self._julianCentJ2000
    # End of Method -----------------------




    ################################################################
    #### DEALING WITH SIDEREAL

    def sidereal_calc_GMST(self):
        ''' calc Greenwich Mean Sidereal Time in DEGREES '''

        # ratio : sideral to tropical year
        #starPerSol = 366.2422/365.2422      
        #starPerSol = 1.0027379093

        # Zeit seit 0h UTC in stunden
        t0h = ( (((self._utcTime.microsecond/1e6) + self._utcTime.second)/60 +
                 self._utcTime.minute)/60 + self._utcTime.hour )

        # Julianisches datum um 0h UTC
        julD0 = self.time_get_julianDate() - t0h/24


        #formel basiert auf
        #[O. Montenbruck, Grundlagen der Ephemeridenrechnung, 7.Auflage 2005,
        #Spektrum Akademischer Verlag, Heidelberg] Page 47

        # GMST in stunden seit J2000
        gmstJ2000 = ( 6.664520 + 0.0657098244*(julD0-2451544.5) +
                     t0h*self.static_sidereal_starPerSol )

        # vielfache von 24h sind nicht interessant
        # umgerechnet in DEGREES
        self._sidereal_gmst = (gmstJ2000 % 24)/24*360
    # End of Method -----------------------




    def sidereal_get_GMST(self, unit="deg"):
        ''' returns Greenwich Mean Sidereal Time in unit (default: degrees) '''
        temp = self._sidereal_gmst

        if (unit in self.static_units_rad):
            temp = math.radians(temp)
        return temp
    # End of Method -----------------------

    def sidereal_get_LMST(self, unit="deg"):
        ''' returns LOCAL Mean Sidereal Time in in unit (default: degrees) '''
        temp = (self.sidereal_get_GMST() + self.pos_get_LLAlon())%360

        if (unit in self.static_units_rad):
            temp = math.radians(temp)
        return temp
    # End of Method -----------------------



    @staticmethod
    def hours2time(fHours):

        h=int(fHours)
        M=(fHours-h)*60
        m=int(M)
        S=(M-m)*60
        s=int(S)

        return datetime.time(h,m,s)

    # End of Method -----------------------



#    def julian_calc_julianDateFromUtc(self):
#        # Code partially provided by Johann Ernst (previous Bsc thesis)
#        # julianisches Datum berechnen , input utc-date
#
#        k = float((4711 + self.utcTime.year)) / 4  # julianische Perioden
#        tj1 = 366  # Tage im Jahr 4613 v. Chr. (Schaltjahr)
#        tj2 = int(k) * 1461  # Tage der vollstaendigen julianischen Perioden
#        tj3 = (k - int(k)) * 1460  # Tage der aktuellen julianischen Periode (bis jetzt)
#
#        tm = 0  # vergangene Tage von Jahresanfang bis Monatsbeginn
#        if (self.utcTime.month > 2):
#            tm = 30.6 * self.utcTime.month - 32.3
#            tm = int(tm)  # nur ganze Tage werden verwertet
#            if ((k - int(k)) == 0.75):  # Schaltjahr!
#                tm = tm + 1
#        elif (self.utcTime.month == 2):
#            tm = 31
#
#        tt = self.utcTime.day - 1  # heutiger Tag ist noch nicht vorbei -> -1!
#        tk = 13  # 13 Tage die ausgefallen sind (bis 2100!)
#        tastr = 0.5  # fuer die astronomische Skala - Tagesstart zu mittag!
#
#        tr = float(self.utcTime.hour)  # restliche Zeit des angebrochenen Tages
#        tr = tr + float(self.utcTime.minute) / 60
#        tr = tr + float(self.utcTime.second) / 3600
#        tr = tr / 24
#
#        tsum = tj1 + tj2 + tj3 + tm + tt - tk - tastr + tr
#        self.julianDate = tsum
#
#
#        # CALCULATING JULIAN CENTURIES SINCE EPOCH J2000
#        #   julianische jahrhunderte ephemeridenzeit seit der epoche J2000
#        self.julianCentJ2000 = (self.julianDate - 2451545.0) / 36525.0
#
#        #-------
#        self.__df_calcJulian=0  # resette julian dirty flag
#        #-------
#
#    # End of Method -----------------------


#    def sidereal_calc_GMST(self):
#        ''' calc Greenwich Mean Sidereal Time '''
#
#        starPerSol = 366.2422/365.2422      # ratio : sideral to tropical year
#        #starPerSol = 1.0027379093
#        tmu =  self._utcTime.microsecond     # microsec of UTC
#        tsec = self._utcTime.second          # secs of UTC
#        tmin = self._utcTime.minute          # mins of UTC
#
#        # Zeit seit 0h UTC
#        t0h = (((tmu/1000000) + tsec)/60 + tmin)/60 + self._utcTime.hour
#        # convert:   to sec         to min     to hour
#
#        # Julianisches datum um 0h UTC
#        julD0 = self.time_get_julianDate() - t0h/24
#
#        ''' formel basiert auf
#        [O. Montenbruck, Grundlagen der Ephemeridenrechnung, 7.Auflage 2005,
#        Spektrum Akademischer Verlag, Heidelberg] Page 47 '''
#        # GMST in stunden seit J2000
#        gmstJ2000 = 6.664520 + 0.0657098244*(julD0-2451544.5) + starPerSol*t0h
#
#        # vielfache von 24h sind nicht interessant
#        self.sidereal_gmst = gmstJ2000 % 24
#    # End of Method -----------------------



#    def utc_set_utcTimeManual(self, year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0):
#        # set a new UTC time manually
#        self.utc_set_utcTimeDatetime( datetime.datetime(year, month, day, hour, minute, second, microsecond) )
#
#        self.__df_calcJulian=1  # setze julian dirty flag
#    # End of Method -----------------------


# End of CLASS /////////////////////////////////////////////

def testing():
    aaa = TimeSpaceMgr((2019,1,25),('N',47+4/60),('E',15+26/60),353)


    # Set Time
    #current utc time
    #aaa.utc_set_utcTimeDatetime(datetime.datetime.utcnow())
    #test time
    aaa.time_set_utcDateTime((2018,12,12,12))
    print(aaa._df_check("time"))
    print(aaa._df_check("pos"))
    print(aaa.pos_get_ECI())
    print(aaa.pos_get_ECI())


if __name__ == "__main__":
    testing()