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



alg = FreeAlgebra("a,b", {'q':[5,1], 'r': [5, 1], 's':[5,3]}, np.matrix([["q","r"],["r","s"]]), True)

q = list(alg.q_matrix.values())[0]


a = U.type_conversion(alg.generators.a, e.Element)
b = U.type_conversion(alg.generators.b, e.Element)
ab = alg.bracket(alg.generators.a, alg.generators.b)
aab = alg.bracket(alg.generators.a, ab)
abaab = alg.bracket(ab, aab)  
aaab = alg.bracket(alg.generators.a, aab)  





l = [a, aaab, aab, abaab, ab, b]
nichols_alg = PBWAlgebra("u f e d c v", l , alg)

u = nichols_alg.get_PBWElement("u")
uuuv = nichols_alg.get_PBWElement("f")
uuv = nichols_alg.get_PBWElement("e")
uvuuv = nichols_alg.get_PBWElement("d")
uv = nichols_alg.get_PBWElement("c")
v = nichols_alg.get_PBWElement("v")

print("We will now compute the BGG resolution")
print("We have to find 20 morphisms and verify that all squares commute")

m_1 = v
print("The morphism -b -> e is given by ", m_1.as_Element(),". No square to verify.")
m_2 = u
print("The morphism -a -> e is given by ", m_2.as_Element(),". No square to verify.")
m_3 = u*u*u*u
print("The morphism -4a-b -> -b is given by ", m_3.as_Element(), ". No square to verify.")
m_4 = nichols_alg.solve_Bruhat_square(m_1, m_3, m_2)
print("The morphism -4a-b -> -a is given by ", m_4.as_Element(),". We verify one square.")
print("(-4a-b -> -a)(-a -> e) + (-4a-b -> -b)(-b -> e) = ", (m_4*m_2 + m_3*m_1).rewrite())
m_5 = v*v
print("The morphism -a-2b -> -a is given by ", m_5.as_Element(),". No square to verify.")
m_6 = nichols_alg.solve_Bruhat_square(m_2, m_5, m_1)
print("The morphism -a-2b -> - b is given by ", m_6.as_Element(),". We verify one square.")
print("(-a-2b -> -b)(-b -> e) + (-a-2b -> -a)(-a -> e) = ", (m_6*m_1 + m_5*m_2).rewrite())
m_7 = u*u*u*u*u
print("The morphism -6a-2b -> - a- 2b is given by ", m_7.as_Element(),". No square to verify.")
m_8 = nichols_alg.solve_Bruhat_square(m_5, m_7, m_4)
print("The morphism -6a-2b -> -4a-b is given by ", m_8.as_Element(),". Two squares to verify.")
print("(-6a-2b -> -4a-b)(-4a-b -> -a) + (-6a-2b -> -a-2b)(-a-2b -> -a) = ", (m_8*m_4 + m_7*m_5).rewrite())
print("(-6a-2b -> -4a-b)(-4a-b -> -b) + (-6a-2b -> -a-2b)(-a-2b -> -b) = ", (m_8*m_3 + m_7*m_6).rewrite())
m_9 = v*v*v
print("The morphism -4a-4b -> - 4a-b is given by ", m_9.as_Element(),". No square to verify.")
m_10 =nichols_alg.solve_Bruhat_square(m_4, m_9, m_5)
print("The morphism -4a-4b -> -a-2b is given by ", m_10,". Two squares to verify.")
print("(-4a-4b -> -4a-b)(-4a-b -> -b) + (-4a-4b -> -a-2b)(-a-2b -> -b) = ", (m_9*m_3 + m_10*m_6).rewrite())
print("(-4a-4b -> -4a-b)(-4a-b -> -a) + (-4a-4b -> -a-2b)(-a-2b -> -a) = ", (m_9*m_1 + m_10*m_5).rewrite())


#print(nichols_alg.solve_Bruhat_square(v, u*u*u*u, u))



#print("[u,v] = ", nichols_alg.bracket([u, v]))
#print("[u,[u,[u,[u,v]]]] = ", nichols_alg.bracket([u,u,u,u,v]))

#print("[",r, ",", s, "] = ", r*s -s*r.scalar_multiply(list(r.terms)[0].q_bilinear(list(s.terms)[0])) )

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