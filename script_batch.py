
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 04:43:17 2014

@author: quare
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 16:12:01 2013

@author: quare
"""


import os,sys


def main():
    test=True
    prob=sys.argv[1]
    for i in range(0,21):
        if i<10:
            i_str="0"+str(i)
        else:
            i_str=str(i)            
        
        
        log_file="out_"+prob+".log"
        if os.path.exists("../"+prob+"_test/p"+i_str+".pddl"):
            if test:
                symb=">"
                test=False
            else:
                symb=">>"
            os.system("python sac_compiler.py -d ../"+prob+"_test -o domain.pddl -f p"+i_str+".pddl -r comp"+i_str+" "+symb+log_file)
    
if __name__ == "__main__":
   main()      
