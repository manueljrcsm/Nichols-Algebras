# -*- coding: utf-8 -*-
from pbw_algebra import c_bilinear
from tensor_element import TensorElement
from element import Element


class Letter:
    """Class where the algebra generators live."""

    def __init__(self, handle):
        self.handle = handle
        self.coproduct = TensorElement({})  # TODO complete this


class PBWLetter(Letter):
    """Class where the PBW generators live.
    """

    def __init__(self, handle: str, presentation: Element):
        self.handle = handle
        self.coproduct = TensorElement({})  # complete this, potentially using the coproduct function
        self.presentation = presentation

    def get_c(self):
        """Return the c of the PBW letter, i.e., (self|self)."""
        #TODO

        return c_bilinear(self.presentation,self.presentation)

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