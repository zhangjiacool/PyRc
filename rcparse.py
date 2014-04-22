'''
Created on Apr 21, 2014

@author: jzhang
'''
import rclex
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import ply.yacc as yacc


class MyClass(object):
    '''
    classdocs
    '''
    tokens = rclex.RcLex.tokens
    
    precedence = (
               ('left', 'PLUS','MINUS'),
               ('left', 'TIMES','DIVIDE'),
               ('left', 'POWER'),
               ('right','UMINUS')
               )


    def __init__(self):
        '''
        Constructor
        '''
        
    ###############################
    