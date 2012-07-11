#!/usr/bin/python -tt

import sys, random, re, math, difflib
from decimal import *

# TODO: assemblytree visualization, alignment for time optimization
# TODO: tutorials
# TODO: fill in methods
# TODO: SOEing, Phosphorylate() fxn, Temperature control, Colony picking?, Sequence() fxn (PCR 1000 bp read), 
#       Primers() fxn (EIPCR vs. wobble vs. SOEing vs. etc.), assemblytree alignment 
# TODO: Blunt end ligation, distinction between PCR product and phosphorylated blunt end digests
# TODO: hashing and recognition of redundant products
# TODO: for PCR, identification of primers on the edge of a circular sequence

dna_alphabet = {'A':'A', 'C':'C', 'G':'G', 'T':'T',
                'R':'AG', 'Y':'CT', 'W':'AT', 'S':'CG', 'M':'AC', 'K':'GT',
                'H':'ACT', 'B':'CGT', 'V':'ACG', 'D':'AGT',
                'N':'ACGT',
                'a': 'a', 'c': 'c', 'g': 'g', 't': 't',
                'r':'ag', 'y':'ct', 'w':'at', 's':'cg', 'm':'ac', 'k':'gt',
                'h':'act', 'b':'cgt', 'v':'acg', 'd':'agt',
                'n':'acgt'}

complement_alphabet = {'A':'T', 'T':'A', 'C':'G', 'G':'C','R':'Y', 'Y':'R',
                       'W':'W', 'S':'S', 'M':'K', 'K':'M', 'H':'D', 'D':'H',
                       'B':'V', 'V':'B', 'N':'N','a':'t', 'c':'g', 'g':'c',
                       't':'a', 'r':'y', 'y':'r', 'w':'w', 's':'s','m':'k',
                       'k':'m', 'h':'d', 'd':'h', 'b':'v', 'v':'b', 'n':'n'}
gencode = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

