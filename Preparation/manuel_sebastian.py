#!/usr/bin/env python
#!/usr/bin sage -python
# -*- coding: utf-8 -*-
#TO RUN ON SAGE (WITH PYTHON 2), GO TO THE FOLDER OF THE FILE AND TYPE sage -python polished_qhs.py
#TO RUN INSIDE PYTHON SHELL (2 OR 3) exec(open"filepath/polished_qhs.py"").read())

#IMPORTS
from operator import add
import platform #to check python version
import copy
import sys
#END OF IMPORTS

#CODE
try: #to make it work on both sage and regular python
	try:
		from sage.all_cmdline import *   # imports sage library
		_sage_const_2 = Integer(2); _sage_const_1 = Integer(1)
        names = ('p','q', 'r') # tuple of strings with the q matrix
        P = FractionField(PolynomialRing(QQ,3,'p,q,r'))
		#K = NumberField(u**_sage_const_2  + u + _sage_const_1 , names=('q',)); (q,) = K._first_ngens(1) #K is the field containing a primitive third root of unity 'r'
		
		## OPTIONAL: This code is to create variables in the field, that can be used as placeholders in generic linear combinations. Computation can be made to then derive relations or conditions and find out
		## precisely what the linear combination coefficients must be.
		#A = PolynomialRing(K, 3,names=('alpha','beta','gamma',)) #to find linear combination of elements
		#(alpha, beta, gamma,) = A._first_ngens(3)
	except ModuleNotFoundError: #IGNORE
		# q=2
		print("Sage Module not found, q=%s" % q)
except NameError: #IGNORE
   #q=2
   print("Sage not found, Name Error, q=%s" % q)

#   SAFE TO IGNORE
if platform.python_version()[0] == '2':
	reload(sys)
	sys.setdefaultencoding('utf-8')

def present(string):
	"""
	Auxiliary function. Takes a monomial written as a concatenation of letters and returns the monomial written with exponents and powers.
	Input: string
	Output: string
	Example: present('aaa') outputs 'a^3'
	"""
	if len(string) <=1:
		return string
	word = ''
	i = 0
	while i < len(string):
		#for different letters
		k= 1
		while i < len(string):
			#to count a letter
			if i == len(string)-1:
				i+=1
				break
			elif string[i+1] == string[i]:
				k +=1
				i+=1
			else:
				i+=1
				break
		if k == 1:
			word += string[i-1]
        ## To change the presentation into x_b, x_a+b, etc., toggle comment in these lines:
        #elif string[i-1] == 't':
			# for j in range(k):
			# word+='x_b'
		#elif string[i-1] == 'u':
			# for j in range(k):
			# word+='x_{a+b}'
        #elif string[i-1] == 'v':
			# for j in range(k):
			# word+='x_{3a+2b}'
		#elif string[i-1] == 'x':
			# for j in range(k):
			# word+='x_{2a+b}'
        #elif string[i-1] == 'y':
			# for j in range(k):
			# word+='x_{3a+b}'
		#elif string[i-1] == 'z':
			# for j in range(k):
			# word+='x_a'
		elif string[i-1] == ")":
			word +="))"
		else:
			word += string[i-1] + "^" + str(k)
	return word
 
