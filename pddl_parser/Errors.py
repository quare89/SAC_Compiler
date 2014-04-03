# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:26:15 2013

@author: quare
"""

class SemanticError(Exception):
    def __init__(self,mess,line=0):
        self.line=line
        self.mess=mess
        
    def  __str__(self):
        return "Semantic Error at line "+str(self.line)+": "+self.mess
        
class NotManagedException(Exception):
    def __init__(self,loc,mess):
        self.loc=loc
        self.mess=mess
        
    def  __str__(self):
        return "ERROR, element not managed: in "+self.loc+", "+self.mess   
    