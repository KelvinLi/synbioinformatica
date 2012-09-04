#!/usr/bin/python -tt -3


######################################################################
### REVIEWER NOTE:                                                 ###
###                   About Reviewer Notes                         ###
###                                                                ###
### Please remove all reviewer notes that I have inserted.         ###
### Those that cannot be resolved immediately should be changed to ###
### "TODO: <message>" comments.                                    ###
###                                                                ###
### To provide response comments, please use "REVIEWER NOTE" as I  ###
### have.                                                          ###
###                                                                ###
######################################################################


import math
import re

# TODO: work on naming scheme
# TODO: add more ORIs
# TODO: assemblytree alignment
# TODO: SOEing
# TODO: (digestion, ligation) redundant products
# TODO: for PCR and Sequencing, renormalize based on LCS
# TODO: tutorials

dna_alphabet = {
'A':'A', 'C':'C', 'G':'G', 'T':'T',
'R':'AG', 'Y':'CT', 'W':'AT', 'S':'CG', 'M':'AC', 'K':'GT',
'H':'ACT', 'B':'CGT', 'V':'ACG', 'D':'AGT', 'N':'ACGT',
'a': 'a', 'c': 'c', 'g': 'g', 't': 't',
'r':'ag', 'y':'ct', 'w':'at', 's':'cg', 'm':'ac', 'k':'gt',
'h':'act', 'b':'cgt', 'v':'acg', 'd':'agt',
'n':'acgt'}

