import math
import time
import datetime
import itertools
import numpy as np
import operator
import functools

def maxSave(w):
	maxSoFar = 0
	saving=0
	for baseStart in range(0, len(w)):
		for baseEnd in range(baseStart + 1, len(w)):
			baseLength = baseEnd - baseStart
			for t in range(baseEnd, len(w)):
				if w[t] != w[t-baseLength]:
					saving = t - baseEnd
					break
			maxSoFar = max(maxSave(w[t + 1:]) + saving, maxSoFar) # t + 1 to make the powers disjoint
	return maxSoFar

def morphismFibonacci(k,i):
	assert(type(k) is int)
	assert(type(i) is int)
	assert(0<= i and i < k)
	if i < k-1:
		return (0, i + 1)
	if i == k-1:
		return (0,)

def morphismWord(k,word):
	return functools.reduce(
		operator.add, (
			morphismFibonacci(k,word[i]) for i in range(0, len(word))
		)
	)

assert(
	functools.reduce(operator.add, [(1, 2), (3, 4), (5, 6)]) == (1, 2, 3, 4, 5, 6)
)

def kbonacci(k,i): #the ith kbonacci word
	assert(type(k) is int)
	assert(type(i) is int)
	assert(0 <= i and 2 <= k)
	if i < k - 1:
		return ()
	if i == k - 1:
		return (k - 1,)
	return morphismWord(k,kbonacci(k,i-1))

class makeUniqRecursive:
	def __init__(self, a, n):
		self.a = a
		self.n = n
		self.numSol = 0

	def isUnique(self):
		self.uniqRecursive([])
		#if self.a[0:2] == [3,4]:
		#	print("ok we found numSol=" + str(self.numSol) + " and a=" + str(self.a))
		return (self.numSol == 1)
	def uniqRecursive(self,i):
		k = len(i)#k is how many parameters to use
		#print self.a[0:k]
		#print i[0:k]
		#print
		if len(i) < len(self.a):
			myDot = np.dot(self.a[0:k],i[0:k])
			if myDot == self.n:
				self.numSol += 1
				if self.numSol > 1:
					return False
			if myDot < self.n:
				for j in range(0, self.n + 1):
					self.uniqRecursive(i + [j])
					if self.numSol > 1:
						return False
		elif np.dot(self.a[0:k],i[0:k]) == self.n:
			#print self.numSol
			self.numSol += 1

def uniqv2(a,n):
	if len(a) > 0 and min(a) <= 0:
		return False
	if max(a) > n:
		return False
	if min(a) <= 1 and len(a) > 1:
		return False
		
	if min(a) <= 1 and len(a)>1 and sorted(a)[1] <= 1: # two coefficients are 1
		return False
	#print "a is " + str(a)
	#print "n is " + str(n)
	numSol = 0
	count = 0
	for i in itertools.product(range(0,n+1),repeat=len(a)):
		count += 1
		if count % 50000 == 0:
			print(i)
		#	#print count
		#	#print
		if np.dot(a,i)==n:
			numSol += 1
			if numSol > 1:
				return False
	return (
		numSol == 1
	)




def uniqueSolution(theAs, theXs):
	#return uniqv2(theAs,np.dot(theAs,theXs))
	#return makeUniqRecursive(theAs,np.dot(theAs,theXs))

	m = makeUniqRecursive(theAs,np.dot(theAs,theXs))
	return m.isUnique()
