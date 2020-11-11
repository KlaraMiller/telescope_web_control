# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:37:05 2019

@author: polsterc16
"""


__relPath = "EPH_STAR_BrightStarCatalogue"




def getStarPos(finder="Polaris", year=None):
    ''' INPUTS:
    * finder: 
        + string mit sternenname (durchsucht tags) ODER
        + tuple mit id-typ(string) und id zB ("sao", 123)
    * optional: year als zahl oder datetime.dateime obj (default: utcnow)
    
    OUTPUTS:
        dict mit name (list), Ra, De und bscElements und bscLine '''
    
    import datetime
    
    # hole star info
    myStar = __getStarInfo(finder)
    if(myStar==None):
        #print("no star found")
        # wenn kein stern gefunden, dann stoppe
        return None
    
    # wenn kein year mitübergeben
    if year == None:
        year = datetime.datetime.utcnow()
        
    # yearDelta = years since 2000
    if type(year)==int or type(year)==float:
        # wenn year vom type zahl ist
        yearDelta = float(year-2000)
    elif type(year) == datetime.datetime:
        # wenn year vom typ datetime ist
        yearDelta = (year - datetime.datetime(2000,1,1)).days/365.25
    else:
        # wenn year von unbekannten typ ist, stoppe
        return None
    
    if yearDelta < 0:
        # diese funktion bricht ab, wenn year < 2000 bzw deltayear < 0
        return None
    
    
    
    
    # right ascencion ist in hhmmss angegeben
    
    Ra = (myStar["bsc"]["rah"] +      # ra stunden 
          myStar["bsc"]["ram"]/60 +   # ra minuten
          myStar["bsc"]["ras"]/3600   # ra sekunden
          ) * 360/24                  # conversion stunden zu degrees
    
    # änderung der RA in winkelsec/jahr
    # pmra = d(ra)/dt in arcsec/year
    # ra_today = ra_J2000 + pmra*(today-2000)
    Ra = Ra + myStar["bsc"]["pmra"]/3600*yearDelta
    
    
    # declination ist in °'" angegeben
    
    # de vorzeichen
    if(myStar["bsc"]["de-"]=="-"):
        vz = -1
    else:
        vz = 1
    
    #declination calculated in degrees
    De = (myStar["bsc"]["ded"] +            # de grad
          myStar["bsc"]["dem"]/60 +         # de winkelmin
          myStar["bsc"]["des"]/3600) * vz   # de winkelsec und vorzeichen
    
    # änderung der de in winkelsec/jahr
    # pmde = d(de)/dt in arcsec/year
    # de_today = de_J2000 + pmde*(today-2000)
    De = De + myStar["bsc"]["pmde"]/3600*yearDelta
    
    # returnval ist dict 'temp' mit namen, ra, de und bsc info (für debuggen)
    temp = {"name": ["Input: '"+str(finder)+"'"],   # füge sofort den suchbegriff dazu
            "Ra":   Ra,
            "De":   De,
            "bsc":  myStar["bsc"],
            "bscLine":  myStar["bscLine"]}
    
    if myStar["bsc"]["name"].strip() != "":
        # wenn name in BSC existiert, dann füge diesen ein
        temp["name"].append("name: {}".format(myStar["bsc"]["name"]))
    
    # und für hr zum namen dazu
    temp["name"].append("hr: {}".format(myStar["bsc"]["hr"]))
    
    return temp




def searchDictKeyListForStr(dictio, match):
    ''' Function durchsucht dict nach Match (nur eine ebene tief).
        nur strings und liste von strings sind zulässig als dict entries! '''
    
    # dictio muss dictionary sein und match muss String sein
    if (type(dictio)!=dict or type(match)!=str):
        return None
    
    target = match.lower()     # search will take place in lower case
    
    
    for key in dictio:
        content = dictio[key]   # variable für inhalt zu key
        
        # untersuche key
        if type(key) == str:
            if target == key.lower():
                # der key ist bereits der gesuchte string
                return key.lower()
        else:
            # es sind zur string keys zulässig (sollte nicht eintreffen)
            return None
        
        #untersuche content
        if type(content) == str:
            # der keyinhalt ist ein str
            if target == content.lower():
                # und ist der gesuchte string
                return key.lower()
            
        elif type(content) == list:
            # der keyinhalt ist eine liste
            for elem in content:
                # überprüfe für jedes element in der content liste
                if type(elem) == str:
                    # wenn die elemente in der content liste strings sind
                    if target == elem.lower():
                        return key.lower()
            
        else:
            # der keyinhalt ist nicht für diese funktion gedacht
            return None
    
    
    # wenn nichts gefunden wurde
    #print("[es wurde nichts gefunden]")
    return None
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



def get_strDict_for_BSC_input_format():
    ''' returns dictionary filled with instructions on correct searching
        of Stars in the BSC ''' 
        
    returnDict={}
    returnDict["info"]= str("Only Stars in the Harvard Revised "+
              "'Bright Star Catalogue' (over 9000 entries for all stars with "+
              "stellar magnitude of 6.5 or brighter) are available!\n"+
              "Inputs have to be in the sequence of input format (if any) "+
              "and according to the format, as the parser uses this to "+
              "recognize the input format.")
    returnDict["id"]= str("SEARCH BY STAR CATALOGUE ID:\n"+
              "Format: ['ID-Type', ':', 'ID'], "+
              "(eg. 'sao: 252838' for Alpha 1 Centauri).\n"+
              "HR (Harvard Revised 'Bright SC'), "+
              "SAO (Smithsonian Astrophysical Observatory SC), "+
              "HD (Henry Draper SC) are valid ID-Type options.\n"+
              "'ID-Type' and 'ID' MUST be seperated by ':'!")
    returnDict["dm"]= str("SEARCH BY DURCHMUSTERUNG: "+
              "Format: ['DM-Type', 'Zone', 'Number'] "+
              "(eg. 'BD-16 1591' for Sirius).\n"+
              "BD (Bonner DM), CD (Cordoba DM), CP (Cape Photographic DM) "+
              "are valid DM-Type options.\n"+
              "'DM-Type' and 'Zone' CAN be seperated by ' ', "+
              "but 'Zone' MUST be a signed integer (preceeded by '+' or '-'). "+
              "'Zone' and 'Number' must be seperated by ' ' or '°' (or both).")
    returnDict["bayer"]= str("SEARCH BY BAYER DESIGNATION: "+
              "Format: ['greek letter', ',', 'constellation'] or "+
              "['greek letter', ',', 'Number' , ',', 'constellation'] "+
              "(eg. 'Beta, Aquarii' or 'Alpha, 1, cen').\n"+
              "The Seperator is a ',' since constellations may have spaces "+
              "in their names (eg. 'Corona Australis'). Allowed inputs are "+
              "romanized Greek Letters and contellation names (nominative or "+
              "genitive form of its Latin name: 'Beta, Aquarius' or "+
              "'Beta, Aquarii'). The IAU short versions are also possible "+
              "inputs (eg. 'Bet, aqr').")
    returnDict["flamsteed"]= str("SEARCH BY FLAMSTEED DESIGNATION: "+
              "Format: ['number', ',', 'constellation'] "+
              "(eg. '22, Aquarii').\n"+
              "The Seperator is a ',' since constellations may have spaces "+
              "in their names (eg. 'Corona Australis'). Allowed inputs are "+
              "numbers and contellation names (nominative or "+
              "genitive form of its Latin name: 'Beta, Aquarius' or "+
              "'Beta, Aquarii'). The IAU short versions are also possible "+
              "inputs (eg. '22, aqr').")
    returnDict["name"]= str("SEARCH BY IAU NAME: "+
              "Format: ['name'] "+
              "(eg. 'Sirius').\n"+
              "When searching by proper name, no seperators of the other "+
              "search formats are allowed. ' ' is allowed since some "+
              "star names bay contain spaces. This will only find stars "+
              "by their approved IAU names.")
    
    return returnDict
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



def parse_text_for_BSC_search(text):
    ''' returned tuple für bsc suche aus suchtext'''
    #THIS FUNCTION ONLY WORKS WITH A STRING
    if( type(text) != str ):
        return None
    
    import EPH_STAR_Starlist as Starlist
    
    
    idList =    ["sao","hr","hd"]   # liste für die zuglassenen idTypen
    idSep =     ":"                 # seperators für die angabe von ids
    
    dmList =    ["cp","cd","bd"]    # liste für durchmusterungen
    dmSep =     "°"
    signList =  ["+","-"]
    
    nameSep =   ","     #bayer flamsteed name seperator
    
    returnVal = None
    typeSearch = None
    
    
    a = text.lower()    # zur vereinfachung nur mit lower case arbeiten
    
    # CASE unterscheidung
    if (idSep in a) and not( any(k in a for k in signList) ):
        # string enthält id seperator
        typeSearch = "id"
    elif any(k in a for k in signList) and not(idSep in a):
        # string enthält dm seperator
        typeSearch = "dm"
    elif (nameSep in a):
        # string enthält seperator für Bayer and/or Flamsteed name
        typeSearch = "bayerflamsteed"
    else:
        # sonst versuche eigennamen zu finden
        typeSearch = "ownname"
        
    
    
    # CASE id
    if (typeSearch == "id"):
        # versuche für ID Search zu parsen
        
        # füge spaces um den idSep ein
        b = a.replace(idSep,str(" "+idSep+" ")) 
        b = b.split()     # teile den text
        
        if(len(b)==3):
            # WENN 3 elemente nach split vorhanden sind (zB ["idtyp",":","id"})
            # DANN kann es das richtige format für id eingabe haben
            
            if (b[0] in idList and b[1] == idSep and b[2].isdigit() ):
                # WENN richtige formatierung für id eingabe
                
                # DANN kann nach entsprechender id nummer gesucht werden
                returnVal = ( b[0], int(b[2]) )     # (idTyp, id)
    # END CASE id --------------------------------------
    
    
    # CASE dm
    if (typeSearch == "dm"):
        # versuche für DM Search zu parsen
        
        b = a.replace(dmSep," ")    # ersetze dmSep mit space
        
        
        for k in signList:
            b = b.replace(k,str(" "+k))     # vor jedem sign ein space
            b = b.replace(str(k+" "),k)     # nach jedem sign kein space
        
        b = b.split()     # teile den text
        
        if(len(b)==3):
            # WENN 3 elemente nach split vorhanden sind 
            #   (zB ['DM-Type', 'Zone', 'Number'})
            # DANN kann es das richtige format für DM eingabe haben
            
            dmType =    b[0]
            zoneSign =  b[1][0]
            zoneNum =   b[1][1:]
            dmNum =     b[2]
            
            tt = []     # simple truth table list
            tt.append(dmType in dmList)     # ist richtiger 'DM-Type'?
            tt.append(zoneSign in signList) # ist 'Zone' ein signed int?
            tt.append(zoneNum.isdigit())    # ist 'Zone' ein signed int?
            tt.append(len(zoneNum) <= 2)    # ist 'Zone' <= 2 ziffern groß?
            tt.append(dmNum.isdigit())      # ist 'Number' eine zahl?
            tt.append(len(dmNum) <= 5)      # ist 'Number' <= 5 ziffern groß?
            
            if all(k==True for k in tt):
                # WENN richtige formatierung für DM eingabe
                
                # FORMAT     DDsZZnnnnn
                # EXAMPLE    BD-16 1591
                searchTerm = "{}{}{:02d}{:5d}".format(
                        dmType.upper(), zoneSign, int(zoneNum), int(dmNum) )
                
                # DANN kann nach entsprechender DM gesucht werden
                returnVal = ("dm", searchTerm)
    # END CASE dm --------------------------------------
    
    
    # CASE bayerflamsteed
    if (typeSearch == "bayerflamsteed"):
        # versuche für namens bayerflamsteed Search zu parsen
        stopBayerFlam = False
        num =       "num"
        greek =     "greek"
        constel =   "constel"
            
        # formatierungen für bayer und flamsteed
        flamsteed = [num,constel]
        bayer =     [greek,constel]
        bayer2 =    [greek,num,constel]
        
        
        b = a.split(nameSep)    # teile den text an kommastellen
        for index in range(len(b)):
            b[index]=b[index].strip()  # entferne spaces links und rechts
        
        
        parseType = []
        parseName = []
        
        for k in b:
            # untersuche den namensstring auf seine komponenten
            if k.isnumeric():
                # k ist eine zahl
                parseType.append(num)
                parseName.append(k)
            else:
                # überprüfe, ob k ein griech. buchstabe oder
                #   ein konstellationsname ist
                p1 = searchDictKeyListForStr(Starlist.GLL, k)
                p2 = searchDictKeyListForStr(Starlist.CAL, k)
                
                if p1 != None:
                    parseName.append(p1)
                    parseType.append(greek)  # ist griech. buscht.
                elif p2 != None:
                    parseName.append(p2)
                    parseType.append(constel) # ist constel. name
                else:
                    parseType.append(None)     # other - falsche eingabe
                    #print("unbekannter typ in [bayerflamsteed]")
                    stopBayerFlam = True
        # END for loop -------------------------
        
        if not(stopBayerFlam):
            # nur weitermachen, wenn jedes element erkannt wurde
            
            if parseType == flamsteed:
                # wenn flamsteed
                r1 = str(parseName[0]).rjust(3)
                r2 = parseName[1]
                returnVal = ( "flamsteed", (r1, r2) )
                
            elif parseType == bayer:
                # wenn bayer zB: 
                returnVal = ( "bayer", (parseName[0], None, parseName[1]) )
                
            elif parseType == bayer2:
                # wenn bayer2 zB Alpha, 2, centauri
                if len(parseName[1])==1:
                    # nur zahlen von 1-9 sind zulässig (zb alpha, 1, cen)
                    returnVal = ( 
                            "bayer", (parseName[0], parseName[1], parseName[2]) )
        
        # wenn nichts gefunden wurde, dann bleibt returnVal auf None
    # END CASE bayerflamsteed --------------------------------------
    
    
    # CASE ownname
    if (typeSearch == "ownname"):
        # versuche für ownname Search zu parsen
        
        SL =    Starlist.SL
        b =     a.strip()
        hr =    None
        
        for key, dictio in SL.items():
            # für alle key, Dictionaries in SL
            for elem in dictio['tags']:
                # für alle elemente in 'tags' eintrag von dictionary
                if b == elem.lower():
                    # wenn gesuchter ownname in tags gefunden wurde,
                    # dann hole hr id und stoppe for schleife
                    hr = dictio['hr']
                    break
        
        if hr != None:
            # wenn hr gefunden wurde
            returnVal = ('hr', hr)
        
    # END CASE ownname --------------------------------------
    
    
    # wenn nichts gefunden wurde, wird None zurückgegeben
    return returnVal
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 













def __getStarInfo(text):
    ''' returns various bsc tags for entered search string. 
        see get_strDict_for_BSC_input_format() for format restrictions. 
        (firstly, the searchtext gets parsed, then the bscLine is extracted
        based on the type of search and finally the bsc elements are
        extracted from the found bscLine which are then returned) '''
    
    # parse den suchtext, um fertiges suchtuple (finder) zu erhalten
    finder =    parse_text_for_BSC_search(text)
    if finder == None:
        # abbrechen: eingabe kann nicht geparst werden
        return None
    
    # default val
    starInfo =  None
    bscLine =   None
    tag_hr =    "hr"
    tag_hd =    "hd"
    tag_sao =   "sao"
    tag_dm =    "dm"
    tag_bayer = "bayer"
    tag_flamsteed = "flamsteed"
    
    
    # fallunterscheidung für die art der suche bzw der formatierung
    # des suchtexts: bscLine wird extrahiert
    
    #CASE hr, hd, sao
    if finder[0] in [tag_hr,tag_hd,tag_sao]:
        bscLine = __get_BSC_line_from_ID(finder[0],finder[1])
    
    #CASE DM
    if finder[0] == tag_dm:
        bscLine = __get_BSC_line_from_DM(finder[1])
    
    #CASE bayer
    if finder[0] == tag_bayer:
        bscLine = __get_BSC_line_from_bayer(finder[1])
    
    #CASE bayer
    if finder[0] == tag_flamsteed:
        bscLine = __get_BSC_line_from_flamsteed(finder[1])
    
    if bscLine == None:
        # abbrechen: keine bsc line gefunden
        return None
    
    
    # bsc elemente werden extrahiert (aus der angegebenen bscLine)
    starInfo = __get_elem_from_BSC_line(bscLine)
        
        
    # wenn nicht gefunden, wird default wert (none) übergeben
    # wenn gefunden, wird starInfo (befülltes dict) übergeben
    return starInfo



def __get_BSC_line_from_flamsteed(flamsteed_tuple):
    ''' returns bsc line for corresponding flamsteed_tuple ''' 
    
    if type(flamsteed_tuple) != tuple:
        # muss ein string sein
        return None
    elif len(flamsteed_tuple) != 2:
        # bayer_tuple muss länge 2 haben, zb "12,cen"
        return None
    
    import EPH_STAR_Starlist as Starlist
    correspond = Starlist.Correspond
    
    index_l = correspond["name"][0]-1
    index_r = correspond["name"][1]
    #castto =  correspond["dm"][2]  # redundant
    EMPTY =   correspond["EMPTY"]
    
    bscLine = None # default return value 
    
    f1 = [0,3]  # fields to match
    f2 = [7,10]
    m1 = flamsteed_tuple[0]     # match values
    m2 = flamsteed_tuple[1]
    
    
    f = open(__relPath+"/bsc5.dat")
    
    for line in f: #FOR LOOP 
        if len(line)>=index_r: # if -----------------------------
            # geht nur, wenn die line lang genug für die indexe ist
            
            # hole den interessanten slice aus der line heraus
            temp = line[index_l:index_r].lower()
            
            if temp == EMPTY[index_l:index_r]:
                # wenn die herausgegriffene stelle nur whitespaces hat,
                # dann kann mit dem tag nichts gefunden werden
                bscLine = None
            else:
                # vergleiche die 2 elemente von der flamsteed designation
                # schreibe in truth variablen
                t1 = m1 == temp[f1[0]:f1[1]]
                t2 = m2 == temp[f2[0]:f2[1]]
                
                if t1 and t2:
                    # wenn alle 2 zutreffen, dann line zurückgeben
                    bscLine = line
                    break
        # END if len(line)>=index_r ---------------------
    # END FOR LOOP 
    
    return bscLine



def __get_BSC_line_from_bayer(bayer_tuple):
    ''' returns bsc line for corresponding bayer_tuple ''' 
    
    if type(bayer_tuple)!=tuple:
        # muss ein string sein
        return None
    elif len(bayer_tuple) != 3:
        # bayer_tuple muss länge 3 haben, zb "alp,None,cen"
        return None
    
    import EPH_STAR_Starlist as Starlist
    correspond = Starlist.Correspond
    
    index_l = correspond["name"][0]-1
    index_r = correspond["name"][1]
    #castto =  correspond["dm"][2]  # redundant
    EMPTY =   correspond["EMPTY"]
    
    bscLine = None # default return value 
    
    f1 = [3,6]  # fields to match
    f2 = [6,7]
    f3 = [7,10]
    m1 = bayer_tuple[0] # match values
    m2 = bayer_tuple[1]
    m3 = bayer_tuple[2]
    
    
    f = open(__relPath+"/bsc5.dat")
    
    for line in f: #FOR LOOP 
        if len(line)>=index_r: # if -----------------------------
            # geht nur, wenn die line lang genug für die indexe ist
            
            # hole den interessanten slice aus der line heraus
            temp =  line[index_l:index_r].lower()
            
            if temp == EMPTY[index_l:index_r]:
                # wenn die herausgegriffene stelle nur whitespaces hat,
                # dann kann mit dem tag nichts gefunden werden
                bscLine = None
            else:
                # vergleiche die drei elemente von der bayer designation
                # schreibe in truth variablen
                t1 = m1 == temp[f1[0]:f1[1]]
                t3 = m3 == temp[f3[0]:f3[1]]
                
                # unterscheidung für spezialfall, dass keine nummer
                # mitgegeben wurde (zb 'alp,None,cen')
                if m2 == None:
                    # wenn 'num'==None, 
                    # dann ist ' ' und '1' zulässig an der stelle
                    t2 = ( '1'== temp[f2[0]:f2[1]] or ' '== temp[f2[0]:f2[1]] )
                else:
                    # sonst vergleiche mit übergebener nummer
                    t2 = m2 == temp[f2[0]:f2[1]]
                
                if t1 and t2 and t3:
                    # wenn alle 3 zutreffen, dann line zurückgeben
                    bscLine = line
                    break
        # END if len(line)>=index_r ---------------------
    # END FOR LOOP 
    
    return bscLine



def __get_BSC_line_from_ID(id_type,id_num):
    ''' returns bsc line for corresponding id ''' 
    
    if not(id_type in ["hr","hd","sao"]):
        # muss ein valider id type sein
        return None
    
    num = None
    
    #überprüfe, ob nummer oder num string übergeben wurde
    if type(id_num) == str:
        if id_num.strip().isnumeric():
            num = int(id_num.strip())
    elif type(id_num) == int:
        num = id_num
        
    if num == None:
        # wenn keine nummer übergeben wurde, endet die funktion hier
        return None
    
            
    import EPH_STAR_Starlist as Starlist
    correspond = Starlist.Correspond
    
    index_l = correspond[id_type][0]-1
    index_r = correspond[id_type][1]
    #castto =  correspond[id_type][2]
    EMPTY =   correspond["EMPTY"]
    
    bscLine = None
    
    
    f = open(__relPath+"/bsc5.dat")
    
    for line in f: #FOR LOOP 
        if len(line)>=index_r: # if -----------------------------
            # geht nur, wenn die line lang genug für die indexe ist
            
            # hole den interessanten slice aus der line heraus
            temp =  line[index_l:index_r]
            
            if temp == EMPTY[index_l:index_r]:
                # wenn die herausgegriffene stelle nur whitespaces hat,
                # dann kann mit dem tag nichts gefunden werden
                bscLine = None
            else:
                temp = temp.strip() # entferne whitespaces links und rechts
                
                if temp.isnumeric():
                    # wenn es eine string zahl ist
                    temp = int(temp) # alle ids sind int
                    
                if num == temp:
                    # wenn eintrag gefunden
                    bscLine = line
                    break
        # END if len(line)>=index_r ---------------------
    # END FOR LOOP
    
    return bscLine


def __get_BSC_line_from_DM(dm_string):
    ''' returns bsc line for corresponding DM string ''' 
    
    if type(dm_string)!=str:
        # muss ein string sein
        return None
    elif len(dm_string) != 10:
        # string muss länge 10 haben (zB "CP-66 2645")
        return None
    
    import EPH_STAR_Starlist as Starlist
    correspond = Starlist.Correspond
    
    index_l = correspond["dm"][0]-1
    index_r = correspond["dm"][1]
    #castto =  correspond["dm"][2]  # redundant
    EMPTY =   correspond["EMPTY"]
    
    bscLine = None
    
    match = dm_string.lower()
    
    
    f = open(__relPath+"/bsc5.dat")
    
    for line in f: #FOR LOOP 
        if len(line)>=index_r: # if -----------------------------
            # geht nur, wenn die line lang genug für die indexe ist
            
            # hole den interessanten slice aus der line heraus
            temp =  line[index_l:index_r]
            
            if temp == EMPTY[index_l:index_r]:
                # wenn die herausgegriffene stelle nur whitespaces hat,
                # dann kann mit dem tag nichts gefunden werden
                bscLine = None
            else:
                if match == temp.strip().lower():
                    # wenn eintrag gefunden
                    bscLine = line
                    break
        # END if len(line)>=index_r ---------------------
    # END FOR LOOP 
    
    return bscLine
            




        
def __get_elem_from_BSC_line(bscLine):
    ''' returns bsc elements for selected relevant tags from a bscLine '''
    
    import EPH_STAR_Starlist as Starlist
    correspond = Starlist.Correspond
    
    #returnDict
    temp={}
    temp["bsc"] = {} #dict für bsc elements
    
    # für diese tags sollen werte zurückgegeben werden
    tags = ["hr","name","dm","hd","sao","fk5","rah","ram","ras","de-","ded",
            "dem","des","pmra","pmde","vmag"]
    
    for key in tags:
        try:
            # versuche die tags aus der line zu extrahieren (slice[a-1:b]) 
            # und auf entsprechenden type (c) zu casten 
            a,b,c = correspond[key]
            temp["bsc"][key] = c(bscLine[a-1:b])
        except:
            # wenn unerfolgreich, dann None
            temp["bsc"][key] = None
    
    # für debugzwecke wird bscLine auch übergeben
    temp["bscLine"] = bscLine
    
    return temp






