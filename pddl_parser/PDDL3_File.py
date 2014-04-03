# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:33:37 2013

@author: quare
"""

import Data_Structures as ds
import handling.STRIPS_File as sf
import Parser as pd
import os,sys
import time

class Model:
    
    def __init__(self,dom_pddl=None,prob_pddl=None):
        self.dom=dom_pddl
        self.prob=prob_pddl
        
        
    
    def save_in_memory(self,directory,domain_filename,problem_filename):
        try:
            dom_f=open(directory+domain_filename,"r")
        except IOError:
            print "ERROR: File '", directory+domain_filename , "' not found"
            sys.exit()
    
        try:
            prob_f=open(directory+problem_filename,"r")
        except IOError:
            print "ERROR: File '", directory+problem_filename , "' not found"
            sys.exit()
        
        self.dom=pd.pddl3_parsing(dom_f) #parsing and data structuring for the domain
        dom_f.close()
        
        self.prob=pd.pddl3_parsing(prob_f) #parsing and data structuring for the problem
       
        prob_f.close()
        
    
    def adl2strips(self):
        new_Mod=sf.New_Model()        
        
        string_dom=self.dom.str_for_file(True)
        string_prob=self.prob.str_for_file(True)
        
               
        temp_dom_f=open("temp_dom.pddl","w")
        temp_dom_f.write(string_dom)
        temp_dom_f.close()
        
        temp_prob_f=open("temp_prob.pddl","w")
        temp_prob_f.write(string_prob)
        temp_prob_f.close()
        
        time_start = time.clock()
        os.system('./adl2strips-linux -o temp_dom.pddl -f temp_prob.pddl')
        time_elapsed = (time.clock() - time_start)
        print("ADL2STRIPS time: " + str(time_elapsed))
                
        time_start = time.clock()
        new_Mod.save_in_memory("","domain.pddl","facts.pddl")
        time_elapsed = (time.clock() - time_start)
        print("Save in memory: " + str(time_elapsed))               
        
        return new_Mod


class Problem():
    '''
    Class that represents a problem file
    '''
    def __init__(self,name,domain_name,requirements,ob,
                 init_state,goal_state,constraints,metric):
        self.name = name                    #name of the problem
        self.domain_name = domain_name      #name of the relative domain
        self.requirements = requirements    #list of requirements
        self.ob = ob                        #list of objects (Parameter_Set)
        self.init_state = init_state        #list of Goal_Descriptor as init_state
        self.goal_state = goal_state        #list of Preconditions as goal_state (Precondition_Set)
        self.constraints = constraints      #list of Preconditions as constraints
        self.metric = metric                #metric of the problem
        
        
    def str_for_file(self,for_adl2strips):
        string="(define (problem "+self.name+")\n"
        string+="(:domain "+self.domain_name+")\n"
        
        if self.requirements != [] :
            string+="(:requirements"        
            for r in self.requirements:
                if not for_adl2strips or r not in [":constraints",":fluents",":numeric-fluents",":object-fluents",":preferences"]:
                    string+=" "+r
            string+=")\n"
        
        if self.ob !={}:
            string+="(:objects"
            for o,t in self.ob.items():
                string+=" "+o+" - "+t
            string+=")\n"
        
        string+="(:init"
        for ie in self.init_state:
            string+="\n\t"+str(ie)
        string+=")\n"
        
        
        string+="(:goal "+str(self.goal_state)+")\n"
        
        if not for_adl2strips and self.constraints is not None:
            string+="(:constraints "+str(self.constraints)+")\n"
        
        if not for_adl2strips and self.metric is not None:
            string+="(:metric "+str(self.metric)+")\n"
        
        string+=")\n"
        
        return string
            


class Domain():
    '''
    Class that represents a domain file
    '''
    def __init__(self,name,requirements,types,constants,predicates,fluents,
                 actions,constraints):
        self.invariants=[]
        self.actions = {}
        self.derived_predicates = {}
        self.name = name                                #name of the domain
        self.requirements = requirements                #list of requirements
        self.types = types                              #dictionary of types
        self.constants = constants                      #dictionary of constants
        self.predicates = predicates                    #dictionary of predicates
        self.fluents = fluents                          #dictionary of fluents
        for a in actions:
            if isinstance(a,ds.Action):
                self.actions[a.name]=ds.Action(a.name,ds.Parameter_Set(),a.preconditions,a.effects,a.dur_cons)
                self.actions[a.name].parameters=a.parameters
            else:
                self.derived_predicates[a.name]=a
       
        self.constraints = constraints                  #list of Preconditions as constraints
        
        
    
    
    def str_for_file(self,for_adl2strips):
        string="(define (domain "+self.name+")\n"
        
        
        if self.requirements != [] :
            string+="(:requirements"        
            for r in self.requirements:
                if not for_adl2strips or r not in [":constraints",":fluents",":numeric-fluents",":object-fluents",":preferences"]:
                    string+=" "+r
            string+=")\n"
        
        if self.types !={}:
            temp_types=self.types
            string+="(:types"
            for typ,sup in temp_types.items():
                if sup=="object":
                    string+=" "+typ
                    temp_types.pop(typ)
            string+=" - object"
            for typ,sup in temp_types.items():
                string+=str_types(temp_types,typ,sup)
            
            
            string+=")\n"
        
        if self.predicates != {}:
            string+="(:predicates"
            for name,pars in self.predicates.items():
                string+="\n\t("+name+" "+str(pars)+")"
            string+=")\n"
        
        if self.constants != {}:
            string+="(:constants"
            for name,typ in self.constants.items():
                string+="\n\t"+name+" - "+typ
            string+=")\n"
        
        if not for_adl2strips and self.fluents != {}:
            string+="(:functions"
            for name,(pars,typ) in self.predicates.items():
                string+="\n\t("+name+" "+str(pars)+")"
            string+=")\n"
        
        #string actions
        
        for name,act in self.actions.items():
            if len(act.dur_cons)==0:
                string+="(:action "+name+"\n"
                string+=":parameters ("
                for p,(typ,_) in act.parameters.items():
                    string+=" ?"+p+" - "+typ                
                string+=")\n"
                string+=":precondition "+str(act.preconditions)+"\n"
                string+=":effect "+str(act.effects)+"\n"                
                string+=")\n"
            else:
                print("durative actions not managed.")
                sys.exit()
                
        for name,der in self.derived_predicates.items():
            string+="(:derived "+str(der)+")\n"
            
            
    
        
        
        if not for_adl2strips and self.constraints is not None:
            string+="(:constraints "+str(self.constraints)+")\n"
            
        
        
        
        string+=")\n"
        
        return string
        

def str_types(Tdict,typ,sup):
    string=""    
    while Tdict.has_key(typ):
        if Tdict.has_key(sup):
            string+=str_types(Tdict,sup,Tdict[sup])
        else:
            string+="\n\t"+typ+" - "+sup
            Tdict.pop(typ)
    
    return string
