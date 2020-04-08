# -*- coding: utf-8 -*-



#from free_algebra import FreeAlgebra
#from pbw_algebra import PBWAlgebra
#import pbw_element
import letters
import word
#import element
#import tensor_element
#from config import *
"""
try:
    from sage.all_cmdline import FractionField,PolynomialRing,QQ  # imports sage library

    names = ('p', 'q', 'r')  # tuple of strings with the q matrix
    P = FractionField(PolynomialRing(QQ, 3, 'p,q,r'))
    (p,q,r) = P._first_ngens(3)
    print(P)

except:  # IGNORE
    (p,q,r) = (2,3,5)
    P = None
    print("Sage Module not found at main, (p,q,r)=(%s,%s,%s)"%(p, q, r))

a = FreeAlgebra("a b", P, [[p, q], [q, r]])
b = PBWAlgebra("x y z t u v",a)
x = b.set_pbw_element('ut')

#print(x)
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

a= letters.Letter("a")
#b= letters.Letter("b")
#c= letters.Letter("c")
d = letters.Letter("")


#r = word.Word([a, b], True)
#s = word.Word([b, a])
#t = word.Word([a,b,c])
u = word.Word([d,a,a,d,d], True)


"""

x = element.Element({r:4, s:1})
y = element.Element({s:1, r:-1})
z = element.Element({t:1})


xa= x
xb = x+z

u = letters.PBWLetter("u", xa, True)
v = letters.PBWLetter("v", xb)

num = u.c_bilinear(v)

print("The result is", num)
"""

