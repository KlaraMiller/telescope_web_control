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



import EPH_CORE_TimeSpaceMgr as TSMgr
import EPH_MOON_Moonlist as Moonlist
import EPH_ADD_math_helper as MH



class MoonMgr:
    
    #moon_L0        # mittlere Laenge des Mondes
    #moon_l         # mittlere Anomalie des Mondes
    #moon_lApos     # mittlere Anomalie der Sonne
    #moon_F         # mittlerer Winkelbstand des Mondes vom aufsteigenden Knoten
    #moon_D         # mittlere Elongation des Mondes 
    
    
    #""" Mittlere Winkel fuer Mondberechnung
    # Daten kommen von "Astronomie mit dem Personal Computer", 
    #   beziehen sich auf J2000 (JD:2451545)
    
    # Format: |a0|a1|a2| mit x = a0 + a1*T + a2*T*T     
    #   (T = julianische jahrhunderte seit J2000 - alle angaben in Grad!!!)
    # MOON_MEAN_ARGUMENTS_CALC 
    
    
    
    
    #---------- time is handles by time manager object
    #julianTime = 0
    #utcTime = datetime.datetime(2000,1,1,12,0)  # initial datetime
    
    
    
    def __init__ (self, timeManagerObject):
        ''' requires a TimeSpaceManager Object for Calculations '''
        
        # default values
        self._success = False
        self._TSMgr = timeManagerObject
        
        
        self._moonMeanArguments = {}
        #self.__moonMeanLongperiodicChanges = {}
        self._moonCoordinates = {
                "equa_Lon" : 0, 
                "equa_Lat": 0, 
                "ecl_Lon": 0, 
                "ecl_Lat": 0 }
        
        
        #self.__df_calcMeanArgs = 1  # mean_args neu berechnen
        self._success = True
    # End of Method -----------------------
    
    
    
#    def __meanArgs_checkDF(self):
#        ''' private methode zum erneuten berechnen der mean Arguments '''
#        if(self.__df_calcMeanArgs > 0):
#            self.calcMoonMeanArgumentsFromDate()
#    # End of Method -----------------------
    
    
    
    # -------------------------------------------------------------------
    
    def get_success(self):
        ''' returns successful creation of Moon '''
        return self._success
    # -------------------------------------------------------------------
    
    def getPos(self):
        ''' returns dict of {'Ra', 'De'} in degrees (or None if error) '''
        
        if self.get_success():
            self.calcMoonCoords_1stSolution() # berechne neu
            return {"Ra": self._moonCoordinates["equa_Lon"], 
                    "De": self._moonCoordinates["equa_Lat"]}
        else:
            return None
    # -------------------------------------------------------------------
    
    
    
    
    
    def calcMoonMeanArgumentsFromDate(self):
        Jcty = self._TSMgr.time_get_julianCenturiesJ2000()
        self._moonMeanArguments = Moonlist.get_mean_args_deg(Jcty)
                    
        #self.__df_calcMeanArgs = 0  #reset DF
    # End of Method -----------------------
            
    
    def calcMoonCoords_1stSolution(self):
        # self.__meanArgs_checkDF()
        self.calcMoonMeanArgumentsFromDate()
        
        L0 = self._moonMeanArguments['L0']
        l  = self._moonMeanArguments['l']
        l_ = self._moonMeanArguments['l_']
        F  = self._moonMeanArguments['F']
        D  = self._moonMeanArguments['D']
