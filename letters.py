# -*- coding: utf-8 -*-

import element
import tensor_element
import word


class Letter:
    """Class where the algebra generators live
    Made to be immutable. I.e. such that generators are fixed once and for all."""

    __slots__ =("handle", "coproduct")

    def __init__(self, handle: str, print_stats=False):
        
        object.__setattr__(self, "handle", handle)
        if handle == "":
            object.__setattr__(self, "coproduct", 
                               tensor_element.TensorElement({word.TensorWord((word.Word([self]), word.Word([self]))):1}))
        else:
            object.__setattr__(self, "coproduct", 
                               tensor_element.TensorElement({word.TensorWord((word.Word([self]), word.Word([]))):1, 
                                                             word.TensorWord((word.Word([]), word.Word([self]))):1}))
        if(print_stats):
            print(self.stats_string())
    
    def __str__(self):
        
        return self.handle
    
    def __setattr__(self, name: str, value):
        
        msg = "It is not allowed to change the value of the attribute '"+name+"'."
        raise AttributeError(msg)
        
    def __eq__(self, other):
        
        if not (type(other)==Letter):
            msg = ("You cannot compare Letters with other classes "+
                   "(including subclasses).\n"
                + "If you need to do so use the 'has_same_handle(other)' method.")
            raise AssertionError(msg)
            return False
        return self.handle == other.handle
    
    def __hash__(self):
        
        return hash(self.handle)
    
    def has_same_handle(self, other):
        """ Returns wether two letter instances have the same handle"""
        
        return isinstance(other, Letter) and self.handle == other.handle
        
    def c_bilinear(self, other):
         """Returns the c of the generator, i.e., (self|self)."""
         
         if type(other) != Letter:
            msg = ("The c_bilinear form of incompatible types was called."+
                   " Execution is aborted.") 
            raise AssertionError(msg)
         
         return 1 if (self==other) else 0
     
    def stats_string(self):
        """This function returns a string summarising the properties of the letter
        it has been called on."""
        
        output = ("This is the generator " + self.handle + 
                  ". Its coproduct is " + str(self.coproduct) + ".")
        return output
    
    def is_unit(self):
        
        return self.handle in ("", "1")

class PBWLetter(Letter, object):
    """Class where the PBW generators live.
    Similarly to letters PBW generators should be fixed once and for all
    """
    __slots__ =("handle","presentation", "coproduct")

    def __init__(self, handle: str, presentation: element.Element, print_stats = False):
        
        object.__setattr__(self,"handle", handle)
        object.__setattr__(self, "presentation", presentation)
        object.__setattr__(self, "coproduct", presentation.coproduct())
        
        if print_stats:
            print(self.stats_string())
    
    def __setattr__(self, name: str, value):
        
        msg = "It is not allowed to change the value of the attribute '"+name+"'."
        raise AttributeError(msg)
        
    def __eq__(self, other):
        
         if not (type(other)==PBWLetter):
            msg = ("You cannot compare PBWLetters with other classes "+
                   "(including superclasses).\n"
                + "If you need to do so use the 'has_same_handle(other)' method.")
            raise AssertionError(msg)
            return False
         return self.handle == other.handle
     
    def __hash__(self):
        
        return hash(self.handle)

    def get_c(self):
        """Return the c of the PBW letter, i.e., (self|self)."""
        
        return self.c_bilinear(self)
    
    def c_bilinear(self, other):
        """ This function returns the c bilinear form (u,v) of two PBW generators u,v
        It relies on the implementation of the c bilinear of its underlying  elements. """
        
        if type(other) != PBWLetter:
            msg = ("The c_bilinear form of incompatible types was called."+
                   " Execution is aborted.") 
            raise AssertionError(msg)
        else:
            return self.presentation.c_bilinear(other.presentation)
        
    def stats_string(self):
        """This function returns a string summarising the properties of the letter
        it has been called on."""
        
        output = ("This is the PBWgenerator " + self.handle + 
                  ". It has a presentation in terms of simple generators, "
                  + str(self.presentation) +
                  ". Its coproduct is given by " + str(self.coproduct) + ".")
        return output

# Consider importing sage.combinat.q_analogues.q_int outside of Anaconda (running via a SAGE Jupyter Notebook),
# similar for q_factorial.
def q_int(n: int, q):
    result = 0
    for i in range(n):
        result += q**i
    return result


def q_factorial(n: int, q):
    result = 1
    for i in range(n):
        result *= q_int(i + 1, q)
    return result


def q_bilinear(first: PBWLetter, second: PBWLetter):
    """Computes the q-bilinear form between two PBW generators."""
    #TODO

    return



        

# --- small example to highlight immutablility ---#
    
#a = Letter("test")
#b = PBWLetter("test", None)
#print(a.has_same_handle(b))
#print(b.has_same_handle(a))
#print(a==b)