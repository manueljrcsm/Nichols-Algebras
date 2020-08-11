from free_algebra import FreeAlgebra
from pbw_algebra import PBWAlgebra
from universe import Universe as U
import numpy as np
import letters as l
import word as w
import element as e
import pbw_element as pe
"""
#from pbw_algebra import PBWAlgebra
#import numpy as np
#import word
#import element
#import letters




"""


alg = FreeAlgebra("a,b", {'q':[11,1], 'r': [11,4], 's':[11,3]}, np.matrix([["q","r"],["r","s"]]), True)


a = U.type_conversion(alg.generators.a, e.Element)
b = U.type_conversion(alg.generators.b, e.Element)
ab = alg.bracket(alg.generators.a, alg.generators.b)
aab = alg.bracket(alg.generators.a, ab)
abaab = alg.bracket(ab, aab)  
aaab = alg.bracket(alg.generators.a, aab)  





l = [a, aaab, aab, abaab, ab, b]
nichols_alg = PBWAlgebra("u v w x y z", l , alg)
u = nichols_alg.get_PBWElement("z")
v = nichols_alg.get_PBWElement("y")
r = u
s = v
print("[",r, ",", s, "] = ", r*s -s*r.scalar_multiply(list(r.terms)[0].q_bilinear(list(s.terms)[0])) )

#b = alg.get_element("b")

#u = alg.create_pbw_letter("u" , alg.bracket( alg.generators["a"], alg.generators["b"]) )

#v = alg.create_pbw_letter("v" , alg.bracket( alg.generators["a"], u) )





"""
algebra = FreeAlgebra("a b", P, np.array([[q_11,q_12],[q_21,q_22]]))
a,b = [e.Element({w.Word([each]):1}) for each in algebra.generators]

pbw_definitions = [None for i in range(6)]
pbw_definitions[0] = b
pbw_definitions[5] = a
pbw_definitions[1] = e.bracket(a,b) # x_a+b = [x_a,x_b]
pbw_definitions[3] = e.bracket(a,pbw_definitions[1]) # x_2a+b = [x_a,x_a+b]
pbw_definitions[4] = e.bracket(a,pbw_definitions[3]) # x_3a+b = [x_a,x_2a+b]
pbw_definitions[2] = e.bracket(pbw_definitions[3],pbw_definitions[1]) # x_3a+2b = [x_2a+b,x_a+b]


pbw_alg = PBWAlgebra("t u v x y z",pbw_definitions, algebra)
t,u,v,x,y,z = pbw_alg.pbw_generators

print(z.presentation)
print(u.presentation)
print(z.q_bilinear(u))
z = z.as_PBWElement()
print(type(z))
t = t.as_PBWElement()
print(type(t))
print(z*t - t*z)
print(type(u),type(v))
test_word = w.Word([u,v])
print(pe.PBWElement({test_word:1}).as_Element())
print(test_word.degree)

print(x.presentation)
print(algebra.generators)
print(pbw_alg.pbw_generators)

"""

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