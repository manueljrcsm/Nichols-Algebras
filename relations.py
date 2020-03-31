# -*- coding: utf-8 -*-

import numpy as np
import sage
from sage.combinat.q_analogues import q_factorial

PBW_GENERATORS = ('x','y')

def degree(word):
    deg = np.zeros(len(PBW_GENERATORS),dtype=int)
    for letter in word:
        for generator in PBW_GENERATORS:
            if letter == generator:
                index = PBW_GENERATORS.index(generator)
                deg[index] +=1
                break     
    return deg #in Z^2

# consider importing sage.combinat.q_analogues.q_int outside of Anaconda (running via a SAGE Jupyter Notebook), similar for q_factorial
def q_int(n,q):
    # only works with 
    result = 0
    for i in range(n):
        result+=q**i
    return result

def q_factorial(n,q):
    result = 1
    for i in range(n):
        result *= q_int(i+1,q)
    return result

def q_bilinear(first,second):
    
    return
        
    
