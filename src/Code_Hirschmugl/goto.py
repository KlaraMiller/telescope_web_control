# -*- coding: utf-8 -*-
"""
* Checkbox question example
* run example by typing `python example/checkbox.py` in your console
"""

from __future__ import print_function, unicode_literals
import os
import nav
import time
import datetime
import math
import threading
import sys
import tty
from pyfiglet import Figlet
import myGPS
from colorama import Fore, Back, Style


# my librarys
import motor_control
import common
#import nmod_GPS
import observe



from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def main(mydata):
    f = Figlet(font='slant')
    running = True
    while running:
        os.system('clear')
        print(f.renderText('Stargate XX'))
        print('system date and time')
        print(datetime.datetime.utcnow())
        print('Status and Data')
        print('Status and Data' + Fore.RED + 'some red text')
        print(Back.GREEN + 'and with a green background')
        print(Style.DIM + 'and in dim text')
        print(Style.RESET_ALL)
        common.print_status('nmod nav status', mydata.get_nmod_nav())
        common.print_status('nmod gps status', mydata.get_nmod_gps())
        print('################ nmod gps status ################')
        print('latitude    :' + str(mydata.get_gps_latitude()))
        print('longitude    :' + str(mydata.get_gps_longitude()))
        print('altitude    :' + str(mydata.get_gps_altitude()))
        print('time UTC    :' + str(mydata.get_gps_time()))
        print('################ motor diff ################')
        print('motor 1    :' + str(mydata.get_motor1_diff()))
        print('motor 2    :' + str(mydata.get_motor2_diff()))    

        questions = [
            {
                'type': 'checkbox',
                'qmark': '?',
                'message': 'Select task',
                'name': 'tasks',
                'choices': [ 
                    Separator('= star ='),
                    {
                        'name': 'Vega',
                    },
                    {
                        'name': 'Enif',
                    },
                    {
                        'name': 'Boteln',
                    },
                    Separator('= planets ='),
                    {
                        'name': 'mars',
                    },
                    {
                        'name': 'venus',
                    },
                    {
                        'name': 'saturn',
                    },
                    Separator('= sat and moon ='),
                    {
                        'name': 'moon',
                    },
                    {
                        'name': 'iss',
                    },
                    Separator('= options ='),
                    {
                        'name': 'exit'
                    }
                ]
            }
        ]

        answers = prompt(questions, style=custom_style_2)
        pprint(answers)
        print(len(answers["tasks"]))
        if len(answers["tasks"]) > 5:
            print('### Please choose only one task at a time ###')
        elif len(answers["tasks"]) < 1:
            print('### Please choose at least one task ###')
        else:
            if 'Vega' in answers["tasks"]:
                observe.main(mydata)
            elif 'nmod' in answers["tasks"]:
                nav.main(mydata)
                print(mydata.get_nmod_nav())
                nmod_nav_ok = mydata.get_nmod_nav()
            elif 'gps' in answers["tasks"]:
                myGPS.main(mydata)
                print(mydata.get_nmod_gps())
                nmod_gps_ok = mydata.get_nmod_gps()
            elif 'manuel_correction' in answers["tasks"]:
                motor_control.mode_manuel(mydata)
            elif 'star3_verification' in answers["tasks"]:
                test2 = nav.testing()
            elif 'exit' in answers["tasks"]:
                    running = False
        
            
            
            
            
            
            