def translate( sequence ):
    """Return the translated protein from 'sequence' assuming +1 reading frame"""
    return ''.join([gencode.get(sequence[3*i:3*i+3],'X') for i in range(len(sequence)//3)])

# Read in all enzymes:
def EnzymeDictionary():
	EnzymeDictionary = {}
	fh = open('REases.tsv', 'rU')
	for line in fh:
		card = line.rstrip().split('\t')
		card[0] = re.sub(r'\-','_',card[0])
		EnzymeDictionary[card[0]] = restrictionEnzyme(card[0],card[1],card[2],card[3],card[4],card[5],card[6],card[7],card[8],card[9])
	return EnzymeDictionary

# Description: Suffix Tree implementation for the purpose of PCR Longest Common Substring identification
# Code from: http://chipsndips.livejournal.com/2005/12/07/
inf = 1000000
# Define a  for a node in the suffix tree
class SuffixNode(dict):
	def __init__(self):
		self.suffixLink = None # Suffix link as defined by Ukkonen
class LCS:
	def __init__(self,str1,str2):
		str = str1 + str2
		inf = len(str)
		self.str = str   #Keep a reference to str to ensure the string is not garbage collected
		self.seed = SuffixNode() #Seed is a dummy node. Suffix link of root points to seed. For any char,there is a link from seed to root
		self.root = SuffixNode() # Root of the suffix tree
		self.root.suffixLink = self.seed
		self.root.depth = 0
		self.deepest = 0,0

		# For each character of str[i], create suffixtree for str[0:i]
		s = self.root; k=0
		for i in range(len(str)):
			self.seed[str[i]] = -2,-2,self.root
			oldr = self.seed
			t = str[i]
			#Traverse the boundary path of the suffix tree for str[0:i-1]
			while True:
				# Descend the suffixtree until state s has a transition for the stringstr[k:i-1]
				while i>k:
					kk,pp,ss = s[str[k]]
					if pp-kk < i-k:
						k = k + pp-kk+1
						s = ss
					else:
						break
			   # Exit this loop if s has a transition for the string str[k:i] (itmeans str[k:i] is repeated);
			   # Otherwise, split the state if necessary
				if i>k:
					tk = str[k]
					kp,pp,sp = s[tk]
					if t.lower() == str[kp+i-k].lower():
						break
					else: # Split the node
						r = SuffixNode()
						j = kp+i-k
						tj = str[j]
						r[tj] = j, pp, sp
						s[str[kp]] = kp,j-1, r
						r.depth = s.depth + (i-k)
						sp.depth = r.depth + pp - j + 1
						if j<len(str1)<i and r.depth>self.deepest[0]:
							self.deepest = r.depth,j-1
				elif t in s:
					break
				else:
					r = s
			   # Add a transition from r that starts with the letter str[i]
				tmp = SuffixNode() 
				r[t] = i,inf,tmp
				# Prepare for next iteration
				oldr.suffixLink = r
				oldr = r
				s = s.suffixLink
			# Last remaining endcase
			oldr.suffixLink = s

	def LongestCommonSubstring(self):
		start = self.deepest[1]-self.deepest[0]+1
		end = self.deepest[1]+1
		return (self.str[start:end],start,end)
	def LCSasRegex(self, currentPrimer, template):
		start = self.deepest[1]-self.deepest[0]+1
		end = self.deepest[1]+1
		MatchIndicesTuple = (self.str[start:end],start,end)
		annealingRegex = re.compile(MatchIndicesTuple[0], re.IGNORECASE)
		PrimerStub = currentPrimer[0:len(currentPrimer)-len(MatchIndicesTuple[0])-1]
		AnnealingMatches = annealingRegex.findall(template)
		return (AnnealingMatches, MatchIndicesTuple, PrimerStub)

# Description: PrimerError class associates information about primer design errors and sequences
class PrimerError(Exception):
    """Exception raised for errors in the primer(s) input.

    Attributes:
        primer -- sequence for one (or both, in tuple form) of the given input primers
        template -- sequence for the given PCR template
        msg  -- explanation of the error
    """

    def __init__(self, primer, template, msg):
        self.primer = primer
        self.template = template
        self.msg = msg

# Description: PCRErrorHandling() function identifies errors in primer design and raises exceptions based on errors and their context
def PCRErrorHandling(InputTuple):
	(fwd,matchCount,matchedAlready,nextOrientation,myList,tooShort1,currentPrimer,template) = InputTuple
	if fwd:
		if matchCount == 0 & len(myList) > 0:				# no Tm > 45 C matches in forward direction
			tooShort1 = True
		else:
			tooShort1 = False
		if matchCount > 1:									# if matches in forward direction more than once
			if nextOrientation == 2: 							# ... but was supposed to match in reverse direction
				raise PrimerError(currentPrimer,template,'primers both anneal in forward (5\'->3\') orientation AND primer anneals to multiple sites in template.')
			raise PrimerError(currentPrimer,template,'primer anneals to multiple sites in template.')
		elif matchCount == 1:								# if matches in the forward direction exactly once
			if nextOrientation == 2: 							# ... but was supposed to match in reverse direction
				raise PrimerError(currentPrimer,template,'primers both anneal in forward  (5\'->3\') orientation.')
			matchedAlready = 1
		return (matchedAlready,tooShort1)
	else:
		if matchCount == 0 & len(myList) > 0:				# no Tm > 45 C matches in reverse direction
			tooShort2 = True
		else:
			tooShort2 = False
		if matchCount > 1:									# if matches in reverse direction more than once
			if matchedAlready == 1:								# ... and already matched in forward direction
				if nextOrientation == 1: 							# ... but was supposed to match in forward direction
					raise PrimerError(currentPrimer,template,'primers both anneal in reverse (3\'->5\') orientation AND error primer anneals to multiple sites in template AND error primer anneals in both orientations.')
				raise PrimerError(currentPrimer,template,'primer anneals to multiple sites in template AND error primer anneals in both orientations.')
			if nextOrientation == 1: 
				raise PrimerError(currentPrimer,template,'primers both anneal in reverse (3\'->5\') orientation AND error primer anneals to multiple sites in template.')
			raise PrimerError(currentPrimer,template,'primer anneals to multiple sites in template.')
		elif matchCount == 1: 								# if matches in the reverse direction exactly once
			if matchedAlready == 1:								# ... and already matched in forward direction
				if nextOrientation == 1: 							# ... but was supposed to match in forward direction
					raise PrimerError(currentPrimer,template,'both primers have same reverse (3\'->5\') orientation AND error primer anneals in both orientations.')
				raise PrimerError(currentPrimer,template,'primer primes in both orientations.')
			else:
				matchedAlready = 2
		if matchedAlready == 0:								# if no matches
			if tooShort1 and tooShort2:							# ... it may be because the annealing region has a tm < 45 C
				raise PrimerError(currentPrimer, template,'primer does not anneal in either orientation (annealing Tm < 45 C).')
			raise PrimerError(currentPrimer,template,'primer does not anneal in either orientation.') 	# ... or not.
		return (matchedAlready, tooShort2)

# Description: RaisePrimerError() function provides context specific warnings to user about PCR failure as a result of primer design
def RaisePrimerError(inputTuple, error):
	(primer1DNA, primer2DNA, templateDNA) = inputTuple
	print('EXCEPTION: For PCR of template ('+templateDNA.name+') with primers ('+primer1DNA.name+', '+primer2DNA.name+'), '+error.msg)
	print('Error Primer: '+error.primer[:-1])

# Description: AssemblyTreeRelationships() function assigns relationships for PCR inputs and PCR product for assembly tree purposes
def AssemblyTreeRelationships(inputTuple, parent, fwdTM, revTM):
	(primer1DNA, primer2DNA, templateDNA) = inputTuple
	for child in inputTuple:
		child.addParent(parent)
	parent.setChildren(inputTuple)
	intVal = int(round(len(parent.sequence)/1000+0.5))
	parent.setTimeStep(intVal)
	parent.addMaterials(['Polymerase','dNTP mix','Polymerase buffer'])
	thermoCycle = str(intVal)+'K'+str(int(round(max(fwdTM,revTM))))
	parent.instructions = thermoCycle+' PCR template '+templateDNA.name+' with primers '+primer1DNA.name+', '+primer2DNA.name
	return parent

# Description: PCR() function constructs generalized suffix tree for template and a given primer to identify annealing region,
# and raises PrimerError exceptions for different cases of failed PCR as a result of primer design
# Note: PCR() product is not case preserving
def PCR(primer1DNA, primer2DNA, templateDNA):
	# Suffix Tree string intiialization, non-alphabet character concatenation
	(template, primer_1, primer_2) = (templateDNA.sequence + '$', primer1DNA.sequence + '$', primer2DNA.sequence + '$')
	# Tuple of assemblyTree 'children', for the purpose of child/parent assignment
	inputTuple = (primer1DNA, primer2DNA, templateDNA)
	# Initialization of all parameters, where indices is the start / stop indices + direction of annealing primer sequences 
	(fwdTM, revTM, indices, counter, rightStub, leftStub, nextOrientation) = (0,0,[0,0,0,0,0,0],0,'','',0)
	try:
		# NOTE: no assumptions made about input primer directionality
		for currentPrimer in (primer_1, primer_2):
			fwdMatch = LCS(template.upper(),currentPrimer.upper())	
			(forwardAnnealingMatches, forwardMatchIndicesTuple, forwardPrimerStub) = fwdMatch.LCSasRegex(currentPrimer, template)
			(matchCount, matchedAlready, start, stop) = (0,0,0,0)
			for match in forwardAnnealingMatches:
				if primerTm(match) >= 45:			# forward match criteria: annealing Tm >= 45 C for matches
					matchCount += 1
			tooShort1 = False 						# Default
			# Forward case error handling: delegated to PCRErrorHandling function
			(matchedAlready,tooShort1) = PCRErrorHandling((1,matchCount,matchedAlready,nextOrientation,forwardAnnealingMatches,tooShort1,currentPrimer,template))
			revMatch = LCS(template.upper(),reverseComplement(currentPrimer).upper()+'$')
			(reverseAnnealingMatches, reverseMatchIndicesTuple, reversePrimerStub) = revMatch.LCSasRegex(currentPrimer, template)
			matchCount = 0
			for match in reverseAnnealingMatches:
				if primerTm(match) >= 45:			# reverse match criteria: annealing Tm >= 45 C for matches
					matchCount += 1
			# Reverse case error handling: delegated to PCRErrorHandling function
			(matchedAlready,tooShort2) = PCRErrorHandling((0,matchCount,matchedAlready,nextOrientation,reverseAnnealingMatches,tooShort1,currentPrimer,template))
			if matchedAlready == 1:
				(indices[counter], indices[counter+1], indices[counter+2]) = (forwardMatchIndicesTuple[1], forwardMatchIndicesTuple[2], 'fwd')
				(counter,nextOrientation,leftStub) = (counter+3, 2, forwardPrimerStub)
			elif matchedAlready == 2:
				(indices[counter], indices[counter+1], indices[counter+2]) = (reverseMatchIndicesTuple[1], reverseMatchIndicesTuple[2], 'rev')
				(counter,nextOrientation,rightStub) = (counter+3, 1, reverseComplement(reversePrimerStub))
		if indices[2] == 'fwd':
			(fwdStart, fwdEnd, revStart, revEnd) = (indices[0], indices[1], indices[3], indices[4])
		else:
			(fwdStart, fwdEnd, revStart, revEnd) = (indices[3], indices[4], indices[0], indices[1])
		(fwdTM, revTM) = (primerTm(template[fwdStart:fwdEnd]), primerTm(template[revStart:revEnd]))		
		if fwdStart < revStart and fwdEnd < revEnd:
			parent = DNA(leftStub+template[fwdStart:revEnd]+rightStub,'PCR product','PCR product of '+primer1DNA.name+', '+primer2DNA.name+' on '+templateDNA.name)
		else:
			# circular template is exception to the fwdStart < revStart and fwdEnd < revEnd rule
			if templateDNA.topology == 'circular':	
				parent = DNA(leftStub+template[fwdStart:len(template)-1]+template[:revStart]+rightStub,'PCR product','PCR product of '+primer1DNA.name+', '+primer2DNA.name+' on '+templateDNA.name)
			else:
				raise PrimerError((primer1DNA.sequence, primer2DNA.sequence),template,'forward primer must anneal upstream of the reverse.')
		return AssemblyTreeRelationships(inputTuple, parent, fwdTM, revTM)
	except PrimerError as error:
		RaisePrimerError(inputTuple, error)

# Description: reverseComplement() is case preserving reverse complementation of nucleotide sequences
def reverseComplement(sequence):
  	return "".join([complement_alphabet.get(nucleotide, '') for nucleotide in sequence[::-1]])

# Description: reverse() is case preserving string reversal
def reverse(sequence):
	return sequence[::-1]

# Description: Complement() is case preserving complementation of nucleotide sequences
def Complement(sequence):
  	return "".join([complement_alphabet.get(nucleotide, '') for nucleotide in sequence[0:]])

# Primer TM function suite: primerTm(), primerTmsimple(), get_55_primer(), nearestNeighborTmNonDegen(), getTerminalCorrectionsDsHash(),
# getTerminalCorrectionsDhHash(), getDsHash(), getDhHash()
# Implemented by Tim Hsaiu in JavaScript, adapted to Python by Nima Emami
# Based on Santa Lucia et. al. papers
def primerTm(sequence):
	milliMolarSalt = 50.
	milliMolarMagnesium = 1.5
	nanoMolarPrimerTotal = 200
	molarSalt = milliMolarSalt/1000
	molarMagnesium = milliMolarMagnesium/1000
	molarPrimerTotal = Decimal(nanoMolarPrimerTotal)/Decimal(1000000000)
	re.sub(r'\s','', sequence)
	return nearestNeighborTmNonDegen(sequence, molarSalt, molarPrimerTotal, molarMagnesium)

def primerTmsimple(sequence):
  	return 64.9+41*(GCcontent(sequence)*len(sequence) - 16.4)/len(sequence)

# phusion notes on Tm
# https://www.finnzymes.fi/optimizing_tm_and_annealing.html
# get substring from the beginning of input that is 55C Tm
def get_55_primer(sequence):
	lastChar = 17
	myPrimer = sequence.substring(0,lastChar)
	while( primerTmsimple(myPrimer) < 54.5 or lastChar > 60):
		lastChar = lastChar + 1
		myPrimer = sequence[0:lastChar]
	return myPrimer

def nearestNeighborTmNonDegen (sequence, molarSalt, molarPrimerTotal, molarMagnesium):
	# The most sophisticated Tm calculations take into account the exact sequence and base stacking parameters, not just the base composition.
	# m = ((1000* dh)/(ds+(R * Math.log(primer concentration))))-273.15;
	# Borer P.N. et al. (1974)  J. Mol. Biol. 86, 843.
	# SantaLucia, J. (1998) Proc. Nat. Acad. Sci. USA 95, 1460.
	# Allawi, H.T. and SantaLucia, J. Jr. (1997) Biochemistry 36, 10581.
	# von Ahsen N. et al. (1999) Clin. Chem. 45, 2094.
	sequence = sequence.lower()

	R = 1.987 # universal gas constant in Cal/degrees C * mol
	ds = 0 	  # cal/Kelvin/mol
	dh = 0    # kcal/mol

	# perform salt correction
	correctedSalt = molarSalt + molarMagnesium * 140 # adjust for greater stabilizing effects of Mg compared to Na or K. See von Ahsen et al 1999
	ds = ds + 0.368 * (len(sequence) - 1) * math.log(correctedSalt) # from von Ahsen et al 1999

	#  perform terminal corrections
	termDsCorr = getTerminalCorrectionsDsHash()
	ds = ds + termDsCorr[sequence[0]]
	ds = ds + termDsCorr[sequence[len(sequence) - 1]]

	termDhCorr = getTerminalCorrectionsDhHash()
	dh = dh + termDhCorr[sequence[0]]
	dh = dh + termDhCorr[sequence[len(sequence) - 1]]

	dsValues = getDsHash()
	dhValues = getDhHash()

	for i in range(len(sequence)-1):
		ds = ds + dsValues[sequence[i] + sequence[i + 1]]
		dh = dh + dhValues[sequence[i] + sequence[i + 1]]
	return (((1000 * dh) / (ds + (R * math.log(molarPrimerTotal / 2)))) - 273.15)

def getTerminalCorrectionsDsHash():
	# SantaLucia, J. (1998) Proc. Nat. Acad. Sci. USA 95, 1460.
	dictionary = {'g' : -2.8,'a': 4.1,'t' : 4.1,'c' : -2.8}
	return dictionary

def getTerminalCorrectionsDhHash():
	# SantaLucia, J. (1998) Proc. Nat. Acad. Sci. USA 95, 1460.
	dictionary = {'g':0.1,'a' : 2.3,'t' : 2.3,'c' : 0.1}
	return dictionary

def getDsHash():
	# SantaLucia, J. (1998) Proc. Nat. Acad. Sci. USA 95, 1460.
	dictionary = {
	'gg' : -19.9,
	'ga' : -22.2,
	'gt' : -22.4,
	'gc' : -27.2,
	'ag' : -21.0,
	'aa' : -22.2,
	'at' : -20.4,
	'ac' : -22.4,
	'tg' : -22.7,
	'ta' : -21.3,
	'tt' : -22.2,
	'tc' : -22.2,
	'cg' : -27.2,
	'ca' : -22.7,
	'ct' : -21.0,
	'cc' : -19.9}
	return dictionary

def getDhHash():
	# SantaLucia, J. (1998) Proc. Nat. Acad. Sci. USA 95, 1460.
	dictionary = {'gg': -8.0,
	'ga' : -8.2,
	'gt' : -8.4,
	'gc' : -10.6,
	'ag' : -7.8,
	'aa' : -7.9,
	'at' : -7.2,
	'ac' : -8.4,
	'tg' : -8.5,
	'ta' : -7.2,
	'tt' : -7.9,
	'tc' : -8.2,
	'cg' : -10.6,
	'ca' : -8.5,
	'ct' : -7.8,
	'cc' : -8.0}
	return dictionary

# TODO: clean up and modularize
# Description: Digest() function
def Digest(InputDNA, Enzymes):
	(indices, frags, sites, totalLength) = ([], [], "", len(InputDNA.sequence)) # Initialization
	enzNames = ''
	incubationTemp = 0
	nameList = []
	for enzyme in Enzymes:
		nameList.append(enzyme.name)
		enzNames = enzNames+enzyme.name+', '
		incubationTemp = max(incubationTemp, enzyme.incubate_temp)
	enzNames = enzNames[:-2]
	if InputDNA.topology == "linear":	
		# Initialize indices array with start and end indices of the linear fragment
			# Add dummy REase to avoid null pointers
		dummy = restrictionEnzyme("dummy", "", "", "", "", "", 0, 0, "(0/0)","")
		indices = [(0,0,'',dummy), (totalLength,0,'',dummy)]
	# Identify restriction sites, fill in indices array
	for enzyme in Enzymes:
		sites = enzyme.find_sites(InputDNA)
		for site in sites:
			# WARNING: end proximity for linear fragments exception
			if InputDNA.topology == 'linear' and int(site[0]) - int(enzyme.endDistance) < 0 or int(site[1]) + int(enzyme.endDistance) > totalLength:
				print('WARNING: end proximity for '+enzyme.name+' restriction site at indices '+str(site[0]%totalLength)+','+str(site[1]%totalLength)+' for input with length '+str(totalLength))
				if InputDNA.topology == 'linear' and site[2] == 'antisense' and site[1] - max(enzyme.bottom_strand_offset,enzyme.top_strand_offset) < 0:
					print('WARNING: restriction cut site for '+enzyme.name+' with recognition indices '+str(site[0]%totalLength)+','+str(site[1]%totalLength)+' out of bounds for input with length '+str(totalLength))
				else:
					pass
			# WARNING: restriction index out of bounds exception
			elif InputDNA.topology == 'linear' and site[2] == 'antisense' and site[1] - max(enzyme.bottom_strand_offset,enzyme.top_strand_offset) < 0:
				print('WARNING: restriction cut site for '+enzyme.name+' with recognition indices '+str(site[0]%totalLength)+','+str(site[1]%totalLength)+' out of bounds for input with length '+str(totalLength))
				pass
			else: 
				site = site + (enzyme, )
				indices.append(site)
		indices.sort()
	# If you have overlapping restriction sites, choose the first one and discard they
		# second (TODO: there may be a better, non-greedy way to do this... not sure)
	filtered = []
	n = 0
	while n < len(indices):
		try:
			(currentTuple, nextTuple) = (indices[n], indices[n+1])
			(currentStart, nextStart, currentEnzyme, nextEnzyme) = (currentTuple[0], nextTuple[0], currentTuple[3], nextTuple[3])
			filtered.append(indices[n])
			if currentStart + len(currentEnzyme.alpha_only_site) >= nextStart:
				currentIndex = indices[n+1]
				if currentIndex[0] == len(InputDNA.sequence):
					pass
				else:
					print('WARNING: overlapping restriction sites '+currentTuple[3].name+' (indices '+str(currentTuple[0])+','+str(currentTuple[1])+') and '+nextTuple[3].name+' (indices '+str(nextTuple[0])+','+str(nextTuple[1])+')')
					n = n + 1
			n = n + 1
		except:
			# got to end of list,
			filtered.append(indices[n])
			n = n + 1
	indices = filtered
	# If it's linear, only act on the first n - 1 fragments until you hit the blunt ending
		# If it's circular, then the 'last' segment is adjacent to the 'first' one, so you
		# need to consider the adjacency relationships among the full n fragments
	if InputDNA.topology == "linear":
		lastIt = len(indices) - 1
	else:
		lastIt = len(indices)
	# Consider enzyme for the current restriction site as well as the next restriction
		# site, so that you can generate overhangs for both sides of the current fragment
	for n in range(lastIt):
		currentTuple = indices[n]
		if n+1 > len(indices) - 1:
			n = -1
		nextTuple = indices[n+1]
		(currentStart, currentEnd, direction, currentEnzyme) = currentTuple
		(nextStart, nextEnd, nextDirection, nextEnzyme) = nextTuple
		# If it's on the sense strand, then overhang is positive
			# If it's on the antisense strand, then you have to go back towards the 5'
			# to generate the overhang (so multiply by -1)
		# CT(B)O = current top (bottom) overhang, AL(R)L = add left (right) length, NT(B)O = next top (bottom) overhang
		(ALL, ARL) = (0,0)
		if direction == "sense":
			(CTO, CBO) = (currentEnzyme.top_strand_offset, currentEnzyme.bottom_strand_offset)
			ALL = max(CTO,CBO)
		else:
			(CTO, CBO) = (-1 * currentEnzyme.top_strand_offset, -1 * currentEnzyme.bottom_strand_offset)
			ALL = max(CTO,CBO)
		if nextDirection == "sense":
			(NTO, NBO) = (nextEnzyme.top_strand_offset, nextEnzyme.bottom_strand_offset)
			ARL = min(NTO,NBO)
		else:
			(NTO, NBO) = (-1 * nextEnzyme.top_strand_offset + 1, -1 * nextEnzyme.bottom_strand_offset + 1)
			ARL = min(NTO,NBO)-1
		# Update start value currentStart and apply ( mod length ) to deal with edge cases
			# Also, update end value digEnd for fragment indices
		currentStart = currentStart+ALL
		currentStart = currentStart % totalLength
		digEnd = nextStart + ARL
		if currentEnzyme.reach and direction == "sense":
			currentStart = currentStart + len(currentEnzyme.alpha_only_site)
		if nextEnzyme.reach and nextDirection == "sense":
			digEnd = digEnd + len(nextEnzyme.alpha_only_site)
		# Loop around fragment case for circular InputDNA's
		if digEnd > 0 and currentStart > 0 and digEnd < currentStart and InputDNA.topology == 'circular':
			if n == -1:
				digested = DNA(InputDNA.sequence[currentStart:]+InputDNA.sequence[:digEnd],'digest','Digest of '+InputDNA.name+' with '+enzNames)
			else:
				print('WARNING: restriction sites for '+currentTuple[3].name+' ('+str(currentTuple[0])+','+str(currentTuple[1])+') and '+nextTuple[3].name+' ('+str(nextTuple[0])+','+str(nextTuple[1])+') contain mutually interfering overhangs -- fragment discarded.')
				continue
		else:
			digested = DNA(InputDNA.sequence[currentStart:digEnd],'digest','Digest of '+InputDNA.name+' with '+enzNames)
		# Adjust top and bottom overhang values based on the orientation of the restriction site
		if direction == "sense":
			(TO, BO) = (CTO, CBO)
		else:
			(TO, BO) = (CBO, CTO)
		difference = abs(abs(BO) - abs(TO))
		# Generate TLO and BLO fragment overhangs
		if abs(TO) < abs(BO) and direction == "sense" or abs(TO) > abs(BO) and direction == "antisense":
			if currentStart - len(currentEnzyme.alpha_only_site) < 0:
				digested.topLeftOverhang = Overhang(InputDNA.sequence[currentStart-difference:]+InputDNA.sequence[:currentStart])
			else:
				digested.topLeftOverhang = Overhang(InputDNA.sequence[currentStart-difference:currentStart])
			digested.bottomLeftOverhang = Overhang('')
		else:
			digested.topLeftOverhang = Overhang('') 
			# Edge case statement
			if currentStart - len(currentEnzyme.alpha_only_site) < 0:
				digested.bottomLeftOverhang = Overhang(Complement(InputDNA.sequence[currentStart-difference:]+InputDNA.sequence[:currentStart]))
			else:
				digested.bottomLeftOverhang = Overhang(Complement(InputDNA.sequence[currentStart-difference:currentStart]))
		# Adjust top and bottom overhang values based on the orientation of the restriction site
		if direction == "sense":
			(TO, BO) = (NTO, NBO)
		else:
			(TO, BO) = (NBO, NTO)
		difference = abs(abs(BO) - abs(TO))
		# Apply ( mod length ) operator to end index value digDiff to deal with edge cases
		digDiff = digEnd + difference
		digDiff = digDiff % totalLength
		# Generate TRO and BRO fragment overhangs
		if abs(TO) < abs(BO) and direction == "sense" or abs(TO) > abs(BO) and direction == "antisense":
			digested.topRightOverhang = Overhang('')
			# Edge case statement
			if digDiff - len(nextEnzyme.alpha_only_site) < 0:
				digested.bottomRightOverhang = Overhang(Complement(InputDNA.sequence[digEnd:]+InputDNA.sequence[:digDiff]))
			else:
				digested.bottomRightOverhang = Overhang(Complement(InputDNA.sequence[digEnd:digDiff])) 
		else:
			# Edge case statement
			if digDiff - len(nextEnzyme.alpha_only_site) < 0:
				digested.topRightOverhang = Overhang(InputDNA.sequence[digEnd:]+InputDNA.sequence[:digDiff])
			else:
				digested.topRightOverhang = Overhang(InputDNA.sequence[digEnd:digDiff])
			digested.bottomRightOverhang = Overhang('')
		# Discard small fragments
		if len(digested.sequence) < 4:
			pass
		else:
			# frags.append((currentStart,digested))
			frags.append(digested)
		# frags.sort()
	for frag in frags:
		frag.setChildren((InputDNA, ))
		InputDNA.addParent(frag)
		if len(nameList) == 2:
			bufferChoices = DigestBuffer(nameList[0],nameList[1])
		else:
			bufferChoices = DigestBuffer(nameList[0])
		bestBuffer = int(bufferChoices[0])
		if bestBuffer < 5:
			bestBuffer = 'NEB'+str(bestBuffer)
		else:
			bestBuffer = 'Buffer EcoRI' 
		frag.setTimeStep(1)
		frag.addMaterials([bestBuffer,'ddH20'])
		frag.instructions = 'Digest ('+InputDNA.name+') with '+enzNames+' at '+str(incubationTemp)+'C in '+bestBuffer+' for 1 hour.'
	return frags

class Overhang(object):
	def __init__(self, seq=""):
		self.sequence = seq

class DNA(object):
	#for linear DNAs, this string should include the entire sequence (5' and 3' overhangs included
	def __init__(self, seq="",DNAclass="", name=""):
		self.sequence = seq
		self.length = len(seq)
		notDNA = re.compile('([^gatcrymkswhbvdn])')
		isnotDNA = False
		exceptionText = "" 
		for m in notDNA.finditer(self.sequence.lower()):
			exceptionText = exceptionText + m.group()+ " at position "+ str( m.start()) + " is not valid IUPAC DNA."
			isnotDNA = True
		if(isnotDNA):
			raise Exception(exceptionText)
		self.name = name 	#would be pbca1256 for vectors or pbca1256-Bth8199 for plasmids
		self.description = "SpecR pUC"							 #this is for humans to read
		self.dam_methylated = True
		# self.overhang = "circular" #blunt, 3', 5', circular... should be a class in itself?
		self.topLeftOverhang = Overhang('')
		self.bottomLeftOverhang = Overhang('')
		self.topRightOverhang = Overhang('')
		self.bottomRightOverhang = Overhang('')
		#PCR product, miniprep, genomic DNA
		self.DNAclass = DNAclass
		self.provenance = ""
		self.parents = []
		self.children = ()
		self.instructions = ""
		self.materials = []
		self.timeStep = 0
		#Here is the linked list references for building up action-chains
		# an action chain would be something like do PCR on day 1, do transformation on day 2, etc
		self.head = None
		self.tail = None
		if DNAclass == "primer" or DNAclass == "genomic" or DNAclass == "PCR product" or DNAclass == "digest":
			self.topology = "linear"
		elif DNAclass == 'plasmid':
			self.topology = "circular" #circular or linear, genomic should be considered linear
		else:
			raise Exception("Invalid molecule class. Acceptable classes are 'digest', genomic', 'PCR product', 'plasmid' and 'primer'.")
	def reversecomp(self):
		return reverseComplement(self.sequence) #reverses string
		#code to handle the overhangs & other object attributes
	def addParent(self, DNA):
		self.parents.append(DNA)
	def addMaterials(self, materialsList):
		self.materials += materialsList
	def setTimeStep(self, timeStep):
		self.timeStep = timeStep
	def setChildren(self, inputDNAs):
		self.children = inputDNAs
	def find(self, string):
		return 0
	def clone(self):
		clone = DNA(self.sequence, self.DNAclass, self.name)
		clone.topLeftOverhang = Overhang(self.topLeftOverhang.sequence)
		clone.topRightOverhang = Overhang(self.topRightOverhang.sequence)
		clone.bottomLeftOverhang = Overhang(self.bottomLeftOverhang.sequence)
		clone.bottomRightOverhang = Overhang(self.bottomRightOverhang.sequence)
		return clone
	def prettyPrint(self):
		#prints out top and bottom strands, truncates middle so length is ~100bp
		#example:
		# TTATCG...[1034bp]...GGAA
		#   ||||              ||||
		#   TAGC..............CCTTAA
		if self.DNAclass == 'digest':
			(TL,TR,BL,BR) = SetFlags(self)
			if len(self.sequence) > 8:
				trExtra = ''
				brExtra = ''
				if TR:
					trExtra = self.topRightOverhang.sequence
				if BR:
					brExtra = self.bottomRightOverhang.sequence
				print("\t"+self.topLeftOverhang.sequence+' '*len(self.bottomLeftOverhang.sequence)+self.sequence[:4]+'.'*3+'['+str(len(self.sequence)-8)+'bp]'+'.'*3+self.sequence[len(self.sequence)-4:]+trExtra)
				print("\t"+' '*len(self.topLeftOverhang.sequence)+'|'*4+' '*(10+len(str(len(self.sequence)-8)))+'|'*4)
				print("\t"+' '*len(self.topLeftOverhang.sequence)+self.bottomLeftOverhang.sequence+reverseComplement(self.sequence[:4])+'.'*(10+len(str(len(self.sequence)-8)))+reverseComplement(self.sequence[len(self.sequence)-4:])+brExtra)
			else:
				trExtra = ''
				brExtra = ''
				if TR:
					trExtra = self.topRightOverhang.sequence
				if BR:
					brExtra = self.bottomRightOverhang.sequence
				print("\t"+self.topLeftOverhang.sequence+' '*len(self.bottomLeftOverhang.sequence)+self.sequence+trExtra)
				print("\t"+' '*len(self.topLeftOverhang.sequence)+'|'*len(self.sequence))
				print("\t"+' '*len(self.topLeftOverhang.sequence)+self.bottomLeftOverhang.sequence+reverseComplement(self.sequence)+brExtra)
		else:
			if len(self.sequence) > 8:
				print("\t"+self.sequence[:4]+'.'*3+'['+str(len(self.sequence)-8)+'bp]'+'.'*3+self.sequence[len(self.sequence)-4:])
				print("\t"+'|'*4+' '*(10+len(str(len(self.sequence)-8)))+'|'*4)
				print("\t"+reverseComplement(self.sequence[:4])+'.'*(10+len(str(len(self.sequence)-8)))+reverseComplement(self.sequence[len(self.sequence)-4:]))
			else:
				print("\t"+self.sequence)
				print("\t"+'|'*len(self.sequence))
				print("\t"+reverseComplement(self.sequence))
		return 0
	
# Description: BaseExpand() for regex generation, taken from BioPython
def BaseExpand(base):
    """BaseExpand(base) -> string.

    given a degenerated base, returns its meaning in IUPAC alphabet.

    i.e:
        b= 'A' -> 'A'
        b= 'N' -> 'ACGT'
        etc..."""
    base = base.upper()
    return dna_alphabet[base]

# Description: regex() function to convert recog site into regex, from Biopython
def regex(site):
    """regex(site) -> string.

    Construct a regular expression from a DNA sequence.
    i.e.:
        site = 'ABCGN'   -> 'A[CGT]CG.'"""
    reg_ex = site
    for base in reg_ex:
        if base in ('A', 'T', 'C', 'G', 'a', 'c', 'g', 't'):
            pass
        if base in ('N', 'n'):
            reg_ex = '.'.join(reg_ex.split('N'))
            reg_ex = '.'.join(reg_ex.split('n'))
        if base in ('R', 'Y', 'W', 'M', 'S', 'K', 'H', 'D', 'B', 'V'):
            expand = '['+ str(BaseExpand(base))+']'
            reg_ex = expand.join(reg_ex.split(base))
    return reg_ex

# Description: ToRegex() function to convert recog site into regex, from Biopython
def ToRegex(site, name):
	sense = ''.join(['(?P<', name, '>', regex(site.upper()), ')'])
	antisense = ''.join(['(?P<', name, '_as>', regex( reverseComplement( site.upper() )), ')'])
	rg = sense + '|' + antisense
	return rg	

# Description: restrictionEnzyme class encapsulates information about buffers, overhangs, incubation / inactivation, end distance, etc.
class restrictionEnzyme(object):
	def __init__(self,name="", buffer1="", buffer2="", buffer3="", buffer4="", bufferecori="", heatinact="", incubatetemp=0., recognitionsite="",distance=""):
		self.name = name
		self.buffer_activity =[buffer1, buffer2, buffer3, buffer4, bufferecori]
		self.inactivate_temp = heatinact
		self.incubate_temp = float(incubatetemp)
		#human-readable recognition site
		self.recognition_site = recognitionsite
		self.endDistance = distance
		#function to convert recog site into regex
		alpha_only_site = re.sub('[^a-zA-Z]+', '', recognitionsite)
		self.alpha_only_site = alpha_only_site
		# print ToRegex(alpha_only_site, name)
		self.compsite = ToRegex(alpha_only_site, name)
		self.reach = False
		#convert information about where the restriction happens to an offset on the top and bottom strand
		#for example, BamHI -> 1/5 with respect to the start of the site match
		hasNum = re.compile('(-?\d+/-?\d+)')
		not_completed = 1
		for m in hasNum.finditer(recognitionsite):
			(top, bottom) = m.group().split('/')
			self.top_strand_offset = int(top)
			self.bottom_strand_offset = int(bottom)
			self.reach = True
			not_completed = 0
		p = re.compile("/")
		for m in p.finditer(recognitionsite):
			if not_completed:
				self.top_strand_offset = int(m.start())
				self.bottom_strand_offset =  len(recognitionsite) - 1 - self.top_strand_offset	

	def prettyPrint(self):
		print("Name: ", self.name, "Recognition Site: ", self.recognition_site)
	def find_sites(self, DNA):
		seq = DNA.sequence
		(fwd, rev) = self.compsite.split('|')
		fwd_rease_re = re.compile(fwd)
		rev_rease_re = re.compile(rev)
		indices = []
		seen = {}
		if DNA.topology == "circular":
			searchSequence = seq.upper() + seq[0:len(self.recognition_site)-2]
		else:
			searchSequence = seq.upper()
		for m in fwd_rease_re.finditer(searchSequence):
			span = m.span()
			span = (span[0] % len(seq), span[1] % len(seq))
			seen[span[0]] = 1
			span = span + ('sense',)
			indices.append(span)
		for m in rev_rease_re.finditer(searchSequence):
			span = m.span()
			try:
				seen[span[0]]
			except:
				span = span + ('antisense',)
				indices.append(span)	
		return indices

# Description: DigestBuffer() function finds the optimal digestBuffer
# todo: If Buffer 2 > 150, return Buffer 2 and list of activity values, else, return buffer 1, 3, or 4 (ignore EcoRI)
# return format will be list, [rec_buff, [buff1_act, buff2_act...buff4_Act]]
def DigestBuffer(*str_or_list):
	best_buff = ""
	best_buff_score = [0,0,0,0,0]
	enzdic = EnzymeDictionary()
	num_enz = 0
	for e in str_or_list:
		enz = enzdic[e]
		best_buff_score = list(x + int(y) for x, y in zip(best_buff_score, enz.buffer_activity))
		num_enz = num_enz + 1
	ret = []	
	if best_buff_score[1] >( 75 * num_enz):
		ret.append(2)
		ret.append(best_buff_score)
	else:
		m = max(best_buff_score)
		p = best_buff_score.index(m)
		ret.append(p)
		ret.append(best_buff_score)
	return ret
#accepts two primers and list of input template DNAs
#todo:implement this with PCR!
def SOERoundTwo(primer1, primer2, templates):
	return 0
def SOE(list_of_primers, templates):
	#assume primers are in the right order  outer  inner_rev  inner_fwd   outer
	#call two pcrs with list[0], [1] and list[2], [3]
	return 0

#given a parent plasmid and a desired product plasmid, design the eipcr primers
#use difflib to figure out where the differences are
#if there is a convenient restriction site in or near the modification, use that
# otherwise, check if there exists bseRI or bsaI sites, and design primers using those
# print/return warning if can't do this via eipcr (insert span too long)

def DesignEIPCR(parent, product):
	diff = difflib.unified_diff(parent, product, lineterm='')
	#fcn to parse difflib output into a list of dict
	# each dict is 'start':pos, 'stop':pos, 'original':origtxt, 'new':newtxt
	return 0

def Distinguish2DNABands(a, b):
        #case of 2
	#for a standard 1-2% agarose gel,
        #we can distinguish a and b if
	#do the following in wolframalpha:  LogLogPlot[|a - b| > (0.208*a+42), {a, 0, 9000}, {b, 0, 9000}]
        return ( abs(a.length - b.length) > (0.208*a.length+42))  & (min(a.length, b.length) > 250 )

#only returns True if can distinguish between all of the DNA bands
def DistinguishDNABands(list_of_dnas):
	ret_val = True
	for i in range(len(list_of_dnas)-1):
		ret_val = ret_val & Distinguish2DNABands(list_of_dnas[i], list_of_dnas[i+1])
	return ret_val

def FindDistinguishingEnzyme(list_of_dnas):
	#find the REase that can distinguish between the input DNAs
	#DistinguishDNABands(a, b) returns true if we can
	# tell apart bands a, b on a gel and a and b are both > 300bp, < 7kb
	#Let n be the number of DNAs in the list.  Let E be the enzyme under question
	# Then we construct a n-dimensional matrix
	# where the dimensions have max value defined by the number of fragments generated by E
	# E can be used to distinguish between the DNAs if there is a complete row or column 
	# that is distinguishable (all True by DistinguishDNABands)
	#ASSUMPTION, for now, only consider n=3	
	#iterate over all enzymes (enzyme list should be prioritized by availability and "goodness")
		#execute find good enz
	#iterate over all combinations of 2 enzymes
		#execute find good enz

	##find good enz
	#for each enzyme/combo in the list
		#calculate fragments for each input DNA
		#skip if any DNA has # fragments > 6
		#n-length list, each character represents the DNA fragment currently under investigation
		#iterate to fill in the hypermatrix values

		#find if the hypermatrix has a column/row that has all True
	
	#returns top 5 list of enzymes/combos that work
	return 0

def FindDistEnz():
	return FindDistinguishingEnzyme(list_of_dnas)

# Description: SetFlags() returns overhang information about a DNA() digest object
def SetFlags(frag):
	(TL,TR,BL,BR) = (0,0,0,0)
	if frag.topLeftOverhang.sequence != '':
		TL = 1
	if frag.topRightOverhang.sequence != '':
		TR = 1
	if frag.bottomLeftOverhang.sequence != '':
		BL = 1
	if frag.bottomRightOverhang.sequence != '':
		BR = 1
	return (TL,TR,BL,BR)

# Description: Ligate() function accepts a list of DNA() digest objects, and outputs list of DNA
def Ligate(inputDNAs):
	products = []
	# self ligation
	for fragment in inputDNAs:
		(TL,TR,BL,BR) = SetFlags(fragment)
		if fragment.DNAclass != 'digest':
			print('WARNING: For ligation reaction, invalid input molecule removed -- ligation input DNA objects must be of class \'digest\'.')
		elif TL+TR+BL+BR == 1:
			pass
		elif TL+TR+BL+BR == 0:
			# blunt end self ligation case --> need to identify that both sides were digested (i.e. both ecoRV blunt ends)
			# and then return circular product of same sequence.
			pass
		elif fragment.topLeftOverhang.sequence != '':
			if fragment.topLeftOverhang.sequence.lower() == Complement(fragment.bottomRightOverhang.sequence.lower()):
				ligated = DNA(fragment.topLeftOverhang.sequence+fragment.sequence,'plasmid',fragment.name+' self-ligation')
				ligated.setChildren((fragment, ))
				fragment.addParent(ligated)
				ligated.setTimeStep(.5)
				ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
				ligated.instructions = 'Self-ligate ('+fragment.name+') with DNA ligase for 30 minutes at room-temperature.'
				products.append(ligated)
		elif fragment.bottomLeftOverhang.sequence != '':
			if fragment.topLeftOverhang.sequence.lower() == Complement(fragment.topRightOverhang.sequence.lower()):
				ligated = DNA(fragment.sequence+fragment.topRightOverhang.sequence,'plasmid',fragment.name+' self-ligation')
				ligated.setChildren((fragment, ))
				fragment.addParent(ligated)
				ligated.setTimeStep(.5)
				ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
				ligated.instructions = 'Self-ligate ('+fragment.name+') with DNA ligase for 30 minutes at room-temperature.'
				products.append(ligated)
	if len(products) > 0 or len(inputDNAs) == 1:
		return products
	i = 0
	while i < len(inputDNAs):
		fragOne = inputDNAs[i]
		j = i + 1
		while j < len(inputDNAs):
			fragTwo = inputDNAs[j]
			(LTL,LTR,LBL,LBR) = SetFlags(fragOne)
			(RTL,RTR,RBL,RBR) = SetFlags(fragTwo)
			# first3 is the number of 3' overhangs for the left fragment, and so on for the other three classifiers
			(first3, first5, second3, second5) = (LTR + LBL, LBR + LTL, RTR + RBL, RBR + RTL)
			if first3 == 2:
				if fragOne.topRightOverhang.sequence.upper() == Complement(fragTwo.bottomLeftOverhang.sequence).upper():
					if fragOne.bottomLeftOverhang.sequence.upper() == Complement(fragTwo.topRightOverhang.sequence).upper():
						ligated = DNA(fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence+fragTwo.topRightOverhang.sequence,'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
						ligated.setChildren((fragOne, fragTwo))
						fragOne.addParent(ligated)
						fragTwo.addParent(ligated)
						ligated.setTimeStep(.5)
						ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
						ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
						products.append(ligated)
				if fragOne.topRightOverhang.sequence.upper() == reverseComplement(fragTwo.topRightOverhang.sequence).upper():
					if fragOne.bottomLeftOverhang.sequence.upper() == reverseComplement(fragTwo.bottomLeftOverhang.sequence).upper():
						ligated = DNA(fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence)+reverse(fragTwo.bottomLeftOverhang.sequence),'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
						ligated.setChildren((fragOne, fragTwo))
						fragOne.addParent(ligated)
						fragTwo.addParent(ligated)
						ligated.setTimeStep(.5)
						ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
						ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
						products.append(ligated)
			elif first3 == 1:
				if LTR:
					# then you know it must have LTL
					if RTR:
						# then, if it is to ligate, it must have compatible RTL
						if fragOne.topRightOverhang.sequence.upper() == reverseComplement(fragTwo.topRightOverhang.sequence).upper():
							if fragOne.topLeftOverhang.sequence.upper() == Complement(fragTwo.topLeftOverhang.sequence).upper():
								ligated = DNA(fragOne.topLeftOverhang.sequence+fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence),'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
								ligated.setChildren((fragOne, fragTwo))
								fragOne.addParent(ligated)
								fragTwo.addParent(ligated)
								ligated.setTimeStep(.5)
								ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
								ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
								products.append(ligated)
					else:
						# to ligate, it must have RBL and RBR
						if fragOne.topRightOverhang.sequence.upper() == Complement(fragTwo.bottomLeftOverhang.sequence).upper():
							if fragOne.topLeftOverhang.sequence.upper() == Complement(fragTwo.bottomRightOverhang.sequence).upper():
								ligated = DNA(fragOne.topLeftOverhang.sequence+fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence,'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
								ligated.setChildren((fragOne, fragTwo))
								fragOne.addParent(ligated)
								fragTwo.addParent(ligated)
								ligated.setTimeStep(.5)
								ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
								ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
								products.append(ligated)
				else:
					# you know it has LBL as its 3 and LBR as its 5
					if RTR:
					# then, if it is to ligate, it must have compatible RTL
						if fragTwo.topRightOverhang.sequence.upper() == Complement(fragOne.bottomLeftOverhang.sequence).upper():
							if fragTwo.topLeftOverhang.sequence.upper() == Complement(fragOne.topLeftOverhang.sequence).upper():
								ligated = DNA(fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence+fragTwo.topRightOverhang.sequence,'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
								ligated.setChildren((fragOne, fragTwo))
								fragOne.addParent(ligated)
								fragTwo.addParent(ligated)
								ligated.setTimeStep(.5)
								ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
								ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
								products.append(ligated)
					else:
						# to ligate, it must have RBL and RBR
						if fragOne.bottomRightOverhang.sequence.upper() == reverseComplement(fragTwo.bottomRightOverhang.sequence).upper():
							if fragOne.bottomLeftOverhang.sequence.upper() == reverseComplement(fragTwo.bottomLeftOverhang.sequence).upper():
								ligated = DNA(Complement(fragOne.bottomLeftOverhang.sequence)+fragOne.sequence+Complement(fragOne.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence),'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
								ligated.setChildren((fragOne, fragTwo))
								fragOne.addParent(ligated)
								fragTwo.addParent(ligated)
								ligated.setTimeStep(.5)
								ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
								ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
								products.append(ligated)
			else:
				if fragOne.topLeftOverhang.sequence.upper() == Complement(fragTwo.bottomRightOverhang.sequence).upper():
					if fragOne.bottomRightOverhang.sequence.upper() == Complement(fragTwo.topLeftOverhang.sequence).upper():
						ligated = DNA(fragOne.topLeftOverhang.sequence+fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence,'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')
						ligated.setChildren((fragOne, fragTwo))
						fragOne.addParent(ligated)
						fragTwo.addParent(ligated)
						ligated.setTimeStep(.5)
						ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
						ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
						products.append(ligated)
				if fragOne.topLeftOverhang.sequence.upper() == reverseComplement(fragTwo.topLeftOverhang.sequence).upper():
					if fragOne.bottomRightOverhang.sequence.upper() == reverseComplement(fragTwo.bottomRightOverhang.sequence.upper()):
						ligated = DNA(fragOne.topLeftOverhang.sequence+fragOne.sequence+reverse(fragTwo.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence),'plasmid',fragOne.name+', '+fragTwo.name+' ligation product')		
						ligated.setChildren((fragOne, fragTwo))
						fragOne.addParent(ligated)
						fragTwo.addParent(ligated)
						ligated.setTimeStep(.5)
						ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
						ligated.instructions = 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'
						products.append(ligated)
			j = j + 1
		i = i + 1
	return products

# TODO: condense and comment
# Description: ZymoPurify() function takes a list of DNA objects and filters out < 300 bp DNA's
def ZymoPurify(inputDNAs):
	if len(inputDNAs) == 0:
		print('WARNING: Zymo purification function passed empty input list -- will return empty output')
		return inputDNAs
	outputBands = []
	sizeTuples = []
	for DNA in inputDNAs:
		fragSize = len(DNA.sequence)
		sizeTuples.append((fragSize,DNA))
	sizeTuples.sort(reverse=True)
	currentTuple = sizeTuples[0]
	currentSize = currentTuple[0]
	while currentSize > 300 and len(sizeTuples) > 1:
		band = currentTuple[1]
		parentBand = band.clone()
		parentBand.setChildren(band)
		band.addParent(parentBand)
		parentBand.setTimeStep(.5)
		parentBand.addMaterials(['Zymo Column','Buffer PE','ddH20'])
		parentBand.instructions = 'Perform standard zymo cleanup on ('+band.name+').'
		outputBands.append(parentBand)
		sizeTuples.pop(0)
		currentTuple = sizeTuples[0]
		currentSize = currentTuple[0]
	if currentSize > 300:
		band = currentTuple[1]
		parentBand = band.clone()
		parentBand.setChildren(band)
		band.addParent(parentBand)
		parentBand.setTimeStep(.5)
		parentBand.addMaterials(['Zymo Column','Buffer PE','ddH20'])
		parentBand.instructions = 'Perform standard zymo cleanup on ('+band.name+').'
		outputBands.append(parentBand)
	return outputBands

# TODO: condense and comment
# Description: ShortFragmentCleanup() function takes a list of DNA objects and filters out < 50 bp DNA's
def ShortFragmentCleanup(inputDNAs):
	if len(inputDNAs) == 0:
		print('WARNING: ShortFragmentCleanup function passed empty input list -- will return empty output')
		return inputDNAs
	outputBands = []
	sizeTuples = []
	for DNA in inputDNAs:
		fragSize = len(DNA.sequence)
		sizeTuples.append((fragSize,DNA))
	sizeTuples.sort(reverse=True)
	currentTuple = sizeTuples[0]
	currentSize = currentTuple[0]
	while currentSize > 50 and len(sizeTuples) > 1:
		band = currentTuple[1]
		parentBand = band.clone()
		parentBand.setChildren(band)
		band.addParent(parentBand)
		parentBand.setTimeStep(.5)
		parentBand.addMaterials(['Zymo Column','Buffer PE','ddH20','Ethanol/Isopropanol'])
		parentBand.instructions = 'Perform short fragment cleanup on ('+band.name+').'
		outputBands.append(parentBand)
		sizeTuples.pop(0)
		currentTuple = sizeTuples[0]
		currentSize = currentTuple[0]
	if currentSize > 50:
		band = currentTuple[1]
		parentBand = band.clone()
		parentBand.setChildren(band)
		band.addParent(parentBand)
		parentBand.setTimeStep(.5)
		parentBand.addMaterials(['Zymo Column','Buffer PE','ddH20','Ethanol/Isopropanol'])
		parentBand.instructions = 'Perform short fragment cleanup on ('+band.name+').'
		outputBands.append(parentBand)
	return outputBands

# TODO: condense and comment
# Description: GelAndZymoPurify() function employs a user-specified purification strategy to cut out a range of band sizes, and
# then filters out < 300 bp DNA's. If 50 bp < [ ] < 300 bp DNAs are detected, switches to short fragment cleanup mode.
def GelAndZymoPurify(inputDNAs, strategy):
	# sort based on size
	shortFlag = False
	lostFlag = False
	if len(inputDNAs) == 0:
		print("WARNING: Gel purification with strategy \'"+strategy+"\' passed empty input list -- will return empty output")
		return inputDNAs
	elif len(inputDNAs) == 1:
		return inputDNAs
	interBands = []
	outputBands = []
	sizeTuples = []
	for DNA in inputDNAs:
		fragSize = len(DNA.sequence)
		sizeTuples.append((fragSize, DNA))
	if isinstance(strategy, str):
		if strategy == 'L':
			sizeTuples.sort(key=lambda x: x[0], reverse=True)
			n = 0
			currentTuple = sizeTuples[n]
			largestSize = currentTuple[n]
			currentSize = largestSize
			while currentSize > largestSize * 5/6 and n < len(sizeTuples) - 1:
				interBands.append(currentTuple[1])
				n = n + 1
				currentTuple = sizeTuples[n]
				currentSize = currentTuple[0]
			if currentSize > largestSize * 5/6:
				if currentSize < 50:
					lostFlag = True
				elif currentSize < 300:
					shortFlag = True
				interBands.append(currentTuple[1])
			if len(interBands) > 1:
				print("WARNING: large fragment purification resulted in purification of multiple, possibly unintended distinct DNAs.")
		elif strategy == 'S':
			sizeTuples.sort()
			n = 0
			currentTuple = sizeTuples[n]
			smallestSize = currentTuple[n]
			currentSize = smallestSize
			while currentSize < smallestSize * 5/6 and n < len(sizeTuples) - 1:
				interBands.append(currentTuple[1])
				n = n + 1
				currentTuple = sizeTuples[n]
				currentSize = currentTuple[0]
			if currentSize > smallestSize * 5/6:
				if currentSize < 50:
					lostFlag = True
				elif currentSize < 300:
					shortFlag = True
				interBands.append(currentTuple[1])
			if len(interBands) > 1:
				print("WARNING: small fragment purification resulted in purification of multiple, possibly unintended distinct DNAs.")
	elif isinstance( strategy, ( int, long ) ):
		sizeTuples.sort(reverse=True)
		currentTuple = sizeTuples[0]
		currentSize = currentTuple[0]
		while currentSize > strategy * 6/5 and len(sizeTuples) > 1:
			sizeTuples.pop(0)
			currentTuple = sizeTuples[0]
			currentSize = currentTuple[0]
		while currentSize > strategy * 5/6 and len(sizeTuples) > 1:
			band = sizeTuples.pop(0)
			interBands.append(band[1])
			currentTuple = sizeTuples[0]
			currentSize = currentTuple[0]
		if currentSize > strategy * 5/6:
			if currentSize < 50:
				lostFlag = True
			elif currentSize < 300:
				shortFlag = True
			interBands.append(currentTuple[1])
		if len(interBands) == 0:
			print("WARNING: For gel purification with strategy \'"+strategy+"\', no digest bands present in given range, with purification yielding zero DNA products.")
		elif len(interBands) > 1:
			print("WARNING: Fragment purification in range of band size '"+str(strategy)+"' resulted in purification of multiple, possibly unintended distinct DNAs.")
	if len(interBands) == 0:
		if lostFlag:
			print("WARNING: Purification with given strategy \'"+strategy+"\' returned short fragments (< 50 bp) that were lost. Returning empty products list.")
		print("WARNING: Purification with given strategy '"+strategy+"' yielded zero products. Returning empty products list.")
	else:
		if lostFlag:
			print("WARNING: Purification with given strategy \'"+strategy+"\' returned at least one short fragment (< 50 bp) that was lost. Returning remaining products.")
			for band in interBands:
				parentBand = band.clone()
				parentBand.setChildren((band,))
				band.addParent(parentBand)
				parentBand.setTimeStep(1)
				parentBand.addMaterials(['Zymo Column','Buffer ADB','Buffer PE','ddH20'])
				parentBand.instructions = 'Gel purify ('+band.name+'), followed by short fragment cleanup.'
				outputBands.append(parentBand)
		elif shortFlag:
			print("WARNING: Purification with given strategy \'"+strategy+"\' yielded short fragments (< 300 bp). Returning short fragment cleanup products.")
			for band in interBands:
				parentBand = band.clone()
				parentBand.setChildren((band,))
				band.addParent(parentBand)
				parentBand.setTimeStep(1)
				parentBand.addMaterials(['Zymo Column','Buffer ADB','Buffer PE','ddH20','Ethanol/Isopropanol'])
				parentBand.instructions = 'Gel purify ('+band.name+'), followed by short fragment cleanup.'
				outputBands.append(parentBand)
		else:
			for band in interBands:
				parentBand = band.clone()
				parentBand.setChildren((band,))
				band.addParent(parentBand)
				parentBand.setTimeStep(1)
				parentBand.addMaterials(['Zymo Column','Buffer ADB','Buffer PE','ddH20'])
				parentBand.instructions = 'Gel purify ('+band.name+'), followed by standard zymo cleanup.'
				outputBands.append(parentBand)
	return outputBands

# Description: HasFeature() function checks for presence of regex-encoded feature in seq
def HasFeature(regex, seq):
	#Regex must be lower case!
	return bool( re.search(regex, seq.lower()) ) | bool( re.search(regex, reverseComplement(seq.lower()) ) )

#####Origins Suite: Checks for presence of certain origins of replication#####
def HasColE2(seq):
	#has ColE2 origin, data from PMID 16428404
	regexp = '....tga[gt]ac[ct]agataagcc[tgc]tatcagataacagcgcccttttggcgtctttttgagcacc' 
	return HasFeature(regexp, seq)
	#necessary and sufficient element for ColE2 replication, however a longer sequence is needed for stable replication
	# 'AGCGCCTCAGCGCGCCGTAGCGTCGATAAAAATTACGGGCTGGGGCGAAACTACCATCTGTTCGAAAAGGTCCGTAAATGGGCCTACAGAGCGATTCGTCAGGGCTGGCCTGTATTCTCACAATGGCTTGATGCCGTTATCCAGCGTGTCGAAATGTACAACGCTTCGCTTCCCGTTCCGCTTTCTCCGGCTGAATGTCGGGCTATTGGCAAGAGCATTGCGAAATATACACACAGGAAATTCTCACCAGAGGGATTTTCCGCTGTACAGGCCGCTCGCGGTCGCAAGGGCGGAACTAAATCTAAGCGCGCAGCAGTTCCTACATCAGCACGTTCGCTGAAACCGTGGGAGGCATTAGGCATCAGTCGAGCGACGTACTACCGAAAATTAAAATGTGACCCAGACCTCGCnnnntga'
	#longer element shown in the Anderson lab that stably replicates

def HasR6K(seq):
	#has R6k, data from Anderson lab observations
	regexp = 'gcagttcaacctgttgatagtacgtactaagctctcatgtttcacgtactaagctctcatgtttaacgtactaagctctcatgtttaacgaactaaaccctcatggctaacgtactaagctctcatggctaacgtactaagctctcatgtttcacgtactaagctctcatgtttgaacaataaaattaatataaatcagcaacttaaatagcctctaaggttttaagttttataagaaaaaaaagaatatataaggcttttaaagcttttaaggtttaacggttgtggacaacaagccagggatgtaacgcactgagaagcccttagagcctctcaaagcaattttgagtgacacaggaacacttaacggctgacatggg'.lower()
	return HasFeature(regexp, seq)

def HasP15A(seq):
	regex = 'aatattttatctgattaataagatgatcttcttgagatcgttttggtctgcgcgtaatctcttgctctgaaaacgaaaaaaccgccttgcagggcggtttttcgaaggttctctgagctaccaactctttgaaccgaggtaactggcttggaggagcgcagtcaccaaaacttgtcctttcagtttagccttaaccggcgcatgacttcaagactaactcctctaaatcaattaccagtggctgctgccagtggtgcttttgcatgtctttccgggttggactcaagacgatagttaccggataaggcgcagcggtcggactgaacggggggttcgtgcatacagtccagcttggagcgaactgcctacccggaactgagtgtcaggcgtggaatgagacaaacgcggccataacagcggaatgacaccggtaaaccgaaaggcaggaacaggagagcgcacgagggagccgccagggggaaacgcctggtatctttatagtcctgtcgggtttcgccaccactgatttgagcgtcagatttcgtgatgcttgtcaggggggcggagcctatggaaaaacggctttgccgcggccctctcacttccctgttaagtatcttcctggcatcttccaggaaatctccgccccgttcgtaagccatttccgctcgccgcagtcgaacgaccgagcgtagcgagtcagtgagcgaggaagcggaatatatcctgtatcacatattctgctgacgcaccggtgcagccttttttctcctgccacatgaagcacttcactgacaccctcatcagtgccaacatagtaag'
	return HasFeature(regex, seq)

def HaspUC(seq):
	regex = 'cccgtagaaaagatcaaaggatcttcttgagatcctttttttctgcgcgtaatctgctgcttgcaaacaaaaaaaccaccgctaccagcggtggtttgtttgccggatcaagagctaccaactctttttccgaaggtaactggcttcagcagagcgcagataccaaatactgtccttctagtgtagccgtagttaggccaccacttcaagaactctgtagcaccgcctacatacctcgctctgctaatcctgttaccagtggctgctgccagtggcgataagtcgtgtcttaccgggttggactcaagacgatagttaccggataaggcgcagcggtcgggctgaacggggggttcgtgcacacagcccagcttggagcgaacgacctacaccgaactgagatacctacagcgtgagcattgagaaagcgccacgcttcccgaagggagaaaggcggacaggtatccggtaagcggcagggtcggaacaggagagcgcacgagggagcttccagggggaaacgcctggtatctttatagtcctgtcgggtttcgccacctctgacttgagcgtcgatttttgtgatgctcgtcaggggggcggagcctatggaaaaacgccagcaacgcggcctttttacggttcctggccttttgctggccttttgctcacat'
	return HasFeature(regex, seq)

#####Resistance Suite: Checks for presence of certain antibiotic resistance markers#####
def HasAAFeature(regex, DNAseq):
	#must be uppercase, checks all six possibilities, fwd, rev x 3 frames
	seq = DNAseq
	retval = bool( re.search(regex, translate(seq.upper() )) ) | bool( re.search(regex,translate(seq[1:].upper() ) ) ) |  bool( re.search(regex,translate(seq[2:].upper() ) ) )
	seq = reverseComplement(seq)
	retval = retval | bool( re.search(regex, translate(seq.upper() )) ) | bool( re.search(regex,translate(seq[1:].upper() ) ) ) |  bool( re.search(regex,translate(seq[2:].upper() ) ) )
	return retval
 
def HasSpecR(seq):
	regex='MRSRNWSRTLTERSGGNGAVAVFMACYDCFFGVQSMPRASKQQARYAVGRCLMLWSSNDVTQQGSRPKTKLNIMREAVIAEVSTQLSEVVGVIERHLEPTLLAVHLYGSAVDGGLKPHSDIDLLVTVTVRLDETTRRALINDLLETSASPGESEILRAVEVTIVVHDDIIPWRYPAKRELQFGEWQRNDILAGIFEPATIDIDLAILLTKAREHSVALVGPAAEELFDPVPEQDLFEALNETLTLWNSPPDWAGDERNVVLTLSRIWYSAVTGKIAPKDVAADWAMERLPAQYQPVILEARQAYLGQEEDRLASRADQLEEFVHYVKGEITKVVGK'
	return HasAAFeature(regex, seq)
def HasAmpR(seq):
	regex='MSIQHFRVALIPFFAAFCLPVFAHPETLVKVKDAEDQLGARVGYIELDLNSGKILESFRPEERFPMMSTFKVLLCGAVLSRIDAGQEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEAIPNDERDTTMPVAMATTLRKLLTGELLTLASRQQLIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW'
	return HasAAFeature(regex, seq)
def HasKanR(seq):
	regex='MSHIQRETSCSRPRLNSNMDADLYGYKWARDNVGQSGATIYRLYGKPDAPELFLKHGKGSVANDVTDEMVRLNWLTEFMPLPTIKHFIRTPDDAWLLTTAIPGKTAFQVLEEYPDSGENIVDALAVFLRRLHSIPVCNCPFNSDRVFRLAQAQSRMNNGLVDASDFDDERNGWPVEQVWKEMHKLLPFSPDSVVTHGDFSLDNLIFDEGKLIGCIDVGRVGIADRYQDLAILWNCLGEFSPSLQKRLFQKYGIDNPDMNKLQFHLMLDEFF'
	return HasAAFeature(regex, seq)
def HasCmR(seq):
	regex='MEKKITGYTTVDISQWHRKEHFEAFQSVAQCTYNQTVQLDITAFLKTVKKNKHKFYPAFIHILARLMNAHPEFRMAMKDGELVIWDSVHPCYTVFHEQTETFSSLWSEYHDDFRQFLHIYSQDVACYGENLAYFPKGFIENMFFVSANPWVSFTSFDLNVANMDNFFAPVFTMGKYYTQGDKVLMPLAIQVHHAVCDGFHVGRMLNELQQYCDEWQGGA'
	return HasAAFeature(regex, seq)
def HasResistance(seq):
	retval = []
	if HasCmR(seq):
		retval.append( 'CmR' )
	if HasKanR(seq):
		retval.append('KanR')
	if HasAmpR(seq):
		retval.append('AmpR')
	if HasSpecR(seq):
		retval.append('SpecR')
	return retval
def HasReplicon(seq):
	retval = []
	if HasColE2(seq):
		retval.append('ColE2')
	if HasR6K(seq):
		retval.append('R6K')
	if HasP15A(seq):
		retval.append('P15A')
	if HaspUC(seq):
		retval.append('pUC')
	return retval
class Strain(object):
	def __init__(self, name="", replication="", resistance="", plasmid=""):
		#pass everything in as a comma separated list
		self.name = name
		self.replication = replication.split(",")
		self.resistance = resistance.split(",") #should include the plasmid resistance!
		if(plasmid != ""):
			self.plasmids = [plasmid] #DNA object
		else:
			self.plasmids = []

# Description: accepts list of dnas and a strain, it should output a list of DNAs that survive the transformation
# this would completely reciplate the TransformPlateMiniprep cycle, it returns all the DNAs present in the cell
def TransformPlateMiniprep(DNAs, strain, selection_antibiotic):
	#strain is an object
	transformed = strain.plasmids
	for dna in DNAs:
		#check if circular, confers new resistance on strain, and doesn't compete with existing plasmid in strain
		if dna.topology == 'circular':
			newR = False
			replicon_ok = False
			no_existing_plasmid = False
			err_msg = ""
			success_msg = ""
			resistances = HasResistance(dna.sequence)
			replicons = HasReplicon(dna.sequence)
			#just need one resistance not already in strain
			for resistance in resistances:
				if not(resistance in strain.resistance):
					newR = True
					success_msg += "Transformation of "+dna.name+" into "+strain.name+" successful -- use "+resistance+" antibiotic selection."
			for replicon in replicons:
				#has the pir/repA necessary for ColE2/R6K?
				if replicon in strain.replication:
					replicon_ok = True
			for replicon in replicons:
				#check if existing plasmid would compete
				existing_plasmids = []
				for p in strain.plasmids:
					existing_plasmids.append( HasReplicon(p.sequence) )
				if not(replicon in existing_plasmids ):
					no_existing_plasmid = True
			if(newR & replicon_ok & no_existing_plasmid):
				parent = dna.clone()
				parent.setChildren((dna, ))
				dna.addParent(parent)
				parent.instructions = 'Transform '+dna.name+' into '+strain.name+', selecting for '+resistance+' resistance.'
				parent.setTimeStep(24)
				parent.addMaterials(['Buffers P1,P2,N3,PB,PE','Miniprep column',resistance[:-1]+' LB agar plates','LB '+resistance[:-1]+' media'])
				transformed.append(dna)	
				print(success_msg)
			else:
				if not(newR):
					print("WARNING: For transformation of "+dna.name+" into "+strain.name+", plasmid either doesn't have an antibiotic resistance or doesn't confer a new one on this strain")
				if not(replicon_ok):
					print("WARNING: For transformation of "+dna.name+" into "+strain.name+", plasmid replicon won't function in this strain")
				if not(no_existing_plasmid):
					print("WARNING: For transformation of "+dna.name+" into "+strain.name+", transformed plasmid replicon competes with existing plasmid in strain")
	if len(transformed)<1:
		print("WARNING: For transformation of "+dna.name+" into "+strain.name+", no DNAs successfully transformed. DNAs may be linear.")
	return transformed
