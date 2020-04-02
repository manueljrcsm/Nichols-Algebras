# -*- coding: utf-8 -*-
from tensor_element import tensor_element
from element import element


class letter:
    """Class where the algebra generators live.
    """

    def __init__(self, handle):
        self.handle = handle
        self.coproduct = tensor_element({})  # TODO complete this


class PBW_letter(letter):
    """Class where the PBW generators live.
    """

    def __init__(self, handle: str, presentation: element):
        self.handle = handle
        self.coproduct = tensor_element({})  # complete this, potentially using the coproduct function
        self.presentation = presentation
