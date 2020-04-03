# -*- coding: utf-8 -*-


import free_algebra
import pbw_algebra
import pbw_element
from config import *

a = free_algebra.FreeAlgebra("a b", P,(p,q,r), [[p, q], [q, r]])
b = pbw_algebra.PBWAlgebra("x y z t u v",a)
x = pbw_element.create_pbw_element('ut')

print(x)

# Example of potential future uses taken from the Zoom chat
"""
A = FreeAlgebra("a b")
A.set_element("abbba",2)
A = FreeAlgebra("a b", "q,r,p", M)
u_1 = A.set_element(Element.bracket(a,b))
u_1 = A.set_element(...)
Element.bracket(a,b)
u_1= Element.bracket(a,b)
a = get_generator("a")
b= A.get_generator("b")
u_1 = Element.bracket(a,b)
c = a+b
"""
