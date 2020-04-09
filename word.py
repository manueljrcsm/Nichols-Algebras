# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 08:36:29 2020

@author: Sebas
"""

"""
    This class is used as a bridge between letters and elements 
    The reason being that:
        element is a sum of words (with scalars)
        and a word is a concatination of letters
"""
import letters
import string_helper
import tensor_element
from universe import Universe

class Word:
    
    __slots__ = ("letters", "degree", "length")
    
    def __init__(self, letters_list):
        try:
            if all(type(l) in (letters.Letter,letters.PBWLetter) for l in letters_list):
                degree_dict = {}
                for l in letters_list:
                    if l in degree_dict:
                        degree_dict[l] += 1
                    else:
                        degree_dict[l] =1
                try:        
                    object.__setattr__(self, "letters", tuple(letters_list))
                except TypeError:
                    raise TypeError("Your given list was not convertible into a tuple.")
                object.__setattr__(self, "length", len(letters_list))
                object.__setattr__(self, "degree", degree_dict)
                        
            else:
                msg = ("The given list of letters contained incompatible types."
                + " Please make sure to only use Letters or PBWLetters.")
                raise AssertionError(msg)
             
        except TypeError:
            raise AssertionError("The given letters were not presented in the expected format.")

    def __str__(self):
        
        if self.length == 0:
            return ""
        else:
            output_string = "".join(str(l) for l in self.letters)
            return string_helper.string_compressor(output_string)
        
    def __add__(self, other):
        gen_list = list(self.letters)
        gen_list.extend(other.letters)

        return Word(gen_list)
    
    def __eq__(self, other):
        if type(other) != Word: 
            msg =("Warning you are comparing a word to a ", type(other))
            raise AssertionError(msg)
            return False
        if(self.length != other.length):
            return False
        else:
            return all(self.letters[i] == other.letters[i] for i in range(self.length))

    def __hash__(self):
        return hash(str(self))

    def __len__(self):
        return len(self.letters_list)
    
    def coproduct(self):
        output = tensor_element.TensorElement({(Word([]), Word([])): 1})
        for l in self.letters:
            print("Current letter, ",l, ",  in the word ", self,".")
            output *= l.coproduct
            print("Yields the output", output)
        print("The word ", self, " yields as output ", output)
        return output

    def q_bilinear(self,other):

        if self == Word.EMPTY or other == Word.EMPTY:
            return 1

        result = 1
        for (row, col) in Universe.q_matrix.keys():
            power = self.degree.get(row, 0)*other.degree.get(col, 0)
            result *= Universe.q_matrix[(row, col)]**power
        return result

Word.EMPTY = Word([])