class nichols:
	"""Class whose objects are elements in the Nichols algebra B.
	Elements are polynomials with coefficients in P. These elements are represented by Python dictionaries. 
	The keys in the dictionary are strings (words) in the letters a, x and z, corresponding to monomials on the variables a,x and xa, respectively (e.g., "azzz" corresponds to a(xa)^3).
	The value of a given key is the coefficient that comes with that monomial term.
	The commutation relations in the letter a, x and z are    
	za = - az - aax - aa + aaa 
	xz = -z	 - xa - xxa - zx
	Here we also have the assumption that a^3 = 1. This can be manually turned off.
	Functionalities: print, comparison (equality test), addition, subtraction, multiplication, reduction to the basis (with order a < xa < x)
	"""
	# TODO needs scalar multiplication,  ordered presentation, lookup terms of certain form (lexicographic order on the monomials), presentation of exponentials, 
	# on a second phase, add y and b and further relations
	def __init__(self, dic):
		"""The constructor of the class nichols. Creates a element in the class, which I call a nichols. This is simply a dictionary. Defines some attributes of the element which can then be manipulated.
		Examples of inputs: 
		x -> 		nichols({'x':1})
		xa + a -> 	nichols({'z':1,'a':1})
		xxa +2xa -> nichols({'xz' : 1,'xa':2})
		IMPORTANT: There is a better method in general to create elements in the class nichols, look below for the method 'nicholsify'
		"""
		newdic = dic.copy()
		self.poly = newdic
		self.scalars = newdic.values()
		self.terms = newdic.keys()
		self.pairs = newdic.items()

	def __str__(self):
		"""Creates the string of an element, i.e., what you see when you do 'print element'.
		"""
		word = ""
		i=0
		for term, sca in self.pairs:
						#Run through the monomial terms of the element
			scalar = str(sca)
			if scalar == "1" and term != "":
								#If the coefficient of a term is 1, then it is ommited
				scalar = ""
			if i > 0:
								#Adds a plus sign between sucessive terms
								word += " + "
			if len(scalar) > 3 or scalar[0:1]=="-":
								#Terms with a minus sign or complicated elements from K are put under parentheses, for clarity
				scalar = "(" + scalar + ")"
			word+= scalar + present(term)#.replace("z","(xa)") #Inserting a '#' before .replace will make the output come out with 'z' instead of '(xa)', if you get tired of 'xa'.
			i+=1
		if word == "":
						#Empty dictionaries correspond to the 0 element
			return "0"
		else:
			return word

	def __eq__(self,other):
		"""Defines when two nichols elements are equal, i.e., when written in the basis, the monomial terms are all the same with the same coefficients.
		"""
		newself = self.red()
		newother = other.red()
		for term1, sca1 in newself.pairs:
			if term1 not in newother.terms:
				return False
			elif sca1 != newother.poly[term1]:
				return False
		for term2, sca2 in newother.pairs:
			if term2 not in newself.terms:
				return False
			elif sca2 != newself.poly[term2]:
				return False
		return True

	def __hash__(self):
		return hash(str(self))

	def __add__(self,other):
		"""Defines addition of two nichols elements with the '+' syntax in python. 
		Inputs must be elements from the class. Returns another nichols element.
		Essentially, what it does is the concatenation of the dictionaries and adds the coefficients for the same monomial term.
		"""
		newdic = self.poly.copy()
		for term,sca in other.pairs:
			if term in newdic:
				newdic[term] += sca
			else:
				newdic[term] = sca
		return nichols(newdic).red()

	def __sub__(self,other):
		"""Defines subtraction of two nichols elements with the '-' syntax in python. 
		"""
		return self + minusnichols*(other)

	def __mul__(self,other):
		"""Defines multiplication of two nichols elements. As for classical polynomials, it consists of the linear expansion of the terms and concatenation
		pairwise of monomial terms (and product of the respetive coefficients).
		"""
		newpoly = nichols({})
		for term1,sca1 in self.pairs:
			for term2,sca2 in other.pairs:
				newterm = term1 + term2
				newpoly += nichols({newterm : sca1 * sca2})
		return newpoly.red()

	def __delitem__(self,term):
		"""Auxiliary method."""
		del self.poly[term]

	def red(self):
		"""Reduction of a polynomial to its standard basis form t > u > v > x > y > z. Where it really gets interesting and where the commutation relations are applied.
		The relations are
			zt = qtz + u
			zu = (pq)uz + x
			zx = (p^2q)xz + y
			xu = (p^2q^3r)ux + v
			zy = (p^3q)yz
			ut = (1+ r - rq^2)/(qr) tu - (1-q^2)(1 - q^2r)/(q^2r) t^2z
			To change this to writing the monomials with the order z > y >x > v > u >t, you would change it here.
		"""
		newpoly = nichols(self.poly.copy()) #create a copy to begin
		for term,sca in newpoly.pairs:
			#run through the monomial terms recursively, applying the relations whenever possible. Bergman's Diamond lemma guarantees this works.
			if sca ==0:	
				#monomial terms with corresponding coefficient 0 are deleted
				del newpoly[term] 
				return newpoly.red()
			for i in range(len(term)-1):
				if term[i]  == 'z' and term[i+1] == 't': 
					# multiplication zt = q tz + u
					del newpoly[term]
					newpoly +=  nichols({term[:i]:sca}) * nichols({'tz':q,'u':1}) * nichols({term[i+2:]:1})
					return newpoly.red()
				elif term[i]  == 'z' and term[i+1] == 'u': 
					# multiplication zu = (pq)uz + x
					del newpoly[term]
					newpoly +=  nichols({term[:i]:sca}) * nichols({'uz':p*q,'x':1}) * nichols({term[i+2:]:1})
					return newpoly.red()
				elif term[i]  == 'z' and term[i+1] == 'x': 
					# multiplication zx = (p^2q)xz + y
					del newpoly[term]
					newpoly +=  nichols({term[:i]:sca}) * nichols({'xz':p*p*q,'y':1}) * nichols({term[i+2:]:1})
					return newpoly.red()
				elif term[i]  == 'x' and term[i+1] == 'u': 
					# multiplication xu = (p^2q^3r)ux + v
					del newpoly[term]
					newpoly +=  nichols({term[:i]:sca}) * nichols({'ux':p*p*q*q*q*r,'v':1}) * nichols({term[i+2:]:1})
					return newpoly.red()
				elif term[i]  == 'z' and term[i+1] == 'y': 
					# multiplication zy = (p^3q)yz
					del newpoly[term]
					newpoly +=  nichols({term[:i]:sca}) * nichols({'yz':p*p*p*q}) * nichols({term[i+2:]:1})
					return newpoly.red()
				elif term[i]  == 'u' and term[i+1] == 't': 
					# multiplication ut = (1+ r - rq^2)/(qr) tu - (1-q^2)(1 - q^2r)/(q^2r) t^2z
					del newpoly[term]
					newpoly +=  nichols({term[:i]:sca}) * nichols({'tu':(1+r-r*q*q)/(q*r),'ttz':(1-q*q)*(1-q*q*r)/(q*q*r)}) * nichols({term[i+2:]:1})
					return newpoly.red()
                ## TODO: infer other commutations from these ones
                
                ## Saving for later if truncation relations are needed
				#elif term[i] == 'K' and term[i+1] == 'K':
					#if i < len(term)-2:
						#if term[i+2] == 'K': 
							##multiplication kkk = 1
							#del newpoly[term]
							#newpoly +=  qhs({term[:i]:sca}) * qhs({term[i+3:]:1})
							#return newpoly.red()

		return newpoly
	