complement_alphabet = {
'A':'T', 'T':'A', 'C':'G', 'G':'C','R':'Y', 'Y':'R',
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

def with_prev(iterable):
    """
    utility function
    list(with_prev(range(4))) --> [(0, 1), (1, 2), (2, 3)]
    """
    hold = ()
    for new in iterable:
        try:
            old = hold[0]
        except IndexError:
            continue
        else:
            yield (old, new)
        finally:
            hold = (new,)

def lreduce(func, iterable):
    """
    like functools.reduce, but reduces on the "left"
    """
    functools.reduce(lambda x,y: func(y,x), iterable)

# Description: converts DNA string to amino acid string
def translate( sequence ):
    """Return the translated protein from 'sequence' assuming +1 reading frame"""
    return ''.join([gencode.get(sequence[3*i:3*i+3],'X') for i in range(len(sequence)//3)])

# Description: read in all enzymes from REase tsv into dict EnzymeDictionary
def EnzymeDictionary():
    EnzymeDictionary = {}
    fh = open('REases.tsv', 'rU')
    for line in fh:
        card = line.rstrip().split('\t')
        card[0] = re.sub(r'\-','_',card[0])
        EnzymeDictionary[card[0]] = restrictionEnzyme(*card)
    return EnzymeDictionary

# Description: Suffix Tree implementation for the purpose of PCR Longest Common Substring identification
# Code adapted from: http://chipsndips.livejournal.com/2005/12/07/
# Define a  for a node in the suffix tree
class SuffixNode(dict):
    def __init__(self):
        self.suffixLink = None # Suffix link as defined by Ukkonen
class LCS:
    def __init__(self,str1,str2):
        # Hack for terimal 3' end matching
        str = str1 + str2 + '#'
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
                        # Original statement was: if j<len(str1)<i and r.depth>self.deepest[0]:
                        # Adapted for PCR by restricting LCS matches to primer terminal 3' end
                        if len(str1)<i and r.depth>self.deepest[0] and j == len(str1) - 1:
                            self.deepest = r.depth, j-1
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
        start, end  = self.deepest[1]-self.deepest[0]+1, self.deepest[1]+1
        return (self.str[start:end],start,end)
    def LCSasRegex(self, currentPrimer, template, fwd):
        annealingRegion = self.str[self.deepest[1] - self.deepest[0] + 1 : self.deepest[1] + 1]
        if not fwd:
            annealingRegion = reverseComplement(annealingRegion)
        (AnnealingMatches, matchCount, MatchIndicesTuple) = ([], 0, ())
        annealingRegex = re.compile(annealingRegion, re.IGNORECASE)
        matchList = annealingRegex.finditer(template)
        for match in matchList:
            if primerTm(match.group()) > 45:
                matchCount += 1
                MatchIndicesTuple = (match.start(), match.end())
        PrimerStub = currentPrimer[0:len(currentPrimer)-len(annealingRegion)-1]
        return (matchCount, MatchIndicesTuple, PrimerStub)

# Description: identifies errors in primer design and raises exceptions based on errors and their context
def PCRErrorHandling(InputTuple):
    (fwd,matchCount,matchedAlready,nextOrientation,currentPrimer,template) = InputTuple
    if len(currentPrimer.sequence) > 7:
        abbrev = currentPrimer.sequence[:3]+'...'+currentPrimer.sequence[-3:]
    else:
        abbrev = currentPrimer.sequence
    if fwd:
        if matchCount > 1:                  # if matches in forward direction more than once
            if nextOrientation == 2:               # ... but was supposed to match in reverse direction
                raise Exception('*Primer error*: primers both anneal in forward (5\'->3\') orientation AND primer '+abbrev+' anneals to multiple sites in template.')
            raise Exception('*Primer error*: primer '+abbrev+' anneals to multiple sites in template.')
        elif matchCount == 1:                # if matches in the forward direction exactly once
            if nextOrientation == 2:               # ... but was supposed to match in reverse direction
                raise Exception('*Primer error*: primers both anneal in forward  (5\'->3\') orientation.')
            matchedAlready = 1
        return matchedAlready
    else:
        if matchCount > 1:                  # if matches in reverse direction more than once
            if matchedAlready == 1:                # ... and already matched in forward direction
                if nextOrientation == 1:               # ... but was supposed to match in forward direction
                    raise Exception('*Primer error*: primers both anneal in reverse (3\'->5\') orientation AND primer '+abbrev+' anneals to multiple sites in template AND primer '+abbrev+' anneals in both orientations.')
                raise Exception('*Primer error*: primer '+abbrev+' anneals to multiple sites in template AND primer '+abbrev+' anneals in both orientations.')
            if nextOrientation == 1: 
                raise Exception('*Primer error*: primers both anneal in reverse (3\'->5\') orientation AND primer '+abbrev+' anneals to multiple sites in template.')
            raise Exception('*Primer error*: primer '+abbrev+' anneals to multiple sites in template.')
        elif matchCount == 1:                 # if matches in the reverse direction exactly once
            if matchedAlready == 1:                # ... and already matched in forward direction
                if nextOrientation == 1:               # ... but was supposed to match in forward direction
                    raise Exception('*Primer error*: both primers have same reverse (3\'->5\') orientation AND primer '+abbrev+' anneals in both orientations.')
                raise Exception('*Primer error*: primer '+abbrev+' primes in both orientations.')
            else:
                matchedAlready = 2
        if matchedAlready == 0:                # if no matches
            raise Exception('*Primer error*: primer '+abbrev+' does not anneal in either orientation.')
        return matchedAlready

def pcrPostProcessing(inputTuple, parent, fwdTM, revTM):
    """
    Assign relationships for PCR inputs and PCR product for assembly
    tree purposes.
    """
    (primer1DNA, primer2DNA, templateDNA) = inputTuple
    for child in inputTuple:
        child.addParent(parent)
    parent_kbp = len(parent.sequence)/1000.
    thermoCycle = str(int(math.ceil(parent_kbp))) + "K" + \
                  str(int(round(max(fwdTM, revTM))))
    parent.setChildren(inputTuple)
    parent.setTimeStep(parent_kbp)
    parent.addMaterials(["Polymerase", "dNTP mix", "Polymerase buffer"])
    parent.instructions = " ".join((thermoCycle,
                                    "PCR template",
                                    templateDNA.name,
                                    "with primers",
                                    primer1DNA.name,
                                    ",",
                                    primer2DNA.name))
    return parent

# Description: PCR() function constructs generalized suffix tree for template and a given primer to identify annealing region,
# and raises PrimerError exceptions for different cases of failed PCR as a result of primer design
# Note: PCR() product is not case preserving
def PCR(primer1DNA, primer2DNA, templateDNA):
    for pcrInput in (primer1DNA, primer2DNA, templateDNA):
        if not isinstance(pcrInput, DNA):
            raise Exception('*PCR error*: PCR function was passed a non-DNA argument.')
            return None
    # Suffix Tree string initialization, non-alphabet character concatenation
    (template, primer_1, primer_2) = (templateDNA.sequence, primer1DNA, primer2DNA)
    # Tuple of assemblyTree 'children', for the purpose of child/parent assignment
    inputTuple = (primer1DNA, primer2DNA, templateDNA)
    # Initialization of all parameters, where indices is the start / stop indices + direction of annealing primer sequences 
    (fwdTM, revTM, indices, counter, rightStub, leftStub, nextOrientation) = (0,0,[0,0,0,0,0,0],0,'','',0)
    try:
        # NOTE: no assumptions made about input primer directionality
        for currentPrimer in (primer_1, primer_2):
            currentSequence = currentPrimer.sequence + '$'
            fwdMatch = LCS(currentSequence.upper(), template.upper())
            (matchCount, forwardMatchIndicesTuple, forwardPrimerStub) = fwdMatch.LCSasRegex(currentSequence, template, 1)
            (matchedAlready, start, stop) = (0,0,0) # Defaults
            # Forward case error handling: delegated to PCRErrorHandling function
            matchedAlready = PCRErrorHandling((1,matchCount,matchedAlready,nextOrientation,currentPrimer,template))
            revMatch = LCS(currentSequence.upper(),reverseComplement(template).upper())
            (matchCount, reverseMatchIndicesTuple, reversePrimerStub) = revMatch.LCSasRegex(currentSequence, template, 0)
            # Reverse case error handling: delegated to PCRErrorHandling function
            matchedAlready = PCRErrorHandling((0,matchCount,matchedAlready,nextOrientation,currentPrimer,template))
            if matchedAlready == 1:
                (indices[counter], indices[counter+1], indices[counter+2]) = (forwardMatchIndicesTuple[0], forwardMatchIndicesTuple[1], 'fwd')
                (counter,nextOrientation,leftStub) = (counter+3, 2, forwardPrimerStub)
            elif matchedAlready == 2:
                (indices[counter], indices[counter+1], indices[counter+2]) = (reverseMatchIndicesTuple[0], reverseMatchIndicesTuple[1], 'rev')
                (counter,nextOrientation,rightStub) = (counter+3, 1, reverseComplement(reversePrimerStub))
        if indices[2] == 'fwd':
            (fwdStart, fwdEnd, revStart, revEnd) = (indices[0], indices[1], indices[3], indices[4])
        else:
            (fwdStart, fwdEnd, revStart, revEnd) = (indices[3], indices[4], indices[0], indices[1])
        (fwdTM, revTM) = (primerTm(template[fwdStart:fwdEnd]), primerTm(template[revStart:revEnd]))    
        if fwdStart < revStart and fwdEnd < revEnd:
            parent = DNA('PCR product','PCR product of '+primer1DNA.name+', '+primer2DNA.name+' on '+templateDNA.name, leftStub+template[fwdStart:revEnd]+rightStub)
        else:
            # circular template is exception to the fwdStart < revStart and fwdEnd < revEnd rule
            if templateDNA.topology == 'circular':  
                parent = DNA('PCR product','PCR product of '+primer1DNA.name+', '+primer2DNA.name+' on '+templateDNA.name, leftStub+template[fwdStart:len(template)-1]+template[:revStart]+rightStub)
            else:
                raise Exception('*PCR Error*: forward primer must anneal upstream of the reverse.')
        return pcrPostProcessing(inputTuple, parent, fwdTM, revTM)
    except:
        raise

# Description: identifies errors in primer design and raises exceptions based on errors and their context
def SequenceErrorHandling(InputTuple):
    (fwd,matchCount,matchedAlready,currentPrimer) = InputTuple
    if len(currentPrimer.sequence) > 7:
        abbrev = currentPrimer.sequence[:3]+'...'+currentPrimer.sequence[-3:]
    else:
        abbrev = currentPrimer.sequence
    if fwd:
        if matchCount > 1:                  # if matches in forward direction more than once
            raise Exception('*Primer error*: primer '+abbrev+' anneals to multiple sites in template.')
        elif matchCount == 1:                # if matches in the forward direction exactly once
            matchedAlready = 1
            return matchedAlready
    else:
        if matchCount > 1:                  # if matches in reverse direction more than once
            if matchedAlready == 1:                # ... and already matched in forward direction
                raise Exception('*Primer error*: primer '+abbrev+' anneals to multiple sites in template AND primer '+abbrev+' anneals in both orientations.')
            raise Exception('*Primer error*: primer '+abbrev+' anneals to multiple sites in template.')
        elif matchCount == 1:                 # if matches in the reverse direction exactly once
            if matchedAlready == 1:                # ... and already matched in forward direction
                raise Exception('*Primer error*: primer '+abbrev+' primes in both orientations.')
            else:
                matchedAlready = 2
        if matchedAlready == 0:                # if no matches
            raise Exception('*Primer error*: primer '+abbrev+' does not anneal in either orientation.')
        return matchedAlready

def Sequence(InputDNA, inputPrimer):
    for seqInput in (InputDNA, inputPrimer):
        if not isinstance(seqInput, DNA):
            raise Exception('*Sequencing error*: Sequence function was passed a non-DNA argument.')
            return None
    # Suffix Tree string initialization, non-alphabet character concatenation
    (template, primer) = (InputDNA.sequence, inputPrimer)
    # Tuple of assemblyTree 'children', for the purpose of child/parent assignment
    # Initialization of all parameters, where indices is the start / stop indices + direction of annealing primer sequences 
    (fwdTM, revTM, indices, counter, rightStub, leftStub, nextOrientation, fwd, rev, read) = (0,0,[0,0,0],0,'','',0,0,0,'')
    try:
        # NOTE: no assumptions made about input primer directionality
        currentSequence = primer.sequence + '$'
        fwdMatch = LCS(currentSequence.upper(), template.upper())
        (matchCount, forwardMatchIndicesTuple, forwardPrimerStub) = fwdMatch.LCSasRegex(currentSequence, template, 1)
        (matchedAlready, start, stop) = (0,0,0) # Defaults
        # Forward case error handling: delegated to SequenceErrorHandling function
        matchedAlready = SequenceErrorHandling((1,matchCount,matchedAlready,primer))
        revMatch = LCS(currentSequence.upper(),reverseComplement(template).upper())
        (matchCount, reverseMatchIndicesTuple, reversePrimerStub) = revMatch.LCSasRegex(currentSequence, template, 0)
        # Reverse case error handling: delegated to SequenceErrorHandling function
        matchedAlready = SequenceErrorHandling((0,matchCount,matchedAlready,primer))
        if matchedAlready == 1:
            (fwdStart, fwdEnd, fwd) = (forwardMatchIndicesTuple[0], forwardMatchIndicesTuple[1], 1)
        elif matchedAlready == 2:
            (revStart, revEnd, rev) = (reverseMatchIndicesTuple[0], reverseMatchIndicesTuple[1], 1)
        if fwd:
            bindingTM = primerTm(template[fwdStart:fwdEnd])
            if InputDNA.DNAclass == 'plasmid':
                if fwdEnd + 1001 > len(template):
                    read = template[fwdEnd+1:] + template[:fwdEnd+1001-len(template)]
                else:
                    read = template[fwdEnd+1:fwdEnd+1001]
            else:
                read = template[fwdEnd+1:fwdEnd+1001]
        else:
            bindingTM = primerTm(template[revStart:revEnd])
            if InputDNA.DNAclass == 'plasmid':
                if revStart - 1001 < 0:
                    read = template[revStart-1001+len(template):] + template[:revStart]
                else:
                    read = template[revStart-1001:revStart]
            else:
                read = template[revStart-1001:revStart]
        if bindingTM >= 55:
            return read
        else:
            return ''
    except:
        raise

# Description: case preserving reverse complementation of nucleotide sequences
def reverseComplement(sequence):
        return "".join([complement_alphabet.get(nucleotide, '') for nucleotide in sequence[::-1]])

# Description: case preserving string reversal
def reverse(sequence):
    return sequence[::-1]

# Description: case preserving complementation of nucleotide sequences
def Complement(sequence):
        return "".join([complement_alphabet.get(nucleotide, '') for nucleotide in sequence[0:]])

### REVIEWER NOTE: I removed usage of Decimal and some int/int division. ###
###                please check whether this is correct ###
# Primer TM function suite: primerTm(), primerTmsimple(), get_55_primer(), nearestNeighborTmNonDegen(), getTerminalCorrectionsDsHash(),
# getTerminalCorrectionsDhHash(), getDsHash(), getDhHash()
# Implemented by Tim Hsaiu in JavaScript, adapted to Python by Nima Emami
# Based on Santa Lucia et. al. papers
def primerTm(sequence):
    if not sequence:
        return 0
    milliMolarSalt = 50.
    milliMolarMagnesium = 1.5
    nanoMolarPrimerTotal = 200.
    molarSalt = milliMolarSalt/10.**3
    molarMagnesium = milliMolarMagnesium/10.**3
    molarPrimerTotal = nanoMolarPrimerTotal/10.**9
    re.sub(r"\s", "", sequence)
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
    ds = 0     # cal/Kelvin/mol
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

# Description: initialize Digest function parameters and checks for acceptable input format
def initDigest(InputDNA, Enzymes):
    # Initialization
    indices = []
    frags = []
    sites = ""
    totalLength = len(InputDNA.sequence)
    enzNames = ""
    incubationTemp = 0.
    nameList = []
    filtered = []

    for enzyme in Enzymes:
        nameList.append(enzyme.name)
        enzNames = enzNames+enzyme.name+', '
        incubationTemp = max(incubationTemp, enzyme.incubate_temp)
    enzNames = enzNames[:-2]
    if len(Enzymes) > 2:
        raise Exception('*Digest error*: only double or single digests allowed (provided enzymes were '+enzNames+')')
    if InputDNA.topology == "linear":  
        # Initialize indices array with start and end indices of the linear fragment
        # Add dummy REase to avoid null pointers
        dummy = restrictionEnzyme(name="dummy", buffer1="", buffer2="",
                                  buffer3="", buffer4="", bufferecori="",
                                  heatinact=0, incubatetemp=0.,
                                  recognitionsite="(0/0)", distance="")
        indices = [(0,0,'',dummy), (totalLength,0,'',dummy)]
    return (indices, frags, sites, totalLength, enzNames, incubationTemp, nameList, filtered)

def restrictionSearch(Enzymes, InputDNA, indices, totalLength):
    """
    Finds restriction sites for given Enzymes in given InputDNA molecule
    """
    for enzyme in Enzymes:
        sites = enzyme.find_sites(InputDNA)
        for site in sites:
            # WARNING: end proximity for linear fragments exception
            if (InputDNA.topology == "linear" and
                int(site[0]) < int(enzyme.endDistance) or
                int(site[1]) + int(enzyme.endDistance) > totalLength):
                print("\n*Digest Warning*: end proximity for "+enzyme.name+
                      " restriction site at indices "+
                      str(site[0]%totalLength)+","+str(site[1]%totalLength)+
                      " for input "+InputDNA.name+
                      " (length "+str(totalLength)+")\n")
                if (InputDNA.topology == 'linear' and
                    site[2] == 'antisense' and
                    site[1] < max(enzyme.bottom_strand_offset,
                                  enzyme.top_strand_offset)):
                    print("\n*Digest Warning*: restriction cut site for "+
                          enzyme.name+" with recognition indices "+
                          str(site[0]%totalLength)+","+
                          str(site[1]%totalLength)+
                          " out of bounds for input "+InputDNA.name+
                          " (length "+str(totalLength)+")\n")
            # WARNING: restriction index out of bounds exception
            elif (InputDNA.topology == "linear" and
                  site[2] == "antisense" and
                  site[1] < max(enzyme.bottom_strand_offset,
                                enzyme.top_strand_offset)):
                print("\n*Digest Warning*: restriction cut site for "+
                      enzyme.name+" with recognition indices "+
                      str(site[0]%totalLength)+","+str(site[1]%totalLength)+
                      " out of bounds for input "+InputDNA.name+
                      " (length "+str(totalLength)+")\n")
            else: 
                site = site + (enzyme,)
                indices.append(site)
        indices.sort()
    return indices

def filterSites(filtered, indices):
    """
    If you have overlapping restriction sites, choose the first one and discard the second
    TODO: revise this?
    """
    siteCounter = 0
    while siteCounter < len(indices):
        try:
            (currentTuple, nextTuple) = (indices[n], indices[n+1])
            (currentStart, nextStart, currentEnzyme, nextEnzyme) = (currentTuple[0], nextTuple[0], currentTuple[3], nextTuple[3])
            filtered.append(indices[siteCounter])
            if currentStart + len(currentEnzyme.alpha_only_site) >= nextStart:
                currentIndex = indices[siteCounter+1]
                if currentIndex[0] == len(InputDNA.sequence):
                    pass
                else:
                    raise Exception('Digest Error*: overlapping restriction sites '+currentTuple[3].name+' (indices '+str(currentTuple[0])+','+str(currentTuple[1])+') and '+nextTuple[3].name+' (indices '+str(nextTuple[0])+','+str(nextTuple[1])+')')
                    siteCounter += 1
            siteCounter += 1
        except:    # got to end of list
            filtered.append(indices[siteCounter])
            siteCounter += 1
    return filtered

# Description: determines digest start and stop indices, as well as overhang indices for left and right restriction
def digestIndices(direction, nextDirection, currentEnzyme, nextEnzyme, currentStart, nextStart, totalLength):
    # CT(B)O = current top (bottom) overhang, AL(R)L = add left (right) length, NT(B)O = next top (bottom) overhang
    (ALL, ARL) = (0,0)
    # If it's on the sense strand, then overhang is positive
    if direction == "sense":
        (CTO, CBO) = (currentEnzyme.top_strand_offset, currentEnzyme.bottom_strand_offset)
    # If it's on the antisense strand, then you have to go back towards the 5' to generate the overhang (so multiply by -1)
    else:
        (CTO, CBO) = (-1 * currentEnzyme.top_strand_offset, -1 * currentEnzyme.bottom_strand_offset)
    ALL = max(CTO,CBO)
    if nextDirection == "sense":
        (NTO, NBO) = (nextEnzyme.top_strand_offset, nextEnzyme.bottom_strand_offset)
        ARL = min(NTO,NBO)
    else:
        (NTO, NBO) = (-1 * nextEnzyme.top_strand_offset + 1, -1 * nextEnzyme.bottom_strand_offset + 1)
        ARL = min(NTO,NBO)-1
    (currentStart, digEnd) = ((currentStart+ALL) % totalLength, nextStart + ARL)
    if currentEnzyme.reach and direction == "sense":
        currentStart = currentStart + len(currentEnzyme.alpha_only_site)
    if nextEnzyme.reach and nextDirection == "sense":
        digEnd = digEnd + len(nextEnzyme.alpha_only_site)
    return (currentStart, digEnd, CTO, CBO, NTO, NBO)

# Description: instantiates Overhang object as the TLO or BLO field of a digested DNA molecule object
def setLeftOverhang(digested, CTO, CBO, direction, currentStart, currentEnzyme, InputDNA):
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
    return digested

# Description: instantiates Overhang object as the TRO or BRO field of a digested DNA molecule object
def setRightOverhang(digested, NTO, NBO, direction, digEnd, nextEnzyme, InputDNA, totalLength):
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
    return digested

# Description: take digest fragments before they're output, and sets assemblytree relationships and fields,
#         as well as digest buffer
def digestPostProcessing(frag, InputDNA, nameList, enzNames, incubationTemp):
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
    frag.instructions = " ".join(("Digest (" + InputDNA.name + ") with",
                                  enzNames, "at", str(incubationTemp) + "C in",
                                  bestBuffer, "for 1 hour."))
    return frag

# Description: takes in InputDNA molecule and list of EnzymeDictionary elements, outputting a list of digest products
def Digest(InputDNA, Enzymes):
    # Initialization
    if not isinstance(InputDNA, DNA):
        raise Exception('*Digest Error*: Digest function passed empty list of DNA arguments. Returning empty list of products.')
        return []
    (indices, frags, sites, totalLength, enzNames, incubationTemp, nameList, filtered) = initDigest(InputDNA, Enzymes)
    # Identify restriction sites, fill in indices array
    indices = restrictionSearch(Enzymes, InputDNA, indices, totalLength)
    # If you have overlapping restriction sites, choose the first one and discard they second 
    indices = filterSites(filtered, indices)
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
        # Update start value currentStart and apply ( mod length ) to deal with edge cases
            # Also, update end value digEnd for fragment indices
        (currentStart, digEnd, CTO, CBO, NTO, NBO) = digestIndices(direction, nextDirection, currentEnzyme, nextEnzyme, currentStart, nextStart, totalLength)
        # Loop around fragment case for circular InputDNA's
        if digEnd > 0 and currentStart > 0 and digEnd < currentStart and InputDNA.topology == 'circular':
            if n == -1:
                digested = DNA('digest','Digest of '+InputDNA.name+' with '+enzNames,InputDNA.sequence[currentStart:]+InputDNA.sequence[:digEnd])
            else:
                raise Exception('Digest Error*: restriction sites for '+currentTuple[3].name+' ('+str(currentTuple[0])+','+str(currentTuple[1])+') and '+nextTuple[3].name+' ('+str(nextTuple[0])+','+str(nextTuple[1])+') contain mutually interfering overhangs -- fragment discarded.')
                continue
        else:
            digested = DNA('digest','Digest of '+InputDNA.name+' with '+enzNames,InputDNA.sequence[currentStart:digEnd])
        # Discard small fragments
        if len(digested.sequence) < 4:
            pass
        else:
            # Adjust top and bottom overhang values based on the orientation of the restriction site
            digested = setLeftOverhang(digested, CTO, CBO, direction, currentStart, currentEnzyme, InputDNA)
            digested = setRightOverhang(digested, NTO, NBO, direction, digEnd, nextEnzyme, InputDNA, totalLength)
            frags.append(digested)
    for frag in frags:
        frag = digestPostProcessing(frag, InputDNA, nameList, enzNames, incubationTemp)
    return frags

class Overhang(object):
    def __init__(self, seq=""):
        self.sequence = seq

class DNA(object):
    #for linear DNAs, this string should include the entire sequence (5' and 3' overhangs included
    def __init__(self, DNAclass="", name="", seq=""):
        self.sequence = seq
        self.length = len(seq)
        notDNA = re.compile('([^gatcrymkswhbvdn])')
        isnotDNA = False
        exceptionText = "" 
        for m in notDNA.finditer(self.sequence.lower()):
            exceptionText += m.group() + " at position "+ str( m.start()) + " is not valid IUPAC DNA. "
            isnotDNA = True
        if(isnotDNA):
            raise Exception(exceptionText)
        self.name = name   #would be pbca1256 for vectors or pbca1256-Bth8199 for plasmids
        # self.description = "SpecR pUC"               #this is for humans to read
        self.dam_methylated = True
        self.topLeftOverhang = Overhang('')
        self.bottomLeftOverhang = Overhang('')
        self.topRightOverhang = Overhang('')
        self.bottomRightOverhang = Overhang('')
        self.pnkTreated = False
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
    def phosphorylate(self):
        self.pnkTreated = True
    def setTimeStep(self, timeStep):
        self.timeStep = timeStep
    def setChildren(self, inputDNAs):
        self.children = inputDNAs
    def find(self, string):
        return 0
    def isEqual(self, other):
        # TODO: implement plasmid rotation to allow circular alignment
        if self.DNAclass == 'plasmid' and other.DNAclass == 'plasmid':
            if self.sequence.lower() == other.sequence.lower():
                return True
        else:
            if self.sequence.lower() == other.sequence.lower() and self.overhangsEqual(other):
                return True
        return False
    def overhangsEqual(self, other):
        if self.bottomLeftOverhang.sequence.lower() == other.bottomLeftOverhang.sequence.lower() and \
              self.topLeftOverhang.sequence.lower() == other.topLeftOverhang.sequence.lower() and \
              self.bottomRightOverhang.sequence.lower() == other.bottomRightOverhang.sequence.lower() and \
              self.topRightOverhang.sequence.lower() == other.topRightOverhang.sequence.lower():
              return True
        return False
    def clone(self):
        clone = DNA(self.DNAclass, self.name, self.sequence)
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
            trExtra = self.topRightOverhang.sequence if TR else ""
            brExtra = self.bottomRightOverhang.sequence if BR else ""
            if len(self.sequence) > 8:
                print("\t"+self.topLeftOverhang.sequence+
                      " "*len(self.bottomLeftOverhang.sequence)+
                      self.sequence[:4]+"."*3+
                      "["+str(len(self.sequence)-8)+"bp]"+
                      "."*3+self.sequence[-4:]+trExtra)
                print("\t"+" "*len(self.topLeftOverhang.sequence)+
                      '|'*4+' '*(10+len(str(len(self.sequence)-8)))+'|'*4)
                print("\t"+" "*len(self.topLeftOverhang.sequence)+
                      self.bottomLeftOverhang.sequence+
                      Complement(self.sequence[:4])+
                      "."*(10 + len(str(len(self.sequence)-8)))+
                      Complement(self.sequence[-4:])+brExtra)
            else:
                print("\t"+self.topLeftOverhang.sequence+
                      " "*len(self.bottomLeftOverhang.sequence)+self.sequence+
                      trExtra)
                print("\t"+" "*len(self.topLeftOverhang.sequence)+
                      "|"*len(self.sequence))
                print("\t"+" "*len(self.topLeftOverhang.sequence)+
                      self.bottomLeftOverhang.sequence+
                      Complement(self.sequence)+brExtra)
        else:
            if len(self.sequence) > 8:
                print("\t"+self.sequence[:4]+
                      "."*3+"["+str(len(self.sequence)-8)+"bp]"+
                      "."*3+self.sequence[-4:])
                print("\t"+"|"*4+
                      " "*(10+len(str(len(self.sequence)-8)))+"|"*4)
                print("\t"+Complement(self.sequence[:4])+
                      "."*(10+len(str(len(self.sequence)-8)))+
                      Complement(self.sequence[-4:]))
            else:
                print("\t"+self.sequence)
                print("\t"+"|"*len(self.sequence))
                print("\t"+Complement(self.sequence))
        return 0

def BaseExpand(base):
    """
    BaseExpand(base) -> string.
    Given a degenerated base, return its meaning in IUPAC alphabet.
    e.g.:
            b= 'A' -> 'A'
            b= 'N' -> 'ACGT'
            etc...

    ### REVIEWER NOTE: is this comment in the right spot? ###
    for regex generation, taken from BioPython
    """
    base = base.upper()
    return dna_alphabet[base]

def regex(site):
    """
    regex(site) -> string.
    Construct a regular expression from a DNA sequence.
    e.g.:
        site = 'ABCGN' -> 'A[CGT]CG.'

    ### REVIEWER NOTE: is this comment in the right spot? ###
    function to convert recog site into regex, from Biopython
    """
    reg_ex = site
    for base in reg_ex:
        ### REVIEWER NOTE: is this if statement needed? ###
        #if base in ('A', 'T', 'C', 'G', 'a', 'c', 'g', 't'):
        #    pass
        if base in {'N', 'n'}:
            reg_ex = '.'.join(reg_ex.split('N'))
            reg_ex = '.'.join(reg_ex.split('n'))
        if base in {'R', 'Y', 'W', 'M', 'S', 'K', 'H', 'D', 'B', 'V'}:
            expand = '['+ str(BaseExpand(base))+']'
            reg_ex = expand.join(reg_ex.split(base))
    return reg_ex

def ToRegex(site, name):
    """
    ToRegex() function to convert recog site into regex, from Biopython
    """
    sense = ''.join(['(?P<', name, '>', regex(site.upper()), ')'])
    antisense = ''.join(['(?P<', name, '_as>', regex( reverseComplement( site.upper() )), ')'])
    rg = sense + '|' + antisense
    return rg  

class restrictionEnzyme(object):
    """
    restrictionEnzyme class encapsulates information about buffers, overhangs, incubation / inactivation, end distance, etc.
    """
    def __init__(self, name="", buffer1="", buffer2="", buffer3="", buffer4="",
                 bufferecori="", heatinact="", incubatetemp=0.,
                 recognitionsite="", distance=""):
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
                self.bottom_strand_offset = (len(recognitionsite) - 1 -
                                             self.top_strand_offset)
  
    def prettyPrint(self):
        print("Name: " + self.name +
              " Recognition Site: " + self.recognition_site)

    def find_sites(self, DNA):
        seq = DNA.sequence
        (fwd, rev) = self.compsite.split('|')
        fwd_rease_re = re.compile(fwd)
        rev_rease_re = re.compile(rev)
        indices = []
        seen = {}
        searchSequence = seq.upper()
        if DNA.topology == "circular":
            searchSequence += seq[:len(self.recognition_site)-2]
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
            ### REVIEWER NOTE: what sort of exception do you expect? ###
            except:
                span = span + ('antisense',)
                indices.append(span)
        return indices

def TreatPNK(inputDNAs):
    """
    phosphorylates 5' end of DNA molecule, allowing blunt end ligation
    see http://openwetware.org/wiki/PNK_Treatment_of_DNA_Ends
    """
    for inputDNA in inputDNAs:
        inputDNA.phosphorylate()
    return inputDNAs

def DigestBuffer(*str_or_list):
    """
    Find the optimal digestBuffer
    return format will be list, [rec_buff, [buff1_act, buff2_act...buff4_Act]]

    TODO: If Buffer 2 > 150, return Buffer 2 and list of activity values, else, return buffer 1, 3, or 4 (ignore EcoRI)
    """
    best_buff = ""
    best_buff_score = 5*[0]
    enzdic = EnzymeDictionary()
    num_enz = 0
    for e in str_or_list:
        enz = enzdic[e]
        best_buff_score = list(x + int(y) for x, y in
                               zip(best_buff_score, enz.buffer_activity))
        num_enz += 1
    ret = []  
    if best_buff_score[1] > (75 * num_enz):
        ret.append(2)
        ret.append(best_buff_score)
    else:
        m = max(best_buff_score)
        p = best_buff_score.index(m)
        ret.append(p)
        ret.append(best_buff_score)
    return ret

def SOERoundTwo(primer1, primer2, templates):
    """
    accepts two primers and list of input template DNAs

    TODO: implement this with PCR!
    """
    return 0

def SOE(list_of_primers, templates):
    """
    Assumes primers are in the right order:
        outer, inner_rev, inner_fwd, outer

    call two pcrs with list[0], [1] and list[2], [3]
    """
    return 0

def Primers(product, template):
    return rPrimers(product, template, 0)

def rPrimers(product, template, baseCase):
    """
    Annealing region design criteria:
    TODO: incorporate these somehow
    In general, the 3' base of your oligos should be a G or C.

    The overall G/C content of your annealing region should be between
    50 and 65%.

    The overall base composition of the sequences should be balanced (no
    missing bases, no excesses of one particular base).

    The length of your sequence can be modified to be around 18 and 25 bp.

    The sequence should appear random. There shouldn't be long stretches
    of a single base, or large regions of G/C rich sequence and all A/T
    in other regions.

    There should be little secondary structure. Ideally, the Tm for the
    oligo should be under 40 degrees.
    """
    try:
        # Die after 2 rounds of recursion
        if baseCase == 2:
            return ()
        # Compute "forward" and "backwards" LCS (i.e. on both sides of a mutation)
        fwdMatch = LCS(template.sequence.upper()+"$", product.sequence.upper())
        (fwdMatchCount, forwardMatchIndicesTuple,
         forwardPrimerStub) = fwdMatch.LCSasRegex(template.sequence.upper()+"$",
                                                  product.sequence.upper(), 1)


        revMatch = LCS(reverse(template.sequence.upper())+"$",
                               reverse(product.sequence.upper()))
        (revMatchCount, reverseMatchIndicesTuple,
         revPrimerStub) = revMatch.LCSasRegex(reverse(template.sequence.upper())+"$",
                                              reverse(product.sequence.upper()), 1)
        fFlag = False
        if not len(forwardMatchIndicesTuple):
            fMI = (len(product.sequence), len(product.sequence))
            fFlag = True
        else:
            fMI = forwardMatchIndicesTuple
        if not len(reverseMatchIndicesTuple):
            if fFlag:
                # neither side matches
                ### REVIEWER NOTE: This exception is caught later, so this message is completely invisible ###
                raise Exception('For primer design, no detectable homology on terminal ends of product and template sequences.')
            rMI = (0, 0)
        else:
            rMI = (0 , len(product.sequence) - reverseMatchIndicesTuple[0])
        # wrap around mutation case
        if not fMI[0] > rMI[1]:
            diffLen = fMI[0] + len(product.sequence) - rMI[1]
            insert = product.sequence[rMI[1]:] + product.sequence[:fMI[0]]
        else:
            diffLen = fMI[0] - rMI[1]
            insert = product.sequence[rMI[1]:fMI[0]]
        if 60 < diffLen <= 100:
            primers = DesignWobble(product, insert, (rMI[1], fMI[0]))
        elif 1 <= diffLen <= 60:
            primers = DesignEIPCR(product, insert, (rMI[1], fMI[0]))
        # test the PCR --> will return an exception if they don't anneal
        amplifies = PCR(primers[0], primers[1], template)
        # if it amplifies up ok, then return the primers
        return primers
    # may be misaligned ==> realign and recurse


    ### REVIEWER NOTE: uh, regarding this try-except statement... ###
    except:
        baseCase += 1
        # If you had an LCS on the fwd direction, re-align using that one
        if fwdMatchCount:
            myLCS = product.sequence[forwardMatchIndicesTuple[0]:forwardMatchIndicesTuple[1]]
            newProduct = DNA("plasmid", product.name,
                             product.sequence[forwardMatchIndicesTuple[0]:] +
                             product.sequence[:forwardMatchIndicesTuple[0]])
            match = re.search(myLCS.upper(), template.sequence.upper())
            if match:
                startSite = match.start()
                newTemplate = DNA("plasmid", template.name,
                                  template.sequence[startSite:]+
                                  template.sequence[:startSite])
            else:
                return ()  
        # If you had an LCS in the rev direction, re-align using that one
        elif revMatchCount:
            myLCS = reverse(reverse(product.sequence)[reverseMatchIndicesTuple[0]:reverseMatchIndicesTuple[1]])
            myMatch = re.search(myLCS.upper(), product.sequence.upper())
            startIndex = myMatch.start()
            newProduct = DNA("plasmid", product.name,
                             product.sequence[startIndex:] +
                             product.sequence[:startIndex])
            match = re.search(myLCS.upper(), template.sequence.upper())
            if match:
                startSite = match.start()
                newTemplate = DNA("plasmid", template.name,
                                  template.sequence[startSite:]+
                                  template.sequence[:startSite])
            else:
                return ()
        else:
            return ()
        return rPrimers(newProduct, newTemplate, baseCase)

def getAnnealingRegion(template, fwd):
    if len(template) <= 10:
        return ''
    if not fwd:
        template = reverseComplement(template)
    for i in range(len(template)):
        currentRegion = template[:i]
        if primerTm(currentRegion) >= 60:
            break
    return currentRegion

def DesignEIPCR(product, insert, diffTuple):
    """
    Given a parent plasmid and a desired product plasmid, design the eipcr primers
    use difflib to figure out where the differences are
    if there is a convenient restriction site in or near the modification, use that
     otherwise, check if there exists bseRI or bsaI sites, and design primers using those
     print/return warning if can't do this via eipcr (insert span too long)
    """
    # use 60 bp to right of mutation as domain for annealing region design
    (fwdStart, fwdEnd) = (diffTuple[1], diffTuple[1]+60)
    # accounting for the wrap around case
    if fwdEnd > len(product.sequence):
        fwdEnd = fwdEnd % len(product.sequence)
        fwdAnneal = getAnnealingRegion(product.sequence[fwdStart:] + product.sequence[:fwdEnd], 1)
    else:
        fwdAnneal = getAnnealingRegion(product.sequence[fwdStart:fwdEnd], 1)
    # same with the 60 bp to the left of the mutation
    (revStart, revEnd) = (diffTuple[0]-60, diffTuple[0])
    if revStart < 0:
        revAnneal = getAnnealingRegion(product.sequence[revStart:] + product.sequence[:revEnd], 0)
    else:
        revAnneal = getAnnealingRegion(product.sequence[revStart:revEnd], 0)
    # use BsaI 'taaGGTCTCx1234' to do reachover digest and ligation
    tail = "taaaGGTCTCA"
    # wrap around case
    if not diffTuple[1] > diffTuple[0]:
        half = ((diffTuple[1] + len(product.sequence) - diffTuple[0]) / 2) + diffTuple[0]
    else:
        half = ((diffTuple[1] - diffTuple[0]) / 2) + diffTuple[0]
    # the 4 bp in the overhang must not contain any N's --> otherwise, ligation won't work
    overhang = product.sequence[half - 2 : half + 2]
    while 'N' in overhang.upper():
            half = half + 1
            overhang = product.sequence[half - 2 : half + 2]
    product.sequence[half - 2 : diffTuple[1] + 1]
    # Accounting for the == 0 case, which would otherwise send the mutagenic region to ''
    if diffTuple[1] == 0:
        fwdPrimer = DNA("primer", "fwd EIPCR "+product.name,
                        tail + product.sequence[half - 2 :] + fwdAnneal)
    else:
        fwdPrimer = DNA("primer", "fwd EIPCR "+product.name,
                        tail + product.sequence[half-2 : diffTuple[1]] +
                        fwdAnneal)
    if half + 2 == 0:
        revPrimer = DNA("primer", "rev EIPCR "+product.name,
                        tail +
                        reverseComplement(product.sequence[diffTuple[0]:]) +
                        revAnneal)
    else:  
        revPrimer = DNA("primer", "rev EIPCR "+product.name,
                        tail +
                        reverseComplement(product.sequence[diffTuple[0] : half+2]) +
                        revAnneal)
    return fwdPrimer, revPrimer

# TODO: Implement this, along with restriction site checking?
def DesignWobble(parent, product):
    return 0

### REVIEWER NOTE: please double-check this re-write of the "Distinguish*" functions ###
def DistinguishDNABands(dna_list):
    """
    Return True if every DNA band is distinguishable.

    For a standard 1-2% agarose gel, we can distinguish a and b if do
    the following in wolframalpha:
        LogLogPlot[|a - b| > (0.208*a+42), {a, 0, 9000}, {b, 0, 9000}]
    """
    sorted_list = sorted(dna_list, key=lambda dna:dna.length)
    iter = map(len, with_prev(sorted_list))
    return all(b - a > 0.208 * b + 42 for a, b in iter)

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
    seqs = (frag.topLeftOverhang.sequence,
            frag.topRightOverhang.sequence,
            frag.bottomLeftOverhang.sequence,
            frag.bottomRightOverhang.sequence)
    return tuple(lreduce(map, (seqs, bool, int)))

def ligatePostProcessing(ligated, childrenTuple, message):
    ligated.setChildren(childrenTuple)
    for child in childrenTuple:
        child.addParent(ligated)
    ligated.setTimeStep(0.5)
    ligated.addMaterials(['DNA Ligase','DNA Ligase Buffer','ddH20'])
    ligated.instructions = message
    return ligated

def isComplementary(seq1, seq2):
    if not seq1 or not seq2: # if one of them is empty
        return False
    else:
        return seq1 == Complement(seq2)

def isReverseComplementary(seq1, seq2):
    if not seq1 or not seq2:
        return False
    else:
        return seq1 == reverseComplement(seq2)

# Description: Ligate() function accepts a list of DNA() digest objects, and outputs list of DNA
def Ligate(inputDNAs):
    products = []
    # self ligation
    for fragment in inputDNAs:
        if not isinstance(fragment, DNA):
            print("\n*Ligate Error*: Ligate function was passed a non-DNA "
                  "argument. Argument discarded.\n")
            continue
        (TL,TR,BL,BR) = SetFlags(fragment)
        if fragment.DNAclass == 'plasmid':
            print("\n*Ligate Warning*: for ligation reaction, invalid input "
                  "molecule removed -- ligation input DNA objects must be of "
                  "class \"digest\" or be PNK treated linear molecules.\n")
        elif TL+TR+BL+BR == 1:
            pass
        elif TL+TR+BL+BR == 0:
            # blunt end self ligation case --> need to identify that both sides were digested (i.e. both ecoRV blunt ends)
            # and then return circular product of same sequence.
            pass
        elif fragment.topLeftOverhang.sequence:
            if isComplementary(fragment.topLeftOverhang.sequence.lower(), fragment.bottomRightOverhang.sequence.lower()):
                ligated = DNA('plasmid',fragment.name+' self-ligation',fragment.topLeftOverhang.sequence+fragment.sequence)
                products.append(ligatePostProcessing(ligated, (fragment, ), 'Self-ligate ('+fragment.name+') with DNA ligase for 30 minutes at room-temperature.'))
        elif fragment.bottomLeftOverhang.sequence:
            if isComplementary(fragment.topLeftOverhang.sequence.lower(), fragment.topRightOverhang.sequence.lower()):
                ligated = DNA('plasmid',fragment.name+' self-ligation',fragment.sequence+fragment.topRightOverhang.sequence)
                products.append(ligatePostProcessing(ligated, (fragment, ), 'Self-ligate ('+fragment.name+') with DNA ligase for 30 minutes at room-temperature.'))
    if len(products) > 0 or len(inputDNAs) == 1:
        return products
    i = 0
    while i < len(inputDNAs):
        fragOne = inputDNAs[i]
        if not isinstance(fragOne, DNA):
            print("\n*Ligate Warning*: Ligate function was passed a non-DNA "
                  "argument. Argument discarded.\n")
            i += 1
            continue
        elif fragOne.DNAclass == 'plasmid':
            i += 1
            continue
        j = i + 1
        while j < len(inputDNAs):
            fragTwo = inputDNAs[j]
            if not isinstance(fragOne, DNA) or not isinstance(fragTwo, DNA):
                j += 1
                continue
            elif fragTwo.DNAclass == 'plasmid':
                j += 1            
                continue                
            (LTL,LTR,LBL,LBR) = SetFlags(fragOne)
            (RTL,RTR,RBL,RBR) = SetFlags(fragTwo)
            # first3 is the number of 3' overhangs for the left fragment, and so on for the other three classifiers
            (first3, first5, second3, second5) = (LTR + LBL, LBR + LTL, RTR + RBL, RBR + RTL)
            # blunt end ligation:
            firstFlag = first3 + first5
            secondFlag = second3 + second5
            if fragOne.pnkTreated and fragTwo.pnkTreated and firstFlag <= 1 and secondFlag <= 1:
                if not firstFlag and secondFlag or firstFlag and not secondFlag:
                    pass
                elif not firstFlag and not secondFlag:
                    ligated = DNA('plasmid', fragOne.name+', '+fragTwo.name+' ligation product', fragOne.sequence + fragTwo.sequence)
                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                elif firstFlag and secondFlag:
                    if first3 and second3:
                        if isComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        if isComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragTwo.sequence+fragTwo.topRightOverhang.sequence+fragOne.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        if isReverseComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence))
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        if isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',reverseComplement(fragTwo.sequence)+reverse(fragTwo.bottomLeftOverhang.sequence)+fragOne.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    else:
                        if isComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragTwo.sequence+fragOne.topLeftOverhang.sequence+fragOne.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        if isComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        if isReverseComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',reverseComplement(fragTwo.sequence)+fragOne.topLeftOverhang.sequence+fragOne.sequence)    
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))  
                        if isReverseComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+Complement(fragOne.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))    
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
            # non-blunt ligation: 
            else:
                if first3 == 2:
                    if isComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                        if isComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence+fragTwo.topRightOverhang.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    if isReverseComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                        if isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence)+reverse(fragTwo.bottomLeftOverhang.sequence))
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                elif first3 == 1:
                    if LTR:
                        # then you know it must have LTL
                        if RTR:
                            # then, if it is to ligate, it must have compatible RTL
                            if isReverseComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                                if isReverseComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                                    ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence))
                                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        else:
                            # to ligate, it must have RBL and RBR
                            if isComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                                if isComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                                    ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence)
                                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    else:
                        # you know it has LBL as its 3 and LBR as its 5
                        if RTR:
                        # then, if it is to ligate, it must have compatible RTL
                            if isComplementary(fragTwo.topRightOverhang.sequence.upper(), fragOne.bottomLeftOverhang.sequence.upper()):
                                if isComplementary(fragTwo.topLeftOverhang.sequence.upper(), fragOne.bottomRightOverhang.sequence.upper()):
                                    ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence+fragTwo.topRightOverhang.sequence)
                                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        else:
                            # to ligate, it must have RBL and RBR
                            if isReverseComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                                if isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                                    ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',Complement(fragOne.bottomLeftOverhang.sequence)+fragOne.sequence+Complement(fragOne.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))
                                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                else:
                    if isComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                        if isComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    if isReverseComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                        if isReverseComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+reverse(fragTwo.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))    
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
            j += 1
        i += 1
    if len(products) == 0:
        raise Exception('*Ligate Error*: ligation resulted in zero products.')  
    return products

