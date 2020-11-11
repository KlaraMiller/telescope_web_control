# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:08:21 2019

@author: hirschmu16
@description: top level of the program

==============================================================================
 LICENCE INFORMATION
==============================================================================
-
==============================================================================

"""

# standard librarys
from __future__ import print_function, unicode_literals
from pprint import pprint

# downloaded librarys
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2

# my librarys
import motor_control
import nav
import common
import myGPS
import goto
import set_polaris
import star3_verification
import observe
import magic


# -----------------------------------------------------------------------------      
# -------------------------------- variables ----------------------------------
# -----------------------------------------------------------------------------  

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

f = Figlet(font='slant')

# Storage for all Data
sg1 = common.stargate()


# =============================================================================      
# ==================================== top ====================================
# ============================================================================= 

# list with options
running = True
while running:
    common.header(sg1, 'top')
    questions = [
        {
            'type': 'checkbox',
            'qmark': '?',
            'message': 'Select task',
            'name': 'tasks',
            'choices': [ 
                Separator('= first setup ='),
                {
                    'name': 'nav',
                },
                {
                    'name': 'gps',
                },
                {
                    'name': 'set_polaris',
                },
                Separator('= alingment ='),
                {
                    'name': 'star3_verification',
                },
                {
                    'name': 'manual_correction',
                },
                {
                    'name': 'goto',
                },
                {
                    'name': 'observe',
                },
                {
                    'name': 'test',
                },
                Separator('= Options ='),
                {
                    'name': 'debug mode',
                },
                {
                    'name': 'refresh sreen',
                },
                {
                    'name': 'exit'
                }
            ]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    pprint(answers)
    print(len(answers["tasks"]))
    if len(answers["tasks"]) > 1:
        print('### Please choose only one task at a time ###')
    elif len(answers["tasks"]) < 1:
        print('### Please choose at least one task ###')
    else:
        if 'nav' in answers["tasks"]:
            nav.main(sg1)
        elif 'gps' in answers["tasks"]:
            myGPS.main(sg1)
        elif 'set_polaris' in answers["tasks"]:
            set_polaris.main(sg1)
        elif 'manual_correction' in answers["tasks"]:
            motor_control.mode_manual(sg1)
        elif 'star3_verification' in answers["tasks"]:
            star3_verification.main(sg1)
        elif 'goto' in answers["tasks"]:
            goto.main(sg1)
        elif 'observe' in answers["tasks"]:
            observe.main(sg1)            
        elif 'test' in answers["tasks"]:
            #motor_control.mode_test(sg1)
            #magic.test_runtime_star(sg1)
            #magic.test_runtime_planet(sg1)
            #magic.test_runtime_moon(sg1)
            #magic.test_runtime_sat(sg1)
            motor_control.test(sg1)
            common.read_character()
        elif 'debug mode' in answers["tasks"]:
            if sg1.mydata.get_debug_mode() == False:
                sg1.mydata.set_debug_mode(True)
            elif sg1.mydata.get_debug_mode() == True:
                sg1.mydata.set_debug_mode(False)
        elif 'exit' in answers["tasks"]:
            running = False
            
        
            
            
            
            
            
            