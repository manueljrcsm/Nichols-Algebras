import element
from universe import Universe
import numpy as np
from letters import Letter
from collections import namedtuple


class FreeAlgebra:
    """Where the free algebra itself lives. It serves a structure superclass for PBW_algebra."""

    def __init__(self, string_generators: str, base_field, q_matrix: np.ndarray):
        self.string_generators = string_generators
        self.base_field = base_field

        GeneratorsTuple = namedtuple('GeneratorsTuple',string_generators)
        self.generators = GeneratorsTuple._make([Letter(handle) for handle in string_generators.split(sep=' ')])

        self.q_matrix: dict = {}
        if q_matrix.shape == (len(self.generators), len(self.generators)):
            for i in range(len(self.generators)):
                row = self.generators[i]
                for j in range(len(self.generators)):
                    col = self.generators[j]
                    self.q_matrix[(row, col)] = q_matrix[i][j]
        else:
            msg = "The matrix has the wrong dimensions. Expected ({2},{2}), but got ({2},{2}).".format(
                q_matrix.shape[0], q_matrix.shape[1], len(self.generators))
            raise AssertionError(msg)

        Universe.set_universe(self)

    def set_element(self, string, scalar) -> element.Element:
        """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
        Inputs: string, scalar (one by default).
        Output: element of the form 'scalar times string' written in the PBW basis.
        """
        if string == 0:
            newelement = Element({'': 0})
        else:
            newelement = Element({string: scalar})
        return newelement.rewrite()

    #def set_pbw_generator(self, handle: str, representation) -> letters.PBWLetter:
    #    """Creates the PBW generator with a given handle and representation."""

    #    return letters.PBWLetter(handle, representation)
