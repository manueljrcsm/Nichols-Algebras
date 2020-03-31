import file1 #access functions, etc. by file1.function
from file1 import * or  bla #access by bla (instead of file1.bla)

import numpy as np

bilinear_matrix = [[]]
coproduct_list = []
order_pbw = []

#SEBASTIAN:  coproduct, bilinear, c_u
#MANUEL: degree,quantum_factorial, q_bilinear, polish other code

class PBWGenerator:
    """
        Objects are pbw generators
    """
    
    
    def __init_(self,handle,definition):
        """ 
            handle is the variable letter
            definition is dictionary
            
        """
    
        self.handle = handle
        self.definition = definition
        self.degree = degree(input)
        self.c = bilinear(definition,definition)
        
        #add the object to the order_pbw list
        order_pbw.append(self) #maybe?
        
def degree(word):
    deg = []
    for letter in word:
        
    return tuple #in Z^2

def coproduct(word):
    # try to use coproduct_list to save time
    return
    
def bilinear(first, second):
    #try to avoid computing things twice, using bilinear_list
    #recursive
    
    return scalar
 
def quantum_factorial(n):
    return 
    
def c_u(word):
    #product of quantum_factorial * pbwgen.c
    return
    
def q_bilinear(first,second):
    return 
    
def braided_commutator(first,second):
    """
        Expresses the braided commutator in terms of the PBW basis
    """
    #determine all the admissible u
    #word = sum all c_u(u) * u
    return word 


    
def compute_relations():
        relations = {}
        
        #compute and add the relations 
        for i in range(len(order_pbw)):
            for j in range(i,len(order_pbw)):
                relation[first * second] = q_bilinear* second * first + braided_commutator(first,second)
                
        return relations
        
        
