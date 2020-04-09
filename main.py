# -*- coding: utf-8 -*-


from free_algebra import FreeAlgebra
from pbw_algebra import PBWAlgebra
import numpy as np
import word
import element
import letters

try:
    from sage.all_cmdline import FractionField,PolynomialRing,QQ  # imports sage library

    names = ('q_11', 'q_12', 'q_21','q_22')  # tuple of strings with the q matrix
    P = FractionField(PolynomialRing(QQ, 4, names))
    (q_11,q_12,q_21,q_22) = P._first_ngens(4)
    print(P)

except ModuleNotFoundError:  # IGNORE
     (q_11,q_12,q_21,q_22) = (2,3,5,7)
     P = None
     print("Sage Module not found at main,  (q_11,q_12,q_21,q_22)=(%s,%s,%s,%s)"% (q_11,q_12,q_21,q_22))

algebra = FreeAlgebra("a b", P, np.array([[q_11,q_12],[q_21,q_22]]))
a,b = [element.Element({word.Word([l]):1}) for  l in algebra.generators]

pbw_definitions = [None for i in range(6)]
pbw_definitions[0] = b
pbw_definitions[5] = a
pbw_definitions[1] = element.bracket(a,b) # x_a+b = [x_a,x_b]
pbw_definitions[3] = element.bracket(a,pbw_definitions[1]) # x_2a+b = [x_a,x_a+b]
pbw_definitions[4] = element.bracket(a,pbw_definitions[3]) # x_3a+b = [x_a,x_2a+b]
pbw_definitions[2] = element.bracket(pbw_definitions[3],pbw_definitions[1]) # x_3a+2b = [x_2a+b,x_a+b]

pbw_alg = PBWAlgebra("t u v x y z",pbw_definitions, algebra)
t,u,v,x,y,z = pbw_alg.pbw_generators

print(z.presentation)
print(u.presentation)
print(z.q_bilinear(u))

print(x.presentation)

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

a= letters.Letter("a",True)
b= letters.Letter("b")
c= letters.Letter("c")


r = word.Word([a, b], True)
s = word.Word([b, a])
t = word.Word([a,b,c])

x = element.Element({r:4, s:1})
y = element.Element({s:1, r:-1})
z = element.Element({t:1})


xa= x
xb = x+z

u = letters.PBWLetter("u", xa)
v = letters.PBWLetter("v", xb)

num = u.c_bilinear(v)

print("The result is", num)


