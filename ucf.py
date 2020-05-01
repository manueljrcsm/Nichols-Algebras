# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:20:40 2020

@author: Sebas
"""
import math
from collections import OrderedDict

class UCF:
    
    
    def __init__(self):
       None
        
    def gen(self, degree, number, name, is_root_of_unity=True):
        
        return UCFNumber(degree, number, name, is_root_of_unity)
        
def lcm(a, b):
    return a*b/math.gcd(a,b)

def to_ucfnumber(x):
    if type(x) == UCFNumber:
        return x
    elif x == 1:
        return UCFNumber(1, 0, str(x), True)
    elif x == -1:
        return UCFNumber(2, 1, str(x), True)
    else: 
        return UCFNumber(0, x, str(x), False)

class UCFNumber:
            
        value = None
        angle= None # 0 to 2
        radius = None
        
        def __init__(self, angle, radius, name ="Nostring", is_root_of_unity= False):
            self.value =[angle, radius]
            self.angle = (float(angle) % 2 if not is_root_of_unity 
                          else int(angle/math.gcd( int(angle), int(radius) )))
            self.radius = (float(radius) if not is_root_of_unity 
                           else int(radius/math.gcd( int(angle), int(radius))%self.angle))
            self. name = self.string_simplifier(name)
            self.is_root_of_unity = is_root_of_unity
            
        def __add__(self, other):
            other_ucf= to_ucfnumber(other)
            coords = self.to_polar(
                    self.to_cart()[0] +other_ucf.to_cart()[0],
                    self.to_cart()[1] +other_ucf.to_cart()[1])
            return UCFNumber(coords[0], coords[1], self.name + "+"+ other_ucf.name, False)
        
        def __radd__(self,other):
            
            other_ucf = to_ucfnumber(other)          
            return other_ucf + self    
        
        def __sub__(self,other):
            return self + (to_ucfnumber(-1)*other)
            
        def __mul__(self, other):
            
            other_ucf = to_ucfnumber(other)
            if self.is_root_of_unity and other_ucf.is_root_of_unity:
                return UCFNumber(lcm(self.angle, other_ucf.angle),
                                 self.radius*other_ucf.angle/math.gcd(self.angle, other_ucf.angle) +
                                 other_ucf.radius*self.angle/math.gcd(self.angle, other_ucf.angle), 
                                 self.name+"*"+other_ucf.name,
                                 True)
            elif self.is_root_of_unity:
                return UCFNumber (2/self.angle*self.radius + other_ucf.angle, other_ucf.radius, 
                                  self.name+"*"+other_ucf.name,
                                  False)
            elif other_ucf.is_root_of_unity:
                return UCFNumber (2/other_ucf.angle*other_ucf.radius + self.angle, self.radius, 
                                  self.name+"*"+other_ucf.name,
                                  False)
            return UCFNumber (self.angle + other_ucf.angle, self.radius*other_ucf.radius, 
                              self.name+"*"+other.name,
                              False)
        
        def __rmul__(self,other):
            other_ucf= to_ucfnumber(other)
            return other_ucf*self
            
        
        def __truediv__(self, other):
             
            other_ucf = to_ucfnumber(other) 
            if self.is_root_of_unity:
                return self * UCFNumber(other_ucf.angle, other_ucf.angle -other_ucf.radius, other_ucf.name + "^(-1)" , True)
            else:
                return self * UCFNumber(other_ucf.angle +1, 1/other_ucf.radius,other_ucf.name +"^(-1)", False)
        
        def __eq__(self, other):
            other_ucf = to_ucfnumber(other)
            
            return ((self.is_root_of_unity and other_ucf.is_root_of_unity and
                self.angle == other_ucf.angle)
                or (self.to_cart()[0] == other_ucf.to_cart()[0] and 
                self.to_cart()[1] == self.to_cart()[1]))
        
        def __str__(self):
            return self.name
            """
            if self.is_root_of_unity:
                return("I am the " + 
                       str(self.radius)+"-th root of unity of degree "
                       +str(self.angle))
            else:
                return ("In polar coordinates: Angle= " + str(self.angle) +
                    "pi; radius=" + str(self.radius) +".")     
            """
            
        def __pow__(self, number):
            output =UCFNumber(1,0,"1", True)
            for i in range(number):
                output = output*self
                
            return output
        
        def to_cart(self):
            internal_radius = self.radius if not self.is_root_of_unity else 1
            internal_angle = (self.angle if not self.is_root_of_unity 
                              else 2/self.angle*self.radius)
            
                
            return [float(internal_radius* math.cos(internal_angle* math.pi)), 
                    float(internal_radius* math.sin(internal_angle* math.pi)) ]
        
        def to_polar(self, xCoord, yCoord):
            
            return [(math.atan2(yCoord, xCoord))/math.pi, 
                    math.sqrt(xCoord*xCoord+ yCoord*yCoord)]
    
        def string_simplifier(self, string):
            math_operators = ["+", "-", "*","^", "^(-1)"]            
            return string