#        print('L0   ',L0)
#        print('l    ',l)
#        print('l_   ',l_)
#        print('F    ',F)
#        print('D    ',D)
        
        term = [None]*13
        
        term[0] = (
                22640 * MH.sin_deg(l) + 
                769   * MH.sin_deg(2*l) + 
                36    * MH.sin_deg(3*l) )       #grosse ungleicheit
        
        term[1] = -4586  * MH.sin_deg(l-2*D)    #evektion
        term[2] = 2370   * MH.sin_deg(2*D)      #variation
        term[3] = -668   * MH.sin_deg(l_)       #jaehrliche ungleichheit
        term[4] = -412   * MH.sin_deg(2*F)      #differenz in bahnlaenge und ekliptikaler laenge
        term[5] = -212   * MH.sin_deg(2*l-2*D)
        term[6] = -206   * MH.sin_deg(l+l_-2*D)
        term[7] = 192    * MH.sin_deg(l+2*D)
        term[8] = -165   * MH.sin_deg(l_-2*D)
        term[9] = 148    * MH.sin_deg(l-l_)
        term[10] = -125  * MH.sin_deg(D)        #paralaktiche gleichung
        term[11] = -110  * MH.sin_deg(l+l_)
        term[12] = -55   * MH.sin_deg(2*F-2*D)
            
        ecl_Laenge = L0 + sum(term)/3600
        self._moonCoordinates["ecl_Lon"] = ecl_Laenge %360


        # Reset des "term" Arrays
        term = [None]*8
        
        term[0] = 18520* MH.sin_deg( F + ecl_Laenge - L0 + 
            0.114*MH.sin_deg(2*F) +0.15*MH.sin_deg(l_) )    
        
        term[1] = -526 * MH.sin_deg(    F - 2*D       )
        term[2] =   44 * MH.sin_deg(    l +   F - 2*D )
        term[3] =  -31 * MH.sin_deg(   -l +   F - 2*D )
        term[4] =  -25 * MH.sin_deg( -2*l +   F       )
        term[5] =  -23 * MH.sin_deg(   l_ +   F - 2*D )
        term[6] =   21 * MH.sin_deg(   -l +   F       )
        term[7] =   11 * MH.sin_deg(  -l_ +   F - 2*D )
            
        self._moonCoordinates["ecl_Lat"] = sum(term)/3600
        
        # ergebnis ist im ekliptischen koordsys
        # wird benötigt im äquatorialen koordsys
        self.__calc_equatorialCoordinates()
        
    # End of Method -----------------------
    
    
    
    
    def __calc_equatorialCoordinates(self): 
        ''' calculates position in equatorial coords from ecliptic '''
        
        import math
        Jcty = self._TSMgr.time_get_julianCenturiesJ2000()
        
        Lam_deg = self._moonCoordinates["ecl_Lon"] # Lambda
        Bet_deg = self._moonCoordinates["ecl_Lat"] # Beta
        Eps_deg = MH.eps_deg(Jcty)                 # Epsilon
        
        sinLam = MH.sin_deg(Lam_deg)
        cosLam = MH.cos_deg(Lam_deg)        
        sinBet = MH.sin_deg(Bet_deg)
        cosBet = MH.cos_deg(Bet_deg)
        sinEps = MH.sin_deg(Eps_deg)
        cosEps = MH.cos_deg(Eps_deg)
        
        # [o. Montenbruck] "Grundlagen der Ephemeridenrechnung" S.14
#        cos(del)*cos(alp) = cos(bet)*cos(lam)
#        cos(del)*sin(alp) = cos(eps)*cos(bet)*sin(lam) - sin(eps)*sin(bet)
#        sin(del)          = sin(eps)*cos(bet)*sin(lam) + cos(eps)*sin(bet)
        
        Del_rad = math.asin( sinEps*cosBet*sinLam + cosEps*sinBet )
        Del_deg = math.degrees(Del_rad)
        cosDel = math.cos(Del_rad)
        
        cosAlp = (cosBet*cosLam) / cosDel
        sinAlp = (cosEps*cosBet*sinLam - sinEps*sinBet) / cosDel
        
        Alp_deg = MH.atan2_deg(sinAlp,cosAlp)%360
        
        self._moonCoordinates["equa_Lon"] = Alp_deg # Alpha / RA
        self._moonCoordinates["equa_Lat"] = Del_deg # Delta / DE
    # End of Method -----------------------
        
    
    
    
    
