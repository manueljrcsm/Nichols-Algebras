# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:00:44 2020

@author: manue
"""

import word


class TensorElement:
    """Its objects are a formal sum of pure tensors in A^{\otimes 2}  with scalar coefficients,
    pure tensors are a pair (tuple) of objects of the class element (NOT simply strings).
    """

    __slots__ = ("dic", "tensor_terms", "scalars", "pairs")

    def __init__(self, dic: dict):

        if (all(type(e) is word.TensorWord for e in list(dic.keys()))):
            new_dic = {}
            
            for tensorand, scalar in dic.items():
                if not scalar == 0:
                    new_dic[tensorand] = scalar
            object.__setattr__(self, "dic", new_dic)
            object.__setattr__(self, "tensor_terms", new_dic.keys())
            object.__setattr__(self, "scalars", new_dic.values())
            object.__setattr__(self, "pairs", new_dic.items())

        else:
            msg = "The tensor element was not in the expected format."
            raise AssertionError(msg)

    def __str__(self):
        
        word = ""

        for term, sca in self.pairs:
            # Run through the monomial terms of the element.z
            scalar = str(sca)
            sign = " + "
            if scalar[0]== "-":
                    sign = " - "
                    scalar = str(-1*sca)
            if scalar == "1" and not term.words[0].is_unit() :
                # If the coefficient of a term is 1, then it is ommited.
                scalar = ""
            elif "+" in scalar or "-" in scalar:
                scalar = "(" + scalar + ")"
            
            word += sign + scalar + str(term)
            
        if word == "":  # Empty dictionaries correspond to the 0 element.
            return "0"
        else:
            return word[3:]

    def __setattr__(self, name: str, value):

        msg = "It is not allowed to change the attribute '" + name + "'."
        raise AttributeError(msg)

    def __add__(self, other):
        output_dict = other.dic.copy()
        for tensor_term, sca in self.pairs:
            if tensor_term in other.dic:
                if sca + output_dict[tensor_term] == 0:
                    output_dict.pop(tensor_term)
                else:
                    output_dict[tensor_term] += sca
            else:
                output_dict[tensor_term] = sca
        return TensorElement(output_dict)

    def __sub__(self, other):
        return self + other.scalar_mulitply(-1)

    def __mul__(self, other):
        if all(w.tensor_degree is list(self.tensor_terms)[0].tensor_degree for w in list(self.tensor_terms)):
            output_dict = {}
            for tensor_term_1, sca_1 in self.pairs:
                for tensor_term_2, sca_2 in other.pairs:
                                       
                    braiding_sca= 1
                    for i in range(tensor_term_2.tensor_degree):
                        for j in range(i+1,tensor_term_1.tensor_degree):
                            braiding_sca*= tensor_term_1.words[j].q_bilinear(tensor_term_2.words[i])
                    
                    new_term = tensor_term_1 + tensor_term_2
                    new_sca = braiding_sca*sca_1*sca_2
                    

                    output_dict[new_term] = (output_dict[new_term] + new_sca if (new_term in output_dict) else new_sca)
            return TensorElement(output_dict)
        else:
            msg = "You tried to multiply tensorands of different length. This is not supported."
            raise AssertionError(msg)

    def coproduct(self):
        return sum([term.coproduct().scalar_mulitply(sca) for term, sca in self.pairs], TensorElement({}))

    def scalar_mulitply(self, number):
        if (number == 0):
            return TensorElement({word.TensorWord([]): 1})
        # TODO CHECK THAT NUMBER IS INT FLOAT SAGE_SCALAR
        if (number == 1):
            return self
        output_dict = {}
        for tensor_term, scalar in self.pairs:
            output_dict[tensor_term] = scalar*number
        result = TensorElement(output_dict)
        return result

    def __delitem__(self, term):
        del self.dic[term]

    def copy(self):
        return TensorElement(self.dic)

    def rewrite(self):
        """Cleaning zero terms."""
        newtensor = self.copy()
        for pair, sca in newtensor.pairs:
            if sca == 0:
                del newtensor[pair]
        return newtensor

    def tensorize(first, second, sca=1):
        """Takes two algebra elements, returns the corresponding pure tensor. """  # TODO update this if necessary
        newdic = {(first, second): sca}
        return TensorElement(newdic)
