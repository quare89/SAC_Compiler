# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 16:13:29 2013

@author: quare
"""

import parsley
import ometa
import STRIPS_File as sf
import pddl_parser.Data_Structures as ds
import pddl_parser.Errors as e
import string
import sys

contatore=0
def stampa():
    global contatore
    contatore=contatore+1
    if contatore%5000==0:
        print(contatore)
    
def strips_parsing(f):
    
    #preparsing
    f.seek(0)     
    #    f_lines = f.readlines()
    #    f_lines = [lin[:-1] for lin in f_lines if (lin[0]!=';' and lin[0]!='\n') ]
    #            
    #    f_in_a_row = string.join(f_lines)
    #    f_in_a_row=f_in_a_row.replace('\t',' ')
    #    f_in_a_row=f_in_a_row.replace('\n',' ')    
    
    f_lines = f.readlines()
    f_str=[]
    for lin in f_lines:
        if len(lin.lstrip())>0 and lin.lstrip()[0]==';' : lin='\n'
        f_str.append(lin)
    
    f_in_a_row = string.join(f_str)
    f_in_a_row=f_in_a_row.lower()
    
    
        
    #parsing    
    gramm = parsley.makeGrammar("""
    #UTILITY    
    
    name =  <lett*>:var_n -> var_n
    var='?' name
    lett = anything:x ?(x in 'abcdefghijklmnopqrstuvwxyz-_1234567890') -> x
    ms = (' ' | '\\n' | '\\t')+
    
    #BNF of PDDL3
    parse = ws (domain | problem):pddl3_file ws -> pddl3_file
    
    #DOMAIN  
    domain = '(' ws 'define' ws '(' ws 'domain' ms name:n ws ')'  ws (require_def|(->[])) ws (predicates_def| (->[])):preds (ws action_def:a -> a)*:acts ws ')' 
            -> sf.New_Domain(n,preds,acts)
    
    #REQUIREMENTS
    require_def = '(' ws ':requirements' ms ':strips' ws ')' 
    
    #PREDICATES
    predicates_def =  '(' ws ':predicates' ms literal:lh (ws literal:l -> l)*:lt ws ')' -> set([lh]+lt)
    predicate = name
    
    #ACTION
    action_def = !(stampa()) '(' ws ':action' ms action_symbol:n ms ':parameters' ws '(' ws ')' ws action_def_body:t ws ')' -> sf.New_Action(None,(n,t[0],t[1]))
    action_symbol = name
    action_def_body = ((':precondition' ws ( pre_gd | ('(' ws ')' ->None)):p -> p) | (-> None)):prec ws ((':effect' ws (pre_gd | ('(' ws ')' -> None)):e -> e) | (-> None)):eff
                    -> (prec,eff)
                    
    #PRECONDITIONS AND EFFECTS
    pre_gd = '(' ws 'and' (ws gd)*:gdl ws ')' -> set(gdl)
                | gd:g -> set([g])
    gd = literal 
        | ( '(' ws 'not' ws gd:g ws ')' !(g.negate()) -> g )
        
    literal = '(' ws predicate:p ws ')' -> ds.Literal(p)    
    
    #PROBLEM
    problem = '(' ws 'define' ws '(' ws 'problem' ms name:pn ws ')' ws '(' ws ':domain' ms name:dn ws ')' ws init:inits ws goal:gs ws ')'
            -> sf.New_Problem(pn,dn,inits,gs)
    init = '(' ws ':init' (ws literal:l -> l)*:ll ws ')' -> set(ll)
    goal = '(' ws ':goal' ms pre_gd:gs ws ')' -> gs
                 
    
    """, {"ds": ds, "sf": sf, "stampa":stampa})

    try:    
        ds_pddl = gramm(f_in_a_row).parse()
        
        #################    
        global contatore
        contatore=0
        ################
        return ds_pddl
    except ometa.runtime.ParseError, parserror:
        print(parserror.formatError())
        sys.exit()
    except e.SemanticError , semerror:
        print(semerror.message)
        sys.exit()
   
#gramm("(and (at ?t ?m) (preference c1 (ramon ?t)))").pre_gd()
#domain = '(' ws 'define' ws '(' ws 'domain' ws domain_name:d_name ws ')' ws (require_def | (-> [])):req ws
#        (type_def:typ)? ws (constant_def:const)? ws (predicates_def:pred)? ws (functions_def:funct)? ws 
#        (constraints:cons)? ws (structure_def)*:struc ws ')' -> pd.Domain(d_name)

#gramm("(:constraints (and (preference c1 (always (or (loaded goods1 truck1 level0) (stored goods1 level0)))) (stored g3 l4)))").constraints()

#(:durative-action turn :parameters (?current-target ?new-target - target) :duration (= ?duration (/ (angle ?current-target ?new-target) (turn-rate)))
#:condition (and (at start (pointing ?current-target))(at start (>= (propellant) propellant-required)) (at start (not (controller-in-use))))
#:effect    (and (at start (not (pointing ?current-target))) (at start (decrease (propellant) propellant-required))
                 # (at start (controller-in-use))
                  #(at start (vibration))
                  #(at end (not (controller-in-use)))
                  #(at end (not (vibration)))
                  #(at end (pointing ?new-target))))