# Description: fragment processing function for zymo, short fragment and gel cleanups
def cleanupPostProcessing(band, source):
    parentBand = band.clone()
    parentBand.setChildren((band,))
    band.addParent(parentBand)
    timeStep = 0.5
    cleanupMaterials = ['Zymo Column','Buffer PE','ddH20']
    if source == 'short fragment':
        cleanupMaterials.append('Ethanol / Isopropanol')
    elif source == 'gel extraction and short fragment':
        cleanupMaterials += ['Buffer ADB', 'Ethanol / Isopropanol']
        timeStep = 1
    elif source == 'gel extraction and zymo':
        cleanupMaterials.append('Buffer ADB')
        timeStep = 1
    parentBand.setTimeStep(timeStep)
    parentBand.addMaterials(cleanupMaterials)
    parentBand.instructions = 'Perform '+source+' cleanup on ('+band.name+').'
    return parentBand

# Description: ZymoPurify() function takes a list of DNA objects and filters out < 300 bp DNA's
def ZymoPurify(inputDNAs):
    counter = 0
    for zymoInput in inputDNAs:
        if not isinstance(zymoInput, DNA):
            print("\n*Zymo Warning*: Zymo purification function was passed a "
                  "non-DNA argument. Argument discarded.\n")
            inputDNAs.pop(counter)
        else:
            counter += 1
    if not inputDNAs:
        raise Exception("*Zymo Error*: Zymo purification function passed empty input list.")
        return inputDNAs
    (outputBands, sizeTuples) = ([], [])
    for DNA in inputDNAs:
        sizeTuples.append((len(DNA.sequence), DNA))
    sizeTuples.sort(key=lambda x: x[0], reverse=True)
    currentTuple = sizeTuples[0]
    currentSize = currentTuple[0]
    while currentSize > 300:
        band = currentTuple[1]
        outputBands.append(cleanupPostProcessing(band,'standard zymo'))
        if sizeTuples:
            sizeTuples.pop(0)
            currentTuple = sizeTuples[0]
            currentSize = currentTuple[0]
        else:
            break
    return outputBands

