
class Free_Algebra:
    """Where the free algebra itself lives. It serves a structure supersclass for PBW_algebra.
    """
    def __init__(self,generators,base_field,q_matrix):
        self.generators = generators
        self.base_field = base_field
        self.q_matrix = q_matrix
        

