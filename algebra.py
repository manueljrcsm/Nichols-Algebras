# -*- coding: utf-8 -*-

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