# Description: ShortFragmentCleanup() function takes a list of DNA objects and filters out < 50 bp DNA's
def ShortFragmentCleanup(inputDNAs):
    if len(inputDNAs) == 0:
        raise Exception("*Short Fragment Cleanup Error*: short fragment "
                        "cleanup function passed empty input list.")
        return inputDNAs
    outputBands = []
    sizeTuples = []
    for DNA in inputDNAs:
        fragSize = len(DNA.sequence)
        sizeTuples.append((fragSize,DNA))
    sizeTuples.sort(key=lambda x: x[0], reverse=True)
    currentTuple = sizeTuples[0]
    currentSize = currentTuple[0]
    while currentSize > 50 and len(sizeTuples) > 1:
        band = currentTuple[1]
        outputBands.append(cleanupPostProcessing(band,'short fragment'))
        sizeTuples.pop(0)
        currentTuple = sizeTuples[0]
        currentSize = currentTuple[0]
    if currentSize > 50:
        band = currentTuple[1]
        outputBands.append(cleanupPostProcessing(band,'short fragment'))
    return outputBands

# Description: GelAndZymoPurify() function employs a user-specified purification strategy to cut out a range of band sizes, and
# then filters out < 300 bp DNA's. If 50 bp < [ ] < 300 bp DNAs are detected, switches to short fragment cleanup mode.
def GelAndZymoPurify(inputDNAs, strategy):
    # sort based on size
    if len(inputDNAs) == 0:
        raise Exception('*Gel Purification Error*: gel purification with strategy \'"+strategy+"\' passed empty input list.')
        return inputDNAs
    elif len(inputDNAs) == 1:
        return inputDNAs
    (shortFlag, lostFlag, interBands, outputBands, sizeTuples) = (False, False, [], [], [])
    for DNA in inputDNAs:
        sizeTuples.append((len(DNA.sequence),DNA))
    if isinstance( strategy, str):
        if strategy == 'L':
            sizeTuples.sort(key=lambda x: x[0], reverse=True)
            n = 0
            currentTuple = sizeTuples[n]
            largestSize = currentTuple[n]
            currentSize = largestSize
            while currentSize > largestSize * 5/6 and n < len(sizeTuples) - 1:
                interBands.append(currentTuple[1])
                n += 1
                currentTuple = sizeTuples[n]
                currentSize = currentTuple[0]
            if currentSize > largestSize * 5/6: ### REVIEWER NOTE: int/int division ###
                if currentSize < 50:
                    lostFlag = True
                elif currentSize < 300:
                    shortFlag = True
                interBands.append(currentTuple[1])
            if len(interBands) > 1:
                print("\n*Gel Purification Warning*: large fragment "
                      "purification resulted in purification of multiple, "
                      "possibly unintended distinct DNAs.\n")
        elif strategy == 'S':
            sizeTuples.sort(key=lambda x: x[0])
            n = 0
            currentTuple = sizeTuples[n]
            smallestSize = currentTuple[n]
            currentSize = smallestSize
            ### REVIEWER NOTE: int/int division ###
            while currentSize < smallestSize * 5/6 and n < len(sizeTuples) - 1:
                interBands.append(currentTuple[1])
                n = n + 1
                currentTuple = sizeTuples[n]
                currentSize = currentTuple[0]
            ### REVIEWER NOTE: int/int division ###
            if currentSize > smallestSize * 5/6:
                if currentSize < 50:
                    lostFlag = True
                elif currentSize < 300:
                    shortFlag = True
                interBands.append(currentTuple[1])
            if len(interBands) > 1:
                print("\n*Gel Purification Warning*: small fragment "
                      "purification resulted in purification of multiple, "
                      "possibly unintended distinct DNAs.\n")
    ### REVIEWER NOTE: should compare against numbers.Integral (an ABC), ###
    ###                but it's not in Py2.5; Py3 doesn't have `long` type ###
    elif isinstance(strategy, int):
        sizeTuples.sort(key=lambda x: x[0], reverse=True)
        currentTuple = sizeTuples[0]
        currentSize = currentTuple[0]
        ### REVIEWER NOTE: int/int division ###
        while currentSize > strategy * 6/5 and len(sizeTuples) > 1:
            sizeTuples.pop(0)
            currentTuple = sizeTuples[0]
            currentSize = currentTuple[0]
        ### REVIEWER NOTE: int/int division ###
        while currentSize > strategy * 5/6 and len(sizeTuples) > 1:
            band = sizeTuples.pop(0)
            interBands.append(band[1])
            currentTuple = sizeTuples[0]
            currentSize = currentTuple[0]
        ### REVIEWER NOTE: int/int division ###
        if currentSize > strategy * 5/6:
            if currentSize < 50:
                lostFlag = True
            elif currentSize < 300:
                shortFlag = True
            interBands.append(currentTuple[1])
        if not interBands:
            raise Exception('*Gel Purification Error*: for gel purification with strategy \'"+strategy+"\', no digest bands present in given range, with purification yielding zero DNA products.')
        elif len(interBands) > 1:
            print("\n*Gel Purification Warning*: fragment purification in "
                  "range of band size \""+str(strategy)+"\" resulted in "
                  "purification of multiple, possibly unintended distinct DNAs"
                  ".\n")
    else:
        raise Exception('*Gel Purification Error*: invalid cleanup strategy argument. Valid arguments are \'L\', \'S\', or integer size of band.')
    if not interBands:
        if lostFlag:
            print("\n*Gel Purification Warning*: purification with given "
                  "strategy \""+strategy+"\" returned short fragments "
                  "(< 50 bp) that were lost. Returning empty products list.\n")
        raise Exception('*Gel Purification Error*: purification with given strategy "'+strategy+'" yielded zero products.')
    else:
        if lostFlag:
            print("\n*Gel Purification Warning*: purification with given "
                  "strategy \""+strategy+"\" returned at least one short "
                  "fragment (< 50 bp) that was lost. Returning remaining "
                  "products.\n")
            for band in interBands:
                outputBands.append(cleanupPostProcessing(band,'gel extraction and zymo'))
        elif shortFlag:
            print("\n*Gel Purification Warning*: purification with given "
                  "strategy \""+strategy+"\" yielded short fragments "
                  "(< 300 bp). Returning short fragment cleanup products.\n")
            for band in interBands:
                outputBands.append(cleanupPostProcessing(band,'gel extraction and short fragment'))
        else:
            for band in interBands:
                outputBands.append(cleanupPostProcessing(band,'gel extraction and zymo'))
    return outputBands

