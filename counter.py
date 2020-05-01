# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 17:46:44 2020

@author: Sebas
"""
import universe as u
import word as w
import math

class Counter:
    
    def __init__(self, start, end, target_degree):

        self.start = start
        self.end = end
        self.target_degree = target_degree
        self.counter = [0 for i in range(end-start+1)]
        self.heights = [determine_height(u.Universe.pbw_generators[j], self. target_degree) for j in range(start, end+1)]
        self.out_of_bounds = False

    def increment(self):
        
        i = self.end- self.start
        self.counter[i]  +=1
        
        overflow =  self.counter[i] > self.heights[i]
        
        
        while overflow:
            if(i > 0):
                self.counter[i] = 0
                i -= 1
                self.counter[i] += 1
                overflow =  self.counter[i] > self.heights[i]
            else:
                overflow = False
                self.out_of_bounds = True
                
    def round_up(self):
        
        i= self.end - self.start
        
        while self.counter[i] == 0 and i>0:
                i -= 1
        
        if i == 0:
            self.out_of_bounds = True
            return
        
        self.counter[i] = 0
        i -=1
        self.counter[i] += 1
        
        overflow =  self.counter[i] > self.heights[i]
        
        while overflow:
            if(i > 0):
                self.counter[i] = 0
                i -= 1
                self.counter[i] += 1
                overflow =  self.counter[i] > self.heights[i]
            else:
                overflow = False
                self.out_of_bounds = True

def determine_height(pbw_letter, target_degree):    
    pw_deg =  w.Word([pbw_letter]).degree  
    output = -1
    
    for handle, value in target_degree.items():
        try:
            output = (math.floor(value/pw_deg[handle]) if output == -1 else
                      min(output, math.floor(value/pw_deg[handle]) ))
        except:
            continue
        
    if(output == -1):
        msg ="The height of the letter ", pbw_letter, " couldn't be determined correctly."
        raise AssertionError(msg)
        
    return output