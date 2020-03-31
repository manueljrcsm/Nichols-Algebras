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

    