# Description: Ligate() function that allows linear ligation products
# Note: also disallows blunt end ligation
def linLigate(inputDNAs):
    products = []
    # self ligation
    for fragment in inputDNAs:
        if not isinstance(fragment, DNA):
            print("\n*Ligate Warning*: Ligate function was passed a non-DNA "
                  "argument. Argument discarded.\n")
            continue
        (TL,TR,BL,BR) = SetFlags(fragment)
        if fragment.DNAclass != 'digest':
            print("\n*Ligate Warning*: for ligation reaction, invalid input "
                  "molecule removed -- ligation input DNA objects must be of "
                  "class \"digest\".\n")
        elif TL+TR+BL+BR == 1:
            pass
        elif TL+TR+BL+BR == 0:
            # blunt end self ligation case --> need to identify that both sides were digested (i.e. both ecoRV blunt ends)
            # and then return circular product of same sequence.
            pass
        elif fragment.topLeftOverhang.sequence:
            if isComplementary(fragment.topLeftOverhang.sequence.lower(), fragment.bottomRightOverhang.sequence.lower()):
                ligated = DNA('plasmid',fragment.name+' self-ligation',fragment.topLeftOverhang.sequence+fragment.sequence)
                products.append(ligatePostProcessing(ligated, (fragment, ), 'Self-ligate ('+fragment.name+') with DNA ligase for 30 minutes at room-temperature.'))
        elif fragment.bottomLeftOverhang.sequence:
            if isComplementary(fragment.topLeftOverhang.sequence.lower(), fragment.topRightOverhang.sequence.lower()):
                ligated = DNA('plasmid',fragment.name+' self-ligation',fragment.sequence+fragment.topRightOverhang.sequence)
                products.append(ligatePostProcessing(ligated, (fragment, ), 'Self-ligate ('+fragment.name+') with DNA ligase for 30 minutes at room-temperature.'))
    if products or len(inputDNAs) == 1:
        return products
    i = 0
    while i < len(inputDNAs):
        fragOne = inputDNAs[i]
        if not isinstance(fragOne, DNA):
            print("\n*Ligate Warning*: Ligate function was passed a non-DNA "
                  "argument. Argument discarded.\n")
            i += 1
            continue
        j = i + 1
        while j < len(inputDNAs):
            fragTwo = inputDNAs[j]
            if not all(isinstance(frag, DNA) for frag in (fragOne, fragTwo)):
                print("\n*Ligate Warning*: Ligate function was passed a "
                      "non-DNA argument. Argument discarded.\n")
                j += 1
                continue
            elif not all(frag.DNAclass == "digest"
                         for frag in (fragOne, fragTwo)):
                j += 1                
                continue
            (LTL,LTR,LBL,LBR) = SetFlags(fragOne)
            (RTL,RTR,RBL,RBR) = SetFlags(fragTwo)
            # first3 is the number of 3' overhangs for the left fragment, and so on for the other three classifiers
            (first3, first5, second3, second5) = (LTR + LBL, LBR + LTL, RTR + RBL, RBR + RTL)
            firstFlag = first3 + first5
            secondFlag = second3 + second5
            # non-blunt end ligation:
            if first3 == 2:
            # Here, you know that it has LTR and LBL
            # But you don't know about its RXX fields
                if isComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                    if isComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                        ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence+fragTwo.topRightOverhang.sequence)
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    else:
                        ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence)
                        ligated.bottomLeftOverhang = Overhang(fragOne.bottomLeftOverhang.sequence)
                        # you don't know whether it is RTR or RBR
                        if RTR:
                            ligated.topRightOverhang = Overhang(fragTwo.topRightOverhang.sequence)
                        elif RBR:
                            ligated.bottomRightOverhang = Overhang(fragTwo.bottomRightOverhang.sequence)
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))                  
                # you know it's not going to circularize, but you also know it has a LBL
                elif isComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                        ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragTwo.sequence+fragTwo.topRightOverhang.sequence+fragOne.sequence)
                        ligated.topRightOverhang = Overhang(fragOne.topRightOverhang.sequence)
                        # you don't know whether it is RTL or RBL
                        if RTL:
                            ligated.topLeftOverhang = Overhang(fragTwo.topLeftOverhang.sequence)
                        elif RBL:
                            ligated.bottomLeftOverhang = Overhang(fragTwo.bottomLeftOverhang.sequence)
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))               
                if isReverseComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                    if isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                        ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence)+reverse(fragTwo.bottomLeftOverhang.sequence))
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    else:
                        ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence))
                        ligated.bottomLeftOverhang = Overhang(fragOne.bottomLeftOverhang.sequence)
                        # you don't know whether it is RBL or RTL
                        if RTL:              
                            ligated.bottomRightOverhang = Overhang(reverse(fragTwo.topLeftOverhang.sequence))
                        elif RBL:
                            ligated.topRightOverhang = Overhang(reverse(fragTwo.bottomLeftOverhang.sequence))
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))  
                # you know it's not going to circularize, but you also know it has a LBL
                elif isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                    ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',reverseComplement(fragTwo.sequence)+reverse(fragTwo.bottomLeftOverhang.sequence)+fragOne.sequence)
                    ligated.topRightOverhang = Overhang(fragOne.topRightOverhang.sequence)
                    # you don't know whether it is RTR or RBR
                    if RTR:
                        ligated.bottomLeftOverhang = Overhang(reverse(fragTwo.topRightOverhang.sequence))
                    elif RBR:
                        ligated.topLeftOverhang = Overhang(reverse(fragTwo.bottomRightOverhang.sequence))
                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))            
            elif first3 == 1:
                if LTR:
                    # then you know it must have LTL
                    if RTR:
                        # then, if it is to ligate, it must have compatible RTL
                        if isReverseComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.topRightOverhang.sequence.upper()):
                            if isReverseComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                                ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence))
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                            else:
                                ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+reverseComplement(fragTwo.sequence))
                                ligated.topLeftOverhang = Overhang(fragOne.topLeftOverhang.sequence)
                                # you don't know whether it is RTL or RBL
                                if RTL:
                                    ligated.bottomRightOverhang = Overhang(reverse(fragTwo.topLeftOverhang.sequence))
                                elif RBL:
                                    ligated.bottomLeftOverhang = Overhang(reverse(fragTwo.bottomLeftOverhang.sequence))
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))              
                        # now, you know it's not going to circularize, but you know it has LTL
                        elif isReverseComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                            ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',reverseComplement(fragTwo.sequence)+fragOne.topLeftOverhang.sequence+fragOne.sequence)
                            ligated.topRightOverhang = Overhang(fragOne.topRightOverhang.sequence)
                            # you dont know whether you have RTR (=> BLO) or RBR (=> TLO) ==> correction: yes you do, you have RTR
                            ligated.bottomLeftOverhang = Overhang(reverse(fragTwo.topRightOverhang.sequence))
                            # if RTR:
                            #   ligated.bottomLeftOverhang = Overhang(reverse(fragTwo.topRightOverhang.sequence))
                            # elif RBR:
                            #   ligated.topLeftOverhang = Overhang(reverse(fragTwo.bottomRightOverhang.sequence))
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))              
            # you know here that you have LTR and LTL, and that you do not have RTR          
                    else:
                        # to ligate, it must have RBL and RBR
                        if isComplementary(fragOne.topRightOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                            if isComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                                ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence)
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                            else:
                                ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragOne.topRightOverhang.sequence+fragTwo.sequence)
                                ligated.topLeftOverhang = Overhang(fragOne.topLeftOverhang.sequence)
                                ligated.bottomRightOverhang = Overhang(fragTwo.bottomRightOverhang.sequence)
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))  
                        elif isComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                            # here, you know you have LTR and LTL, has a complementary RBR and does not have a RTR
                            ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragTwo.sequence+fragOne.topLeftOverhang.sequence+fragOne.sequence)
                            ligated.topRightOverhang = Overhang(fragOne.topRightOverhang.sequence)
                            if RTL:
                                ligated.topLeftOverhang= Overhang(fragTwo.topLeftOverhang.sequence)
                            elif RBL:
                                ligated.bottomLeftOverhang = Overhang(fragTwo.bottomLeftOverhang.sequence)
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                else:
                    # you know it has LBL as its 3 and LBR as its 5
                    if RTR:
                    # then, if it is to ligate, it must have compatible RTL
                        if isComplementary(fragTwo.topRightOverhang.sequence.upper(), fragOne.bottomLeftOverhang.sequence.upper()):
                            if isComplementary(fragTwo.topLeftOverhang.sequence.upper(), fragOne.bottomRightOverhang.sequence.upper()):
                                ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence+fragTwo.topRightOverhang.sequence)
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                            else:
                                ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence)
                                ligated.bottomRightOverhang = Overhang(fragOne.bottomRightOverhang.sequence)
                                # you don't know whether it is a RBL or RTL
                                if RTL:
                                    ligated.topLeftOverhang = Overhang(fragTwo.topLeftOverhang.sequence)
                                elif RBL:
                                    ligated.bottomLeftOverhang = Overhang(fragTwo.bottomLeftOverhang.sequence)
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        # you know it's not going to circularize, but you know it has LBR
                        elif isComplementary(fragTwo.topLeftOverhang.sequence.upper(), fragOne.bottomRightOverhang.sequence.upper()):
                            ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence)
                            ligated.bottomLeftOverhang = Overhang(fragOne.bottomLeftOverhang.sequence)
                            if RTR:
                                ligated.topRightOverhang = Overhang(fragTwo.topRightOverhang.sequence)
                            elif RBR:
                                ligated.bottomRightOverhang = Overhang(fragTwo.bottomRightOverhang.sequence)
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))              
                # up to here is good
                    else:
                        # you kno it has LBL, LBR, and not RTR
                        # to ligate, it must have RBL and RBR
                        if isReverseComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                            if isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                                ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',Complement(fragOne.bottomLeftOverhang.sequence)+fragOne.sequence+Complement(fragOne.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                            else:
                                ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+Complement(fragOne.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))
                                ligated.bottomLeftOverhang = Overhang(fragOne.bottomLeftOverhang.sequence)
                                if RTL:
                                    ligated.bottomRightOverhang = Overhang(reverse(fragTwo.topLeftOverhang.sequence))
                                elif RBL:
                                    ligated.topRightOverhang = Overhang(reverse(fragTwo.bottomLeftOverhang.sequence))
                                products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                        # you know it's not going to circularize, but you know it has LBL
                        elif isReverseComplementary(fragOne.bottomLeftOverhang.sequence.upper(), fragTwo.bottomLeftOverhang.sequence.upper()):
                            ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',reverseComplement(fragTwo.sequence)+Complement(fragOne.bottomLeftOverhang.sequence)+fragOne.sequence)
                            ligated.bottomRightOverhang = Overhang(fragOne.bottomRightOverhang.sequence)
                            ligated.topLeftOverhang = Overhang(reverse(fragTwo.bottomRightOverhang))
                            products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
            # here first3 == 0, so you know it has LTL and LBR          
            else:
                if isComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                    if isComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                        ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence)
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    else:
                        ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragTwo.sequence+fragOne.topLeftOverhang.sequence+fragTwo.sequence)
                        ligated.bottomRightOverhang = Overhang(fragOne.bottomRightOverhang.sequence)
                        if RTL:
                            ligated.topLeftOverhang = Overhang(fragTwo.topLeftOverhang.sequence)
                        elif RBL:
                            ligated.bottomLeftOverhang = Overhang(fragTwo.bottomLeftOverhang)
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                elif isComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                    ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+fragTwo.topLeftOverhang.sequence+fragTwo.sequence)
                    ligated.topLeftOverhang = Overhang(fragOne.topLeftOverhang.sequence)
                    if RTR:
                        ligated.topRightOverhang = Overhang(fragTwo.topRightOverhang.sequence)
                    elif RBR:
                        ligated.bottomRightOverhang = Overhang(fragTwo.bottomRightOverhang.sequence)
                    products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                # up to here is good
                # here first3 == 0, so you know it has LTL and LBR          
                if isReverseComplementary(fragOne.topLeftOverhang.sequence.upper(), fragTwo.topLeftOverhang.sequence.upper()):
                    if isReverseComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                        ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.topLeftOverhang.sequence+fragOne.sequence+reverse(fragTwo.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))    
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                    else:
                        ligated = DNA('digest',fragOne.name+', '+fragTwo.name+' ligation product',reverseComplement(fragTwo.sequence)+fragOne.topLeftOverhang.sequence+fragOne.sequence)    
                        ligated.bottomRightOverhang = Overhang(fragOne.bottomRightOverhang.sequence)
                        if RTR:
                            ligated.bottomLeftOverhang = Overhang(reverse(fragTwo.topRightOverhang.sequence))
                        if RBR:
                            ligated.topLeftOverhang = Overhang(reverse(fragTwo.bottomRightOverhang.sequence))
                        products.append(ligatePostProcessing(ligated, (fragOne, fragTwo), 'Ligate ('+fragOne.name+', '+fragTwo.name+') with DNA ligase for 30 minutes at room-temperature.'))
                elif isReverseComplementary(fragOne.bottomRightOverhang.sequence.upper(), fragTwo.bottomRightOverhang.sequence.upper()):
                    ligated = DNA('plasmid',fragOne.name+', '+fragTwo.name+' ligation product',fragOne.sequence+Complement(fragOne.bottomRightOverhang.sequence)+reverseComplement(fragTwo.sequence))    
                    ligated.topLeftOverhang = Overhang(fragOne.topLeftOverhang.sequence)
                    ligated.bottomRightOverhang = Overhang(reverse(fragTwo.topLeftOverhang.sequence))
            j += 1
        i += 1
    return products

