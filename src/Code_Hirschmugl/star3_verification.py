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
import time

# downloaded librarys
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2

# my librarys
import common
import observe

# variables
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def main(sg1 : common.stargate):
    running = True
    
    while running:
        common.header(sg1, '3 star verification')
    
        questions = [
            {
                'type': 'checkbox',
                'qmark': '?',
                'message': 'please select 3 stars',
                'name': 'tasks',
                'choices': [ 
                    Separator('= star ='),
                    {
                        'name': 'Polaris',
                    },
                    {
                        'name': 'Capella',
                    },
                        {
                        'name': 'Sirius',
                    },
                    {
                        'name': 'Prokyon',
                    },
                    {
                        'name': 'Aldebaran',
                    },
                    {
                        'name': 'Regulus',
                    },
                    {
                        'name': 'Hamal',
                    },
                    {
                        'name': 'Vega',
                    },
                    {
                        'name': 'Enif',
                    },
                    {
                        'name': 'Boteln',
                    },
                    {
                        'name': 'Acamar',
                    },
                    {
                        'name': 'Errai',
                    },
                    {
                        'name': 'Marsic',
                    },
                    {
                        'name': 'Naos',
                    },
                    {
                        'name': 'Procyon',
                    },
                    {
                        'name': 'Rukbat',
                    },
                    {
                        'name': 'Salm',
                    },                
                    Separator('= Options ='),
                    {
                        'name': 'debug mode',
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
        if (len(answers["tasks"]) > 3) and not 'exit' in answers["tasks"]:
            print('### Please choose 3 stars ###')
        elif (len(answers["tasks"]) < 3) and not 'exit' in answers["tasks"]:
            print('### Please choose 3 stars ###')
        elif not 'exit' in answers["tasks"]:
            print(answers.values())
            A = answers["tasks"][0]
            print (str(A))            
            sg1.mytarget.set_star1(answers["tasks"][0])
            sg1.mytarget.set_star2(answers["tasks"][1])            
            sg1.mytarget.set_star3(answers["tasks"][2])            
            time.sleep(1)
            running = False
            select(sg1)
        else:
            running = False
                
            
def select(sg1 : common.stargate):
    running = True
    
    while running:
        common.header(sg1, '3 star verification')
            
        print('star 1: ' + str(sg1.mytarget.get_star1()) + ' -> ', end='')
        common.print_status(sg1.mytarget.star1_ok)
        print('star 2: ' + str(sg1.mytarget.get_star2()) + ' -> ', end='')
        common.print_status(sg1.mytarget.star2_ok)  
        print('star 3: ' + str(sg1.mytarget.get_star3()) + ' -> ', end='')
        common.print_status(sg1.mytarget.star3_ok)  
        print('' )
    
    
        questions = [
            {
                'type': 'checkbox',
                'qmark': '?',
                'message': 'please select 3 stars',
                'name': 'tasks',
                'choices': [ 
                    Separator('= star ='),
                    {
                        'name': sg1.mytarget.get_star1(),
                    },
                    {
                        'name': sg1.mytarget.get_star2(),
                    },
                    {
                        'name': sg1.mytarget.get_star3(),
                    },                
                    Separator('= Options ='),
                    {
                        'name': 'debug mode',
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
        if (len(answers["tasks"]) > 1) and not 'exit' in answers["tasks"]:
            print('### Please choose 3 stars ###')
        elif (len(answers["tasks"]) < 1) and not 'exit' in answers["tasks"]:
            print('### Please choose 3 stars ###')
        elif not 'exit' in answers["tasks"]:
            print(answers.values())
            A = answers["tasks"][0]
            print (str(A))            
            sg1.mytarget.target = (answers["tasks"][0])           
            time.sleep(1)
            running = False
            observe.main(sg1, answers["tasks"][0])
        else:
            running = False           
            
            
            
            
            