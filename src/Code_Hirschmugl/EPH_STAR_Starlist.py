# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 15:07:42 2019

@author: polsterc16

NOTE: The SL (Starlist) is created from the document available at
http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt



# "IAU Catalog of Star Names (IAU-CSN)"
# IAU Division C Working Group on Star Names (WGSN)
# https://www.iau.org/science/scientific_bodies/working_groups/280/
# WGSN Chair: Eric Mamajek. Email questions or comments to: IAUWGSN@gmail.com
# Last updated 2018-09-07 (see notes on latest edits at end of file)
#
# For use of the contents of the data of this file, we encourage users
# to refer to the (identical) official IAU version of the data at:
# https://www.iau.org/public/themes/naming_stars/. All IAU-produced
# products (Images, Videos, Texts) are released under Creative Commons
# Attribution (i.e. free to use in all perpetuity, world-wide, as long
# as the source is mentioned). Row (4) IDs require reading file with
# text encoding set to UTF-8. Etymological information for each star
# will be added in late 2018.


"""

    
# GreekLetterList
GLL = {}
GLL['alp'] = 'alpha'
GLL['bet'] = 'beta'
GLL['gam'] = 'gamma'
GLL['del'] = 'delta'
GLL['eps'] = 'epsilon'
GLL['zet'] = 'zeta'
GLL['eta'] = 'eta'
GLL['the'] = 'theta'
GLL['iot'] = 'iota'
GLL['kap'] = 'kappa'
GLL['lam'] = 'lambda'
GLL['mu '] = 'mu'
GLL['nu '] = 'nu'
GLL['xi '] = 'xi'
GLL['omi'] = 'omicron'
GLL['pi '] = 'pi'
GLL['rho'] = 'rho'
GLL['sig'] = 'sigma'
GLL['tau'] = 'tau'
GLL['ups'] = 'upsilon'
GLL['phi'] = 'phi'
GLL['chi'] = 'chi'
GLL['psi'] = 'psi'
GLL['ome'] = 'omega'



#ConstellationAssociationList
CAL = {}
CAL['And']=['Andromeda', 'Andromedae', 'Andr']
CAL['Ant']=['Antlia', 'Antliae', 'Antl']
CAL['Aps']=['Apus', 'Apodis', 'Apus']
CAL['Aqr']=['Aquarius', 'Aquarii', 'Aqar']
CAL['Aql']=['Aquila', 'Aquilae', 'Aqil']
CAL['Ara']=['Ara', 'Arae', 'Arae']
CAL['Ari']=['Aries', 'Arietis', 'Arie']
CAL['Aur']=['Auriga', 'Aurigae', 'Auri']
CAL['Boo']=['Boötes', 'Boötis', 'Boot']
CAL['Cae']=['Caelum', 'Caeli', 'Cael']
CAL['Cam']=['Camelopardalis', 'Camelopardalis', 'Caml']
CAL['Cnc']=['Cancer', 'Cancri', 'Canc']
CAL['CVn']=['Canes Venatici', 'Canum Venaticorum', 'CVen']
CAL['CMa']=['Canis Major', 'Canis Majoris', 'CMaj']
CAL['CMi']=['Canis Minor', 'Canis Minoris', 'CMin']
CAL['Cap']=['Capricornus', 'Capricorni', 'Capr']
CAL['Car']=['Carina', 'Carinae', 'Cari']
CAL['Cas']=['Cassiopeia', 'Cassiopeiae', 'Cass']
CAL['Cen']=['Centaurus', 'Centauri', 'Cent']
CAL['Cep']=['Cepheus', 'Cephei', 'Ceph']
CAL['Cet']=['Cetus', 'Ceti', 'Ceti']
CAL['Cha']=['Chamaeleon', 'Chamaeleontis', 'Cham']
CAL['Cir']=['Circinus', 'Circini', 'Circ']
CAL['Col']=['Columba', 'Columbae', 'Colm']
CAL['Com']=['Coma Berenices', 'Comae Berenices', 'Coma']
CAL['CrA']=['Corona Australis', 'Coronae Australis', 'CorA']
CAL['CrB']=['Corona Borealis', 'Coronae Borealis', 'CorB']
CAL['Crv']=['Corvus', 'Corvi', 'Corv']
CAL['Crt']=['Crater', 'Crateris', 'Crat']
CAL['Cru']=['Crux', 'Crucis', 'Cruc']
CAL['Cyg']=['Cygnus', 'Cygni', 'Cygn']
CAL['Del']=['Delphinus', 'Delphini', 'Dlph']
CAL['Dor']=['Dorado', 'Doradus', 'Dora']
CAL['Dra']=['Draco', 'Draconis', 'Drac']
CAL['Equ']=['Equuleus', 'Equulei', 'Equl']
CAL['Eri']=['Eridanus', 'Eridani', 'Erid']
CAL['For']=['Fornax', 'Fornacis', 'Forn']
CAL['Gem']=['Gemini', 'Geminorum', 'Gemi']
CAL['Gru']=['Grus', 'Gruis', 'Grus']
CAL['Her']=['Hercules', 'Herculis', 'Herc']
CAL['Hor']=['Horologium', 'Horologii', 'Horo']
CAL['Hya']=['Hydra', 'Hydrae', 'Hyda']
CAL['Hyi']=['Hydrus', 'Hydri', 'Hydi']
CAL['Ind']=['Indus', 'Indi', 'Indi']
CAL['Lac']=['Lacerta', 'Lacertae', 'Lacr']
CAL['Leo']=['Leo', 'Leonis', 'Leon']
CAL['LMi']=['Leo Minor', 'Leonis Minoris', 'LMin']
CAL['Lep']=['Lepus', 'Leporis', 'Leps']
CAL['Lib']=['Libra', 'Librae', 'Libr']
CAL['Lup']=['Lupus', 'Lupi', 'Lupi']
CAL['Lyn']=['Lynx', 'Lyncis', 'Lync']
CAL['Lyr']=['Lyra', 'Lyrae', 'Lyra']
CAL['Men']=['Mensa', 'Mensae', 'Mens']
CAL['Mic']=['Microscopium', 'Microscopii', 'Micr']
CAL['Mon']=['Monoceros', 'Monocerotis', 'Mono']
CAL['Mus']=['Musca', 'Muscae', 'Musc']
CAL['Nor']=['Norma', 'Normae', 'Norm']
CAL['Oct']=['Octans', 'Octantis', 'Octn']
CAL['Oph']=['Ophiuchus', 'Ophiuchi', 'Ophi']
CAL['Ori']=['Orion', 'Orionis', 'Orio']
CAL['Pav']=['Pavo', 'Pavonis', 'Pavo']
CAL['Peg']=['Pegasus', 'Pegasi', 'Pegs']
CAL['Per']=['Perseus', 'Persei', 'Pers']
CAL['Phe']=['Phoenix', 'Phoenicis', 'Phoe']
CAL['Pic']=['Pictor', 'Pictoris', 'Pict']
CAL['Psc']=['Pisces', 'Piscium', 'Pisc']
CAL['PsA']=['Piscis Austrinus', 'Piscis Austrini', 'PscA']
CAL['Pup']=['Puppis', 'Puppis', 'Pupp']
CAL['Pyx']=['Pyxis', 'Pyxidis', 'Pyxi']
CAL['Ret']=['Reticulum', 'Reticuli', 'Reti']
CAL['Sge']=['Sagitta', 'Sagittae', 'Sgte']
CAL['Sgr']=['Sagittarius', 'Sagittarii', 'Sgtr']
CAL['Sco']=['Scorpius', 'Scorpii', 'Scor']
CAL['Scl']=['Sculptor', 'Sculptoris', 'Scul']
CAL['Sct']=['Scutum', 'Scuti', 'Scut']
CAL['Ser']=['Serpens', 'Serpentis', 'Serp']
CAL['Sex']=['Sextans', 'Sextantis', 'Sext']
CAL['Tau']=['Taurus', 'Tauri', 'Taur']
CAL['Tel']=['Telescopium', 'Telescopii', 'Tele']
CAL['Tri']=['Triangulum', 'Trianguli', 'Tria']
CAL['TrA']=['Triangulum Australe', 'Trianguli Australis', 'TrAu']
CAL['Tuc']=['Tucana', 'Tucanae', 'Tucn']
CAL['UMa']=['Ursa Major', 'Ursae Majoris', 'UMaj']
CAL['UMi']=['Ursa Minor', 'Ursae Minoris', 'UMin']
CAL['Vel']=['Vela', 'Velorum', 'Velr']
CAL['Vir']=['Virgo', 'Virginis', 'Virg']
CAL['Vol']=['Volans', 'Volantis', 'Voln']
CAL['Vul']=['Vulpecula', 'Vulpeculae', 'Vulp']


# corresponding fields in the BSC
Correspond = {
        "hr":       (  1,  4,int),      #   1-  4  I4     ---     HR       [1/9110]+ Harvard Revised Number
        "name":     (  5, 14,str),      #   5- 14  A10    ---     Name     Name, generally Bayer and/or Flamsteed name
        "dm":       ( 15, 25,str),      #  15- 25  A11    ---     DM       Durchmusterung Identification (zone in bytes 17-19)
        "hd":       ( 26, 31,int),      #  26- 31  I6     ---     HD       [1/225300]? Henry Draper Catalog Number
        "sao":      ( 32, 37,int),      #  32- 37  I6     ---     SAO      [1/258997]? SAO Catalog Number
        "fk5":      ( 38, 41,int),      #  38- 41  I4     ---     FK5      ? FK5 star Number
        "irflag":   ( 42, 42,str),      #      42  A1     ---     IRflag   [I] I if infrared source
        "r_irflag": ( 43, 43,str),      #      43  A1     ---   r_IRflag  *[ ':] Coded reference for infrared source
        "multiple": ( 44, 44,str),      #      44  A1     ---    Multiple *[AWDIRS] Double or multiple-star code
        "ads":      ( 45, 49,str),      #  45- 49  A5     ---     ADS      Aitken's Double Star Catalog (ADS) designation
        "adscomp":  ( 50, 51,str),      #  50- 51  A2     ---     ADScomp  ADS number components
        "varid":    ( 52, 60,str),      #  52- 60  A9     ---     VarID    Variable star identification
        "rah1900":  ( 61, 62,int),      #  61- 62  I2     h       RAh1900  ?Hours RA, equinox B1900, epoch 1900.0 (1)
        "ram1900":  ( 63, 64,int),      #  63- 64  I2     min     RAm1900  ?Minutes RA, equinox B1900, epoch 1900.0 (1)
        "ras1900":  ( 65, 68,float),    #  65- 68  F4.1   s       RAs1900  ?Seconds RA, equinox B1900, epoch 1900.0 (1)
        "de-1900":  ( 69, 69,str),      #      69  A1     ---     DE-1900  ?Sign Dec, equinox B1900, epoch 1900.0 (1)
        "ded1900":  ( 70, 71,int),      #  70- 71  I2     deg     DEd1900  ?Degrees Dec, equinox B1900, epoch 1900.0 (1)
        "dem1900":  ( 72, 73,int),  	#  72- 73  I2     arcmin  DEm1900  ?Minutes Dec, equinox B1900, epoch 1900.0 (1)
        "des1900":  ( 74, 75,int),      #  74- 75  I2     arcsec  DEs1900  ?Seconds Dec, equinox B1900, epoch 1900.0 (1)
        "rah":      ( 76, 77,int),      #  76- 77  I2     h       RAh      ?Hours RA, equinox J2000, epoch 2000.0 (1)
        "ram":      ( 78, 79,int),      #  78- 79  I2     min     RAm      ?Minutes RA, equinox J2000, epoch 2000.0 (1)
        "ras":      ( 80, 83,float),    #  80- 83  F4.1   s       RAs      ?Seconds RA, equinox J2000, epoch 2000.0 (1)
        "de-":      ( 84, 84,str),      #      84  A1     ---     DE-      ?Sign Dec, equinox J2000, epoch 2000.0 (1)
        "ded":      ( 85, 86,int),      #  85- 86  I2     deg     DEd      ?Degrees Dec, equinox J2000, epoch 2000.0 (1)
        "dem":      ( 87, 88,int),      #  87- 88  I2     arcmin  DEm      ?Minutes Dec, equinox J2000, epoch 2000.0 (1)
        "des":      ( 89, 90,int),      #  89- 90  I2     arcsec  DEs      ?Seconds Dec, equinox J2000, epoch 2000.0 (1)
        "glon":     ( 91, 96,float),    #  91- 96  F6.2   deg     GLON     ?Galactic longitude (1)
        "glat":     ( 97,102,float),    #  97-102  F6.2   deg     GLAT     ?Galactic latitude (1)
        "vmag":     (103,107,float),    # 103-107  F5.2   mag     Vmag     ?Visual magnitude (1)
        "n_vmag":   (108,108,str),      #     108  A1     ---   n_Vmag    *[ HR] Visual magnitude code
        "u_vmag":   (109,109,str),      #     109  A1     ---   u_Vmag     [ :?] Uncertainty flag on V
        "b-v":      (110,114,float),    # 110-114  F5.2   mag     B-V      ? B-V color in the UBV system
        "u_b-v":    (115,115,str),      #     115  A1     ---   u_B-V      [ :?] Uncertainty flag on B-V
        "u-b":      (116,120,float),    # 116-120  F5.2   mag     U-B      ? U-B color in the UBV system
        "u_u-b":    (121,121,str),      #     121  A1     ---   u_U-B      [ :?] Uncertainty flag on U-B
        "r-i":      (122,126,float),    # 122-126  F5.2   mag     R-I      ? R-I   in system specified by n_R-I
        "n_r-i":    (127,127,str),      #     127  A1     ---   n_R-I      [CE:?D] Code for R-I system (Cousin, Eggen)
        "sptype":   (128,147,str),      # 128-147  A20    ---     SpType   Spectral type
        "n_sptype": (148,148,str),      #     148  A1     ---   n_SpType   [evt] Spectral type code
        "pmra":     (149,154,float),    # 149-154  F6.3 arcsec/yr pmRA    *?Annual proper motion in RA J2000, FK5 system
        "pmde":     (155,160,float),    # 155-160  F6.3 arcsec/yr pmDE     ?Annual proper motion in Dec J2000, FK5 system
        "n_parallax":(161,161,str),     #     161  A1     ---   n_Parallax [D] D indicates a dynamical parallax, otherwise a trigonometric parallax
        "parallax": (162,166,float),    # 162-166  F5.3   arcsec  Parallax ? Trigonometric parallax (unless n_Parallax)
        "radvel":   (167,170,int),      # 167-170  I4     km/s    RadVel   ? Heliocentric Radial Velocity
        "n_radvel": (171,174,str),      # 171-174  A4     ---   n_RadVel  *[V?SB123O ] Radial velocity comments
        "l_rotvel": (175,176,str),      # 175-176  A2     ---   l_RotVel   [<=> ] Rotational velocity limit characters
        "rotvel":   (177,179,int),      # 177-179  I3     km/s    RotVel   ? Rotational velocity, v sin i
        "u_rotvel": (180,180,str),      #     180  A1     ---   u_RotVel   [ :v] uncertainty and variability flag on RotVel
        "dmag":     (181,184,float),    # 181-184  F4.1   mag     Dmag     ? Magnitude difference of double, or brightest multiple
        "sep":      (185,190,float),    # 185-190  F6.1   arcsec  Sep      ? Separation of components in Dmag if occultation binary.
        "multid":   (191,194,str),      # 191-194  A4     ---     MultID   Identifications of components in Dmag
        "multcnt":  (195,196,int),      # 195-196  I2     ---     MultCnt  ? Number of components assigned to a multiple
        "noteflag": (197,197,str),      #     197  A1     ---     NoteFlag [*] 
        "EMPTY":    ('                                                                                                                                                                                                        ')
        }


# Starlist with ownnames
SL={}
SL['Acamar'] =            {'hr': 897,  'tags': ['Acamar']}
SL['Achernar'] =          {'hr': 472,  'tags': ['Achernar']}
SL['Achird'] =            {'hr': 219,  'tags': ['Achird']}
SL['Acrab'] =             {'hr': 5984, 'tags': ['Acrab']}
SL['Acrux'] =             {'hr': 4730, 'tags': ['Acrux']}
SL['Acubens'] =           {'hr': 3572, 'tags': ['Acubens']}
SL['Adhafera'] =          {'hr': 4031, 'tags': ['Adhafera']}
SL['Adhara'] =            {'hr': 2618, 'tags': ['Adhara']}
SL['Adhil'] =             {'hr': 390,  'tags': ['Adhil']}
SL['Ain'] =               {'hr': 1409, 'tags': ['Ain']}
SL['Ainalrami'] =         {'hr': 7116, 'tags': ['Ainalrami']}
SL['Aladfar'] =           {'hr': 7298, 'tags': ['Aladfar']}
SL['Albaldah'] =          {'hr': 7264, 'tags': ['Albaldah']}
SL['Albali'] =            {'hr': 7950, 'tags': ['Albali']}
SL['Albireo'] =           {'hr': 7417, 'tags': ['Albireo']}
SL['Alchiba'] =           {'hr': 4623, 'tags': ['Alchiba']}
SL['Alcor'] =             {'hr': 5062, 'tags': ['Alcor']}
SL['Alcyone'] =           {'hr': 1165, 'tags': ['Alcyone']}
SL['Aldebaran'] =         {'hr': 1457, 'tags': ['Aldebaran']}
SL['Alderamin'] =         {'hr': 8162, 'tags': ['Alderamin']}
SL['Aldhanab'] =          {'hr': 8353, 'tags': ['Aldhanab']}
SL['Aldhibah'] =          {'hr': 6396, 'tags': ['Aldhibah']}
SL['Aldulfin'] =          {'hr': 7852, 'tags': ['Aldulfin']}
SL['Alfirk'] =            {'hr': 8238, 'tags': ['Alfirk']}
SL['Algedi'] =            {'hr': 7754, 'tags': ['Algedi']}
SL['Algenib'] =           {'hr': 39,   'tags': ['Algenib']}
SL['Algieba'] =           {'hr': 4057, 'tags': ['Algieba']}
SL['Algol'] =             {'hr': 936,  'tags': ['Algol']}
SL['Algorab'] =           {'hr': 4757, 'tags': ['Algorab']}
SL['Alhena'] =            {'hr': 2421, 'tags': ['Alhena']}
SL['Alioth'] =            {'hr': 4905, 'tags': ['Alioth']}
SL['Aljanah'] =           {'hr': 7949, 'tags': ['Aljanah']}
SL['Alkaid'] =            {'hr': 5191, 'tags': ['Alkaid']}
SL['Alkalurops'] =        {'hr': 5733, 'tags': ['Alkalurops']}
SL['Alkaphrah'] =         {'hr': 3594, 'tags': ['Alkaphrah']}
SL['Alkarab'] =           {'hr': 8905, 'tags': ['Alkarab']}
SL['Alkes'] =             {'hr': 4287, 'tags': ['Alkes']}
SL['Almaaz'] =            {'hr': 1605, 'tags': ['Almaaz']}
SL['Almach'] =            {'hr': 603,  'tags': ['Almach']}
SL['Alnair'] =            {'hr': 8425, 'tags': ['Alnair']}
SL['Alnasl'] =            {'hr': 6746, 'tags': ['Alnasl']}
SL['Alnilam'] =           {'hr': 1903, 'tags': ['Alnilam']}
SL['Alnitak'] =           {'hr': 1948, 'tags': ['Alnitak']}
SL['Alniyat'] =           {'hr': 6084, 'tags': ['Alniyat']}
SL['Alphard'] =           {'hr': 3748, 'tags': ['Alphard']}
SL['Alphecca'] =          {'hr': 5793, 'tags': ['Alphecca']}
SL['Alpheratz'] =         {'hr': 15,   'tags': ['Alpheratz']}
SL['Alpherg'] =           {'hr': 437,  'tags': ['Alpherg']}
SL['Alrakis'] =           {'hr': 6370, 'tags': ['Alrakis']}
SL['Alrescha'] =          {'hr': 596,  'tags': ['Alrescha']}
SL['Alruba'] =            {'hr': 6618, 'tags': ['Alruba']}
SL['Alsafi'] =            {'hr': 7462, 'tags': ['Alsafi']}
SL['Alsciaukat'] =        {'hr': 3275, 'tags': ['Alsciaukat']}
SL['Alsephina'] =         {'hr': 3485, 'tags': ['Alsephina']}
SL['Alshain'] =           {'hr': 7602, 'tags': ['Alshain']}
SL['Alshat'] =            {'hr': 7773, 'tags': ['Alshat']}
SL['Altair'] =            {'hr': 7557, 'tags': ['Altair']}
SL['Altais'] =            {'hr': 7310, 'tags': ['Altais']}
SL['Alterf'] =            {'hr': 3773, 'tags': ['Alterf']}
SL['Aludra'] =            {'hr': 2827, 'tags': ['Aludra']}
SL['Alula Australis'] =   {'hr': 4375, 'tags': ['Alula Australis']}
SL['Alula Borealis'] =    {'hr': 4377, 'tags': ['Alula Borealis']}
SL['Alya'] =              {'hr': 7141, 'tags': ['Alya']}
SL['Alzirr'] =            {'hr': 2484, 'tags': ['Alzirr']}
SL['Ancha'] =             {'hr': 8499, 'tags': ['Ancha']}
SL['Angetenar'] =         {'hr': 850,  'tags': ['Angetenar']}
SL['Ankaa'] =             {'hr': 99,   'tags': ['Ankaa']}
SL['Anser'] =             {'hr': 7405, 'tags': ['Anser']}
SL['Antares'] =           {'hr': 6134, 'tags': ['Antares']}
SL['Arcturus'] =          {'hr': 5340, 'tags': ['Arcturus']}
SL['Arkab Posterior'] =   {'hr': 7343, 'tags': ['Arkab Posterior']}
SL['Arkab Prior'] =       {'hr': 7337, 'tags': ['Arkab Prior']}
SL['Arneb'] =             {'hr': 1865, 'tags': ['Arneb']}
SL['Ascella'] =           {'hr': 7194, 'tags': ['Ascella']}
SL['Asellus Australis'] = {'hr': 3461, 'tags': ['Asellus Australis']}
SL['Asellus Borealis'] =  {'hr': 3449, 'tags': ['Asellus Borealis']}
SL['Ashlesha'] =          {'hr': 3482, 'tags': ['Ashlesha']}
SL['Aspidiske'] =         {'hr': 3699, 'tags': ['Aspidiske']}
SL['Asterope'] =          {'hr': 1151, 'tags': ['Asterope']}
SL['Athebyne'] =          {'hr': 6132, 'tags': ['Athebyne']}
SL['Atik'] =              {'hr': 1131, 'tags': ['Atik']}
SL['Atlas'] =             {'hr': 1178, 'tags': ['Atlas']}
SL['Atria'] =             {'hr': 6217, 'tags': ['Atria']}
SL['Avior'] =             {'hr': 3307, 'tags': ['Avior']}
SL['Azelfafage'] =        {'hr': 8301, 'tags': ['Azelfafage']}
SL['Azha'] =              {'hr': 874,  'tags': ['Azha']}
SL['Azmidi'] =            {'hr': 3045, 'tags': ['Azmidi']}
SL['Baten Kaitos'] =      {'hr': 539,  'tags': ['Baten Kaitos']}
SL['Beemim'] =            {'hr': 1393, 'tags': ['Beemim']}
SL['Beid'] =              {'hr': 1298, 'tags': ['Beid']}
SL['Bellatrix'] =         {'hr': 1790, 'tags': ['Bellatrix']}
SL['Betelgeuse'] =        {'hr': 2061, 'tags': ['Betelgeuse']}
SL['Bharani'] =           {'hr': 838,  'tags': ['Bharani']}
SL['Biham'] =             {'hr': 8450, 'tags': ['Biham']}
SL['Botein'] =            {'hr': 951,  'tags': ['Botein']}
SL['Brachium'] =          {'hr': 5603, 'tags': ['Brachium']}
SL['Bunda'] =             {'hr': 8264, 'tags': ['Bunda']}
SL['Canopus'] =           {'hr': 2326, 'tags': ['Canopus']}
SL['Capella'] =           {'hr': 1708, 'tags': ['Capella']}
SL['Caph'] =              {'hr': 21,   'tags': ['Caph']}
SL['Castor'] =            {'hr': 2891, 'tags': ['Castor']}
SL['Castula'] =           {'hr': 265,  'tags': ['Castula']}
SL['Cebalrai'] =          {'hr': 6603, 'tags': ['Cebalrai']}
SL['Celaeno'] =           {'hr': 1140, 'tags': ['Celaeno']}
SL['Cervantes'] =         {'hr': 6585, 'tags': ['Cervantes']}
SL['Chalawan'] =          {'hr': 4277, 'tags': ['Chalawan']}
SL['Chamukuy'] =          {'hr': 1412, 'tags': ['Chamukuy']}
SL['Chara'] =             {'hr': 4785, 'tags': ['Chara']}
SL['Chertan'] =           {'hr': 4359, 'tags': ['Chertan']}
SL['Copernicus'] =        {'hr': 3522, 'tags': ['Copernicus']}
SL['Cor Caroli'] =        {'hr': 4915, 'tags': ['Cor Caroli']}
SL['Cujam'] =             {'hr': 6117, 'tags': ['Cujam']}
SL['Cursa'] =             {'hr': 1666, 'tags': ['Cursa']}
SL['Dabih'] =             {'hr': 7776, 'tags': ['Dabih']}
SL['Dalim'] =             {'hr': 963,  'tags': ['Dalim']}
SL['Deneb'] =             {'hr': 7924, 'tags': ['Deneb']}
SL['Deneb Algedi'] =      {'hr': 8322, 'tags': ['Deneb Algedi']}
SL['Denebola'] =          {'hr': 4534, 'tags': ['Denebola']}
SL['Diadem'] =            {'hr': 4968, 'tags': ['Diadem']}
SL['Diphda'] =            {'hr': 188,  'tags': ['Diphda']}
SL['Dschubba'] =          {'hr': 5953, 'tags': ['Dschubba']}
SL['Dubhe'] =             {'hr': 4301, 'tags': ['Dubhe']}
SL['Dziban'] =            {'hr': 6636, 'tags': ['Dziban']}
SL['Edasich'] =           {'hr': 5744, 'tags': ['Edasich']}
SL['Electra'] =           {'hr': 1142, 'tags': ['Electra']}
SL['Elgafar'] =           {'hr': 5409, 'tags': ['Elgafar']}
SL['Elkurud'] =           {'hr': 2177, 'tags': ['Elkurud']}
SL['Elnath'] =            {'hr': 1791, 'tags': ['Elnath']}
SL['Eltanin'] =           {'hr': 6705, 'tags': ['Eltanin']}
SL['Enif'] =              {'hr': 8308, 'tags': ['Enif']}
SL['Errai'] =             {'hr': 8974, 'tags': ['Errai']}
SL['Fafnir'] =            {'hr': 6945, 'tags': ['Fafnir']}
SL['Fang'] =              {'hr': 5944, 'tags': ['Fang']}
SL['Fawaris'] =           {'hr': 7528, 'tags': ['Fawaris']}
SL['Felis'] =             {'hr': 3923, 'tags': ['Felis']}
SL['Fomalhaut'] =         {'hr': 8728, 'tags': ['Fomalhaut']}
SL['Fulu'] =              {'hr': 153,  'tags': ['Fulu']}
SL['Fumalsamakah'] =      {'hr': 8773, 'tags': ['Fumalsamakah']}
SL['Furud'] =             {'hr': 2282, 'tags': ['Furud']}
SL['Fuyue'] =             {'hr': 6630, 'tags': ['Fuyue']}
SL['Gacrux'] =            {'hr': 4763, 'tags': ['Gacrux']}
SL['Giausar'] =           {'hr': 4434, 'tags': ['Giausar']}
SL['Gienah'] =            {'hr': 4662, 'tags': ['Gienah']}
SL['Ginan'] =             {'hr': 4700, 'tags': ['Ginan']}
SL['Gomeisa'] =           {'hr': 2845, 'tags': ['Gomeisa']}
SL['Grumium'] =           {'hr': 6688, 'tags': ['Grumium']}
SL['Gudja'] =             {'hr': 5879, 'tags': ['Gudja']}
SL['Guniibuu'] =          {'hr': 6402, 'tags': ['Guniibuu']}
SL['Hadar'] =             {'hr': 5267, 'tags': ['Hadar']}
SL['Haedus'] =            {'hr': 1641, 'tags': ['Haedus']}
SL['Hamal'] =             {'hr': 617,  'tags': ['Hamal']}
SL['Hassaleh'] =          {'hr': 1577, 'tags': ['Hassaleh']}
SL['Hatysa'] =            {'hr': 1899, 'tags': ['Hatysa']}
SL['Helvetios'] =         {'hr': 8729, 'tags': ['Helvetios']}
SL['Heze'] =              {'hr': 5107, 'tags': ['Heze']}
SL['Homam'] =             {'hr': 8634, 'tags': ['Homam']}
SL['Iklil'] =             {'hr': 5928, 'tags': ['Iklil']}
SL['Imai'] =              {'hr': 4656, 'tags': ['Imai']}
SL['Intercrus'] =         {'hr': 3743, 'tags': ['Intercrus']}
SL['Izar'] =              {'hr': 5506, 'tags': ['Izar']}
SL['Jabbah'] =            {'hr': 6027, 'tags': ['Jabbah']}
SL['Jishui'] =            {'hr': 2930, 'tags': ['Jishui']}
SL['Kaffaljidhma'] =      {'hr': 804,  'tags': ['Kaffaljidhma']}
SL['Kang'] =              {'hr': 5315, 'tags': ['Kang']}
SL['Kaus Australis'] =    {'hr': 6879, 'tags': ['Kaus Australis']}
SL['Kaus Borealis'] =     {'hr': 6913, 'tags': ['Kaus Borealis']}
SL['Kaus Media'] =        {'hr': 6859, 'tags': ['Kaus Media']}
SL['Keid'] =              {'hr': 1325, 'tags': ['Keid']}
SL['Khambalia'] =         {'hr': 5359, 'tags': ['Khambalia']}
SL['Kitalpha'] =          {'hr': 8131, 'tags': ['Kitalpha']}
SL['Kochab'] =            {'hr': 5563, 'tags': ['Kochab']}
SL['Kornephoros'] =       {'hr': 6148, 'tags': ['Kornephoros']}
SL['Kraz'] =              {'hr': 4786, 'tags': ['Kraz']}
SL['Kurhah'] =            {'hr': 8417, 'tags': ['Kurhah']}
SL['Larawag'] =           {'hr': 6241, 'tags': ['Larawag']}
SL['La Superba'] =        {'hr': 4846, 'tags': ['La Superba']}
SL['Lesath'] =            {'hr': 6508, 'tags': ['Lesath']}
SL['Libertas'] =          {'hr': 7595, 'tags': ['Libertas']}
SL['Lilii Borea'] =       {'hr': 824,  'tags': ['Lilii Borea']}
SL['Maasym'] =            {'hr': 6526, 'tags': ['Maasym']}
SL['Mahasim'] =           {'hr': 2095, 'tags': ['Mahasim']}
SL['Maia'] =              {'hr': 1149, 'tags': ['Maia']}
SL['Marfik'] =            {'hr': 6149, 'tags': ['Marfik']}
SL['Markab'] =            {'hr': 8781, 'tags': ['Markab']}
SL['Markeb'] =            {'hr': 3734, 'tags': ['Markeb']}
SL['Marsic'] =            {'hr': 6008, 'tags': ['Marsic']}
SL['Matar'] =             {'hr': 8650, 'tags': ['Matar']}
SL['Mebsuta'] =           {'hr': 2473, 'tags': ['Mebsuta']}
SL['Megrez'] =            {'hr': 4660, 'tags': ['Megrez']}
SL['Meissa'] =            {'hr': 1879, 'tags': ['Meissa']}
SL['Mekbuda'] =           {'hr': 2650, 'tags': ['Mekbuda']}
SL['Meleph'] =            {'hr': 3429, 'tags': ['Meleph']}
SL['Menkalinan'] =        {'hr': 2088, 'tags': ['Menkalinan']}
SL['Menkar'] =            {'hr': 911,  'tags': ['Menkar']}
SL['Menkent'] =           {'hr': 5288, 'tags': ['Menkent']}
SL['Menkib'] =            {'hr': 1228, 'tags': ['Menkib']}
SL['Merak'] =             {'hr': 4295, 'tags': ['Merak']}
SL['Merga'] =             {'hr': 5533, 'tags': ['Merga']}
SL['Meridiana'] =         {'hr': 7254, 'tags': ['Meridiana']}
SL['Merope'] =            {'hr': 1156, 'tags': ['Merope']}
SL['Mesarthim'] =         {'hr': 546,  'tags': ['Mesarthim']}
SL['Miaplacidus'] =       {'hr': 3685, 'tags': ['Miaplacidus']}
SL['Mimosa'] =            {'hr': 4853, 'tags': ['Mimosa']}
SL['Minchir'] =           {'hr': 3418, 'tags': ['Minchir']}
SL['Minelauva'] =         {'hr': 4910, 'tags': ['Minelauva']}
SL['Mintaka'] =           {'hr': 1852, 'tags': ['Mintaka']}
SL['Mira'] =              {'hr': 681,  'tags': ['Mira']}
SL['Mirach'] =            {'hr': 337,  'tags': ['Mirach']}
SL['Miram'] =             {'hr': 834,  'tags': ['Miram']}
SL['Mirfak'] =            {'hr': 1017, 'tags': ['Mirfak']}
SL['Mirzam'] =            {'hr': 2294, 'tags': ['Mirzam']}
SL['Misam'] =             {'hr': 941,  'tags': ['Misam']}
SL['Mizar'] =             {'hr': 5054, 'tags': ['Mizar']}
SL['Mothallah'] =         {'hr': 544,  'tags': ['Mothallah']}
SL['Muliphein'] =         {'hr': 2657, 'tags': ['Muliphein']}
SL['Muphrid'] =           {'hr': 5235, 'tags': ['Muphrid']}
SL['Muscida'] =           {'hr': 3323, 'tags': ['Muscida']}
SL['Musica'] =            {'hr': 8030, 'tags': ['Musica']}
SL['Nahn'] =              {'hr': 3627, 'tags': ['Nahn']}
SL['Naos'] =              {'hr': 3165, 'tags': ['Naos']}
SL['Nashira'] =           {'hr': 8278, 'tags': ['Nashira']}
SL['Nekkar'] =            {'hr': 5602, 'tags': ['Nekkar']}
SL['Nembus'] =            {'hr': 464,  'tags': ['Nembus']}
SL['Nihal'] =             {'hr': 1829, 'tags': ['Nihal']}
SL['Nunki'] =             {'hr': 7121, 'tags': ['Nunki']}
SL['Nusakan'] =           {'hr': 5747, 'tags': ['Nusakan']}
SL['Okab'] =              {'hr': 7235, 'tags': ['Okab']}
SL['Paikauhale'] =        {'hr': 6165, 'tags': ['Paikauhale']}
SL['Peacock'] =           {'hr': 7790, 'tags': ['Peacock']}
SL['Phact'] =             {'hr': 1956, 'tags': ['Phact']}
SL['Phecda'] =            {'hr': 4554, 'tags': ['Phecda']}
SL['Pherkad'] =           {'hr': 5735, 'tags': ['Pherkad']}
SL['Piautos'] =           {'hr': 3268, 'tags': ['Piautos']}
SL['Pipirima'] =          {'hr': 6252, 'tags': ['Pipirima']}
SL['Pleione'] =           {'hr': 1180, 'tags': ['Pleione']}
SL['Polaris'] =           {'hr': 424,  'tags': ['Polaris']}
SL['Polaris Australis'] = {'hr': 7228, 'tags': ['Polaris Australis']}
SL['Polis'] =             {'hr': 6812, 'tags': ['Polis']}
SL['Pollux'] =            {'hr': 2990, 'tags': ['Pollux']}
SL['Porrima'] =           {'hr': 4825, 'tags': ['Porrima']}
SL['Praecipua'] =         {'hr': 4247, 'tags': ['Praecipua']}
SL['Prima Hyadum'] =      {'hr': 1346, 'tags': ['Prima Hyadum']}
SL['Procyon'] =           {'hr': 2943, 'tags': ['Procyon']}
SL['Propus'] =            {'hr': 2216, 'tags': ['Propus']}
SL['Ran'] =               {'hr': 1084, 'tags': ['Ran']}
SL['Rasalas'] =           {'hr': 3905, 'tags': ['Rasalas']}
SL['Rasalgethi'] =        {'hr': 6406, 'tags': ['Rasalgethi']}
SL['Rasalhague'] =        {'hr': 6556, 'tags': ['Rasalhague']}
SL['Rastaban'] =          {'hr': 6536, 'tags': ['Rastaban']}
SL['Regulus'] =           {'hr': 3982, 'tags': ['Regulus']}
SL['Revati'] =            {'hr': 361,  'tags': ['Revati']}
SL['Rigel'] =             {'hr': 1713, 'tags': ['Rigel']}
SL['Rigil Kentaurus'] =   {'hr': 5459, 'tags': ['Rigil Kentaurus']}
SL['Rotanev'] =           {'hr': 7882, 'tags': ['Rotanev']}
SL['Ruchbah'] =           {'hr': 403,  'tags': ['Ruchbah']}
SL['Rukbat'] =            {'hr': 7348, 'tags': ['Rukbat']}
SL['Sabik'] =             {'hr': 6378, 'tags': ['Sabik']}
SL['Saclateni'] =         {'hr': 1612, 'tags': ['Saclateni']}
SL['Sadachbia'] =         {'hr': 8518, 'tags': ['Sadachbia']}
SL['Sadalbari'] =         {'hr': 8684, 'tags': ['Sadalbari']}
SL['Sadalmelik'] =        {'hr': 8414, 'tags': ['Sadalmelik']}
SL['Sadalsuud'] =         {'hr': 8232, 'tags': ['Sadalsuud']}
SL['Sadr'] =              {'hr': 7796, 'tags': ['Sadr']}
SL['Saiph'] =             {'hr': 2004, 'tags': ['Saiph']}
SL['Salm'] =              {'hr': 8880, 'tags': ['Salm']}
SL['Sargas'] =            {'hr': 6553, 'tags': ['Sargas']}
SL['Sarin'] =             {'hr': 6410, 'tags': ['Sarin']}
SL['Sceptrum'] =          {'hr': 1481, 'tags': ['Sceptrum']}
SL['Scheat'] =            {'hr': 8775, 'tags': ['Scheat']}
SL['Schedar'] =           {'hr': 168,  'tags': ['Schedar']}
SL['Secunda Hyadum'] =    {'hr': 1373, 'tags': ['Secunda Hyadum']}
SL['Segin'] =             {'hr': 542,  'tags': ['Segin']}
SL['Seginus'] =           {'hr': 5435, 'tags': ['Seginus']}
SL['Sham'] =              {'hr': 7479, 'tags': ['Sham']}
SL['Shaula'] =            {'hr': 6527, 'tags': ['Shaula']}
SL['Sheliak'] =           {'hr': 7106, 'tags': ['Sheliak']}
SL['Sheratan'] =          {'hr': 553,  'tags': ['Sheratan']}
SL['Sirius'] =            {'hr': 2491, 'tags': ['Sirius']}
SL['Situla'] =            {'hr': 8610, 'tags': ['Situla']}
SL['Skat'] =              {'hr': 8709, 'tags': ['Skat']}
SL['Spica'] =             {'hr': 5056, 'tags': ['Spica']}
SL['Sualocin'] =          {'hr': 7906, 'tags': ['Sualocin']}
SL['Subra'] =             {'hr': 3852, 'tags': ['Subra']}
SL['Suhail'] =            {'hr': 3634, 'tags': ['Suhail']}
SL['Sulafat'] =           {'hr': 7178, 'tags': ['Sulafat']}
SL['Syrma'] =             {'hr': 5338, 'tags': ['Syrma']}
SL['Tabit'] =             {'hr': 1543, 'tags': ['Tabit']}
SL['Taiyangshou'] =       {'hr': 4518, 'tags': ['Taiyangshou']}
SL['Taiyi'] =             {'hr': 4916, 'tags': ['Taiyi']}
SL['Talitha'] =           {'hr': 3569, 'tags': ['Talitha']}
SL['Tania Australis'] =   {'hr': 4069, 'tags': ['Tania Australis']}
SL['Tania Borealis'] =    {'hr': 4033, 'tags': ['Tania Borealis']}
SL['Tarazed'] =           {'hr': 7525, 'tags': ['Tarazed']}
SL['Tarf'] =              {'hr': 3249, 'tags': ['Tarf']}
SL['Taygeta'] =           {'hr': 1145, 'tags': ['Taygeta']}
SL['Tegmine'] =           {'hr': 3208, 'tags': ['Tegmine']}
SL['Tejat'] =             {'hr': 2286, 'tags': ['Tejat']}
SL['Terebellum'] =        {'hr': 7597, 'tags': ['Terebellum']}
SL['Theemin'] =           {'hr': 1464, 'tags': ['Theemin']}
SL['Thuban'] =            {'hr': 5291, 'tags': ['Thuban']}
SL['Tiaki'] =             {'hr': 8636, 'tags': ['Tiaki']}
SL['Tianguan'] =          {'hr': 1910, 'tags': ['Tianguan']}
SL['Tianyi'] =            {'hr': 4863, 'tags': ['Tianyi']}
SL['Titawin'] =           {'hr': 458,  'tags': ['Titawin']}
SL['Toliman'] =           {'hr': 5460, 'tags': ['Toliman']}
SL['Tonatiuh'] =          {'hr': 4609, 'tags': ['Tonatiuh']}
SL['Torcular'] =          {'hr': 510,  'tags': ['Torcular']}
SL['Tureis'] =            {'hr': 3185, 'tags': ['Tureis']}
SL['Ukdah'] =             {'hr': 3845, 'tags': ['Ukdah']}
SL['Unukalhai'] =         {'hr': 5854, 'tags': ['Unukalhai']}
SL['Unurgunite'] =        {'hr': 2646, 'tags': ['Unurgunite']}
SL['Vega'] =              {'hr': 7001, 'tags': ['Vega']}
SL['Veritate'] =          {'hr': 8930, 'tags': ['Veritate']}
SL['Vindemiatrix'] =      {'hr': 4932, 'tags': ['Vindemiatrix']}
SL['Wasat'] =             {'hr': 2777, 'tags': ['Wasat']}
SL['Wazn'] =              {'hr': 2040, 'tags': ['Wazn']}
SL['Wezen'] =             {'hr': 2693, 'tags': ['Wezen']}
SL['Wurren'] =            {'hr': 338,  'tags': ['Wurren']}
SL['Xamidimura'] =        {'hr': 6247, 'tags': ['Xamidimura']}
SL['Xuange'] =            {'hr': 5351, 'tags': ['Xuange']}
SL['Yed Posterior'] =     {'hr': 6075, 'tags': ['Yed Posterior']}
SL['Yed Prior'] =         {'hr': 6056, 'tags': ['Yed Prior']}
SL['Yildun'] =            {'hr': 6789, 'tags': ['Yildun']}
SL['Zaniah'] =            {'hr': 4689, 'tags': ['Zaniah']}
SL['Zaurak'] =            {'hr': 1231, 'tags': ['Zaurak']}
SL['Zavijava'] =          {'hr': 4540, 'tags': ['Zavijava']}
SL['Zhang'] =             {'hr': 3903, 'tags': ['Zhang']}
SL['Zibal'] =             {'hr': 984,  'tags': ['Zibal']}
SL['Zosma'] =             {'hr': 4357, 'tags': ['Zosma']}
SL['Zubenelgenubi'] =     {'hr': 5531, 'tags': ['Zubenelgenubi']}
SL['Zubenelhakrabi'] =    {'hr': 5787, 'tags': ['Zubenelhakrabi']}
SL['Zubeneschamali'] =    {'hr': 5685, 'tags': ['Zubeneschamali']}