##### AUXILIARY FUNCTIONS #####

#def deg(string):
	#"""Given a word in the letters, x, z and a, returns a triple of the number of ocurrences of each.
	#Currently useless. The idea was to use this to make the program return the monomial terms ordered in some way.
	#"""
	#degx = 0
	#degz = 0
	#dega = 0
	#for letter in string:
		#if letter == "x":
			#degx += 1
		#if letter == "z":
			#degz += 1    
		#if letter == "a":
			#dega += 1
	#return (degx,degz,dega)
				
def nicholsify(string,scalar =1):
	"""The most pratical way to construct nichols element. Constructs individual monomial terms as nichols elements.
	Inputs: string, scalar (one by default).
	Output: nichols element of the form 'scalar times string' written in the basis.
	Examples: 
	1) x can be created as nicholsify('x')  #no need to include the 1
	2) 3*a*x can be created as nicholsify('ax',3)
	3) 1 can be created as nicholsify('') #empty string
	4) nicholsify("xa") is automatically turned into a nichols element 'z'
	5) Block can be quickly constructed using '+', '-', '*', e.g., z + 3x can be created as nicholsify('z') + nicholsify('x',3)
	"""
	if string ==0:
		newnichols =  nichols({'':0})
	else:
		newnichols = nichols({string:scalar})
	return newnichols.red()

