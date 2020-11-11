# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:08:58 2019

@author: polsterc16

==============================================================================
 LICENCE INFORMATION
==============================================================================
This Software uses Code (spg4) provided by "Brandon Rhodes" under
the "MIT License". For more Information see "licence-info.txt".

Diese Software benutzt Code (spg4), welcher von "Brandon Rhodes" unter
der "MIT License" zur Verfuegung gestellt wird. Fuer weitere Information
siehe "licence-info.txt".
==============================================================================


# Dieser Code baut auf der Bachelor Arbeit 1 von Johann Ernst auf.
#
# Orbital Elements der Planeten wurden von der Website von 
# NASA (Jet Propulsion Lab) entnommen
# https://ssd.jpl.nasa.gov/?planet_pos
# https://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf

["Grundlagen der Ephemeridenrechung", O. Montenbruck]

# astronomical almanach 2018
http://asa.usno.navy.mil/static/files/2018/Astronomical_Constants_2018.pdf


# ["The Planet Mars: A History of Observation and Discovery", William Sheehan]
# https://web.archive.org/web/20100625043926/http://www.uapress.arizona.edu/
                                                    onlinebks/mars/appends.htm
"""


# ---------------------------------------------------
# IMPORTS
import EPH_CORE_TimeSpaceMgr as TSMgr
import EPH_PLANET_Planetlist as Planetlist
import EPH_ADD_math_helper as MH

#import norad_lists
# -*- coding: utf-8 -*-

class PlanetMgr:
    ''' Class that handles planet ephemeris '''

    def __init__(self, TSMgrObj:TSMgr.TimeSpaceMgr, planet:str):
        ''' Create a planet by its name,
            with reference to a TimeSpaceMgr object
            (preferably one for all planets). '''
        print("PLANET: "+str(planet))
            
        # default values
        self._successPlanet = False
        self._planetName =  None
        self._TSMgr =       None
        
        if (planet.lower() in Planetlist.Planetlist and 
            planet.lower() != "earth"):
            #wenn planet sich in der liste bekannter planeten befindet
            
            self._planetName = planet.lower()
            self._TSMgr = TSMgrObj   # reference to the global TSMgr
            
            Jcty = self._TSMgr.time_get_julianCenturiesJ2000()
            self._keplerPlanet = Planetlist.getCurrentKeplerElem(
                    self._planetName, Jcty ) #get kepler elements
            self._keplerEarth = Planetlist.getCurrentKeplerElem(
                    "earth", Jcty ) #get kepler elements
            
            # astronomical almanach 2018
            # schiefe der eklitptic epsilon = epsJ2000 + epsDot * T
            # T = julian centuries since J2000
            # epsJ2000 = 84381.406 arcsec
            # epsDot =  -46.836769 arcsec per julian century
#            self._eps = (84381.406 - 
#                         46.836769*self._TSMgr.time_get_julianCenturiesJ2000()
#                         )/3600
            self._eps = MH.eps_deg(Jcty)
            
            # astronomic unit in km
            self._AU = 149597870.7
            
            self._successPlanet = True
            
    # -------------------------------------------------------------------
    
    def get_success(self):
        ''' returns successful creation of planet '''
        return self._successPlanet
    # -------------------------------------------------------------------
    
    def getPos(self, utcDateTime=None):
        ''' returns dict of {'Ra', 'De'} in degrees (or None if error) '''
        if self.get_success():
            pos = self.calcPos(utcDateTime)
            return {"Ra": pos["Ra"], 
                    "De": pos["De"]}
        else:
            return None
    # -------------------------------------------------------------------

    
    def calcPos(self, utcDateTime=None):
        # es müssen position von erde und planet immer gleichzeitig
        # berechnet werden, da wir den relativen richtungsvektor
        # zwischen beiden benötigen (und alles im heliozentr koord sys
        # berechnet wird)
        import EPH_ADD_math_helper as math_helper
        from EPH_ADD_wgs72_complete import wgs72_complete
        
        #update time in TSMgr
        #self._TSMgr.time_set_utcDateTime(utcDateTime)
        
        # -------------------------------------------------------------------
        #get kepler elements 
        Jcty = self._TSMgr.time_get_julianCenturiesJ2000()
        self._keplerPlanet = Planetlist.getCurrentKeplerElem(
                self._planetName, Jcty ) #get kepler elements
        self._keplerEarth = Planetlist.getCurrentKeplerElem(
                "earth", Jcty ) #get kepler elements
        
        # -------------------------------------------------------------------
        # get eccentric anomaly with KEPLER EQUATION (newton verfahren)
        # PLANET
        self._keplerPlanet["E"] = Planetlist.keplerEquation(
                self._keplerPlanet["M"],self._keplerPlanet["e"])
        # EARTH
        self._keplerEarth["E"] = Planetlist.keplerEquation(
                self._keplerEarth["M"],self._keplerEarth["e"])
        
        # -------------------------------------------------------------------
        # heliocentric coordinates in the planet's orbital plane
        # x-axis aligned from focus towards perihelion 
        # PLANET
        xyzHelioOrbitP=self.__calc_helio_orbit_from_kepler(self._keplerPlanet)
        
        # EARTH
        xyzHelioOrbitE=self.__calc_helio_orbit_from_kepler(self._keplerEarth)
        
        
        # -------------------------------------------------------------------
        # heliocentric coordinates in the ecliptic plane (earths orbit)
        # x-axis aligned towards the equinox
        # PLANET
        xyzHelioEclP = self.__calc_helio_ecliptical_from_helio_orbit(
                xyzHelioOrbitP, self._keplerPlanet)
        
        # EARTH
        xyzHelioEclE = self.__calc_helio_ecliptical_from_helio_orbit(
                xyzHelioOrbitE, self._keplerEarth)
        
        # -------------------------------------------------------------------
        # relativer vektor von erde zu planet (Erde2Planet) im heliocentr.
        # ekliptikalen kartes. koordin system (entspricht geozentr.
        # ekliptikalen kartes. koord system)
        # Sonne2Planet = Sonne2Erde + Erde2Planet
        # Erde2Planet = Sonne2Planet - Sonne2Erde
        xyzHelioEcl_E2P = math_helper.vector_sub(xyzHelioEclP,xyzHelioEclE)
        
        # (entspricht geozentr. ekliptikalen kartes. koord system)
        planetGeoEclCartesian = tuple(xyzHelioEcl_E2P)
        
        # -------------------------------------------------------------------
        # an dieser stelle ist der relative vektor vom zentrum der erde zum
        # gesuchten planeten im heliocentr, ecliptical cartes. coord sys
        # bekannt - es folgen umrechungen in koordin systeme für die
        # beobachtung von der erde aus.
        # -------------------------------------------------------------------
        
        # drehe koordinate von ekliptical zu equatorial
        planetGeoEquCartesian=self.__rotate_from_ecliptical_to_equatorial(
                planetGeoEclCartesian, self._eps)
        
        #get geocentr equatorial pos of tele in KM!!!
        pos_tele_GeoEquCartesian =  self._TSMgr.pos_get_ECI()
        
       
        
        planetTopoEquCartesian = [0,0,0]
        # um parallax effekte zu vermeiden, wird die position des teleskops
        # abgezogen.
        # Im falle von Mars würde die maximale parallaxe bei seinem letzten
        # Closest approach in 2018 Jul 27 (näheste annäherung an die erde)
        # ca 22.78 arcsec betragen (dist_min = 0.386 AU, 
        # parallax_max = asin(earthradius in km / dist in km ),
        # parallax_max = asin(6378/57744778) ) 
        for k in range(3):
            planetTopoEquCartesian[k] = (planetGeoEquCartesian [k] - 
                                  pos_tele_GeoEquCartesian[k]/self._AU)
        
#        # wandle in spherical koordinaten um
#        planetGeoEquSpherical = self.__calc_spherical_from_cartesian(
#                planetGeoEquCartesian)
            
        # wandle in spherical koordinaten um
        planetTopoEquSpherical = self.__calc_spherical_from_cartesian(
                planetTopoEquCartesian)
        
        
        return {"Ra": planetTopoEquSpherical[0], 
                "De": planetTopoEquSpherical[1], 
                "R":  planetTopoEquSpherical[2]}
        
        
    @staticmethod
    def __calc_helio_orbit_from_kepler(keplerelements:dict):
        ''' returns heliocentric cartesian coordinates (x', y', z') in the
            orbital plane with x' aligned from the focus (Sun) to the
            perihel of the planet '''
        import math
        
        x_,y_,z_ = 0,0,0     # x', y', z'
        a = keplerelements["a"]
        e = keplerelements["e"]
        E = keplerelements["E"]
        
        # x',y' koordinaten aus a,e und E (exzentrischer anomalie)
        #siehe ["Grundlagen der Ephemeridenrechung", O. Montenbruck] p 56
        # PLANET
        x_ = a * (math.cos(E) - e)
        y_ = a * math.sqrt(1 - e*e) * math.sin(E)
        
        return (x_, y_, z_)
        
    @staticmethod
    def __calc_helio_ecliptical_from_helio_orbit(xyzHelioOrbitTuple, 
                                                 keplerelements:dict):
        ''' returns heliocentric cartesian coordinates (x, y, z) in the
            ecliptic plane with x aligned to the vernal Equinox J2000 '''
        
        import math
        
        if len(xyzHelioOrbitTuple) != 3:
            # wenn tuple nicht 3 elemente enthält (x',y',z')
            # dann stoppe
            return None
        
        x_,y_,z_ = xyzHelioOrbitTuple
        
        # hilfssinuse
        sin_w = math.sin(keplerelements["w"])
        cos_w = math.cos(keplerelements["w"])
        sin_W = math.sin(keplerelements["W"])
        cos_W = math.cos(keplerelements["W"])
        sin_i = math.sin(keplerelements["i"])
        cos_i = math.cos(keplerelements["i"])
        
        # berechung von heliozentrischen, ekliptikalen kartesischen 
        # koordinaten mit gaussschen vektoren
        #siehe ["Grundlagen der Ephemeridenrechung", O. Montenbruck] p 11
        Px = cos_w*cos_W - sin_w*sin_W*cos_i
        Py = cos_w*sin_W + sin_w*cos_W*cos_i
        Pz = sin_w*sin_i
        Qx = -sin_w*cos_W - cos_w*sin_W*cos_i
        Qy = -sin_w*sin_W + cos_w*cos_W*cos_i
        Qz = cos_w*sin_i
        
        x_ecl = x_*Px + y_*Qx
        y_ecl = x_*Py + y_*Qy
        z_ecl = x_*Pz + y_*Qz
        
        return (x_ecl, y_ecl, z_ecl)
    
    
    @staticmethod
    def __calc_spherical_from_cartesian(xyz=[0,0,0]):
        import math
        
        x,y,z=xyz
        
        r = math.sqrt(x*x+y*y+z*z)  # radius der kugel
        if r<=0:
            # wenn radius nicht mindestens größer 0 ist
            return (0,0,0)
        
        # sin(b) = z/r
        b = math.degrees(math.asin(z/r))      # breite wird von xy ebene weg gemessen
        
        # tan(l) = y/x
        l = math.degrees(math.atan2(y,x))    # vorzeichenkorrekter atan
        
        return (l,b,r) # länge, breite, radius
            
        
    @staticmethod
    def __rotate_from_ecliptical_to_equatorial(xyzEcl=[0,0,0],eps=0):
        # ekliptische schiefe epsilon (obliquity of the ecliptic) 
        # bedeutet eine drehung um die x-achse mit epsilon
        import math
        
        x,y,z = xyzEcl
        sinEps = math.sin(math.radians(eps))
        cosEps = math.cos(math.radians(eps))
        
        # [ xEqu ]   [ 1    0        0    ]   [ xEcl ]
        # [ yEqu ] = [ 0  cosEps  -sinEps ] * [ yEcl ]          
        # [ zEqu ]   [ 0  sinEps   cosEps ]   [ zEcl ]        

        xEqu = x +    0     +    0
        yEqu = 0 + cosEps*y - sinEps*z
        zEqu = 0 + sinEps*y + cosEps*z
        
        return (xEqu,yEqu,zEqu)
    
    
    
    
    
    
    
    
    
    
#        
#        
#        
#    
#    #""" Konstanten
#    # Daten kommen von der NASA-Homepage
#    
#    planet_const = {}
#    
#    # Format: |Merkur|Venus|Erde|Mars|Jupiter|Saturn|Uranus|Neptun|Pluto|
#    a1 = [0.38709927, 0.72333566, 1.00000261, 1.52371034, 5.20288700, 9.53667594, 19.18916464, 30.06992276, 39.48211675] # in AE
#    a2 = [0.00000037, 0.00000390, 0.00000562, 0.00001847, -0.00011607, -0.00125060, -0.00196176, 0.00026291, -0.00031596]
#    e1 = [0.20563593, 0.00677672, 0.01671123, 0.09339410, 0.04838624, 0.05386179, 0.04725744, 0.00859048, 0.24882730]
#    e2 = [0.00001906, -0.00004107, -0.00004392, 0.00007882, -0.00013253, -0.00050991, -0.00004397, 0.00005105, 0.00005170]
#    i1 = [7.00497902, 3.39467605, -0.00001531, 1.84969142, 1.30439695, 2.48599187, 0.77263783, 1.77004347, 17.14001206]
#    i2 = [-0.00594749, -0.00078890, -0.01294668, -0.00813131, -0.00183714, 0.00193609, -0.00242939, 0.00035372, 0.00004818]
#    L1 = [252.25032350, 181.97909950, 100.46457166, -4.55343205, 34.39644051, 49.95424423, 313.23810451, -55.12002969, 238.92903833]
#    L2 = [149472.67411175, 58517.81538729, 35999.37244981, 19140.30268499, 3034.74612775, 1222.49362201, 428.48202785, 218.45945325, 145.20780515]
#    w1 = [77.45779628, 131.60246718, 102.93768193, -23.94362959, 14.72847983, 92.59887831, 170.95427630, 44.96476227, 224.06891629]
#    w2 = [0.16047689, 0.00268329, 0.32327364, 0.44441088, 0.21252668, -0.41897216, 0.40805281, -0.32241464, -0.04062942]
#    W1 = [48.33076593, 76.67984255, 0.0, 49.55953891, 100.47390909, 113.66242448, 74.01692503, 131.78422574, 110.30393684]
#    W2 = [-0.12534081, -0.27769418, 0.0, -0.29257343, 0.20469106, -0.28867794, 0.04240589, -0.00508664, -0.01183482]
#
#    # Lookup-Tabelle für die Refraktion unter 15°. -> kann nicht mittels Formel berechnet werden, nur näherungsweise über 15°
#    # Erster Wert ist die horziontale Höhe
#    # Zweiter Wert ist 1/Refraktion, da dies einen annähernd linearen Verlauf ergibt
#    REFRACTION = [[0.0, 1.6949],
#                  [0.3, 1.9262],
#                  [0.5, 2.0408],
#                  [1.0, 2.4374],
#                  [1.5, 2.8458],
#                  [2.0, 3.2787],
#                  [2.5, 3,7152],
#                  [3.0, 4.1763],
#                  [3.5, 4.6392],
#                  [4.0, 5.1064],
#                  [5.0, 6.0811],
#                  [6.0, 7.0866],
#                  [7.0, 8.1081],
#                  [8.0, 9.1603],
#                  [9.0, 10.2273],
#                  [10.0, 11.2853],
#                  [15.0, 16.8224]]
#
#    ORBITAL_ELEMENTS = {"mercury" : {}, "venus" : {}, "earth" : {}, "mars" : {}, "jupiter" : {}, "saturn" : {}, "uranus" : {}, "neptune" : {}, "pluto" : {}}	# erstellt dictionary mit den planetennamen als key
#    KEY_LOOKUP = {0 : "mercury", 1 : "venus", 2: "earth", 3 : "mars", 4 : "jupiter", 5 : "saturn", 6 : "uranus", 7 : "neptune", 8 : "pluto"}
#    YEAR_TROPICAL = 365.24219    # Tage
#    YEAR_STAR = 366.24219        # Tage
#    ECLIPTIC_ANGLE = 23.43929   # Grad
#    #"""
#    
#    @classmethod
#    def calcOrbitalElements(cls, date):
#        t = (cls.julianDate(date) - 2451545.0) / 36525.0  # Wieviele Jahrhunderte nach dem Jahr J2000.0 vergangen sind
#
#        for i in range(0, 9):
#            cls.ORBITAL_ELEMENTS[cls.KEY_LOOKUP[i]]["a"] = cls.a1[i] + t * cls.a2[i]    # grosse Halbachse in AE
#            cls.ORBITAL_ELEMENTS[cls.KEY_LOOKUP[i]]["e"] = cls.e1[i] + t * cls.e2[i]    # numerische Exzentrizitaet (zwischen 0 und 1)
#            cls.ORBITAL_ELEMENTS[cls.KEY_LOOKUP[i]]["W"] = cls.W1[i] + t * cls.W2[i]    # Omega, Laenge des aufsteigenden Knotens in grad
#            cls.ORBITAL_ELEMENTS[cls.KEY_LOOKUP[i]]["i"] = cls.i1[i] + t * cls.i2[i]    # Neigung der Bahnebene gegen die Ekliptik in grad
#            cls.ORBITAL_ELEMENTS[cls.KEY_LOOKUP[i]]["M"] = (cls.L1[i] + t * cls.L2[i]) - (cls.w1[i] + t * cls.w2[i])  # Mittlere Anomalie in grad
#            cls.ORBITAL_ELEMENTS[cls.KEY_LOOKUP[i]]["w"] = (cls.w1[i] + t * cls.w2[i]) - (cls.W1[i] + t * cls.W2[i])  # Argument des Perihels in grad
#
#    @classmethod
#    def calcPositionAequatorial(cls, planet, date):
#        #Ephemeriden eines bestimmten Planeten zu bestimmten Zeitpunkt im sphaerischen Aequatorialsystem berechnen
#
#        # Bahnelemente für das gewuenschte Datum berechnen
#        cls.calcOrbitalElements(date)
#
#        # Position der Erde kann nicht berechnet werden
#        if(planet == "earth"):
#            raise ValueError("You cannot calculate the position of the earth!")
#
#        try:
#            # als erstes Radius und wirkliche Anomalie des Planeten zum gewuenschten Zeitpunkt berechnen, alle Variablen des Planeten mit _p
#            m_p = cls.ORBITAL_ELEMENTS[planet]["M"] % 360      # falls Winkel groesser als 360 grad ist, ganze Kreise davon abziehen
#            m_p = m_p * math.pi / 180                           # in rad umwandeln
#        except KeyError as error:
#            raise KeyError("No valid planet!")
#        
#        e_p = cls.ORBITAL_ELEMENTS[planet]["e"]
#        a_p = cls.ORBITAL_ELEMENTS[planet]["a"]
#
#        E_p = cls.keplerEquation(m_p, e_p, 1e-7)           # Keplergleichung loesen um exzentrische Anomalie des Planeten zu bekommen
#        r_p = a_p  * (1 - e_p * math.cos(E_p))              # Abstand ("Radius") von der Sonne zum Planeten
#        v_p = math.acos((math.cos(E_p) - e_p) / (1 - e_p * math.cos(E_p)))    # wirkliche Anomalie berechnen
#
#        if(m_p >  math.pi):                                 # wenn der Planet bereits am Rueckweg von Aphel zum Perihel ist, Winkel korrigieren
#            v_p = 2 * math.pi - v_p
#
#        v_p = v_p * 180 / math.pi                           # Winkel in grad umrechnen
#
#
#        # heliozentrisch-ekliptikale Koordinaten des gewuenschten Planeten ausrechnen
#        helio_p = cls.helioEclipticCoordinates(r_p, cls.ORBITAL_ELEMENTS[planet]["w"], cls.ORBITAL_ELEMENTS[planet]["W"], v_p, cls.ORBITAL_ELEMENTS[planet]["i"])
#
#        # als naechstes Radius und wirkliche Anomalie der Erde zum gewuenschten Zeitpunkt berechnen, alle Variablen der Erde mit _e
#        m_e = cls.ORBITAL_ELEMENTS["earth"]["M"] % 360     # falls Winkel groesser als 360 grad ist, ganze Kreise davon abziehen
#        m_e = m_e * math.pi / 180                           # in rad umwandeln
#
#        e_e = cls.ORBITAL_ELEMENTS["earth"]["e"]
#        a_e = cls.ORBITAL_ELEMENTS["earth"]["a"]
#
#        E_e = cls.keplerEquation(m_e, e_e, 1e-6)           # Keplergleichung loesen um exzentrische Anomalie der Erde zu bekommen
#        r_e = a_e * (1 - e_e * math.cos(E_e))               # Abstand ("Radius") von der Sonne zur Erde
#        v_e = math.acos((math.cos(E_e) - e_e) / (1 - e_e * math.cos(E_e)))  # wirkliche Anomalie berechnen
#
#        if(m_e > math.pi):                                  # wenn die Erde bereits am Rueckweg von Aphel zum Perihel ist, Winkel korrigieren
#            v_e = 2 * math.pi - v_e
#
#        v_e = v_e * 180 / math.pi                           # Winkel in grad umrechnen
#
#        # heliozentrisch-ekliptikale Koordinaten der Erde ausrechnen
#        helio_e = cls.helioEclipticCoordinates(r_e, cls.ORBITAL_ELEMENTS["earth"]["w"], cls.ORBITAL_ELEMENTS["earth"]["W"], v_e, cls.ORBITAL_ELEMENTS["earth"]["i"])
#
#        # Koordinatenursprung von der Sonne zur Erde verschieben -> ins geozentrische Ekliptiksystem
#        geo_ecl = cls.geoEclipticCoordinates(helio_p["x"], helio_p["y"], helio_p["z"], helio_e["x"], helio_e["y"], helio_e["z"])
#
#        # vom geozentrischen Ekliptiksystem ins sphaerengebundene Aequatorsystem
#        geo_sph = cls.equatorialCoordinates(geo_ecl["lambda"], geo_ecl["beta"], cls.ECLIPTIC_ANGLE)
#
#        # Positionen von Rad in Grad umrechnen
#        return geo_sph
#
#    @classmethod
#    def calcPositionHorizontal(cls, planet, date, geo_length, geo_width, air_pressure, temperature):  # Luftdruck in hPa, Temperatur in grad Celsius
#        # Ephemeriden eines bestimmten Planeten zu bestimmten Zeitpunkt im Horizontalsystem berechnen
#
#        # Position im sphaerengebunden Aequatorsystem berechnen
#        geo_sph = cls.calcPositionAequatorial(planet, date)
#
#        # vom sphaerengebundenen Aequatorsystem ins Horizontalsystem
#        hor = cls.horizontalCoordinates(geo_sph["alpha"], geo_sph["delta"], cls.julianDate(date), geo_length, geo_width, air_pressure, temperature)
#
#        return hor
#
#    @classmethod
#    def refraction(cls, h, temperature, air_pressure): # h in grad, nicht in Rad!
#        # h in rad umwandeln
#        h_degr = h
#        h = h * math.pi / 180
#        z = math.pi / 2 - h
#
#        if(h < 0): # nicht sichtbar
#            R = 0
#        elif((h * 180 / math.pi) > 15): # Refraktion über 15° -> Näherungsformel
#            R = 0.27 * air_pressure / (273.15 + temperature) * (
#            57.7 * math.tan(z) - 0.066 * (math.tan(z) ** 3))  # Refraktion
#            R = (R / 3600)  # von Sekunden in Grad umwandeln
#
#        else: # Refraktion unter 15° -> Lookup-Tabelle
#            low_val = cls.REFRACTION[0]
#            high_val = cls.REFRACTION[0]
#            R = 0
#            for refr in cls.REFRACTION:
#                low_val = high_val
#                high_val = refr
#                if(refr[0] > h_degr):
#                    break
#                elif(refr[0] == h_degr):
#                    R = 1 / refr[1]
#                    return R
#
#            dx = high_val[0] - low_val[0]
#            dy = high_val[1] - low_val[1]
#
#            R = (dx / dy * (h_degr - low_val[0])) + low_val[1] # lineare Interpolation
#            R = 1 / R       # Es sind die invertierten Werte gegeben
#
#        return R
#
#    @classmethod
#    def siderealTime(cls, date, lambd):
#        try:
#            T = float(date)
#        except:
#            T = Ephemeris.julianDate(date)
#
#        if ((T - int(T)) < 0.5):
#            day = float(int(T)) - 0.5
#        else:
#            day = float(int(T)) + 0.5
#
#        hours = (T - day) * 24
#
#        cent = (float(day) - 2451545.0) / 36525.0
#
#        # Formel von Wikipedia
#        gw_0h = 24110.54841 + 8640184.812866 * cent + 0.093104 * (cent ** 2.0) - 6.2e-6 * (
#        cent ** 3.0)  # Greenwich Sternzeit zum gewuenschten Tag um 0:00
#        gw_0h = (gw_0h / 3600.0)  # Sternzeit von Sekunden auf Stunden umrechnen
#        O = gw_0h + lambd / 15.0  # Position des Beobachters hinzufuegen
#        O = O + (cls.YEAR_STAR / cls.YEAR_TROPICAL) * hours  # Uhrzeit hinzufuegen
#        O = O % 24  # nur die Stunden sind interessant, die vergangenen Tage nicht
#
#        return O
#
#    @staticmethod
#    def angleToTime(angle):
#        # wandelt einen Winkel von 0-360 grad in eine Zeit von 0-24h um
#
#        h = angle / 15
#        m = (h - int(h)) * 60
#        s = (m - int(m)) * 60
#        us = (s - int(s)) * 1000000
#
#        h = int(h)
#        m = int(m)
#        s = int(s)
#        us = int(us)
#        return datetime.time(h, m, s, us)
#
#    @staticmethod
#    def angleToHours(angle):
#        # wandelt einen Winkel von 0-360 grad in eine Zeit von 0-24h um
#
#        h = angle / 15
#        m = (h - int(h)) * 60
#        s = (m - int(m)) * 60
#        us = (s - int(s)) * 1000000
#
#        h = int(h)
#        m = int(m)
#        s = int(s)
#        us = int(us)
#
#        hours = h + float(m) / 60 + float(s) / 3600 + float(us) / 3600 / 1000 / 1000
#        return hours
#
#    @staticmethod
#    def timeToAngle(time):
#        # wandelt eine Zeit von 0-24h in einen Winkel von 0-360 grad um
#        angle = (float(time.hour) + float(time.minute) / 60 + float(time.second) / 3600 + float(time.microsecond) / 3600 / 1000 / 1000) * 15
#        return angle
#
#    @staticmethod
#    def julianDate(date):
#        # julianisches Datum berechnen , input utc-date
#
#        k = float((4711 + date.year)) / 4  # julianische Perioden
#        tj1 = 366  # Tage im Jahr 4613 v. Chr. (Schaltjahr)
#        tj2 = int(k) * 1461  # Tage der vollstaendigen julianischen Perioden
#        tj3 = (k - int(k)) * 1460  # Tage der aktuellen julianischen Periode (bis jetzt)
#
#        tm = 0  # vergangene Tage von Jahresanfang bis Monatsbeginn
#        if (date.month > 2):
#            tm = 30.6 * date.month - 32.3
#            tm = int(tm)  # nur ganze Tage werden verwertet
#            if ((k - int(k)) == 0.75):  # Schaltjahr!
#                tm = tm + 1
#        elif (date.month == 2):
#            tm = 31
#
#        tt = date.day - 1  # heutiger Tag ist noch nicht vorbei -> -1!
#        tk = 13  # 13 Tage die ausgefallen sind (bis 2100!)
#        tastr = 0.5  # fuer die astronomische Skala - Tagesstart zu mittag!
#
#        tr = float(date.hour)  # restliche Zeit des angebrochenen Tages
#        tr = tr + float(date.minute) / 60
#        tr = tr + float(date.second) / 3600
#        tr = tr / 24
#
#        tsum = tj1 + tj2 + tj3 + tm + tt - tk - tastr + tr
#        return tsum
#
#    @staticmethod
#    def keplerEquation(m, e, tol):
#        # Kepler-Gleichung loesen
#        E = m
#        z = 0
#        while (m - z) > tol:
#            z = E - e * math.sin(E)
#            E = E + (m - z)
#
#        return E
#
#    @staticmethod    
#    def helioEclipticCoordinates(r, w, W, v, i): # Winkel in grad uebergeben!
#        # heliozentrisch Koordinaten des Planeten
#
#        # von grad in rad umrechnen
#        v = v * math.pi / 180
#        w = w * math.pi / 180
#        W = W * math.pi / 180
#        i = i * math.pi / 180
#
#        u = v + w
#        
#        x = r * (math.cos(u) * math.cos(W) - math.sin(u) * math.cos(i) * math.sin(W))
#        y = r * (math.cos(u) * math.sin(W) + math.sin(u) * math.cos(i) * math.cos(W))
#        z = r * (math.sin(u) * math.sin(i))
#       
#        return {"x" : x, "y" : y, "z" : z}
#
#    @staticmethod
#    def geoEclipticCoordinates(x_sh, y_sh, z_sh, x_se, y_se, z_se):
#        # geozentrisch ekliptikale Koordinaten
#        
#        x = x_sh - x_se
#        y = y_sh - y_se
#        z = z_sh - z_se       # die Erde liegt direkt in der Ekliptikebene, daher ist ihr z-Wert 0
#        
#        lambd = math.atan(y / x)
#        
#        if(x < 0):
#            lambd = lambd + math.pi
#        elif(y < 0):
#            lambd = lambd + 2 * math.pi
#        
#        beta = math.atan((z / x) * math.cos(lambd))
#        delta = z / math.sin(beta)
#        
#        return {"lambda" : lambd * 180 / math.pi, "beta" : beta * 180 / math.pi, "delta" : delta}
#    
#    @staticmethod
#    def equatorialCoordinates(lambd, beta, eps): # Winkel in grad uebergeben!
#        # geozentrisch-ekliptikale Koordinaten des himmelsgebundenen Aequatorsystems
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
#    @staticmethod
#    def horizontalCoordinates(alpha, delta, te, lambd, phi, air_pressure, temperature): # Winkel in grad uebergeben!
#        # horizontales Koordinatensystem
#
#        delta = delta * math.pi / 180
#        phi = phi * math.pi / 180
#
#        # Sternzeit
#        O = Ephemeris.siderealTime(te, lambd)
#        t = O - Ephemeris.angleToHours(alpha)   # Stundenwinkel
#
#        t = (t * 15) * math.pi / 180 # in rad umwandeln
#
#        h = math.asin(math.sin(delta) * math.sin(phi) + math.cos(delta) * math.cos(t) * math.cos(phi)) # horizontale Hoehe
#        z = math.pi / 2 - h  # Zenitdistanz
#
#        R = Ephemeris.refraction(h * 180 / math.pi, temperature, air_pressure)
#        R = R * math.pi / 180 # ins Bogenmaß zurückrechnen
#        hr = h + R # korrigierte Hoehe
#
#        # Azimut berechnen
#        sin_a = math.cos(delta) * math.sin(t) / math.cos(h) * (-1) # *(-1) weil Azimut in die entgegengesetzte Richtung gemessen wird
#        cos_a = (math.cos(delta) * math.cos(t) * math.sin(phi) - math.sin(delta) * math.cos(phi)) / math.cos(h) * (-1) # *(-1) weil Azimut in die entgegengesetzte Richtung gemessen wird
#
#        if((cos_a < 0) and (sin_a < 0)):    # 3. Quadrant
#            a = 2 * math.pi - math.acos(cos_a)
#        elif((cos_a > 0) and (sin_a < 0)):  # 4. Quadrant
#            a = 2 * math.pi + math.asin(sin_a)
#        else:
#            a = math.acos(cos_a)            # 1. & 2. Quadrant
#
#        return {"azimut" : a * 180 / math.pi, "hoehe_s" : hr * 180 / math.pi, "hoehe_r" : h * 180 / math.pi}
#
#
#
#test_date = datetime.datetime(2018, 3, 28, 9, 39)
#planet = "uranus"
#
## Für Greenwich
#"""
#horizontal_coordinates = Ephemeris.calcPositionHorizontal(planet, test_date, 0, 51.4825766, 1000, 1)
#aequatorial_coordinates = Ephemeris.calcPositionAequatorial(planet, test_date)
##"""
#
## Für Graz
##"""
#horizontal_coordinates = Ephemeris.calcPositionHorizontal(planet, test_date, 15.45836667, 47.06666944, 1021, 0)
#aequatorial_coordinates = Ephemeris.calcPositionAequatorial(planet, test_date)
##"""
#
#print(planet + " am " + str(test_date) + "\n")
#print("Echte horizontale Hoehe: " + str(horizontal_coordinates["hoehe_r"]) + "°")
#print("Scheinbare horizontale Hoehe: " + str(horizontal_coordinates["hoehe_s"]) + "°")
#print("Azimut: " + str(horizontal_coordinates["azimut"]) + "°")
#print("")
#print("Deklination: " + str(aequatorial_coordinates["delta"]) + "°")
#print("Rektaszension " + str(aequatorial_coordinates["alpha"]) + "°")