#    def calcMoonMeanArgumentsFromDate(self, julianDate):
#        t = (julianDate - 2451545.0) / 36525.0  
#        # julianische Jahrhunderte Ephemeridenzeit seit Epoche J2000
#
#        for k,v in self.const_calcMoonMeanArguments.items():
#            self._moonMeanArguments[k] = (v[0] + t*v[1] + (t**2)*v[2])%360
#            """# für jeden key in const_calcMoonMeanArguments werden die Groessen 
#            entsprechden dem julianischen Datum fuer die Berechnung 
#            der Mondposition (MOON_MEAN_ARGUMENTS) aus dem value-array berechnet"""
#            
#        self.__df_calcMeanArgs = 0  #reset DF
#    # End of Method -----------------------
#            
#    
#    def get_moonLon(self):
#        return self._moonCoordinates["Laenge"]
#    # End of Method -----------------------
#            
#    
#    def get_moonLat(self):
#        return self._moonCoordinates["Breite"]
#    # End of Method -----------------------
#            
#    
#    def calcMoonCoords_1stSolution(self):
#        self.__meanArgs_checkDF()
#        
#        L0 =    self._moonMeanArguments['L0']
#        l =     self._moonMeanArguments['l']
#        lApo =  self._moonMeanArguments['lApo']
#        F =     self._moonMeanArguments['F']
#        D =     self._moonMeanArguments['D']
#        print('L0   ',L0)
#        print('l    ',l)
#        print('lApo ',lApo)
#        print('F    ',F)
#        print('D    ',D)
#        
#        term = [None]*13
#        
#        term[0] = 22640  * self.sinGrad(l) + 769*self.sinGrad(2*l) + 36*self.sinGrad(3*l)    #grosse ungleicheit
#        term[1] = -4586  * self.sinGrad(l-2*D)              #evektion
#        term[2] = 2370   * self.sinGrad(2*D)                #variation
#        term[3] = -668   * self.sinGrad(lApo)            #jaehrliche ungleichheit
#        term[4] = -412   * self.sinGrad(2*F)                #differenz in bahnlaenge und ekliptikaler laenge
#        term[5] = -212   * self.sinGrad(2*l-2*D)
#        term[6] = -206   * self.sinGrad(l+lApo-2*D)
#        term[7] = 192    * self.sinGrad(l+2*D)
#        term[8] = -165   * self.sinGrad(lApo-2*D)
#        term[9] = 148    * self.sinGrad(l-lApo)
#        term[10] = -125  * self.sinGrad(D)                  #paralaktiche gleichung
#        term[11] = -110  * self.sinGrad(l+lApo)
#        term[12] = -55   * self.sinGrad(2*F-2*D)
#            
#        Laenge = L0 + sum(term)/3600
#        self._moonCoordinates["Laenge"] = Laenge %360
#
#        # Reset des "term" Arrays
#        term = [None]*8
#        
#        term[0] = 18520* self.sinGrad( F + Laenge - L0 + 0.114*self.sinGrad(2*F) +0.15*self.sinGrad(lApo) )    
#        term[1] = -526 * self.sinGrad( F - 2*D )
#        term[2] = 44   * self.sinGrad( l + F - 2*D )
#        term[3] = -31  * self.sinGrad( -l + F - 2*D )
#        term[4] = -25  * self.sinGrad( -2*l + F )
#        term[5] = -23  * self.sinGrad( lApo + F - 2*D )
#        term[6] = 21   * self.sinGrad( -l + F )
#        term[7] = 11   * self.sinGrad( -lApo + F - 2*D )
#            
#        self._moonCoordinates["Breite"] = sum(term)/3600
#    # End of Method -----------------------
#                    