# Note: going to stick with the convention where they actually pass a list of restriction enzymes
# As in: GoldenGate(vector_DNA, list_of_DNAs, EnzymeDictionary['BsaI'], ['AmpR', 'KanR'])
def GoldenGate(VectorPlasmid, InputDNAs, reASE, resistanceList):
    # ggEnzyme = EnzymeDictionary()[reASE]
    ggDNAs, outputDNAs, resistanceList, vector = [], [], map(str.lower, resistanceList), None
    vecDigest = Digest(VectorPlasmid, (reASE, ))
    for frag in vecDigest:
        if len(HasReplicon(frag.sequence)):
            vector = frag
            ggDNAs.append(vector)
            break
    if vector == None:
        raise Exception('For GoldenGate function, no viable vector input provided (must contain origin of replication).')
    for ggDNA in InputDNAs:
        if ggDNA.DNAclass != 'plasmid':
            print("\n*GoldenGate Warning*: linear inputs disallowed.\n")
            continue
        try:
            ggDigest = Digest(ggDNA, (reASE, ))
            ggDNAs += ggDigest
        ### REVIEWER NOTE: blanket except statement ###
        except:
            pass
    ggLigation = rGoldenGate(vector, [0], ggDNAs)
  
  # for a ligation product to be part of the gg output, it must fulfill three criteria:
    # 1) It must be circular (handled by Ligate() function)
    # 2) It must have at least one replicon
    # 3) It must have all of the above specified resistance markers

    for product in ggLigation:
        if product is None:
            continue
        if HasReplicon(product.sequence):
            resistanceFlag = 1
            resistanceMarkers = map(str.lower, HasResistance(product.sequence))
            for resistance in resistanceList:
                if resistance not in resistanceMarkers:
                    resistanceFlag = 0
            if resistanceFlag:
                if not DNAlistContains(outputDNAs, product):
                    outputDNAs.append(product)
    return outputDNAs

