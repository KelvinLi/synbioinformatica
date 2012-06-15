#!/usr/bin/python -tt
# Copyright Nima Emami, 2012

import synbioinformatica, sys
from synbioinformatica import DNA, restrictionEnzyme, Ligate

def main(template, primer_1, primer_2):
	print PCR(template, primer_1, primer_2)

if __name__ == "__main__":
	InitializeEnzymes = getattr(synbioinformatica,'EnzymeDictionary')
	PCR = getattr(synbioinformatica,'PCR')
	Digest = getattr(synbioinformatica,'Digest')
	Ligate = getattr(synbioinformatica,'Ligate')
	EnzymeDictionary = InitializeEnzymes()
	plasmid = DNA('ACTTCATGGTGAGATGAGTGAAGGCGAGCTGGTGGATGCATTCCGCCATGTGAGTGATGCGTTTGAGCAAACCAGCGAAACCATCGGCGTGCGCGCCAATAACGCGATCAACGACATGGTGCGTCAACGTCTGCTGAACCGCTTTACCAGCGAGCAGGCGGAAGGGAACGCAATTTACCGTCTGACGCCGCTCGGCATCGGCATTACTGACTACNNNATCCGTCAGCGCGAGTTTTCTACGCTGCGTCTTTCTATGCAGTTGTCGATTGTGGCGGGTGAGCTCAAACGCGCAGCAGATGCCGCCGAAGAGGGCGGTGATGAATTTCACTGGCACCGTAATGTCTATGCGCCACTGAAATATTCGGTAGCAGAAATTTTCGACAGTATCGACCTGACGAATTCGCAACGTCTGATGGACGAACAGCAGCAGCAGGTGAAGGACGATATCGCCCAGTTGCTGAACAAAGACTGGCGGGCGGCGATTTCCAGCTGGATCCTGAATTGTTGCTTTCGGAAACTTCCGGAACGCTGCGTGAATTGCAGGATACGCTGGAAGCGGCAGGCGACAAATTGCAGGCTAATCTGTTGCGCATTCAGGATGCGACGATGACCCATGACGATCTGCATTTCGTCGATCGTCTGGTGTTCGATCTGCAGAGCAAACTCGATCGTATTATCAGTTGGGGCCAGCAATCCATCGACTTGTGGATTGGCTACGACCGCCACGTACACAAATTTATTCGTACCGCGATCGATATGGATAAAAACCGCGTCTTTGCTCAGCGGTTACGTCAGTCGGTACAAACCTATTTTGATGAGGGCGCTAACTTATGCCAATGCCGATCGTCTGCTGGATATGCGTGACGAAGAGATGGCACTGCGCGATGAAGAAGTGACTGGGGAACTTCCTGAGGATCTGGAATACGAAGAGTTTAACGAGATCCGCGAACAGCTGGCGGCGATCATCGAAGAACAACTTGTACAAAACCAGACAAGTGCCGCTGGATCTTGGTCTGGTGGTACGCGAATATCTGTCACAGTATCCGCGTGCACGTCACTTTGACGTTGCGCGTATTGTTATTGATACCTGACGCAACGTCTGCGAATTCCTGCAGTA', 'PCR product')
	# primer_1 = DNA("CCAGCTCGCCTTCACTCATCTCAwwwwwwwwwwwwww",'primer')
	# primer_2 = DNA("wwwwwwwwwwwwwwwwwATAACGCGATCAACGACATGGTGCGTCA",'primer')
	# pcrProduct = PCR(plasmid, primer_1, primer_2)
	# print pcrProduct.sequence
	products = Digest(plasmid,[EnzymeDictionary["EcoRI"], EnzymeDictionary["BceAI"]])
	ligated = Ligate(products)
	print "\nLigation product(s):"
	for product in ligated:
		print product.sequence
