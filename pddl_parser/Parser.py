# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 16:13:29 2013

@author: quare
"""

import parsley
import ometa
import PDDL3_File as pd
import Data_Structures as ds
import Errors as e
import random,string,copy,sys

def list2dict_withDupErr(l,mess):
    d=dict(l)
    if len(d)==len(l):
        return d
    else:
        raise e.SemanticError(mess)

def param_Set_from_typeList(par_list,isVar):
    '''
    Method that generates a Parameter_Set giving a list of parameter and the entity
    '''
    if type(isVar)==bool: #if type is bool
        l=[(name,(typ,isVar)) for (name,typ) in par_list]
    else: #isVar=None
        l=[(name,(typ,isV)) for ((name,typ),isV) in zip(par_list,isVar)]        
        
    return ds.Parameter_Set(l)
 
contatore=0
def stampa(lit):
    lit.negate()
    print(lit)
	
    
def rand_str(size=6, chars=string.ascii_letters + string.digits):
     return ''.join(random.choice(chars) for x in range(size))

def pddl3_parsing(f):
    
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
    
        
    non_stat_pred=[]
    #parsing    
    gramm = parsley.makeGrammar("""
    #UTILITY    
    digit_no_zero = anything:x ?(x in '123456789') -> x
    number = ('-' |'+' | -> ''):sign (<((digit_no_zero digit*)|digit)>:ds) ((<('.' digit*)>:f_part -> float(sign+ds+f_part))| -> int(sign + ds))
    
    name =  < letter (letterOrDigit | '_' letterOrDigit | '-' letterOrDigit)*>:var_n -> var_n
    
    var='?' name
    
    ms = (' ' | '\\n' | '\\t')+
    
    #BNF of PDDL3
    parse = ws (domain | problem):pddl3_file ws -> pddl3_file
    
    #DOMAIN  
    domain = '(' ws 'define' ws '(' ws 'domain' ms name:n ws ')'  ws (require_def|(->[])):req ws (type_def| (->{})):typ ws (predicates_def| (->{})):pred ws (constants_def| (->{})):const ws (functions_def | (-> {}) ):f ws (constraints | (-> None) ):c (ws structure_def:s -> s)*:act ws ')' 
            -> pd.Domain(n,req,typ,const,pred,f,act,c)
    
    #REQUIREMENTS
    require_def = '(' ws ':requirements' (ms require_key )+:l ws ')' -> list(set(l)) 
    require_key = (':strips' | ':typing' | ':negative-preconditions' | ':disjunctive-preconditions' |
                ':equality' | ':existential-preconditions' | ':universal-preconditions' | ':quantified-preconditions' |
                ':conditional-effects' | ':fluents' | ':adl' | ':durative-actions' | ':derived-predicates' |
                ':timed-initial-literals' | ':preferences' | ':constraints' ):r -> r
    
    #TYPES
    type_def = '(' ws ':types' ms typed_list('name'):l ws ')' -> list2dict(l,'Double reference to the same type.')
    typed_list :x = ((( supp_list(x):names ms '-' ms type:t (ms typed_list(x):t2 (->t2) | (->[]) ):tail ) -> [(n,t) for (n,b) in names]+tail) | ( (supp_list(x) | (->[])):l -> [(a,'object') for (a,b) in l]) ):r  -> r
    supp_list :x= !(self.apply(x)):head (ms !(self.apply(x)))*:tail ->[head]+tail
    type = ( ('(' ws 'either' ms primitive_type:h ms primitive_type*:l  ws ')' -> [h]+l ) | primitive_type ):t -> t
    primitive_type = name
    
    #CONSTANTS
    constants_def = '(' ws ':constants' ms typed_list('name'):l ws ')' -> list2dict(l,'Double reference to the same constant.')
    
    #PREDICATES
    predicates_def = '(' ws ':predicates' ws atomic_formula_skeleton+:l ')' -> list2dict(l,'Double reference to the same predicate.')
    atomic_formula_skeleton = '(' ws predicate:p (ms typed_list('var'):t (-> t) | (-> [])):tl ws ')' ws -> (p,gen_ps(tl,True))
    predicate = name
    
    
    #FUNCTIONS
    functions_def = '(' ws ':functions' func_typed_list('atomic_func_skeleton'):l ws ')' -> list2dict(l,'Double reference to the same function.')
    func_typed_list :x = ((( ((ms !(self.apply(x)):f ) -> f )+:funcs ms '-' ms func_type:t func_typed_list(x):tail) -> [(n,(p,t)) for ((n,p),b) in funcs]+tail) | (( ((ms !(self.apply(x)):f ) -> f )*:l )-> [(n,(p,'number')) for ((n,p),_) in l])):r  -> r
    func_type = <'number'>:t -> t
    atomic_func_skeleton = '(' ws function_symbol:n typed_list('var'):tl ws ')' -> (n,gen_ps(tl,True))
    function_symbol = name
    
    #STRUC_DEF
    structure_def = (action_def | durative_action_def | derived_def):r -> r
    
    #ACTION
    action_def = '(' ws ':action' ms action_symbol:n ms ':parameters' ws '(' ws typed_list('var'):p ws ')' ws action_def_body:t ws ')' -> ds.Action(n,gen_ps(p,True),t[0],t[1])
    action_symbol = name
    action_def_body = ((':precondition' ws ((pre_gd(ds.Precondition_Set([],{})):pr !(pr.process_cond()) -> pr) | ('(' ws ')' ->None)):p -> p) | (-> None)):prec ws ((':effect' ws (effect | ('(' ws ')' -> None)):e -> e) | (-> None)):eff
                    -> (prec,eff)
    #PRECONDITIONS
    pre_gd :ps =('(' ws 'preference' ms (pref_name | (->rand_str())):pn ms gd:g ws ')' !(ps.add_pref(ds.Preference(pn,g)))
                | '(' ws 'and' (ws pre_gd(ps))* ws ')'
                | gd:g !(ps.goal_descriptors.append(g))
                | '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws pre_gd(ds.Precondition_Set([],{})):p !(p.process_cond()) ws ')' !(ps.goal_descriptors.append(ds.Forall_Precond(gen_ps(pars,True),p,'forall')))) -> ps
    pref_name = name
    gd = literal('term') 
        | ( '(' ws 'and' (ws gd:g -> g)*:gl ws ')' -> ds.And_Or_GD('and',gl) )
        | ( '(' ws 'or' (ws gd:g -> g)*:gl ws ')' -> ds.And_Or_GD('or',gl) )
        | ( '(' ws 'not' ws gd:g ws ')' !(g.negate()) -> g )
        | ( '(' ws 'imply' ws gd:g1 ws gd:g2 ws ')' !(g1.negate()) -> ds.And_Or_GD('or',[g1,g2]) )
        | ( '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws gd:g ws ')' -> ds.Forall_Exists_GD(gen_ps(pars,True),g,'forall'))   
        | ( '(' ws 'exists' ws '(' ws typed_list('var'):pars ws ')' ws gd:g ws ')' -> ds.Forall_Exists_GD(gen_ps(pars,True),g,'exists'))
        | f_comp
    f_comp ='(' ws binary_comp:op ms f_exp:f1 ms f_exp:f2 ws ')' -> ds.F_Exp(op,[f1,f2])
    literal :x = atomic_formula(x) | ('(' ws 'not' ws atomic_formula(x):l ws ')' !(l.negate()) -> l ) 
    atomic_formula :x = ( ?(x=='name') '(' ws predicate:p (ms name:t ->(t,False) )*:tl ws ')' 
                       |  '(' ws predicate:p (ms !(self.apply(x)):t ->t[0])*:tl ws ')'   
                       | '(' ws '=':p ms ( !(self.apply(x)):t1 ms !(self.apply(x)):t2 (->[t1[0],t2[0]]) ):tl  ws ')' )
                       -> ds.Literal(p,gen_ps([(n,None) for (n,_) in tl],[isVar for (_,isVar) in tl]))
    term = (name:n -> (n,False)) | ( var:n -> (n,True))
    f_exp = ( number:n -> ds.F_Exp(value=n))  
            | ( '(' ws multi_op:op ms f_exp:f1 (ms f_exp:fn -> fn)+:fl ws ')' -> ds.F_Exp(op,[f1]+fl) )
            | ( '(' ws binary_op:op ms f_exp:f1 ms f_exp:f2 ws ')' -> ds.F_Exp(op,[f1,f2]) )
            | ( '(' ws '-' ms f_exp:f1 ws ')' -> ds.F_Exp('-',[f1]) ) 
            | ( f_head )
    f_head =  ( '(' ws function_symbol:fs (ms term:t -> t)*:tl ws ')' -> ds.F_Exp(fs,gen_ps([(n,None) for (n,_) in tl],[isVar for (_,isVar) in tl]))) 
            | ( function_symbol:fs -> ds.F_Exp(fs) )
    binary_op = multi_op | '-' | '/'
    multi_op = '*' | '+'
    binary_comp = '>=' | '<=' | '>' | '<' | '='
    
    
    #EFFECTS
    effect = ('(' ws 'and' (ws c_effect:e -> e)*:el ws ')' -> ds.Effect_Set(el))
            | (c_effect:e -> ds.Effect_Set([e]) ) 
    c_effect = ( '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws effect:e ws ')' -> ds.Forall_Exists_GD(gen_ps(pars,True),e,'forall'))  
                | ( '(' ws 'when' ws gd:g ws cond_effect:c_e ')' -> ds.When_GD(g,c_e) ) 
                | p_effect
    p_effect =  ( '(' ws assign_op:op ms f_head:f1 ms f_exp:f2 ws ')' -> ds.F_Exp(op,[f1,f2]) ) 
                | (literal('term'):l !(non_stat_pred.append(l.predicate)) -> l )
    cond_effect = ('(' ws 'and' (ws p_effect:e -> e)*:el ws ')' ->ds.Effect_Set(el) ) | (p_effect:e -> ds.Effect_Set([e]))
    assign_op = 'assign' | 'scale-up' | 'scale-down' | 'increase' | 'decrease'
    
    
    #DURATIVE ACTION (NOT READY)
    durative_action_def = '(' ws ':durative-action' ms da_symbol:n ms ':parameters' ws '(' ws typed_list('var'):p ws ')' ws da_def_body:t ws ')' -> ds.Action(n,gen_ps(p,True),t[0],t[1],t[2])
    da_symbol = name
    da_def_body = ':duration' ws duration_constraint:cons ws ':condition' ws ((da_gd(ds.Precondition_Set([],{})):pr !(pr.process_cond()) -> pr) | ('(' ws ')' ->None)):prec ws ':effect' ws (da_effect | ('(' ws ')' ->None)):eff -> (prec,eff,cons) 
    
    #DA_COND
    da_gd :ps = ('(' ws 'preference' ms (pref_name | (->rand_str())):pn ms timed_gd:g ws ')' !(ps.add_pref(ds.Preference(pn,g)))
                | '(' ws 'and' (ws da_gd(ps))* ws ')'
                | timed_gd:g !(ps.goal_descriptors.append(g))
                | '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws da_gd(ds.Precondition_Set([],{})):p !(p.process_cond()) ws ')' !(ps.goal_descriptors.append(ds.Forall_Precond(gen_ps(pars,True),p,'forall')))) -> ps
    timed_gd =    ( '(' ws 'at' ms time_specifier:op ws gd:g ws ')' -> ds.Timed_GD(g,op,None))
                | ( '(' ws 'over' ms interval:i ws gd:g ws ')' -> ds.Timed_GD(g,None,i))
    time_specifier = 'start' | 'end'
    interval = 'all'
    
    #DA_CONSTRAINTS
    duration_constraint = ( '(' ws 'and' ws simple_duration_constraint+:l ws ')' -> l )
                        | ( '(' ws ')' -> [] )
                        | ( simple_duration_constraint:s -> [s] )
    simple_duration_constraint = ( '(' ws d_op:op ms '?duration' ms d_value:v ws ')' -> ds.Duration_Constraint(d_op=op,duration=v) )
                                | ( '(' ws at ms time_specifier:ts ws simple_duration_constraint:dc ws ')' -> ds.Duration_Constraint(ts,dc) )
    d_op = '<=' | '>=' | '='
    d_value = f_exp
    
    #DA_EFFECTS (DATA STRUCTURE NOT READY)
    da_effect = ('(' ws 'and' (ws da_effect:e -> e)*:el ws ')' -> ds.Effect_Set(el))
            | (timed_effect:e -> ds.Effect_Set([e]) )
            | ( '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws da_effect:e ws ')' -> ds.Effect_Set([ds.Forall_Exists_GD(gen_ps(pars,True),e,'forall')]))  
            | ( '(' ws 'when' ws da_gd:g ws timed_effect:t_e ')' -> ds.When_GD(g,ds.Effect_Set([t_e]))) 
    timed_effect =  ( '(' ws assign_op_t:op ms f_head:f1 ms f_exp_t:f2 ws ')' -> ds.F_Exp(op,[f1,f2]) ) 
                | ( '(' ws at ms time_specifier:ts ws ( timed_effect | f_assign_da ):g ws ')' -> ds.Timed_GD(g,ts,None) )
    f_assign_da = '(' ws assign_op:op ms f_head:f1 ms f_exp_da:f2 ws ')' -> ds.F_Exp(op,[f1,f2])
    f_exp_da = ( '?duration' -> ds.F_Exp())  
            | ( '(' ws binary_op:op ms f_exp_da:f1 ms f_exp_da:f2 ws ')' -> ds.F_Exp(op,[f1,f2]) )
            | ( '(' ws '-' ms f_exp_da:f1 ws ')' -> ds.F_Exp('-',[f1]) ) 
            | f_exp
    assign_op_t = 'increase' | 'decrease'
    f_exp_t = '(' ws '*' ms f_exp ms '#t' ws ')' | '(' ws '*' ms '#t' ms  f_exp ws ')' | '#t'
    
    #DERIVED PREDICATES
    derived_def = '(' ws ':derived' ws atomic_formula_skeleton:t ws gd:g ws ')' -> ds.Derived_Predicate(t[0],t[1],g)
    
    #CONSTRAINTS
    constraints = '(' ws ':constraints' ms pref_con_gd(ds.Precondition_Set([],{})):p !(p.process_cond()) ws ')' -> p
    pref_con_gd :ps =('(' ws 'preference' ms (pref_name | (->rand_str())):pn ms con_gd:g ws ')' !(ps.add_pref(ds.Preference(pn,g)))
                    | '(' ws 'and' (ws pref_con_gd(ps))* ws ')'
                    | con_gd:g !(ps.goal_descriptors.append(g))
                    | '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws pref_con_gd(ds.Precondition_Set([],{})):p !(p.process_cond()) ws ')' !(ps.goal_descriptors.append(ds.Forall_Precond(gen_ps(pars,True),p,'forall')))) -> ps
    con_gd = ( '(' ws 'and' (ws con_gd:g -> g)*:gl ws ')' -> ds.And_Or_GD('and',gl) )
            | ( '(' ws 'forall' ws '(' ws typed_list('var'):pars ws ')' ws con_gd:g ws ')' -> ds.Forall_Exists_GD(gen_ps(pars,True),g,'forall'))
            | ( '(' ws ('always-within'):op ms number:n ms con2_gd:g1 ws con2_gd:g2 ws ')' -> ds.Trajectory_GD(op,g1,g2,n) )
            | ( '(' ws ('sometime-after' | 'sometime-before' ):op ws con2_gd:g1 ws con2_gd:g2 ws ')' -> ds.Trajectory_GD(op,g1,g2) )
            | ( '(' ws ('at end' | 'always' | 'sometime' | 'at-most-once'):op ws con2_gd:g ws ')' -> ds.Trajectory_GD(op,g) )
            | ( '(' ws ('within' | 'hold-after'):op ms number:n ms con2_gd:g ws ')' -> ds.Trajectory_GD(op,g,num1=n) )
            | ( '(' ws ('hold-during'):op ms number:n1 ms number:n2 ms con2_gd:g ws ')' -> ds.Trajectory_GD(op,g1,num1=n1,num2=n2) )
    con2_gd = gd
    #        | con_gd
    
    #PROBLEM
    problem = '(' ws 'define' ws '(' ws 'problem' ms name:pn ws ')' ws '(' ws ':domain' ms name:dn ws ')' ws (require_def|(->[])):req ws (object_declaration| (->{})):obj ws init:inits ws goal:gs ws (constraints| (->ds.Precondition_Set([],{}))):c ws (metric_spec | (-> None) ):m ws ')'
            -> pd.Problem(pn,dn,req,obj,inits,gs,c,m)
    object_declaration = '(' ws ':objects' ms typed_list('name'):tl ws ')' -> list2dict(tl,'Double reference to the same object.')
    init = '(' ws ':init' (ws init_el:ie -> ie)*:il ws ')' -> il
    init_el = literal('name')
            | ('(' ws '=':op ms f_head:f ms number:n ws ')' -> ds.F_Exp(op,[f,n]))
            | ('(' ws 'at':op ms number:n ms literal('name'):l ws ')' -> ds.Timed_GD(l,op,n))
    goal = ('(' ws ':goal' ms (pre_gd(ds.Precondition_Set([],{}))):ps ws ')' !(ps.process_cond()) -> ps)
         | ('(' ws ':goal' ws ')'  -> ds.Precondition_Set([],{})) 
    metric_spec = '(' ws ':metric' ms optimization:op ms metric_f_exp:f ws ')' -> ds.Metric_Spec(op,f)
    optimization = 'maximize' | 'minimize'
    metric_f_exp = ( number:n -> ds.F_Exp(value=n))  
                  | ( '(' ws multi_op:op ms metric_f_exp:f1 (ws metric_f_exp:fn -> fn)+:fl ws ')' -> ds.F_Exp(op,[f1]+fl) )
                  | ( '(' ws binary_op:op ms metric_f_exp:f1 ms metric_f_exp:f2 ws ')' -> ds.F_Exp(op,[f1,f2]) )
                  | ( '(' ws '-' ms metric_f_exp:f1 ws ')' -> ds.F_Exp('-',[f1]) ) 
                  | ( '(' ws function_symbol:fs (ms name:t -> t)*:tl ws ')' -> ds.F_Exp(fs,ds.Parameter_Set([(n,(None,False)) for n in tl])))
                  | ( function_symbol:fs -> ds.F_Exp(fs) )
                  | ( 'total-time':op -> ds.F_Exp(op) )
                  | ( '(' ws 'is-violated':op ms pref_name:pn ws ')' -> ds.F_Exp(op,[pn]) )
                  
    
    """, {"ds": ds, "pd": pd, "list2dict":list2dict_withDupErr, "gen_ps":param_Set_from_typeList, "rand_str":rand_str, "stampa":stampa,"non_stat_pred":non_stat_pred})

    try:    
        ds_pddl = gramm(f_in_a_row).parse()
        
        #recognize static preds in the domain
        if isinstance(ds_pddl,pd.Domain) and len(non_stat_pred)!=len(ds_pddl.predicates):
            stat_pred=copy.copy(ds_pddl.predicates)
            for i in non_stat_pred:  
                if stat_pred.has_key(i):
                    stat_pred.pop(i)
            ds_pddl.invariants=stat_pred
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