def DNAlistContains(DNAlist, candidateDNA):
    return any(candidateDNA.isEqual(listDNA) for listDNA in DNAlist)

def rGoldenGate(currentLink, linkList, allDNAs):
    products = []
    if currentLink.DNAclass == 'plasmid':
        return (currentLink, )
    else:
        counter = 0
        for myDNA in allDNAs:
            newLink = linLigate([currentLink, myDNA])
            if newLink:
                for link in newLink:
                    if counter == 0:
                        return (None, )
                    elif counter in linkList:
                        return (None, )
                    else:
                        nextList = list(linkList)
                        nextList.append(counter)
                        nextLink = link
                        futureProducts = rGoldenGate(nextLink, nextList, allDNAs)
                        products.extend(futureProduct
                                        for futureProduct in futureProducts
                                        if (isinstance(futureProduct, DNA) and
                                            futureProduct.DNAclass == "plasmid"))
            else:
                counter += 1
                continue
            counter += 1
        return products

# Description: HasFeature() function checks for presence of regex-encoded feature in seq
def HasFeature(regex, seq):
    #Regex must be lower case!
    ### REVIEWER NOTE: come up with better variable names
    a = re.search(regex, seq.lower())
    b = re.search(regex, reverseComplement(seq.lower()))
    return bool(a) or bool(b)