def scalar(num,den = True):
	if den:
		return nicholsify('',num)
	else:
      # to force actual divison instead of floor division, if arguments are integers
      return nicholsify('', (num + 0*q)/den) 

def shownichols(newnichols):
	"""Enumerates the terms of a nichols class element. Use it as a better form of 'print', for very long elements.
	Input: nichols class element
	Output: one monomial term per line
	"""
	i=1
	for term, sca in newnichols.pairs:
		print(str(i) + " (" + str(nicholsify(term)) +  ") : " +str(sca))
		i+=1
	print "END"
		
#def showtensor(newtensor):
	#"""Same as 'shownichols' but for tensor class elements. Enumerates the terms of a tensor class element. Use it as a better form of 'print', for very long elements. 
	#Input: tensor class element
	#Output: one pure tensor term per line"""
	#i=1
	#for pair, sca in newtensor.items:
		#print(str(i) + " (" + str(pair[0]) + " , " + str(pair[1]) + ") : " +str(sca))
		#i+=1;
	#print "END"

#class PiTensorGammapi(tensor):
	#"""Subclass of tensor. Let pi : A to A/AB^+  be the quotient map. Pi maps x to zero, if it is on the right of the monomial term.
	#Let \Gamma be a (partially computed) cleaving map  A/AB^+ to A.
	#Computes Pi \otimes \Gamma\Pi of a tensor class element.  The maps Pi and \Gamma \Pi can be optionally turned off individually. In practice,
	#it can be used to compute coaction images together with Delta:  (\pi \otimes 1)Delta : A \to A/AB^+ \otimes A
	#"""
	##TODO build up inductively a dictionary storing images of the cleaving map
	#def __init__(self, dic,PiFirst = True,PiSecond = True,already = {}):
		#newdic = {}
		#for pair, sca in dic.items:
			#newsca = sca
			#firstterm  = pair[0].terms[0]
			#secondterm = pair[1].terms[0]
			#newfirstterm = ''
			#newsecondterm = ''
			#if PiFirst == True:
				#for letter in firstterm:
					#if letter == 'x':
						#newsca *= 0
					#else:
						#newfirstterm +=letter
			#else:
				#newfirstterm = firstterm
			#firstqhs = qhsify(newfirstterm)
			#if PiSecond == True:
				#for letter in secondterm:
						#if letter == 'x':
							#newsca *= 0
						#else:
							#newsecondterm += letter
				#if newsecondterm in already: #TODO make this much less ad hoc
					#secondqhs = already[newsecondterm]
					##print "Already on the list: ",newsecondterm, secondqhs
				#else:
					#secondqhs = qhsify(newsecondterm)
			#else:
				#secondqhs = qhsify(secondterm)
			#for term2,sca2 in secondqhs.pairs:
				#newsecondqhs = qhsify(term2)
				##print "Will be a right componennt on the final: ",newsecondqhs
				#if (firstqhs,newsecondqhs) in  newdic:
					#newdic[(firstqhs,newsecondqhs)] += newsca*sca2
				#else:
					#newdic[(firstqhs,newsecondqhs)] = newsca*sca2;
		#for pair,sca in newdic.items():
			#if sca == 0:
				#del newdic[pair]
		#self.items =  newdic.items()
		#self.dic = newdic
		#self.tensors = newdic.keys()
		#self.scalars = newdic.values()
		
	#def __str__(self):
		#word = ""
		#i=0
		#for pair, sca in self.items:
			#scalar = str(sca)
			#first = pair[0].terms[0]
			#second = pair[1].terms[0]
			#if scalar == "1":
				#scalar = ""
			#if first == "":
				#first = "1"
			#if second == "":
				#second = "1"
			#if i > 0:
				#if scalar[0:1] == '-':
					#word += " - "
					#if scalar == "-1":
						#scalar = ""
					#else: 
						#scalar = str(sca)[1:]
				#else:
					#word += " + "
			#if len(scalar) > 3:
				#scalar = "(" + scalar + ")"
			#firststr = present(first).replace("z","xa")
			#secondstr = present(second).replace("z","xa")
			#firststr = u"\u03c0" + "(" + firststr + ")"
			##secondstr = u"\u03b1"+"_%s0 " %j+ newsecondterm
			##secondstr = u"\u03b3" + "(" + u"\u03c0" + "(" + newsecondterm + "))" #for gamma(pi(term))
			#newstr = scalar + firststr + u"\u2297"+ secondstr
			#word+= newstr
			#i+=1
		## to print an enumerated list of terms  
		#i=0
		#for pair, sca in self.items:
			#print(str(i) + " " + pair[0].terms[0] + " " + u"\u2297" + " " + pair[1].terms[0] + " : " + str(sca))
			#i+=1
		#if word == "":
			#return "0"
		#else:
			##return word
			#return ""
		
	#def __add__(self,other):
		#selftensor = tensor(self.dic)
		#othertensor = tensor(other.dic)
		#newtensor = selftensor+othertensor
		#return PiTensorGammapi(newtensor.red(),False,False)            
