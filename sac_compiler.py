#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 16:12:01 2013

@author: quare
"""


import pddl_parser.PDDL3_File as m
import time
import os



import sys, getopt

def main(argv):
    '''
    main function
    '''
    directory = ''
    domain_filename=''
    problem_filename=''
    output_filename=''
    try:
        opts, args = getopt.getopt(argv,"d:o:f:r:")
    except getopt.GetoptError:
        print 'sac_compiler.py -d <directory> -o <domainfile> -f <problemfile> -r <resultfile>'
        sys.exit(2)
    if len(opts)!=4:
        print 'sac_compiler.py -d <directory> -o <domainfile> -f <problemfile> -r <resultfile>'
        sys.exit()
    for opt, arg in opts:
        if opt == "-d":
            directory = arg
        elif opt == "-o":
            domain_filename = arg    
        elif opt == "-f":
            problem_filename = arg
        elif opt == "-r":
            output_filename = arg 
    
    #directory="PDDL3_ex/"
    #domain_filename="domain.pddl"
    #problem_filename="p04.pddl"
    #output_filename="comp"
    
    
    mod_pddl=m.Model() #instantiate a model
    
    
    time_start = time.clock()
    tot_time_start=time_start

    mod_pddl.save_in_memory(directory+"/",domain_filename,problem_filename) #save the structure of a pddl3 model in memory
    
    time_elapsed = (time.clock() - time_start)
    print("Save in memory: " + str(time_elapsed)+"s")
    
   
    mod_strips = mod_pddl.adl2strips() #new model in strips (without constraints, functions and preferences)
   
    
    #joining pddl and strips
    new_dom=mod_strips.new_dom
    print('New Domain created')
    mod_strips.new_prob.join_pddl(mod_pddl,new_dom) 
    print('New Problem created')
    
    time_start = time.clock()
    mod_strips.separation_in_operator_classes() 
    time_elapsed = (time.clock() - time_start)
    print("Separation in class: " + str(time_elapsed)+"s")
    print("Classification of operators done")
    
    
    #compiling
    time_start = time.clock()
    comp_mod=mod_strips.compile_model()
    time_elapsed = (time.clock() - time_start)
    print("Compiling time: " + str(time_elapsed)+"s")
    print("Compiled")
    string_dom=str(comp_mod.new_dom)
    
    string_prob=str(comp_mod.new_prob)
    
    if not os.path.exists(directory+"/output"):
        os.mkdir(directory+"/output")
    temp_dom_f=open(directory+"/output/"+output_filename+"_dom.pddl","w")
    temp_dom_f.write(string_dom)
    temp_dom_f.close()
        
    temp_prob_f=open(directory+"/output/"+output_filename+"_prob.pddl","w")
    temp_prob_f.write(string_prob)
    temp_prob_f.close()
    
    tot_time_elapsed = (time.clock() - tot_time_start)
    print("Total: " + str(tot_time_elapsed)+"s")
    
    #os.system('./adl2strips-linux -p output/ -o comp_dom.pddl -f comp_prob.pddl')
            
    return
    
if __name__ == "__main__":
   main(sys.argv[1:])    
    
    #dom_strips,prob_strips=p.transform(dom_pddl,prob_pddl) #strips file is created
        
    #try:
        #f_str=open(directory+domain_filename+".strips","w")
        #f_str.write(dom_strips) #writing output file
        #f_str.close()
    #except IOError:
        #print("Problems writing domain output")
        #return -1
    
    #try:
        #f_str=open(directory+problem_filename+".strips","w")
        #f_str.write(prob_strips) #writing output file
        #f_str.close()
    #except IOError:
        #print("Problems writing problem output")
        #return -1
    
    
    #print("output files produced") #everything was correct
    #return 0
    
        
    
    
    
