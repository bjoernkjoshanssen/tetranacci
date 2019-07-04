import itertools

def maxSave(w): # July 3, 2019, works on 1st try
	maxSoFar = 0
	for baseStart in range(0, len(w)):
		for baseEnd in range(baseStart + 1, len(w)):
			baseLength = baseEnd - baseStart
			for t in range(baseEnd, len(w)):
				if w[t] != w[t-baseLength]:
					saving = t - baseEnd
					break
			maxSoFar = max(maxSave(w[t + 1:]) + saving, maxSoFar) # t + 1 to make the powers disjoint
	return maxSoFar


#Clyde start
def dot(v1, v2):
	return sum(x*y for x,y in zip(v1,v2))

def uniqv2(a,n):
	sol=[]
	#for i in range(len(a)):
	#	#if a[i] > n or a[i] < 0:
	#	#	print
	#	#	print i
	#	#	print("Invalid: Try again")
	#	#	print a
	#	#	print
	#	#	return 0
	var=list(itertools.product(range(0,n+1),repeat=len(a)))
	for i in range(len(var)):
		if dot(a,var[i])==n:
			sol.append(var[i])
	if len(sol) == 1:
		return True
	#print("The Solutions are:")
	#if len(sol)==0:
	#	print("There are no Solutions")
	#else:
	#	for k in range(len(sol)):
	#		print(sol[k])

#uniqv2(theAs,dot(theAs,theXs))
#Clyde end

def uniqueSolution(theAs, theXs):
	print theAs, theXs,dot(theAs,theXs)
	if uniqv2(theAs,dot(theAs,theXs)):
		print "OK"
	else:
		print "No"
	#copy from Clyde Felix
	return True

def maxSaveWithDiophantus(w,theAs, theXs): # a1x1+...+asxs is beginning of equation
	#UNDER CONSTRUCTION
	maxSoFar = 0
	for baseStart in range(0, len(w)):
		for baseEnd in range(baseStart + 1, len(w)):
			baseLength = baseEnd - baseStart
			for t in range(baseEnd, len(w)):
				if w[t] != w[t-baseLength]:
					saving = t - baseEnd
					break
			if uniqueSolution(theAs + [baseLength],theXs + [(t-baseEnd)/baseLength]):#FIX THE LOGIC HERE
				maxSoFar = max(maxSave(w[t + 1:]) + saving, maxSoFar) # t + 1 to make the powers disjoint
	return maxSoFar


print maxSaveWithDiophantus((0,1,0,1,0,0,0,0,1),[],[])
raise SystemExit

def morphismFibonacci(k,i):
	assert(type(k) is int)
	assert(type(i) is int)
	assert(0<= i and i < k)
	if i < k-1:
		return (0, i + 1)
	if i == k-1:
		return (0,)

def morphismWord(k,word):
	return reduce(
		operator.add, (
			morphismFibonacci(k,word[i]) for i in range(0, len(word))
		)
	)

assert(
	reduce(operator.add, [(1, 2), (3, 4), (5, 6)]) == (1, 2, 3, 4, 5, 6)
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

[T0,T1,T2,T3,T4,T5,T6,T7,T8,T9,TA] = [kbonacci(3,i) for i in range(0, 11)]

maxSave(TA)