#END OF CODE

#COMPUTATIONS		
#Auxiliary terms that are good to have defines
nichols1 = nichols({'':1})
#qhse = qhsify('E')
#qhsf = qhsify('F')
#qhsk = qhsify('K')
minusnichols = nichols({'':-1})
#tensorminus = tensorize(qhs1,minusqhs)

#qhsx = scalar(1,2*q+1)*qhsk*(qhsf-scalar(1/(q-q*q))*qhse) + scalar(-1,3) + scalar(1,3)*qhsk*qhsk
#print qhsx
#qhsa = qhsk*qhsk
#qhsx2 = qhsx*qhsx
#qhse2 =qhse*qhse
#eqn = qhsx2 + qhsx2*qhsx
#print qhsk*qhse
#print qhsk*qhsf
#print qhsf*qhse
#print qhsa*qhsa*qhsx + qhsa*qhsx*qhsa + qhsx*qhsa*qhsa +qhsa*qhsa - qhs1
#print qhsa*qhsx*qhsx + qhsx*qhsa*qhsx + qhsx*qhsx*qhsa +qhsa*qhsx + qhsx*qhsa
#print qhse2*qhse - scalar(6*q+3)*eqn 
#print "CHECK"
#casi = scalar((1-q*q)*3,2*q+1)*(scalar(1,q-q*q)*qhse*qhsf - scalar(1,3)*(scalar(q*q)*qhsk + scalar(q)*qhsk*qhsk))
#alpha=-q-2
#beta = 1
#gamma=-q-1
#c= scalar(alpha)*qhse*qhsf + scalar(beta)*qhsk + scalar(gamma)*qhsk*qhsk
#print c*c*c - scalar(3*q*q)*c-scalar(2)
#print casi
#print qhse*c - c*qhse
#print qhsf*c - c*qhsf
#print qhsk*c - c*qhsk
#print qhsx*qhsa*qhsx*qhsa - qhsa*qhsa*qhsx*qhsx - qhsa*qhsa*qhsx + scalar(1,3)
#print casi*qhse - qhse*casi
#print casi*qhsf - qhsf*casi
#print casi*qhsk - qhsk*casi
#casi2 = casi*casi
#casi3 = casi2*casi
#factor1 = casi+scalar(q)
#factor2 = casi - scalar(2*q)
##print scalar((2)*q+1,3*q)*factor1
##print factor1*factor2
#coideal = factor1*factor1
#Deltacoideal = Delta(coideal)

