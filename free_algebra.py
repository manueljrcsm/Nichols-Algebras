#from element import Element
import re
import math
import letters
from typing import Dict, Iterable
#from sage.all_cmdline import UniversalCyclotomicField as UCF  # imports sage library


class FreeAlgebra:
    """Where the free algebra itself lives. It serves a structure superclass for PBW_algebra."""



    def __init__(self, string_generators: str, roots_of_unity: Dict[str,tuple] ={},
                 q_matrix: Iterable[Iterable[str]] = None):
        
        #STEP 1: CHECK THAT THE INPUT IS CONSISTENT
        
        seperator_string="[ , ;]" # characters which can be used to seperate letters
        generators_list = [gen for gen in re.split(seperator_string, string_generators) if gen != ""]
        
        #CHECK THAT NO GENERATOR IN THE GENERATOR STRING IS ALSO USED TO DENOTE SOME ROOT OF UNITY
        for gen in generators_list:
            if gen in roots_of_unity:
                msg ="It is not allowed to use the same variable names for the generators and constants in the field."
                raise AssertionError(msg)
              
        if q_matrix == None or q_matrix ==[]:
            q_matrix = [[1 for x in generators_list] for y in generators_list]
        
        object.__setattr__(self,"letters",{ gen: letters.Letter(gen) for gen in generators_list})
        object.__setattr__(self, "field", UCF())
        object.__setattr__(self, "field_variables_dict",
                           {name: self.field.gen(roots_of_unity[name][0], roots_of_unity[name][1]) 
                            for name, val in roots_of_unity.items()}
                           )
         #TODO         
        
        print(generators_list)
        
        field = UCF()
        field_variables_dict = {}
        
        for name,val in roots_of_unity.items():
            field_variables_dict[name] = field.gen(roots_of_unity[name][0], roots_of_unity[name][1])
            
        
        
        
        
        #UCF = UniversalCyclotomicField()
    """
        def __init__(self, string_generators: str, base_field, q_matrix):
            self.string_generators = string_generators
            self.base_field = base_field
            self.q_matrix = q_matrix
            self.generators = string_generators.split(sep=' ')
            Element.set_universe(self)
    
    def set_element(self, string, scalar) -> Element:
    """
    """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
    Inputs: string, scalar (one by default).
    Output: element of the form 'scalar times string' written in the PBW basis.
    """
    """   
        if string == 0:
            newelement = Element({'': 0})
        else:
            newelement = Element({string: scalar})
        return newelement.rewrite()
    """
    #def set_pbw_generator(self, handle: str, representation) -> letters.PBWLetter:
    #    """Creates the PBW generator with a given handle and representation."""

    #    return letters.PBWLetter(handle, representation)
class UCF:
    
    
    def __init__(self):
        print("I'm the universal cyclotomic field")
        
    def gen(self, degree, number, is_root_of_unity=True):
        
        return UCFNumber(degree, number, is_root_of_unity)
        
def lcm(a, b):
    return a*b/math.gcd(a,b)

class UCFNumber:
            
        value = None
        angle= None # 0 to 2
        radius = None
        
        def __init__(self, angle, radius, is_root_of_unity= None):
            self.value =[angle, radius]
            self.angle = (float(angle) % 2 if not is_root_of_unity 
                          else int(angle/math.gcd( int(angle), int(radius) )))
            self.radius = (float(radius) if not is_root_of_unity 
                           else int(radius/math.gcd( int(angle), int(radius))%self.angle))
            self.is_root_of_unity = is_root_of_unity
            
        def __add__(self, other):
            coords = self.to_polar(
                    self.to_cart()[0] +other.to_cart()[0],
                    self.to_cart()[1] +other.to_cart()[1])
            return UCFNumber(coords[0], coords[1], False)
        
        def __sub__(self,other):
            return self +(other * UCFNumber(2,1))
            
        def __mul__(self, other):
            if self.is_root_of_unity and other.is_root_of_unity:
                return UCFNumber(lcm(self.angle, other.angle),
                                 self.radius*other.angle/math.gcd(self.angle, other.angle) +
                                 other.radius*self.angle/math.gcd(self.angle, other.angle), True)
            elif self.is_root_of_unity:
                return UCFNumber (2/self.angle*self.radius + other.angle, other.radius, False)
            elif other.is_root_of_unity:
                return UCFNumber (2/other.angle*other.radius + self.angle, self.radius, False)
            return UCFNumber (self.angle + other.angle, self.radius*other.radius, False)
        
        def __truediv__(self, other):
             
            if self.is_root_of_unity:
                return UCFNumber(self.angle, -self.radius + self.angle, True) *other
                 
            else:
                return UCFNumber(self.angle +1, 1/self.radius, False) *other
        
        def __eq__(self, other):

            return ((self.is_root_of_unity and other.is_root_of_unity and
                self.angle == other.angle)
                or (self.to_cart()[0] == other.to_cart()[0] and 
                self.to_cart()[1] == self.to_cart()[1]))
        
        def __str__(self):
            if self.is_root_of_unity:
                return("I am the " + 
                       str(self.radius)+"-th root of unity of degree "
                       +str(self.angle))
            else:
                return ("In polar coordinates: Angle= " + str(self.angle) +
                    "pi; radius=" + str(self.radius) +".")
            
        
        def to_cart(self):
            internal_radius = self.radius if not self.is_root_of_unity else 1
            internal_angle = (self.angle if not self.is_root_of_unity 
                              else 2/self.angle*self.radius)
            
                
            return [float(internal_radius* math.cos(internal_angle* math.pi)), 
                    float(internal_radius* math.sin(internal_angle* math.pi)) ]
        
        def to_polar(self, xCoord, yCoord):
            
            return [(math.atan2(yCoord, xCoord))/math.pi, 
                    math.sqrt(xCoord*xCoord+ yCoord*yCoord)]                    
        
FreeAlgebra("a,b", {'q':[3,2], 'r': [3,5]}, [[1,1],[1,1]])
field = UCF()
x   = field.gen(4,1,True)
y   = field.gen(0.5, 1, False)