#    
#        
#    @staticmethod
#    def sinGrad(angleDegree):
#        return math.sin(angleDegree * math.pi/180.0)
#    @staticmethod
#    def cosGrad(angleDegree):
#        return math.cos(angleDegree * math.pi/180.0)
#    @staticmethod
#    def tanGrad(angleDegree):
#        return math.tan(angleDegree * math.pi/180.0)
#    @staticmethod
#    def arcsinGrad(argument):
#        return math.asin(argument)*180/math.pi
#    @staticmethod
#    def arccosGrad(argument):
#        return math.acos(argument)*180/math.pi
#    @staticmethod
#    def arctanGrad(argument):
#        return math.atan(argument)*180/math.pi
#    
#    @staticmethod
#    def equatorialCoordinates(lambd, beta, julCent): # Winkel in grad uebergeben!
#        # provided by Johann Ernst
#        # geozentrisch-ekliptikale Koordinaten des himmelsgebundenen Aequatorsystems
#        
#        eps = 23.439291-0.013004*julCent
#
#        # Winkel in rad umrechnen
#        lambd = lambd * math.pi / 180
#        beta = beta * math.pi / 180
#        eps = eps * math.pi / 180
#
#        delta = math.asin(math.sin(beta) * math.cos(eps) + math.cos(beta) * math.sin(lambd) * math.sin(eps))
#        cos_a = (math.cos(beta) * math.cos(lambd) / math.cos(delta))
#        sin_a = (math.cos(beta) * math.sin(lambd) * math.cos(eps) - math.sin(beta) * math.sin(eps)) / math.cos(delta)
#        a = 0
#
#        if((cos_a < 0) and (sin_a < 0)):      # 3. Quadrant
#            a = 2 * math.pi - math.acos(cos_a)
#        elif((cos_a > 0 ) and (sin_a < 0)):     # 4. Quadrant
#            a = 2 * math.pi + math.asin(sin_a)
#        else:                                   # 1. & 2. Quadrant
#            a = math.acos(cos_a)
#
#        return {"alpha": a * 180 / math.pi, "delta": delta * 180 / math.pi}
#        
#        
#
## Für Greenwich
#"""
#horizontal_coordinates = Ephemeris.calcPositionHorizontal(planet, test_date, 0, 51.4825766, 1000, 1)
#aequatorial_coordinates = Ephemeris.calcPositionAequatorial(planet, test_date)
##"""
#
### Für Graz
###"""
##horizontal_coordinates = Ephemeris.calcPositionHorizontal(planet, test_date, 15.45836667, 47.06666944, 1021, 0)
##aequatorial_coordinates = Ephemeris.calcPositionAequatorial(planet, test_date)
###"""
##
##print(planet + " am " + str(test_date) + "\n")
##print("Echte horizontale Hoehe: " + str(horizontal_coordinates["hoehe_r"]) + "°")
##print("Scheinbare horizontale Hoehe: " + str(horizontal_coordinates["hoehe_s"]) + "°")
##print("Azimut: " + str(horizontal_coordinates["azimut"]) + "°")
##print("")
##print("Deklination: " + str(aequatorial_coordinates["delta"]) + "°")
##print("Rektaszension " + str(aequatorial_coordinates["alpha"]) + "°")
#myTime = TSMgr.Cls_TimeSpace_Manager()
#myTime.utc_set_utcTimeManual(2018,1,1,0)
#myTime.geo_set_gpsPosition("N",47+4/60,"E",15+26/60)
#myTime.julian_calc_julianDateFromUtc()
#myTime.sidereal_calc_GMST()
#myTime.sidereal_calc_GAST()
#
#moon1 = Cls_Ephemeris_Moon(myTime)
#moon1.calcMoonCoords_1stSolution()
#
#def degree_toLongDeg(degree):
#    d=int(degree)
#    M=(degree-d)*60
#    m=int(M)
#    s=int((M-m)*60)
#    return "{:02d}° {:02d}' {:05.2f}".format(d,m,s)+'"'
#    
#
#print('Date utc: ', myTime.utcTime.strftime("%Y-%m-%d %H:%M:%S"))
#print('Date jul: ', myTime.julian_get_julianDate())
#print('Date JDC: ', myTime.julian_get_julianCenturiesJ2000())
#print('Geo_lon:  ', myTime.geo_get_geoLon())
#print('Geo_lat:  ', myTime.geo_get_geoLat())
#print('LSMT:     ', myTime.fHours2hhmmssString(myTime.sidereal_get_LMST()))
#print("")
#
#equa = moon1.equatorialCoordinates(moon1.get_moonLon(),moon1.get_moonLat(),myTime.julian_get_julianCenturiesJ2000())
#print('MoonRA°:  \t', degree_toLongDeg(equa["alpha"]))
#print('MoonRA :  \t', myTime.fHours2hhmmssString(equa["alpha"]/360*24))
##print('MoonDecl°: ', equa["delta"])
#print('MoonDecl°:\t', degree_toLongDeg(equa["delta"]))
#
#testmoon = {"date":"2018-01-01 00:00:00"}
#testmoon["RA"] = {"h":5,"m": 38,"s":0.43}
#testmoon["RA"]["H"] = testmoon["RA"]["h"] + testmoon["RA"]["m"]/60 + testmoon["RA"]["s"]/3600
#
#testmoon["decl"] = {"deg":19,"min":19,"sec":10.2}
#testmoon["decl"]["DEG"] = testmoon["decl"]["deg"] + testmoon["decl"]["min"]/60 + testmoon["decl"]["sec"]/3600
#
#print("\nastropixel.com")
#print("2018-01-01 00:00:00")
#print("Apparent RA:  \t", degree_toLongDeg(testmoon["RA"]["H"]/24*360))
#print("Apparent RA:  \t",myTime.fHours2hhmmssString(testmoon["RA"]["H"]))
#print("Apparent Decl:\t", degree_toLongDeg(testmoon["decl"]["DEG"]))
