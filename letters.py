# -*- coding: utf-8 -*-
import tensor_element
import word
from universe import Universe


class Letter:
    """Class where the algebra generators live
    Made to be immutable. I.e. generators are fixed once and for all."""

    __slots__ = ("handle", "coproduct")

    def __init__(self, handle: str):

        object.__setattr__(self, "handle", handle)
        if handle == "":
            object.__setattr__(self, "coproduct", tensor_element.TensorElement({(word.Word(self), word.Word(self)): 1}))
        else:
            object.__setattr__(self, "coproduct", tensor_element.TensorElement({(word.Word([self]), word.Word([])): 1, (
                word.Word([]), word.Word([
                    self])): 1}))  # TODO: Coproduct  # super(Letter, self).__setattr__("coproduct",tensor_element.TensorElement({}))  # self.coproduct =   #(Non-immutable way)

    def __str__(self):
        return self.handle

    def __setattr__(self, name: str, value):
        msg = "It is not allowed to change the value of the attribute '" + name + "'."
        raise AttributeError(msg)

    def __eq__(self, other):
        if not (type(other) == Letter):
            msg = (
                    "You cannot compare Letters with other classes " + "(including subclasses).\n" + "If you need to do so use the 'has_same_handle(other)' method.")
            raise AssertionError(msg)
            return False
        return self.handle == other.handle

    def __hash__(self):
        return hash(self.handle)

    def has_same_handle(self, other):
        if not isinstance(other, Letter):
            return False
        else:
            return self.handle == other.handle


class PBWLetter(Letter):
    """Class where the PBW generators live."""

    __slots__ = ("handle", "presentation", "coproduct")

    def __init__(self, handle: str, presentation):
        object.__setattr__(self, "handle", handle)
        object.__setattr__(self, "presentation", presentation)

        # TODO is this necessary?   # self.coproduct = tensor_element.TensorElement({})

    def __setattr__(self, name: str, value):
        """Overwritten method, raising an AttributeError. Use object.__setattr__ to change attributes."""
        msg = "It is not allowed to change the value of the attribute '" + name + "'."
        raise AttributeError(msg)

    def __eq__(self, other):
        if not (type(other) == PBWLetter):
            msg = (
                    "You cannot compare PBWLetters with other classes " + "(including superclasses).\n" + "If you need to do so use the 'has_same_handle(other)' method.")
            raise AssertionError(msg)
            return False
        return self.handle == other.handle and self.presentation == other.presentation

    def __hash__(self):
        return hash(self.handle)

    def q_bilinear(self,other):
        if  self.presentation.poly == {} or other.presentation.poly == {}:
            return 1
        return tuple(self.presentation.terms)[0].q_bilinear(tuple(other.presentation.terms)[0])

# import element
# PBWLetter.EMPTY = PBWLetter("", element.ElementZERO)


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

