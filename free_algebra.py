from element import Element
from letters import PBWLetter


class FreeAlgebra:
    """Where the free algebra itself lives. It serves a structure superclass for PBW_algebra."""

    def __init__(self, generators: str, base_field, q_matrix):
        self.generators = generators.split(sep=' ')
        self.base_field = base_field
        self.q_matrix = q_matrix

    def set_element(self, string, scalar) -> Element:
        """The most pratical way to construct a new element. Constructs individual monomials (with an optional scalar).
        Inputs: string, scalar (one by default).
        Output: element of the form 'scalar times string' written in the PBW basis.
        """
        if string == 0:
            newelement = Element({'': 0})
        else:
            newelement = Element({string: scalar})
        return newelement.rewrite()

    def set_pbw_generator(self, handle: str, representation: Element) -> PBWLetter:
        """Creates the PBW generator with a given handle and representation."""

        return PBWLetter(handle, representation)