### REVIEWER NOTE: put these functions (containing literal sequences) in a separate file! ###
#####Origins Suite: Checks for presence of certain origins of replication#####
def HasColE2(seq):
    #has ColE2 origin, data from PMID 16428404
    regexp = '....tga[gt]ac[ct]agataagcc[tgc]tatcagataacagcgcccttttggcgtctttttgagcacc' 
    return HasFeature(regexp, seq)
    #necessary and sufficient element for ColE2 replication, however a longer sequence is needed for stable replication
    # 'AGCGCCTCAGCGCGCCGTAGCGTCGATAAAAATTACGGGCTGGGGCGAAACTACCATCTGTTCGAAAAGGTCCGTAAATGGGCCTACAGAGCGATTCGTCAGGGCTGGCCTGTATTCTCACAATGGCTTGATGCCGTTATCCAGCGTGTCGAAATGTACAACGCTTCGCTTCCCGTTCCGCTTTCTCCGGCTGAATGTCGGGCTATTGGCAAGAGCATTGCGAAATATACACACAGGAAATTCTCACCAGAGGGATTTTCCGCTGTACAGGCCGCTCGCGGTCGCAAGGGCGGAACTAAATCTAAGCGCGCAGCAGTTCCTACATCAGCACGTTCGCTGAAACCGTGGGAGGCATTAGGCATCAGTCGAGCGACGTACTACCGAAAATTAAAATGTGACCCAGACCTCGCnnnntga'
    #longer element shown in the Anderson lab that stably replicates

def HasColE1(seq):
    regexp = 'tcatgaccaaaatcccttaacgtgagttttcgttccactgagcgtcagaccccgtagaaaagatcaaaggatcttcttgagatcctttttttctgcgcgtaatctgctgcttgcaaacaaaaaaaccaccgctaccagcggtggtttgtttgccggatcaagagcta[cagt]caactctttttccgaaggtaactggcttcagcagagcgcagataccaaatactgt[cagt]cttctagtgtagccgtagttaggccaccacttcaagaactctgtagcaccgcctacatacctcgctctgctaatcctgttaccagtggctgctgccagtggcgataagtcgtgtcttaccgggttggactcaagacgatagttaccggataaggcgcagcggtcgggctgaacggggggttcgtgcacacagcccagcttggagcgaacgacctacaccgaactgagatacctacagcgtgagc[cagt][cagt]tgagaaagcgccacgcttcccgaagggagaaaggcggacaggtatccggtaagcggcagggtcggaacaggagagcgcacgagggagcttccaggggg[acgt]aacgcctggtatctttatagtcctgtcgggtttcgccacctctgacttgagcgtcgatttttgtgatgctcgtcaggggggc[acgt]gagcct[ga]tggaaaaacgccagcaacgcggcc' 
    return HasFeature(regexp, seq)

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
    # was: regex='MSIQHFRVALIPFFAAFCLPVFAHPETLVKVKDAEDQLGARVGYIELDLNSGKILESFRPEERFPMMSTFKVLLCGAVLSRIDAGQEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEAIPNDERDTTMPVAMATTLRKLLTGELLTLASRQQLIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW'
    # compared with: 'MSIQHFRVALIPFFAAFCLPVFAHPETLVKVKDAEDQLGARVGYIELDLNSGKILESFRPEERFPMMSTFKVLLCGAVLSRIDAGQEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEAIPNDERDTTMPVAMATTLRKLLTGELLTLASRQQLIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW'
    # result: aligned with clustal, got following output:
    regex = 'MSTFKVLLCGAVLSR[VI]DAGQEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEAIPNDERDTTMP[VA]AMATTLRKLLTGELLTLASRQQLIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW'
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
    if HasColE1(seq):
        retval.append('ColE1')
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
        delimit = re.compile(r'\s*,\s*')
        self.replication = delimit.split(replication)
        self.resistance = delimit.split(resistance) #should include the plasmid resistance!
        if(plasmid != ""):
            self.plasmids = [plasmid, ] #DNA object
        else:
            self.plasmids = []

# Description: accepts list of dnas and a strain, it should output a list of DNAs that survive the transformation
# this would completely reciplate the TransformPlateMiniprep cycle, it returns all the DNAs present in the cell
def TransformPlateMiniprep(DNAs, strain):
    #strain is an object
    transformed = strain.plasmids
    selectionList = []
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
                if resistance not in strain.resistance:
                    newR = True
                    ### REVIEWER NOTE: should this be "(not x) in y" or "x not in y"? ###
                    if not resistance in selectionList:
                        selectionList.append(resistance)
                    success_msg += "\nTransformation of "+dna.name+" into "+strain.name+" successful -- use "+resistance+" antibiotic selection.\n"
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
            if(newR and replicon_ok and no_existing_plasmid):
                parent = dna.clone()
                parent.setChildren((dna, ))
                dna.addParent(parent)
                parent.instructions = 'Transform '+dna.name+' into '+strain.name+', selecting for '+resistance+' resistance.'
                parent.setTimeStep(24)
                parent.addMaterials(['Buffers P1,P2,N3,PB,PE',
                                     'Miniprep column',
                                     resistance[:-1]+' LB agar plates',
                                     'LB '+resistance[:-1]+' media'])
                transformed.append(dna)  
                print(success_msg)
            else:
                if not(newR):
                    raise Exception('*Transformation Error*: for transformation of '+dna.name+' into '+strain.name+', plasmid either doesn\'t have an antibiotic resistance or doesn\'t confer a new one on this strain')
                if not(replicon_ok):
                    raise Exception('*Transformation Error*: for transformation of "'+dna.name+'" into "'+strain.name+'", plasmid replicon won\'t function in this strain')
                if not(no_existing_plasmid):
                    raise Exception('*Transformation Error*: for transformation of "'+dna.name+'" into "'+strain.name+'", transformed plasmid replicon competes with existing plasmid in strain') 
    if len(transformed)<1:
        raise Exception("*Transformation Error*: For transformation of "+dna.name+" into "+strain.name+", no DNAs successfully transformed. DNAs may be linear.")
    return transformed
