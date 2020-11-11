# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 13:09:46 2019

@author: polsterc16
"""


import datetime

import EPH_CORE_SkyObjectMgr as SOMgr
import EPH_CORE_TimeSpaceMgr as TSMgr
import EPH_ADD_math_helper as MH


def main():
    
    tnow = datetime.datetime(2019, 3, 30, 0)
    #tnow = datetime.datetime.utcnow()
    
    # GREENWICH
    tele = (("N",51+28/60+40.12/3600), ("E",0), 0)
    
    skyObj = None
    pos={} # leeres dict für positionen
    
    
    
    
    # erstelle TSMgr Objekt
    myTS = TSMgr.TimeSpaceMgr(tnow, tele[0], tele[1], tele[2])
    
    # setze auf utcNow
    #myTS.time_set_utcNow()
    
    
    
    # -------------------------
    # dieser prozess kann zeit dauern!
    # benötigt internet verbindung und dass die celestrak website
    # noch existiert.
    maxAge = 0.5
    print("\nTLE age: {}".format(myTS.norad_get_age_in_days_str()))
    print("(update TLE if older than {:.2f} days)".format(maxAge))
    myTS.norad_update_if_older_than_days(maxAge)
    # -------------------------
    
    
    # testliste
    objList = [
            ["planet","mars"],
            ["sat", "25544"], #ISS
            ["star","Alpheratz"],
            ["star","BD+28°4"],
            ["star","HR:8998"],
            ["star","HR:8999"],
            ["moon",None]
            ]
    
    
#    for obj in objList:
#        #erstelle skyObject
#        skyObj = SOMgr.SkyObjectMgr(myTS,obj[0],obj[1])
#        
#        # hole aktuelle postion in "pos"
#        skyObj.write_pos_to_dict(pos,tnow)
#        
#        # AUSGABE
#        print("")
#        print(myTS.time_get_utcDateTime()) #utc zeit
#        
#        # typ: name
#        print(str(skyObj.get_type())+": "+str(skyObj.get_name()))
#        
#        # position
#        print(pos)
#    
#    
#    print("\n\ntest moon:")
#    
#    month_prev = 0
#    month = 0
#    for k in range(0,365):
#        
#        tnow = datetime.datetime(2019, 1, 1, 0) + datetime.timedelta(k)
#        month_prev = month
#        month = tnow.month
#        day = tnow.day
#        
#        skyObj = SOMgr.SkyObjectMgr(myTS,"moon",None)
#        
#        # hole aktuelle postion in "pos"
#        skyObj.write_pos_to_dict(pos,tnow)
#        
#        
#        # position
#        pos_ra = pos["Ra"]
#        pos_de = pos["De"]
#        
#        if month>month_prev:
#            print("")
#        
#        # AUSGABE
#        print("{:02}-{:02}".format(month,day)+"  Ra: "+MH.deg_deg2hms(pos_ra)+"  De: "+MH.deg_deg2dms(pos_de))
        
    

# exectute, if this is the main file
if __name__ == "__main__":
    main()





