# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 14:18:05 2019

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
# http://tdc-www.harvard.edu/catalogs/bsc5.html


# ---------------------------------------------------
# IMPORTS
import EPH_CORE_TimeSpaceMgr as TSMgr
import EPH_STAR_Starsearch as Starsearch





# ---------------------------------------------------
# ---------------------------------------------------
# CLASSES

class StarMgr:
    ''' Handles Stars as objects '''
    
    
    # aufruf in skyobjectmgr:
    # self._skyObject = StarMgr.StarMgr(TSMgrObj,identifier)

    def __init__(self, TSMgrObj, starSearchString:str):
        ''' Create a Star with a TSMgr and searchstring. '''
        
        # default values
        self._starObj =     None
        self._successStar = False
        self._successTSMgr = False
        
        self._TSMgr = TSMgrObj   # reference to the global TSMgr
        # check if the TimeSpaceMgrObj is a TSMgr object
        self._successTSMgr = (type(self._TSMgr)==TSMgr.TimeSpaceMgr)
        
        # fahre nur fort, wenn valider TSMgr vorhanden
        if (self.__get_successTSMgr()):
            # erstelle datetimeObj für aktuelle sternenpos
            self._datetimeObj = (self._TSMgr).time_get_utcDateTime()
            
            # erstelle starObj mit suchstring und _datetimeObj
            self._starObj = Starsearch.getStarPos(
                    starSearchString, self._datetimeObj)
            
            self._successStar = (self._starObj != None)
        
        
    # ---------------------------------------------------
    
    def __get_successStar(self):
        ''' returns whether the STAR was created successfully '''
        return self._successStar;

    def __get_successTSMgr(self):
        ''' returns whether the STAR has valid TSMgr member variable '''
        return self._successTSMgr;

    def get_success(self):
        ''' returns whether all init actions were successful '''
        return all(
                [self.__get_successStar(), 
                 self.__get_successTSMgr()]
                );
    # ---------------------------------------------------
    
    def getPos(self):
        ''' returns dict of {'Ra', 'De'} in degrees (or None if error) '''
        if self.get_success():
            return {"Ra": self._starObj["Ra"], "De": self._starObj["De"]}
        else:
            return None
    
    def getPosRa(self):
        ''' returns number of 'Ra' in degrees (or None if error) '''
        if self.get_success():
            return self._starObj["Ra"]
        else:
            return None
    
    def getPosDe(self):
        ''' returns number of 'De' in degrees (or None if error) '''
        if self.get_success():
            return self._starObj["De"]
        else:
            return None
    
    def getName(self):
        return self._starObj["name"]






