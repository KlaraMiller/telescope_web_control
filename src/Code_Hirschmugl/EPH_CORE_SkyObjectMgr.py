# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 16:25:45 2019

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

"""


import EPH_CORE_TimeSpaceMgr as TSMgr
import EPH_SAT_SatelliteMgr as SatMgr
import EPH_PLANET_PlanetMgr as PlanetMgr
import EPH_STAR_StarMgr as StarMgr
import EPH_MOON_MoonMgr as MoonMgr



class SkyObjectMgr:
    ''' deals with all allowed sky objects. '''

    ################################################################
    #### STATIC / CLASS VARIABLES


    ################################################################
    #### INIT

    def __init__(self, TSMgrObj, skyObjType:str, identifier=None ):
        ''' TimeSpaceManager Instance, type of sky object, identifier '''
        
        constrString = ("Constructor for Type: '"+str(skyObjType)+
                        "' ("+str(identifier)+"): ")
        self._cnstrMsg = (constrString+"failed immediatly.") # immediate fail
        
        self._success = False
        self._skyObject = None
        
        self._skyObjName = identifier
        self._skyObjType = skyObjType
        
        if(type(TSMgrObj)==(TSMgr.TimeSpaceMgr)):
            # Wenn TSMgrObj wirklich ein TSMgr.TimeSpaceMgr objekt ist
            self._TSMgr = TSMgrObj
        
            if  (skyObjType.lower() in ["planet"]):
                # TODO: implementierung
                # wenn typ = planet
                self._skyObjType = "planet"
                self._skyObject = PlanetMgr.PlanetMgr(self._TSMgr,identifier)
                
            elif(skyObjType.lower() in ["star"]):
                # wenn typ = stern
                self._skyObjType = "star"
                self._skyObject = StarMgr.StarMgr(self._TSMgr,identifier)
                self._skyObjName = str(self._skyObject.getName())
                
            elif(skyObjType.lower() in ["moon"]):
                # TODO: implementierung
                # wenn typ = Mond
                self._skyObjType = "moon"
                self._skyObject = MoonMgr.MoonMgr(self._TSMgr)
                
            elif(skyObjType.lower() in ["sat","satellite"]):
                # wenn typ = satellit
                
                self._skyObjType = "satellite"
                
                
                tempID = identifier
                
                # für den fall einer string eingabe
                if type(tempID) == str:
                    tempID = tempID.strip()
                    
                    if tempID.isnumeric():
                        tempID = int(tempID)
                    
                if type(tempID) == int:
                    # geht nur für int eingabe (bzw erkennbarer int-string)
                    self._skyObject = SatMgr.SatelliteMgr(self._TSMgr,tempID)
                
            else:
                # wenn typ = UNBEKANNT
                self._cnstrMsg = (constrString+
                                  "failed - unknown 'skyObjType' string.")
            
        else:
            # this is not a TSMgr object!
            self._cnstrMsg = (constrString+
                              "failed - 'TSMgrObj' must be of type "+
                              str(type(TSMgr.TimeSpaceMgr()))+".")
        
        
    def get_pos_spherical(self, utcTime = None):
        #set TSMgr to utcTime (if None, then utcNow)
        self._TSMgr.time_set_utcDateTime(utcTime)
        
#       TODO: für alle implementieren
        if self._skyObject != None:
            # wenn skyObject existiert
            
            if self._skyObjType in ["planet","star","satellite","moon"]:
                # wenn type eine umsetzung hat (atm star und sat)
                pos = self._skyObject.getPos()
                if pos != None:
                    return {"Ra":       pos['Ra'], 
                            "De":       pos['De'],
                            'Success':  self._skyObject.get_success()}
                else:
                    return None
            else:
                return None
        else:
            # wenn kein skyobject existiert
            return None
        
    
    def write_pos_to_dict(self, destDict: dict, utcTime = None):
        ''' writes Ra, De and Success to a provided dictionary.
            (OPTIONAL: get the pos for a specific utc datetime) '''
        # get pos for specified utctime (inf none, then utcNow)
        temp = self.get_pos_spherical(utcTime)
        
        if(temp != None):
            # if it has a return value, then write this to dict
            destDict['Ra'] =        temp['Ra']
            destDict['De'] =        temp['De']
            destDict['Success'] =   temp['Success']
        else:
            # if it returns none, then return default none values
            destDict['Ra'] =        None
            destDict['De'] =        None
            destDict['Success'] =   False
    
    
    def get_type(self):
        return self._skyObjType
    
    def get_name(self):
        return self._skyObjName
    
    
    
    
    
    
    
    
    
    
    