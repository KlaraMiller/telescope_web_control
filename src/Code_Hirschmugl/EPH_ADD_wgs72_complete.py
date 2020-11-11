# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 10:44:53 2019

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

import sgp4.earth_gravity as sgp4_earth_gravity
import math

# https://apps.dtic.mil/dtic/tr/fulltext/u2/a110165.pdf
# Page 20

wgs72_complete = sgp4_earth_gravity.wgs72._asdict()

wgs72_complete["1/f"] = 298.2638
wgs72_complete["f"] = 1/wgs72_complete["1/f"]

wgs72_complete["a"] = wgs72_complete["radiusearthkm"]*1000
wgs72_complete["b"] = wgs72_complete["a"] * (1-wgs72_complete["f"])

wgs72_complete["e^2"] = wgs72_complete["f"] * (2 - wgs72_complete["f"])
wgs72_complete["e"] = math.sqrt(wgs72_complete["e^2"])

wgs72_complete["omega_RadPerSec"] = 7.292115147e-5
wgs72_complete["gamma_e_mgal"] = 978033.26

wgs72_complete["C_2,0"] = -484.1605e-6