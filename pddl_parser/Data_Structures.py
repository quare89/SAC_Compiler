# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:44:31 2013

@author: quare
"""

import Errors as err
import itertools,sys


flag_forall_grounding=True #activate the forall grounding 
time_spec_list=["start","end"]


def cart_prod_from_list(lit_list):
    code="list(itertools.product("
    for el in lit_list:
        code=code+str(el)+","
    code=code[:-1]+"))"
    return eval(code)


class Parameter_Set():
    '''
    Class defining a set of Parameters.
    
    A parameter is every attribute, either variable or not, with a type.
    
    The set is a list structured in this way: [(name,(type,isVariable))].
    
    '''
    
    def __init__(self,param_set=[]):
        self.param_set=param_set

    def __str__(self):
        string=""
        for (n,(t,isvar)) in self.param_set:
            
            if isvar:
                string+="?"
            if t is None:
                string+=n+" "
            else:
                string+=n+" - "+t+" "
                
        return string[:-1]
            
        
    


class Duration_Constraint:
    '''
    Class representing a Duration Constraint
    
    There are 2 kinds of duration constraint: 
        1. <d_op> ?duration <duration>
        2. at <time_spec> <dc_nested>
        
    So, the class permits to represent both the situations.
    '''       
    def __init__(self,time_spec=None,dc_nested=None,d_op=None,duration=None):
        self.time_spec = time_spec  #time specifier (start or end). It's an int value corresponding to the index in the time_spec_list
        self.dc_nested = dc_nested  #nested duration constraint for the duration constraints of type 2
        self.d_op = d_op            #durative operation (=,>=,<=)
        self.duration = duration    #duration
        
   
class Precondition_Set:
    '''
    Class defining a set of Preconditions. They may be of 2 types: Preferences or normal (Goal_Descriptor)
    A preference is a goal descriptor with a name, so it is represented inside a dictionary    
    '''
    def __init__(self,gd=[],pref={}):
             
        self.goal_descriptors=gd #list of preconditions
        self.preferences = pref  #dictionary of preferences
        
        self.proposition=None
    
    def __str__(self):
        return str(self.proposition)
    
    def process_cond(self):
        if len(self.goal_descriptors)>1:
            self.proposition=And_Or_GD('and',self.goal_descriptors)
        elif len(self.goal_descriptors)==1:
            self.proposition=self.goal_descriptors[0]
        else:
            self.proposition=None
            
            
    
    def add_pref(self,pref):
        if self.preferences.has_key(pref.name):
            raise(err.SemanticError("Double reference to the same preference "+pref.name))
        else:
            self.preferences[pref.name]=pref
            self.goal_descriptors.append(pref)
            
    
    def move_not_inwards(self):
        if self.proposition is not None:
            self.proposition.move_not_inwards()
    
    def ground_process(self,obj):
        new_gd=self.proposition.ground_process(obj)
        if new_gd is not None:
                self.proposition=new_gd
    
    def grounding(self,par_name,obj_list):
        prop_list=self.proposition.grounding(par_name,obj_list)
        
        return prop_list
    
    
    def convert2CNF_without_distribution(self,obj):
        if self.proposition is not None:
            #1st stage: DELETE IMPLY -> managed by the parser
        
            #2nd stage: MOVE NOT INWARDS
            self.proposition.move_not_inwards()
            
        
            #3rd stage: GROUND FORALL AND EXISTS
            new_cond=self.proposition.ground_process(obj)
            if new_cond is not None:
                self.proposition=new_cond
            
            
            
            if isinstance(self.proposition, And_Or_GD):
                self.proposition.normalize()
            '''
            res=[]
            
            #4th stage: DISTRIBUTE OR OVER AND
            try:
                self.proposition.normalize() #(a AND (b AND c)) becomes (a AND b AND c)
                res=self.proposition.distribute() #Distribution of or over and
            except:
                print("Distribution of OR over AND failed")
            
            
            return res
            '''
       

class Effect_Set():
    '''
    Class defining a set of effects (structured in Goal Descriptors)
    '''
    
    def __init__(self,gd=[]):
        self.gd=gd
        
           
    def __str__(self):
        string=""
        if len(self.gd)==0:
            string+="()"
        elif len(self.gd)==1:
            string+=str(self.gd[0])
        else:
            string+="(and "
            for g in self.gd:
                string+=str(g)+" "
            string+=")"    
        
        return string



class Goal_Descriptor:
    '''
    This is an interface. It's useless for the moment but it may have an utility in the future
    '''
        
    
    isNegate=False
    
    def negate(self):
        self.isNegate=not self.isNegate
        return self
    
    
        
    


class Action():
    '''
    Class defining an action.
    
    The action may be durative, if the duration constraints list is empty.
       
    '''
    
    
    def __init__(self,name,parameters=Parameter_Set(),preconditions=Precondition_Set(),
                 effects=Effect_Set(),dur_cons=[]):
        self.name=name                                  #name of the action
        self.parameters=dict(parameters.param_set)      #dictionary of parameters
        self.preconditions=preconditions                #preconditions field (Precondition_Set)
        self.effects=effects                            #effects field (Effects)
        self.dur_cons=dur_cons                          #duration constraints (list of Duration_Constraint)
        #self.verify_action()
  
        

class Preference(Goal_Descriptor):
    '''
    Class defining Preference
    '''
    def __init__(self,name,gd):
        self.name=name
        self.gd=gd

    def move_not_inwards(self):
        if self.isNegate:
            self.negate()
            self.gd.negate()
        self.gd.move_not_inwards()
    
    def ground_process(self,obj):
        new_gd=self.gd.ground_process(obj)
        if new_gd is not None:
                self.gd=new_gd
    
    def grounding(self,par_name,obj_list):
        prop_list=self.gd.grounding(par_name,obj_list)
        
        return [Preference(self.name+'-g'+str(n),p) for (p,n) in zip(prop_list,range(0,len(prop_list)))]
    

    
        
    
    def __str__(self):
        string=""
        if self.isNegate:
            string+="(not "
            
        string+="(preference "+self.name+" "+str(self.gd)+")"
        
        if self.isNegate:
            string+=")"
        
        string+="\n"
        return string


class Forall_Exists_Decl(Goal_Descriptor):
    '''
    Class describing a forall or exists declaration 
    '''
    def __init__(self,params,cond,for_ex_op):
        self.params=params
        self.cond=cond
        self.orig_cond=cond
        self.for_ex_op=for_ex_op  
        self.convert_dict={} #useful for the grounding
        self.flag=flag_forall_grounding
        
    def create_conv_dict(self,obj):
       
        #for each parameter, for each object, check the type and populate a dictionary with the param as key and the objects as value
        for (name,(typ,_)) in self.params.param_set:
            ob_list=[]            
            for n,t in obj.items():
                if typ == t: ob_list.append(n)
            if len(ob_list)>=1: self.convert_dict[name]=ob_list
    
    def ground_process(self,obj):
        new_cond=self.cond.ground_process(obj)
        if new_cond is not None:
            self.cond=new_cond            
        
        #if the flag "grounding forall" is activated, the proposition will be grounded
        #otherwise the proposition will be the original forall
        if self.for_ex_op=='forall' and not self.flag:
            return self
        
        self.create_conv_dict(obj)
        for par,obj_list in self.convert_dict.items():
            g=self.cond.grounding(par,obj_list)
            if len(g)>1:
                if self.for_ex_op=="exists":
                    self.cond=And_Or_GD('or',g)
                else:
                    self.cond=And_Or_GD('and',g)
            else:
                self.cond=g[0]
        
        return self.cond
    
    def grounding(self,par_name,obj_list):
        prop_list=self.cond.grounding(par_name,obj_list)
        return [Forall_Exists_GD(self.params,p,'forall') for p in prop_list]
        
    def __str__(self):
        string=""
        if self.isNegate:
            string+="(not "
            
        string+="("+self.for_ex_op+" ("+str(self.params)+") "+str(self.cond)+")"
        
        if self.isNegate:
            string+=")"
        
        return string
        
    
        
class Forall_Precond(Forall_Exists_Decl):
    '''
    Class that manages forall preconditions
    '''
    def move_not_inwards(self):
        if self.isNegate:
            self.negate()
            self.cond.proposition.negate()
            if self.for_ex_op == "exists":
                self.for_ex_op = "forall"
            else:
                self.for_ex_op = "exists"
       
        self.cond.move_not_inwards()


class Forall_Exists_GD(Forall_Exists_Decl):
    '''
    Class that manages forall and exists goal descriptors
    '''
    def move_not_inwards(self):
        if self.isNegate:
            self.negate()
            self.cond.negate()
            if self.for_ex_op == "exists":
                self.for_ex_op = "forall"
            else:
                self.for_ex_op = "exists"
        
        self.cond.move_not_inwards()
    
    

class Trajectory_GD(Goal_Descriptor):
    '''
    Class that manages goal descriptors on the trajectory of states
    '''
    def __init__(self,traj_op,gd1,gd2=None,num1=None,num2=None):
        self.traj_op=traj_op
        self.num1=num1
        self.num2=num2
        self.gd1=gd1
        self.gd2=gd2       
        
    def move_not_inwards(self):
        if self.traj_op=="always":
            if self.isNegate:
                self.negate()
                self.gd1.negate()
            self.gd1.move_not_inwards()
        else:
            print("modal operator not managed")
            sys.exit()
    
    def ground_process(self,obj):
        new_gd1=self.gd1.ground_process(obj) 
        if new_gd1 is not None:
            self.gd1=new_gd1        
        
        if self.gd2 is not None:
            new_gd2=self.gd2.ground_process(obj)
            if new_gd2 is not None:
                self.gd2=new_gd2
                
    
    def grounding(self,par_name,obj_list):
        n=len(obj_list)
        prop_list1=self.gd1.grounding(par_name,obj_list)
        prop_list2=[]
        if self.gd2 is not None:
            prop_list2=self.gd2.grounding(par_name,obj_list)
            
            if len(prop_list2)==len(prop_list1) :
                prop_list=zip(prop_list1,prop_list2)
            else:
                prop_list3=[prop_list2[0] for x in range(0,n)]
                prop_list=zip(prop_list1,prop_list3)
            return [Trajectory_GD(self.traj_op,p1,p2,self.num1,self.num2) for (p1,p2) in prop_list]
        else:
            return [Trajectory_GD(self.traj_op,p1,None,self.num1,self.num2) for p1 in prop_list1]
    
    def __str__(self):
        string=""
        if self.isNegate:
            string+="(not "
            
        string+="("+self.traj_op
        if self.num1 is not None:
            string+=" "+str(self.num1)
        if self.num2 is not None:
            string+=" "+str(self.num2)
        if self.gd1 is not None:
            string+=" "+str(self.gd1)
        if self.gd2 is not None:
            string+=" "+str(self.gd2)
        
        
        string+=")"
        
        if self.isNegate:
            string+=")"
        
        return string

        
class And_Or_GD(Goal_Descriptor):
    '''
    Class that manages And and Or goal descriptors
    '''
    def __init__(self,log_op,gd_list):
        self.log_op=log_op
        self.gd_list=gd_list
    
    def move_not_inwards(self):
        if self.isNegate:
            self.negate()
            self.invert_op()
            for gd in self.gd_list :
                gd.negate()
        for gd in self.gd_list:
            gd.move_not_inwards()
        
#    def verify_gd(self, act_params):
#        for gd in self.gd_list:
#            gd.verify_gd(act_params)
    
    def invert_op(self):
        if self.log_op=="and" : self.log_op="or"
        elif self.log_op == "or" : self.log_op="and" 
    
    
    def ground_process(self,obj):
        for i in range(0,len(self.gd_list)):
            new_gd=self.gd_list[i].ground_process(obj)
            if new_gd is not None:
                self.gd_list[i]=new_gd
        
    
    def grounding(self,par_name,obj_list):
        
        ground_list=[] #list that contains lists that result from the application of method 'grounding()' on every gd in gd_list
        for gd in self.gd_list:
            ground_list.append(gd.grounding(par_name,obj_list))
        
        n=len(obj_list)     #length of obj_list   

        no_empty=False #check if there is at least one parameter        
        
        #now ground_list contains all the possible proposition with an object instead a parameter.
        #with no parameters, the same proposition        
        
        for g in ground_list:
            if len(g)==n:
                no_empty=True
                break

        lit_list=[] #list of list literals that will become the gd_lists of the new and_or_gd      
        
            
        new_and_or=[]
        if no_empty:
            
            for i in range(0,n):
                lit_list.append([])
                
            for i in range(0,n): #for each object (instead of the parameter)
                for g in ground_list: #for each list of propositions
                    if len(g)!=n:
                        lit_list[i].append(g[0]) #add the same proposition everytime (no parameters inside)
                    else:
                        lit_list[i].append(g[i]) #add the i-th proposition to the and_or_gd
            
            for l in lit_list:
                new_prop=And_Or_GD(self.log_op,l)
                new_and_or.append(new_prop)
                
                        
                        
        return new_and_or                
                
    #function to not have AND (OR) proposition inside AND (OR) proposition
    #now AND and OR propositions are alternated
    def normalize(self):
        new_gd_list=[]
        for gd in self.gd_list:
            if isinstance(gd,Literal):
                gd=gd.ground_predicate()
                new_gd_list.append(gd)
            elif isinstance(gd,And_Or_GD):
                gd=gd.normalize()
                if self.log_op==gd.log_op:
                    new_gd_list.extend(gd.gd_list)
                else:
                    new_gd_list.append(gd)
            else:
                new_gd_list.append(gd)
                #raise err.NotManagedException(str(gd)," only OR and AND propositions are managed")
        
        self.gd_list=new_gd_list
        return self
    
    def distribute(self):
        lit_list=[]
        for gd in self.gd_list:
            if self.log_op=='and':
                if isinstance(gd,Literal):
                    lit_list.append([gd])
                elif isinstance(gd,And_Or_GD): #it's a OR proposition because of the normalize function
                    temp_list=gd.distribute() #distribute the nested proposition
                    lit_list.extend(temp_list) #temp list is a conjunction of disjuctions so temp_list extends lit_list
                else: #not managed
                    raise Exception
            else:
                if isinstance(gd,Literal):
                    lit_list.append([[gd]])
                elif isinstance(gd,And_Or_GD): #it's a AND proposition because of the normalize function
                    temp_list=gd.distribute() #distribute the nested proposition
                    lit_list.append(temp_list) #temp list is a conjunction of disjuctions so temp_list extends lit_list
                else: #not managed
                    raise Exception
        #end for
        if self.log_op=='and':
            return lit_list
        else:
            #we need a translation in numbers for every literal in lit_list because of the function cart_prod_from_list
            lit_dict={}  
            i=0
            
            lit_list1=[]
            for z in lit_list:
                z1=[]
                for y in z:
                    y1=[]
                    for x in y:
                        lit_dict[i]=x
                        x=i
                        y1.append(x)
                        i=i+1
                    z1.append(y1)
                lit_list1.append(z1)
                   
            temp_list=cart_prod_from_list(lit_list1) #cartesian product between all the disjunction inside the conjunctions
            temp_list=map(list,temp_list)
            return [[lit_dict[z] for y in x for z in y] for x in temp_list] #basically a list of every nested list of literals without other nested lists
        
    def __str__(self):
        string=""
        if self.isNegate:
            string+="(not "
            
        string+="("+self.log_op
        for gd in self.gd_list:
            string+=" "+str(gd)
        
        string+=")"
        
        if self.isNegate:
            string+=")"
        
        return string
            



class Literal(Goal_Descriptor):
    '''
    Class that manages a literal
    '''
    def __init__(self,predicate,terms=[]):
        
        self.predicate=predicate
        self.terms=terms
        
    def move_not_inwards(self):
        pass
#    def verify_gd(self, act_params):
#        pass
        
    def ground_predicate(self):
        
        new_name=self.predicate
        
        if new_name=="=":
            t1=self.terms.param_set[0][0]
            t2=self.terms.param_set[1][0]
            if t1==t2:
                if self.isNegate:
                    return Literal("#false#")
                else:
                    return Literal("#true#")
            else:
                if self.isNegate:
                    return Literal("#true#")
                else:
                    return Literal("#false#")
            
        for (n,_) in self.terms.param_set:
            new_name+="-"+n            
        
                       
        l=Literal(new_name)
        l.isNegate=self.isNegate
        
        return l
    
    def ground_process(self,obj):
        pass
    
    def grounding(self,par_name,obj_list):
        lis=[]
        ver= par_name in [x for (x,_) in self.terms.param_set]
        lit_list=[self]
        if ver:
            for _ in obj_list:
                lis.append([]) #initialize the resulting list with as many lists as the number of objects in the obj_list
            
            length=len(obj_list)
            
            for p in self.terms.param_set:
                (n,_)=p
                if n==par_name:
                    for i in range(0,length):
                        lis[i].append((obj_list[i],(None,False)))
                else:
                    for l in lis:
                        l.append(p)
            lit_list=[]      
            for l in lis:
                    new_lit=Literal(self.predicate,Parameter_Set(l))
                    new_lit.isNegate=self.isNegate
                    lit_list.append(new_lit)
        
        return lit_list
    
    def __eq__(self,y):
        return self.predicate==y.predicate and self.isNegate==y.isNegate
        
    def __ne__(self,y):
        return self.predicate!=y.predicate or self.isNegate!=y.isNegate
    
    def inverse(self,y):
        return self.predicate==y.predicate and self.isNegate!=y.isNegate
        
    def __hash__(self):
        return hash((self.isNegate,self.predicate,self.isNegate))
        
        
    def __str__(self):
        string=""
        if self.isNegate:
            string+="(not "
             
        string+="("+self.predicate
        
        if self.terms!=[]:
            string+=" "+str(self.terms)
            
        string+=")"
            
        if self.isNegate:
            string+=")"
        return string    
        
    
class F_Exp(Literal):
    '''
    Class defining a fluent expression
    
    This class defines an operation, a set of terms (other f_exp, function names) and an optional value
    '''
    def __init__(self,op=None,terms=[],value=None):
        self.predicate=op   #operation number in the op_list or function name
        self.terms=terms    #terms of the operation. They may depend by the funct name
        self.value=value    #f_expr could be a value. In this case, terms and op are None
    
    def __str__(self):
        string=""
        if self.value is not None:
            string=str(self.value)
            return string
        else:
            string+=str(Literal(self.predicate,self.terms))
    
    
        
    
class Metric_Spec:
    '''
    Class defining a metric.
    
    It has an operation (minimum or maximum) and a fluent expression.
    '''

    def __init__(self,optim_op=None,f_exp=None):
        self.optim_op=optim_op  #min or max
        self.f_exp=f_exp
    
    def __str__(self):
        string=self.optim_op+" "+str(self.f_exp)
        return string


######## THE FOLLOWING CLASSES ARE NOT USED AT THE MOMENT ###################

    
class Timed_GD(Goal_Descriptor):
    '''
    Class that manages a timed goal descriptor
    '''
    
    def __init__(self,gd,time_spec=None,interval=None):
        self.time_spec=time_spec  #start or end, None means <over all gd>
        self.gd=gd
        self.interval=interval
        
    def move_not_inwards(self):
        pass
#    def verify_gd(self, act_params):
#        self.gd.verify_gd(act_params)
    def ground_process(self,obj):
       self.gd.ground_process(obj)
        
class When_GD(Goal_Descriptor):
    '''
    Class that manages a conditional goal descriptor
    '''
    def __init__(self,gd_cond,cond_eff):
        self.gd_cond=gd_cond
        self.cond_eff=cond_eff  #Effect_set
    
    def __str__(self):
        string="(when "+str(self.gd_cond)+" "+str(self.cond_eff)+")"
        return string
        
    def move_not_inwards(self):
        pass
#    def verify_gd(self, act_params):
#        self.gd_cond.verify_gd(act_params)


    
class Op_F_Exp(F_Exp):
    '''
    Class that manages the fluent expressions with a normal operation
    '''
    pass

class Func_F_Exp(F_Exp):
    '''
    Class that manages the fluent expressions with functions
    '''
    pass

class Timed_F_Exp(F_Exp):
    '''
    Class that manages the temporal fluent expressions
    '''
    pass


class Derived_Predicate:
    '''
    Class that manages the derived predicates
    '''
    
    def __init__(self, name,par_set, gd):
        self.name=name
        self.par_set = par_set
        self.gd=gd
    
    def __str__(self):
        string="("+self.name+" "+str(self.par_set)+") "+str(self.gd)
        return string