def maxSaveWithDiophantus(w,theAs, theXs): # a1x1+...+asxs is beginning of equation
	threshold = 2
	#print("Starting maxSaveWithDiophantus")
	if len(w) > 20:
		print(str((len(w),theAs, theXs)) )

	maxSoFar = 0
	numberOfSaves = 0

	saving=0

	#print theAs
	#print "test"
	for baseStart in range(0, len(w)):
		#print("\t\t\t\tbaseStart: " +str(baseStart))
		for baseEnd in range(baseStart + 1, len(w)):
			#print("\t\t\t\tbaseEnd: " +str(baseEnd))
			baseLength = baseEnd - baseStart
			patternBroken = False
			for maxDesired in range(baseEnd, len(w)): #for advanced processing where we don't greedily absorb everything
				#print("\t\t\t\tmaxDesired: " + str(maxDesired))
				if not patternBroken:
					for t in range(baseEnd, maxDesired+1):
						#print("*"*(t+1-baseEnd) + "."*(len(w)-(t-baseEnd)))
						if w[t] != w[t-baseLength]:
							patternBroken = True
							saving = t - baseEnd
							break
					#print "this"
					#print((t,baseEnd,baseLength))
					if not patternBroken:
						saving = t + 1 - baseEnd
					#print("saving:"+str(saving))
					if saving >= baseLength and len(theAs) < len(w): #and ((t+1-baseEnd) // baseLength > 0):
						tryTheAs = theAs + [baseLength]
						tryTheXs = theXs + [1 + ((t+1-baseEnd) // baseLength)]
						#if tryTheAs[0:2] == [3,4] and tryTheXs[0:2] == [2,2]:
						#	print
						#	print(w)
						#	print("saving:" + str(saving))
						#	print("t:" + str(t))
						#	print("baseStart:" + str(baseStart))
						#	print("baseEnd:" + str(baseEnd))
						#	#print("tryTheAs:" + str(tryTheAs))
						#	#print("tryTheXs:" + str(tryTheXs))
						if (
							#(np.dot(tryTheAs,tryTheXs) <= len(w)) and #this is flawed since w is now shorter and a is still longer.
							len(tryTheAs) > 0 and 
							uniqueSolution(tryTheAs,tryTheXs)
						):
							#if tryTheAs[0:2] == [3,4] and tryTheXs[0:2] == [2,2]:
							#	print("Passed next test")
							if len(w[t + 1:])>0:#FIX THE LOGIC HERE
								#print("unique (" + str((tryTheAs, tryTheXs)) + "): Yes")
								#print
								[recursiveMax,recursiveNumberOfSaves] = maxSaveWithDiophantus(w[t + 1:], tryTheAs, tryTheXs)
								#print
								if recursiveMax + saving > maxSoFar:
									#print "Whoa..."
									maxSoFar = max(
										recursiveMax + saving - baseLength,
										maxSoFar
									) # t + 1 to make the powers disjoint
									if saving >= baseLength:
										numberOfSaves = recursiveNumberOfSaves + 1
								#print
								#print "New maxSoFar: " + str(maxSoFar)
							else:
								maxSoFar = max(saving - baseLength, maxSoFar) # was: saving - baseLength
								if saving >= baseLength: # and maxSoFar > 0:
									numberOfSaves = 1
							#	print "unique: No"
	#print "maxSoFar: " + str(maxSoFar) #+ " with theAs=" + str(theAs)
	#print
	return [maxSoFar,numberOfSaves]

def savUnique(word):
	#print("Considering word " + str(word))
	[maxSave,numberOfSaves] =  maxSaveWithDiophantus(word,[],[])
	#print "\tmaxSave:" + str(maxSave)
	#print "\tnumberOfSaves:" + str(numberOfSaves)
	return maxSave + numberOfSaves

def lowerAutomaticComplexity(word):
	#print "savUnique is " + str(savUnique(word))
	print "Lower automatic complexity of " + str(word) + " is:"
	return int(math.ceil(
		(len(word) + 1 - savUnique(word)) / float(2) # This is true
		#We have to keep track of the number of powers! savingsPair = [savings, numberOfSaves]
	))



#
#Length		Average A_N		Average lower A_N
#	0			1				1
#	1			1				1
#	2			1.5				1.5
#	3			1.75			1.75
#	4			1.875			more			(it gives 2 for 0010 but 3 for 0100 which is awkward.)



#print lowerAutomaticComplexity((0,0,1,0))

for xseq in itertools.product((0,1),repeat=3):
	print lowerAutomaticComplexity(xseq)



raise SystemExit
print lowerAutomaticComplexity((0,0,1))
print lowerAutomaticComplexity((0,1,0,0))
print lowerAutomaticComplexity((0,1,2,3,4,5,6,7,8,9))
print lowerAutomaticComplexity((0,1,2,3,0,1,2,3))
print lowerAutomaticComplexity((0,1,1,0,1,0,0,1))
print lowerAutomaticComplexity((0,0))
print lowerAutomaticComplexity((0,0,0))

for k in range(0, 20):
	print lowerAutomaticComplexity((0,)*k)

print lowerAutomaticComplexity((0,0,1))
print lowerAutomaticComplexity((0,0,0,0,0,1))



mseq63 = ( # according to https://ece.uwaterloo.ca/~j25ni/CP460/3_Modern_Stream_Cipher_Part_2.pdf
	0,0,0,0,0,1,0,0,0,
	0,1,1,0,0,0,1,0,1,
	0,0,1,1,1,1,0,1,0,
	0,0,1,1,1,0,0,1,0,
	0,1,0,1,1,0,1,1,1,
	0,1,1,0,0,1,1,0,1,
	0,1,0,1,1,1,1,1,1
)

#print lowerAutomaticComplexity((0,)*5+(1,)*5)

#print lowerAutomaticComplexity(mseq63) #30... 0.24 seconds... vs. the Hyde bound 32
#Can also do this for n=127 LFSR now then:
mseq127 = (
	0,0,0,0,1,1,1,0,
	1,1,1,1,0,0,1,0,
	1,1,0,0,1,0,0,1,
	0,0,0,0,0,0,1,0,
	0,0,1,0,0,1,1,0,
	0,0,1,0,1,1,1,0,
	1,0,1,1,0,1,1,0,
	0,0,0,0,1,1,0,0,
	1,1,0,1,0,1,0,0,
	1,1,1,0,0,1,1,1,
	1,0,1,1,0,1,0,0,
	0,0,1,0,1,0,1,0,
	1,1,1,1,1,0,1,0,
	0,1,0,1,0,0,0,1,
	1,0,1,1,1,0,0,0,
	1,1,1,1,1,1,1,
) # and it gives the answer 63 in half a second # https://math.stackexchange.com/questions/1293240/generator-polynomial-creates-a-127-bit-sequence
print lowerAutomaticComplexity(mseq127)
raise SystemExit



word=kbonacci(2,9)
#word=kbonacci(3,10)
#print "'bonacci of length " + str(len(word))
#word=(0,0,0,1,0,0,0,1)
word = (0,0,0,0,0,0)
word = (0,1,0,1,0,1)
word = kbonacci(3, 9)
print lowerAutomaticComplexity(word)
raise SystemExit



print datetime.datetime.now()
startTime = time.time()
print savUnique(kbonacci(2,9))
print(" took " + str(round((time.time() - startTime)/60,1)) + " minutes")

raise SystemExit

for length in range(0, 44+1):
	print
	print datetime.datetime.now()
	startTime = time.time()
	print savUnique(kbonacci(3,9)[0:length])
	print "Length " + str(length) + " took " + str(round((time.time() - startTime)/60,1)) + " minutes"
	#Length 29 took 1.7 minutes
	#Length 30 took 2.5 minutes
	#Length 31 took 3.7 minutes
	#Length 32 took 6.0 minutes
	#Length 33 took 7.6 minutes
	#Length 34 took 10.3 minutes
	#Length 35 took 15.9 minutes
	#Length 42 takes 3 hours?
	#Length 43 takes 4 hours?
	#Length 44 takes 5 hours?
extensiveTesting = False
if extensiveTesting: #__name__ == '__main__':
	#print savUnique((0,1,0))
	assert(savUnique((0,1,0)) == 1)
	assert(savUnique((0,1,0,1,0,1)) == 4)
	assert(savUnique((0,0,0,0,0)) == 4)
	assert(savUnique((0,0,1,0,0,0,0)) == 3)
	assert(savUnique((0,0,0,0,1,0,0)) == 3)
	assert(savUnique((0,1,0,1,0,1)) == 4)
	assert(savUnique((0,0,0,1,0,1,0)) == 3)
	myWord = (0,0,0,0,0,0,1,0,1,0,1)
	#myWord = (0,0,0,0,0,0,1,0,1,0,1,0,1)
	myWord = kbonacci(3,0) #0
	myWord = kbonacci(3,1) #0
	myWord = kbonacci(3,2) #0
	myWord = kbonacci(3,3) #0
	myWord = kbonacci(3,4) #0
	#print("bonacci..." + str(kbonacci(3,5)))
	#myWord = kbonacci(3,5) #1 for 0102
	#myWord = kbonacci(3,6) #3 for 0102010
	#myWord = kbonacci(3,7) #6 for 0102010010201
	#myWord = kbonacci(3,8) #output: 11 (was 9)
	myWord = kbonacci(3,9) #output: 20 (was 19 / 44) #25 minutes!
	myWord = kbonacci(3,10) #output: 37 / 81 but this is only based on whole powers? i.e. on python 2 instead of py3
	#myWord = kbonacci(2,7) # answer 6... 1/2 a second
	#myWord = kbonacci(2,8) # answer 11... 24 seconds... length 21... so saving 11 gives q=22-11=11 which is Hyde bound.
	#myWord = kbonacci(2,9) # 19... 375 secs

	assert(savUnique((0,1,0,0,1,1,1,0,0,0,0)*2) == 11)
	assert(savUnique((1,) + (0,1,0,0,1,1,1,0,0,0,0)*2) == 11)
	assert(savUnique((0,1,1,1,1)*2 + (1,)) == 5)


	word = (0,1,2)*2 + (3,) + (4,5,6,7)*2 + (4,8) #3x+4y=14 gives 5
	assert(savUnique(word) == 8)
	for prefix in range(len(word)-2, len(word)-1):
		myWord = word[0:prefix]
		print("**************")
		print(myWord)
		print("Length " + str(len(myWord)))
		print("Savings " + str(maxSaveWithDiophantus(myWord,[],[])))
		print("Done")




[T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,TA] = [kbonacci(3,i) for i in range(0, 11)]

maxSave(TA)
