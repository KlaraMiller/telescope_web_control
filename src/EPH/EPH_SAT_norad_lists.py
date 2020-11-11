# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:08:21 2019

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
__relative_path = "EPH_SAT_from_celestrak/"
__url_celestrak_elements = "http://celestrak.com/NORAD/elements/"


sat_list =   ("stations.txt",
              "weather.txt",
              "noaa.txt",
              "goes.txt",
              "resource.txt",
              "sarsat.txt",
              "goes.txt",
              "dmc.txt",
              "tdrss.txt",
              "argos.txt",
              "planet.txt",
              "spire.txt",
              "geo.txt",
              "intelsat.txt",
              "ses.txt",
              "iridium.txt",
              "iridium-NEXT.txt",
              "orbcomm.txt",
              "globalstar.txt",
              "amateur.txt",
              "x-comm.txt",
              "other-comm.txt",
              "satnogs.txt",
              "gorizont.txt",
              "raduga.txt",
              "molniya.txt",
              "gps-ops.txt",
              "glo-ops.txt",
              "galileo.txt",
              "beidou.txt",
              "sbas.txt",
              "nnss.txt",
              "musson.txt",
              "science.txt",
              "geodetic.txt",
              "engineering.txt",
              "education.txt",
              "military.txt",
              "radar.txt",
              "cubesat.txt",
              "other.txt"
              )

def keep_file():
    relative_path = __relative_path
    
    f_keep = open(relative_path+"/.keep","w")
    f_keep.write("# dummy file to keep the folder\n")
    f_keep.close()
    

def get_norad_age():
    ''' returns the first line in "_last_update.txt" '''
    import datetime
    from pathlib import Path
    
    #
    keep_file() # for gitignore
    #
    
    relative_path = __relative_path
    file_path = relative_path+"/_last_update.txt"
    
    # verwende pathlib, um herauszufinden, ob das file existiert
    test_path = Path(file_path)
    
    if test_path.is_file():
        # wenn file existiert
    
        # lies die erste zeile aus "_last_update.txt"
        f_update = open(file_path)
        line_full = f_update.readline().strip()
        f_update.close()
    else:
        # wenn file nicht existiert
        # stoppe funktion und returne fehler string
        return '[Missing "_last_update.txt"]'
    
    
    #versuche ein datetime object zu erstellen
    if len(line_full) >= 19:
        line = line_full[:19]
        
        # 2019-02-21 00:00:00
        try:
            date = datetime.datetime.strptime(line,"%Y-%m-%d %H:%M:%S")
        except:
            date = "[{}]".format(line_full)
            
        return date
        
    elif len(line_full) >= 10:
        line = line_full[:10]
        
        # 2019-02-21 00:00:00
        try:
            date = datetime.datetime.strptime(line,"%Y-%m-%d")
        except:
            date = "[{}]".format(line_full)
        return date
        
    else:
        # wenn nicht möglich, dann einfach lineStr zurückgeben
        return "[{}]".format(line_full)
    

def retrieve_norad_tle_from_url(filename=None):
    ''' retrive file.txt from "http://celestrak.com/NORAD/elements/" '''
    
    import datetime
    
    #
    keep_file() # for gitignore
    #
    
    if(try_connect_to_celestrak()):
        # nur, wenn internet connection vorhanden
    
        relative_path = __relative_path
        url = __url_celestrak_elements
        
        if(hasattr(filename,'__iter__')):
            print("Retrieving ["+str(filename)+"] from ["+str(url)+"].")
            
            dt = datetime.datetime.utcnow()
            
            if (filename[-4:]==".txt"):
                __try_retrieve_from_url(filename, url, relative_path)
            else:
                print("Filenames must be strings, that end in '.txt'.")
                
            dt = datetime.datetime.utcnow() - dt
            print("Retrieving process completed. Time taken: "+str(dt)+".")
            print("If any failed, check the used filename.")
            
        else:
            st1 = "Retrieving ALL known satellite TLE files ("+str(len(sat_list))
            st2 = ") from ["+url+"]. (this may take about 30s.)"
            print(st1+st2)
            
            dt = datetime.datetime.utcnow()
            
            index=0
            for element in sat_list:
                #Progress indicator
                index = index+1
                if(index >= len(sat_list)/10): 
                    index = index - len(sat_list)/10
                    print('.', end='')
                
                #try to retreive
                __try_retrieve_from_url(element, url, relative_path)
            # END for ----------------------------
            
            dt = datetime.datetime.utcnow() - dt
            print("\nRetrieving process completed. Time taken: "+str(dt)+".")
            print("If any failed, check 'sat_list' tuple.")
        
        # write date for last update to "_last_update.txt"
        f_update = open(relative_path+"/_last_update.txt","w")
        f_update.write(str(datetime.datetime.utcnow())+"\n")
        f_update.close()
        
        
def __try_retrieve_from_url(filename, url=None, to_relative_path=None):
    import urllib
    
    if(try_connect_to_celestrak()):
        # nur, wenn internet connection vorhanden
        
        # default values
        if(url==None): url=__url_celestrak_elements
        if(to_relative_path==None): to_relative_path = __relative_path
        
        
        # test if valid url to a TLE file
        response = urllib.request.urlopen(url+filename)
    #    data = response.read()      # a `bytes` object
    #    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
        t1=response.readline()                  #ignore first line
        t1=response.readline().decode('utf-8')  #save 2nd line
        t2=response.readline().decode('utf-8')  #save 3rd line
        
        if((t1[0:2]=="1 ")and(t2[0:2]=="2 ")):
            # seems to be a correct file (at least the first 2 lines)
            try:
                urllib.request.urlretrieve(url+filename, to_relative_path+filename)
            except:
                print("Could not retrieve ["+filename+"].")
        else:
            # seems to be an incorrect file
            print("Could not retrieve ["+filename+"].")


def try_connect_to_celestrak():
    import urllib
    
    url = __url_celestrak_elements
    
    try:
        # try get response from url / check if internet connection exists
        urllib.request.urlopen(url)
    except:
        return False
    else:
        return True
    