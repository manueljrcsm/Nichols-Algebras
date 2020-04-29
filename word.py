# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 08:36:29 2020

@author: Sebas
"""

import letters as l
import tensor_element as te
from string_helper import string_compressor
from universe import Universe
from collections import UserList


class Word(UserList):
    """This class is used as a bridge between letters and elements.

    The reason being that Element is a sum of Words (with scalars)and a Word is a concatenation of Letters.
    """
    __slots__ = ("letters", "degree", "length", "data")


    def __init__(self, letters_list, print_stats=False):

        try:
            # Basically a list of letters can be divided into three types:
            # 1) 'Pure type': contains a non-empty list with non-unitary letters
            # 2) 'Unit type':  contains a non-empty list with only unit letters
            # 3) 'Empty type': The list is empty.
            # In the first step we harmonise these types to ensure that units do not exist in non-trivial words and
            # the empty word is the word in the empty letter
            # Thus it has a coproduct (and maybe other desirable properties)
            try:
                contains_non_unit = any(not letter.is_unit() for letter in letters_list)

                if contains_non_unit:
                    internal_letters_list = [x for x in letters_list if not x.is_unit()]
                elif not contains_non_unit and len(letters_list) > 0:
                    internal_letters_list = [letters_list[0]]
                else:
                    internal_letters_list = [l.Letter("")]  # internal_letters_list = [l.Letter("")] if not
                    # internal_letters_list else internal_letters_list

                object.__setattr__(self, "letters", tuple(internal_letters_list))
                object.__setattr__(self, "data", self.letters)
                object.__setattr__(self, "length", len(internal_letters_list) - 1 + int(contains_non_unit))

                if all(type(letter) is l.Letter for letter in internal_letters_list):
                    degree_dict = {}
                    for letter in internal_letters_list:
                        if not letter.is_unit():
                            degree_dict[letter] = degree_dict[letter] + 1 if (letter in degree_dict) else 1
                    object.__setattr__(self, "degree", degree_dict)
                elif all(type(letter) is l.PBWLetter for letter in internal_letters_list):
                    degree_dict = {}
                    for pbw_letter in internal_letters_list:
                        if not pbw_letter.is_unit():
                            representative: Word = list(pbw_letter.presentation.poly)[0]
                            for letter in representative.letters:
                                degree_dict[letter] = degree_dict[letter] + 1 if (letter in degree_dict) else 1
                    object.__setattr__(self, "degree", degree_dict)

                else:
                    msg = ("The given list of letters contained incompatible types." +
                           " Please make sure to only use letters or PBWLetters.")
                    raise AssertionError(msg)
                if (print_stats):
                    print(self.stats_string())
            except TypeError:
                raise TypeError("The list of letters was not iterable.")

        except TypeError:
            raise AssertionError("The given letters were not presented in the expected format.")

    def __setattr__(self, name: str, value):
        msg = "It is not allowed to change the value of the attribute '" + name + "'."
        raise AttributeError(msg)

    def __str__(self):
        return "" if (self.length == 0) else string_compressor("".join(str(each) for each in self.letters))

    def __add__(self, other):
        """To prevent ambiguity: Addition of words means concatenation.
        """
        if type(other) != Word:
            msg = ("Two incompatible types, " + str(type(self)) + " and " + str(
                type(other)) + " were tried to be added.")
            raise AssertionError(msg)

        gen_list = list(self.letters)
        gen_list.extend(other.letters)

        return Word(gen_list)

    def __eq__(self, other):

        if type(other) != Word:
            msg = ("Warning you are comparing a word to a ", type(other))
            raise AssertionError(msg)
            
        if (self.length != other.length):
            return False
        else:
            for i in range(self.length):
                if not self.letters[i] == other.letters[i]:
                    return False

            return True

    def __hash__(self):
        return hash(str(self))

    def __getitem__(self, i):
        res = self.data[i]
        return type(self)(res) if isinstance(i, slice) else res

    def coproduct(self):
        """Computes the coproduct of a word.

            The underlying principle is that cop(ab....x)= 1@1 * cop(a)* cop(b) *... cop(x)
        """
        output = te.TensorElement({TensorWord((Word([]), Word([]))): 1})
        for letter in self.letters:
            output *= letter.coproduct

        return output

    def c_bilinear(self, other):
        """Computes the c_bilinear form of a word and another word.

            Basic idea is to use the compatibility of co-products with the c bilinear to reduce the word length.
            Roughly the process is: word A = ab...c, word B = uv....x
                Step one: reduce word A until it has length 1 i.e. is a letter.
                    Beware that this changes word B into a tensor element T consisting of tensorands B(1) +.....+ B(n).
                Step two: reduce the words B(1)+....+ B(n) until they reach the length of a letter.
                Step three: Pass the coproduct to to specific coproduct functions on the letters.
        """

        if type(other) != Word:
            msg = ("The c_bilinear form of incompatible types was called." + " Execution is aborted.")
            raise AssertionError(msg)

        output_number = 0
        # Step 1: Reduce the length of self
        if self.length > 1:
            for term, sca in other.coproduct().pairs:
                output_number += (
                        sca*Word([self.letters[0]]).c_bilinear(term.words[0])*Word(self.letters[1:]).c_bilinear(
                    term.words[1]))
        # Step 2: Reduce the length of other
        elif other.length > 1:
            for term, sca in self.coproduct().pairs:
                output_number += (sca*term.words[0].c_bilinear(Word([other.letters[0]]))*term.words[1].c_bilinear(
                    Word(other.letters[1:])))
        # Step 3: Pass words of length 1 to the specific function on letters
        # TODO QUESTIONS is the word 1 given as Word(()) or as Word((Letter("")))?
        elif self.length == 1 and other.length == 1:
            output_number += (self.letters[0]).c_bilinear(other.letters[0])
        elif self.length == 0 and other.length == 0:
            output_number = 1

        # The left cases, i.e. self/other has length 1 and other/self has lengt 0 always yield zero. 
        # Thus they need not be treated specifically
        return output_number

    def q_bilinear(self, other):
        
        if self == Word([]) or other == Word([]):
            return 1

        result = 1
        for (row, col) in Universe.q_matrix.keys():
            power = self.degree.get(row, 0)*other.degree.get(col, 0)
            result *= Universe.q_matrix[(row, col)]**power
        return result

    def stats_string(self):
        """This function returns a string summarising the properties of the word
        it has been called on."""

        output = ("This is the word " + str(self) + ". Its length is " + str(self.length) + ". "
                                                                                            "It has the degrees " + ",".join(
            str(key) + ": " + str(val) for key, val in self.degree.items()) + ".")
        return output

    def is_unit(self):
        return self.length == 0

# STATIC CONSTANTS
# Word.EMPTY = Word([])

class TensorWord:
    __slots__ = ("words", "tensor_degree")

    def __init__(self, word_list):
        try:
            if not word_list:
                msg = "The empty tensor product is not well-defined in this program."
                raise AssertionError(msg)

            if (all(type(w) is Word for w in word_list)):
                try:
                    object.__setattr__(self, "words", tuple(word_list))
                except TypeError:
                    raise TypeError("Your given list was not convertible into a tuple.")

                object.__setattr__(self, "tensor_degree", len(word_list))

            else:
                msg = ("Please make sure to initialize this class " + "with a list of words as parameter .")
                raise AssertionError(msg)

        except TypeError:
            raise AssertionError("The given letters were not presented in the expected format.")

    def __setattr__(self, name: str, value):

        msg = "It is not allowed to change the value of the attribute '" + name + "'."
        raise AttributeError(msg)

    def __str__(self):

        return (u'\u2297').join(
            str(self.words[i]) if (i == 0 or not self.words[i].is_unit()) else "1" for i in range(self.tensor_degree))

    def __add__(self, other):

        if (self.tensor_degree != other.tensor_degree):
            msg = ("You tried to concatenate elements " + "of different tensor degrees. This is not supported.")
            raise AssertionError(msg)
        return TensorWord([(self.words[i] + other.words[i]) for i in range(self.tensor_degree)])

    def __eq__(self, other):
        if type(other) != TensorWord:
            msg = ("Warning you are comparing a word to a ", type(other))
            raise AssertionError(msg)
        else:
            return (self.tensor_degree == other.tensor_degree and all(
                self.words[i] == other.words[i] for i in range(self.tensor_degree)))

    def __hash__(self):
        return hash(str(self))

    def coproduct(self):
        """Computes the coproduct of a given TensorWord by applying the coproduct to its first term
        """
        # Case 1: The tensor word is just a word
        if self.tensor_degree == 1:
            return self.words[0].coproduct()
        # Case 2: Its an honest tensor word e.g. a@a with a primitive
        else:
            output_dict = {}
            # Iterate trough every term of the coproduct of the first word
            # For example (a@1, 1@a)
            for term, sca in ((self.words[0]).coproduct()).pairs:
                # Append The remainders of the tensor_word to each term
                # e.g. (a@1@a, 1@a@a)
                extended_term = list(term.words)
                extended_term.extend(list(self.words)[1:])

                output_dict[TensorWord(extended_term)] = sca

            return te.TensorElement(output_dict)