#def redqhs2(poly):
	#newpoly = qhs(poly.poly.copy())
	#for term,sca in newpoly.pairs:
			#if sca ==0:	
				#del newpoly[term] 
				#return redqhs2(newpoly)
			#for i in range(len(term)-1):
				#if term[i]  == 'E' and term[i+1] == 'F': 
					##relation EF = (1-q)/3 K - (q+2)/3 K^2 + (2*q+1)/3'
					#del newpoly[term]
					#newpoly +=  qhs({term[:i]:sca}) * qhs({'K':(1-q)/3,'KK': -(q+2)/3,'':(2*q+1)/3}) * qhs({term[i+2:]:1})
					#return redqhs2(newpoly.red())
	#return newpoly

#def redtensor(tensor1):
	#newtensor = tensor({})
	#for pair, scalar in tensor1.items:
		#first = pair[0]
		#second = pair[1]
		#print "OLD", tensor({pair:scalar})
		#newfirst =redqhs2(first)
		#newsecond = redqhs2(second)
		#newsummand = tensor({(newfirst,newsecond):scalar})
		#print "NEW", newsummand
		#newtensor+=newsummand
	#return newtensor.red()	

#print scalar(2*q+1,3)
#print redqhs2(qhs({'EFFKK':1}))

#showtensor(redtensor(Deltacoideal))
#print "casi=",casi
#print "coideal="
#showtensor(Deltacoiddeal)
#print "coideal*f=",coideal*qhsf
#print "coideal*f*f=",coideal*qhsf*qhsf
#print "coideal*e=",coideal*qhse
#print "coideal*e*e=",coideal*qhse*qhse
#print "Delta(coideal)=",Deltacoidal
#print coideal*qhsf
#print qhse*coideal
#showtensor(Delta(coideal))# - tensorize(coideal,qhs1 - qhsk - qhsk*qhsk) -tensorize(qhs1  qhsk - qhsk*qhsk, coideal))
#showtensor(Delta(coideal) - tensorize(coideal,qhs1))
#print Delta(coideal)-tensorize(qhs1,coideal)
#print (factor1*factor2)*(factor1*factor2)

#print casi3 - scalar(1,3)*casi + scalar(2,27) 

#Computation of the element 'F' and 'e' from the article
#alpha = 1 + r
#beta = (r + 2)/3
#f = qhsz + qhsify('ax',alpha) + qhsify('a',beta) + qhsify('aa',-beta)
#e = qhsify('',r)*qhsa*qhsx + qhsify('xa',-1) + qhsify('a',(r-1)/3) + qhsify('aa',-(r-1)/3)
#f3 = f*f*f
#Deltaf3 = Delta(f3)
#print "r is a primitive third root of unity"
#print "F^3 = ", f3, "\n"
#print "Term description of F^3 - monomial: scalar "
#showqhs(f3)
#print "Delta(F^3) = ",Deltaf3,"\n" 
#print "Term description of Delta(F^3) - (tensor1, tensor2): scalar "
#showtensor(Deltaf3)

#casi = minusqhs*e*f +qhsify('aa',(r*r)*(2*r+1)*(2*r+1)/9)+qhsify('a',r*(2*r+1)*(2*r+1)/9) #casimir element

#Other previous computations that serve as examples of how I use the code

# #1. Trying to see if an element is (a^2,a)-twisted primitive
# showtensor(Deltacasi -tensorize(qhsa*qhsa,casi) - tensorminus*tensorize(casi,qhsa)) 

# #2. Trying to see if a given commutator is zero (to check if the casimir element candidate is really central)
# showqhs(casi*qhsx-qhsx*casi)

# #3. Element c from the article
# x2 = qhsx*qhsx
# eqn = x2 + x2*qhsx # The qhs element 'xx + xxx', from the equation of the nodal cubic
# c = f3 + qhsify('',(3*r - 6))*eqn
