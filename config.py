
try:
    from sage.all_cmdline import *  # imports sage library

    _sage_const_2 = Integer(2);
    _sage_const_1 = Integer(1)
    names = ('p', 'q', 'r')  # tuple of strings with the q matrix
    P = FractionField(PolynomialRing(QQ, 3, 'p,q,r'))
    (p,q,r) = P._first_ngens(3)
    # print(P)

except:  # IGNORE
    (p,q,r) = (2,3,5)
    print("Sage Module not found, (p,q,r)=(%s,%s,%s)"%(p, q, r))