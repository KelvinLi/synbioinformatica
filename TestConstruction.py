import synbioinformatica, sys
from synbioinformatica import DNA, restrictionEnzyme, Ligate, Strain

if __name__ == "__main__":
	InitializeEnzymes = getattr(synbioinformatica,'EnzymeDictionary')
	PCR = getattr(synbioinformatica,'PCR')
	Digest = getattr(synbioinformatica,'Digest')
	Ligate = getattr(synbioinformatica,'Ligate')
	GelAndZymoPurify = getattr(synbioinformatica,'GelAndZymoPurify')
	ShortFragmentCleanup = getattr(synbioinformatica,'ShortFragmentCleanup')
	ZymoPurify = getattr(synbioinformatica,'ZymoPurify')
	TransformPlateMiniprep = getattr(synbioinformatica, 'TransformPlateMiniprep')	
	EnzymeDictionary = InitializeEnzymes()

	olib001 = DNA('GGATCtggtctcGCTAGCGGTAGCGGCAGTagtgcc','primer', 'olib001')
	olib002 = DNA('AAAGGTCTCggatccGAGGAGatgcctaaGCgcgccagctctttcaggg','primer', 'olib002')
	olib003 = DNA('taataaGGTCTCatctttMNNggtgctgacatcgagataac','primer', 'olib003')
	olib004 = DNA('taataaGGTCTCAAAGAGNNKGCGCGCTTAGGCATCTCCT','primer', 'olib004')
	olib005 = DNA('AAAggtctcGCTAGCGAGGAGatgcctaaGCcgcNNKaagccggaaattctggatggttt','primer', 'olib005')
	olib006 = DNA('TATAggtctcGGATCCttaMNNcttMNNMNNatgctcgcgMNNgtaagccagctccgcca','primer', 'olib006')
	olib011 = DNA('GTagtgccaatgaaaacaacctgattNNKatcgatcttgagatgaccggtct','primer', 'olib011')
	olib012 = DNA('GGATCtggtctcgctagcGGTAGCGGCAGTagtgccaatgaaaacaacctgatt','primer', 'olib012')
	olib013 = DNA('tAAAggtctcGGATCCGAGGAGatgcctaaataacggtagtggaagtaggctt','primer', 'olib013')
	olib014 = DNA('gttggcatcggtcaccag','primer', 'olib014')
	olib015 = DNA('ctggtgaccgatgccaacNNKaatattctggcagaagggccgac','primer', 'olib015')
	olib007 = DNA('tAAAggtctcGCTAGCGAGGAGatgcctaaATNNKgatNNKagcaccctgaaagagctgg','primer', 'olib007')
	olib008 = DNA('TATAggtctcGGATCCttacagcttgataaaatgctcgc','primer', 'olib008')
	olib009 = DNA('taataaGGTCTCaatcgNNKgcggagNNKgcttactaccgcgagcattt','primer', 'olib009')
	olib010 = DNA('taataaGGTCTCacgattcacgMNNatcatccatcgcctgatgcg','primer', 'olib010')
	olib016 = DNA('GGATCtggtctcgctagcGGTAGCGGCAGTtctgaagtcg','primer', 'olib016')
	olib017 = DNA('tAAAggtctcGGATCCGAGGAGatgcctaataaMNNcgcgccgaccggcacttcc','primer', 'olib017')
	olib018 = DNA('tAAAggtctcGatacNNKNNKcgtcacgcgctgacgctg','primer', 'olib018')
	olib019 = DNA('tAAAggtctcGgtattcMNNgctaaattcgacttcagaACTGC','primer', 'olib019')
	olib020 = DNA('tAAAggtctcGCTAGCGAGGAGatgcctaataNNKcataacaatcgggtaatcggc','primer', 'olib020')
	olib021 = DNA('TATAggtctcGGATCCttaatccgtcgaggattgcgc','primer', 'olib021')
	olib022 = DNA('cacgcgaccaatgcgactg','primer', 'olib022')
	olib023 = DNA('cagtcgcattggtcgcgtgNNKtttggtgcgcgtgacgcgaa','primer', 'olib023')
	olib024 = DNA('taataaGGTCTCacgccNNKttgNNKgtcacgcttgaaccatgtg','primer', 'olib024')
	olib025 = DNA('taataaGGTCTCaggcgtcgatcagacgataa','primer', 'olib025')
	olib026 = DNA('tAAAggtctcGGATCCGAGGAGatgcctaagcatgtgcggtgggatcatgg','primer', 'olib026')
	olib027 = DNA('tAAAggtctcGCTAGCGGTAGCGGCAGTtctgaagtcgaatt','primer', 'olib027')
	olib028 = DNA('tAAAggtctcGCTAGCGAGGAGatgcctaagcagaaatcatggccctgc','primer', 'olib028')
	olib029 = DNA('TATAggtctcGGATCCttaatccgtcgaggattgcg','primer', 'olib029')
	olib030 = DNA('aataaGGTCTCAtggtNNKcatNNKNNKNNKGCACATGCTTAGGCATCTCCTCG','primer', 'olib030')
	olib031 = DNA('aataaGGTCTCAaccaatcgggcggttccagc','primer', 'olib031')
	olib032 = DNA('taataaGGTCTCacaccctgMNNcagggccatMNNttctgcTTAGGCATCTCCTC','primer', 'olib032')
	olib033 = DNA('taataaGGTCTCaggtggtNNKgtgatgcaaNNKtatcgtctgatcgacgcca','primer', 'olib033')
	olib034 = DNA('ccatccagaatttccggcttMNNgcggcgcgcMNNctctttcagggtgctgacatcga','primer', 'olib034')
	olib035 = DNA('AAAGGTCTCggatccGAGGAGatgcctaaccatccagaatttccggctt','primer', 'olib035')
	olib036 = DNA('tAAAggtctcGCTAGCGGTAGCGGCAGTagtgccaatgaaaa','primer', 'olib036')
	olib037 = DNA('caatggtcggcccttctgccagaatattMNNMNNggcatcggtcaccagcgtggcaat','primer', 'olib037')
	olib038 = DNA('aatattctggcagaagggccg','primer', 'olib038')
	olib039 = DNA('tAAAggtctcGCTAGCGAGGAGatgcctaaggttttaccaagcaggggacgca','primer', 'olib039')
	olib040 = DNA('TATAggtctcGGATCCttacagcttgataaaatgctcgc','primer', 'olib040')
	olib041 = DNA('aataaGGTCTCAgcatNNKNNKaagNNKtaagGATCCtaaCTCGCTCagg','primer', 'olib041')
	olib042 = DNA('aataaGGTCTCAatgctcMNNgtagtaagcMNNctccgccaccgattcacgga','primer', 'olib042')
	olib043 = DNA('tAAAggtctcGCTAGCGGTAGCGGCAGTtctgaagtcgaat','primer', 'olib043')
	olib044 = DNA('ggccatgatttctgcatgtg','primer', 'olib044')
	olib045 = DNA('cacatgcagaaatcatggccNNKcggcagggtggtctggtgat','primer', 'olib045')
	olib046 = DNA('AAAGGTCTCggatccGAGGAGatgcctaacgctccggcacacattaca','primer', 'olib046')
	olib047 = DNA('aataaGGTCTCActtgaaNNKtgtgtaatgtgtgccgga','primer', 'olib047')
	olib048 = DNA('aataaGGTCTCAcaagcgtMNNataMNNcgtggcgtcgatcagacgata','primer', 'olib048')
	olib049 = DNA('AAAggtctcGCTAGCGAGGAGatgcctaacgNNKatccacagtcgcattggt','primer', 'olib049')
	olib050 = DNA('TATAggtctcGGATCCttaatccgtcgaggattgcg','primer', 'olib050')
	olib051 = DNA('catcatccgggtatgaatcaccgaNNKgaaattacggaaggaatactggc','primer', 'olib051')
	olib052 = DNA('tcggtgattcatacccggatgatgMNNcacatccattaaagatcccgcagc','primer', 'olib052')
	olib053 = DNA('AAAggtctcGCTAGCGAGGAGatgcctaacg','primer', 'olib053')
	olib054 = DNA('aataaGGTCTCAagacMNNgcgaccaatgcgactgtgg','primer', 'olib054')
	olib055 = DNA('aataaGGTCTCAgtctttggtgcgcgtgac','primer', 'olib055')
	olib056 = DNA('AAAggtctcGGATCCGAGGAGatgcctaaagcttgtcgaagttgttctc','primer', 'olib056')
	olib057 = DNA('tAAAggtctcGCTAGCGGAAGCGGATCGcagcactggctgg','primer', 'olib057')
	olib058 = DNA('ttgccgaacatttcggcttcaccggctatgcctatNNKcatatccagcacaaacacacc','primer', 'olib058')
	olib059 = DNA('gtgaagccgaaatgttcggcaa','primer', 'olib059')
	olib060 = DNA('aataaGGTCTCAgtgacNNKcgatcggctNNKNNKgagaacaacttcgacaagct','primer', 'olib060')
	olib061 = DNA('aataaGGTCTCAtcacgatgMNNattMNNgaccgcgatggtgtgtttgt','primer', 'olib061')
	olib062 = DNA('AAAggtctcGCTAGCGAGGAGatgcctaactcNNKccggtcgtcaagcgcgcgaa','primer', 'olib062')
	olib063 = DNA('gccgaaatcggccgcatgcgcMNNMNNggcacgctcttccttcg','primer', 'olib063')
	olib064 = DNA('gcgcatgcggccgatttcggcNNKcgctccggcatcaccatt','primer', 'olib064')
	olib065 = DNA('TATAggtctcGGATCCttagatcagctttcttctgattgcgagg','primer', 'olib065')
	olib066 = DNA('aataaGGTCTCAggcaaagacgtgcttcctgga','primer', 'olib066')
	olib067 = DNA('aataaGGTCTCActggcgtcggaaaggccggcg','primer', 'olib067')
	olib068 = DNA('aataaGGTCTCAtgccNNKtccggcgaacaggaacg','primer', 'olib068')
	olib069 = DNA('aataaGGTCTCAccagMNNgaacatcgacattgatccgttg','primer', 'olib069')



	pth7035K_nd033 = DNA("GATCTTTTATAGCTTGCTCAGTCCTAGGTACAATGCTTGCTACCTAGTAGACATAAAAACGGCAAAGTATGagcacaaaaaagaaaccattaacacaagagcagcttgaggacgcacgtcgccttaaagcaatttatgaaaaaaagaaaaatgaacttggcttatcccaggaatctgtcgcagacaagatggggatggggcagtcaggcgttggtgctttatttaatggcatcaatgcattaaatgcttataacgccgcattgcttgcaaaaattctcaaagttagcgttgaagaatttagcccttcaatcgccagagaaatctacgagatgtatgaagcggttagtatgcagccgtcacttagaagtgagtatgagtaccctgttttttctcatgttcaggcagggatgttctcacctgagcttagaacctttaccaaaggtgatgcggagagatgggtaagcacagctagcGGTAGCGGCAGTagtgccaatgaaaacaacctgatttggatcgatcttgagatgaccggtctggatcccgagcgcgatcgcattattgagattgccacgctggtgaccgatgccaacctgaatattctggcagaagggccgaccattgcagtacaccagtctgatgaacagctggcgctgatggatgactggaacgtgcgcacccataccgccagcgggctggtagagcgcgtgaaagcgagcacgatgggcgatcgggaagctgaactggcaacgctcgaatttttaaaacagtgggtgcctgcgggaaaatcgccgatttgcggtaacagcatcggtcaggaccgtcgtttcctgtttaaatacatgccggagctggaagcctacttccactaccgttatctcgatgtcagcaccctgaaagagctggcgcgccgctggaagccggaaattctggatggttttaccaagcaggggacgcatcaggcgatggatgatatccgtgaatcggtggcggagctggcttactaccgcgagcattttatcaagctgtaaGATCCtaaCTCGCTCCTCaggcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatCAATTCGACCCAGCTTTCTTGTACAAAGTTGGCATTATAAAAAATAATTGCTCATCAATTTGTTGCAACGAACAGGTCACTATCAGTCAAAATAAAATCATTATTTGCCATCCAGCTGATATCCCCTATAGTGAGTCGTATTACATGGTCATAGCTGTTTCCTGGCAGCTCTGGCCCGTGTCTCAAAATCTCTGATGTTACATTGCACAAGATAAAAATATATCATCATGCCTCCTCTAGAgtgttacaaccaattaaccaattctgattagaaaaactcatcgagcatcaaatgaaactgcaatttattcatatcaggattatcaataccatatttttgaaaaagccgtttctgtaatgaaggagaaaactcaccgaggcagttccataggatggcaagatcctggtatcggtctgcgattccgactcgtccaacatcaatacaacctattaatttcccctcgtcaaaaataaggttatcaagtgagaaatcaccatgagtgacgactgaatccggtgagaatggcaaaagcttatgcatttctttccagacttgttcaacaggccagccattacgctcgtcatcaaaatcactcgcatcaaccaaaccgttattcattcgtgattgcgcctgagcgagacgaaatacgcgatcgctgttaaaaggacaattacaaacaggaatcgaatgcaaccggcgcaggaacactgccagcgcatcaacaatattttcacctgaatcaggatattcttctaatacctggaatgctgttttcccggggatcgcagtggtgagtaaccatgcatcatcaggagtacggataaaatgcttgatggtcggaagaggcataaattccgtcagccagtttagtctgaccatctcatctgtaacatcattggcaacgctacctttgccatgtttcagaaacaactctggcgcatcgggcttcccatacaatcgatagattgtcgcacctgattgcccgacattatcgcgagcccatttatacccatataaatcagcatccatgttggaatttaatcgcggcctggagcaagacgtttcccgttgaatatggctcataacaccccttgtattactgtttatgtaagcagacagttttattgttcatgatgatatatttttatcttgtgcaatgtaacatcagagattttgagacacaacgtggctttgttgaataaatcgaacttttgctgagttgaaggatcagCTCGAGaGCAGTTCAACCTGTTGATAGtacgtactaagctctcatgtttcacgtactaagctctcatgtttaacgtactaagctctcatgtttaacgaactaaaccctcatggctaacgtactaagctctcatggctaacgtactaagctctcatgtttcacgtactaagctctcatgtttgaacaataaaattaatataaatcagcaacttaaatagcctctaaggttttaagttttataagaaaaaaaagaatatataaggcttttaaagcttttaaggtttaacggttgtggacaacaagccagggatgtaacgcactgagaagcccttagagcctctcaaagcaattttgagtgacacaggaacacttaacggctgacatgggaattagccatgggcccgtgcgaatcaccctaggTGTAAAACGACGGCCAGTCTTAAGCTCGGGCCCCAAATAATGATTTTATTTTGACTGATAGTGACCTGTTCGTTGCAACAAATTGATGAGCAATGCTTTTTTATAATGCCAACTTTGTACAAAAAAGCAGGCTCCGAATTGgtatcacgaggcagaatttcagataaaaaaaatCCTTAGCTTTCGCTAAGGATCTGAAGTGgaattcatgA", 'plasmid', 'pth7035K_nd033')

	pth7035K_nd031 = DNA("GATCTTTTATAGCTTGCTCAGTCCTAGGTACAATGCTTGCTACCTAGTAGACATAAAAACGGCAAAGTATGagcacaaaaaagaaaccattaacacaagagcagcttgaggacgcacgtcgccttaaagcaatttatgaaaaaaagaaaaatgaacttggcttatcccaggaatctgtcgcagacaagatggggatggggcagtcaggcgttggtgctttatttaatggcatcaatgcattaaatgcttataacgccgcattgcttgcaaaaattctcaaagttagcgttgaagaatttagcccttcaatcgccagagaaatctacgagatgtatgaagcggttagtatgcagccgtcacttagaagtgagtatgagtaccctgttttttctcatgttcaggcagggatgttctcacctgagcttagaacctttaccaaaggtgatgcggagagatgggtaagcacagctagcGGTAGCGGCAGTtctgaagtcgaatttagccacgaatactggatgcgtcacgcgctgacgctggcgaaacgtgcctgggatgagcgggaagtgccggtcggcgcggtattagtgcataacaatcgggtaatcggcgaaggctggaaccgcccgattggtcgccatgatcccaccgcacatgcagaaatcatggccctgcggcagggtggtctggtgatgcaaaattatcgtctgatcgacgccacgttgtatgtcacgcttgaaccatgtgtaatgtgtgccggagcgatgatccacagtcgcattggtcgcgtggtctttggtgcgcgtgacgcgaaaactggcgctgcgggatctttaatggatgtgctgcatcatccgggtatgaatcaccgagtggaaattacggaaggaatactggcggatgagtgcgcggcgttgctcagtgacttctttcgcatgcgccgccaggaaattaaagcgcagaaaaaagcgcaatcctcgacggattaaGATCCtaaCTCGCTCCTCaggcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatCAATTCGACCCAGCTTTCTTGTACAAAGTTGGCATTATAAAAAATAATTGCTCATCAATTTGTTGCAACGAACAGGTCACTATCAGTCAAAATAAAATCATTATTTGCCATCCAGCTGATATCCCCTATAGTGAGTCGTATTACATGGTCATAGCTGTTTCCTGGCAGCTCTGGCCCGTGTCTCAAAATCTCTGATGTTACATTGCACAAGATAAAAATATATCATCATGCCTCCTCTAGAgtgttacaaccaattaaccaattctgattagaaaaactcatcgagcatcaaatgaaactgcaatttattcatatcaggattatcaataccatatttttgaaaaagccgtttctgtaatgaaggagaaaactcaccgaggcagttccataggatggcaagatcctggtatcggtctgcgattccgactcgtccaacatcaatacaacctattaatttcccctcgtcaaaaataaggttatcaagtgagaaatcaccatgagtgacgactgaatccggtgagaatggcaaaagcttatgcatttctttccagacttgttcaacaggccagccattacgctcgtcatcaaaatcactcgcatcaaccaaaccgttattcattcgtgattgcgcctgagcgagacgaaatacgcgatcgctgttaaaaggacaattacaaacaggaatcgaatgcaaccggcgcaggaacactgccagcgcatcaacaatattttcacctgaatcaggatattcttctaatacctggaatgctgttttcccggggatcgcagtggtgagtaaccatgcatcatcaggagtacggataaaatgcttgatggtcggaagaggcataaattccgtcagccagtttagtctgaccatctcatctgtaacatcattggcaacgctacctttgccatgtttcagaaacaactctggcgcatcgggcttcccatacaatcgatagattgtcgcacctgattgcccgacattatcgcgagcccatttatacccatataaatcagcatccatgttggaatttaatcgcggcctggagcaagacgtttcccgttgaatatggctcataacaccccttgtattactgtttatgtaagcagacagttttattgttcatgatgatatatttttatcttgtgcaatgtaacatcagagattttgagacacaacgtggctttgttgaataaatcgaacttttgctgagttgaaggatcagCTCGAGaGCAGTTCAACCTGTTGATAGtacgtactaagctctcatgtttcacgtactaagctctcatgtttaacgtactaagctctcatgtttaacgaactaaaccctcatggctaacgtactaagctctcatggctaacgtactaagctctcatgtttcacgtactaagctctcatgtttgaacaataaaattaatataaatcagcaacttaaatagcctctaaggttttaagttttataagaaaaaaaagaatatataaggcttttaaagcttttaaggtttaacggttgtggacaacaagccagggatgtaacgcactgagaagcccttagagcctctcaaagcaattttgagtgacacaggaacacttaacggctgacatgggaattagccatgggcccgtgcgaatcaccctaggTGTAAAACGACGGCCAGTCTTAAGCTCGGGCCCCAAATAATGATTTTATTTTGACTGATAGTGACCTGTTCGTTGCAACAAATTGATGAGCAATGCTTTTTTATAATGCCAACTTTGTACAAAAAAGCAGGCTCCGAATTGgtatcacgaggcagaatttcagataaaaaaaatCCTTAGCTTTCGCTAAGGATCTGAAGTGgaattcatgA", "plasmid", "pth7035K_nd031")
	pth7035K_brp038 = DNA("GATCTTTTATAGCTTGCTCAGTCCTAGGTACAATGCTTGCTACCTAGTAGACATAAAAACGGCAAAGTATGagcacaaaaaagaaaccattaacacaagagcagcttgaggacgcacgtcgccttaaagcaatttatgaaaaaaagaaaaatgaacttggcttatcccaggaatctgtcgcagacaagatggggatggggcagtcaggcgttggtgctttatttaatggcatcaatgcattaaatgcttataacgccgcattgcttgcaaaaattctcaaagttagcgttgaagaatttagcccttcaatcgccagagaaatctacgagatgtatgaagcggttagtatgcagccgtcacttagaagtgagtatgagtaccctgttttttctcatgttcaggcagggatgttctcacctgagcttagaacctttaccaaaggtgatgcggagagatgggtaagcacagctagcGGAAGCGGATCGcagcactggctggacaagttgaccgatcttgccgcaattcagggcgacgagtgcatcctgaaggatggccttgccgaccttgccgaacatttcggcttcaccggctatgcctatctccatatccagcacaaacacaccatcgcggtcaccaattatcatcgtgactggcgatcggcttacttcgagaacaacttcgacaagctcgatccggtcgtcaagcgcgcgaaatccaggaagcacgtctttgcctggtccggcgaacaggaacgatcgcggctatcgaaggaagagcgtgccttctacgcgcatgcggccgatttcggcatccgctccggcatcaccattccgatcaagaccgccaacggatcaatgtcgatgttcacgctggcgtcggaaaggccggcgatcgacctcgaccgtgagatcgacgcggccgcagccgcgggcgccgtcgggcagctccatgcccgcatctctttccttcagaccactccgacagtggaagatgccgcctggctcgatccgaaagaggcgacctatctcagatggatcgccgtcggcatgacaatggaggaagtcgcagacgtggagggcgtcaagtacaacagcgtccgtgtcaagctccgcgaggccatgaagcgcttcgacgttcgcagcaaggcccatctcaccgccctcgcaatcagaagaaagctgatctgaggatccGGATCCtaaCTCGCTCCTCaggcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatCAATTCGACCCAGCTTTCTTGTACAAAGTTGGCATTATAAAAAATAATTGCTCATCAATTTGTTGCAACGAACAGGTCACTATCAGTCAAAATAAAATCATTATTTGCCATCCAGCTGATATCCCCTATAGTGAGTCGTATTACATGGTCATAGCTGTTTCCTGGCAGCTCTGGCCCGTGTCTCAAAATCTCTGATGTTACATTGCACAAGATAAAAATATATCATCATGCCTCCTCTAGAgtgttacaaccaattaaccaattctgattagaaaaactcatcgagcatcaaatgaaactgcaatttattcatatcaggattatcaataccatatttttgaaaaagccgtttctgtaatgaaggagaaaactcaccgaggcagttccataggatggcaagatcctggtatcggtctgcgattccgactcgtccaacatcaatacaacctattaatttcccctcgtcaaaaataaggttatcaagtgagaaatcaccatgagtgacgactgaatccggtgagaatggcaaaagcttatgcatttctttccagacttgttcaacaggccagccattacgctcgtcatcaaaatcactcgcatcaaccaaaccgttattcattcgtgattgcgcctgagcgagacgaaatacgcgatcgctgttaaaaggacaattacaaacaggaatcgaatgcaaccggcgcaggaacactgccagcgcatcaacaatattttcacctgaatcaggatattcttctaatacctggaatgctgttttcccggggatcgcagtggtgagtaaccatgcatcatcaggagtacggataaaatgcttgatggtcggaagaggcataaattccgtcagccagtttagtctgaccatctcatctgtaacatcattggcaacgctacctttgccatgtttcagaaacaactctggcgcatcgggcttcccatacaatcgatagattgtcgcacctgattgcccgacattatcgcgagcccatttatacccatataaatcagcatccatgttggaatttaatcgcggcctggagcaagacgtttcccgttgaatatggctcataacaccccttgtattactgtttatgtaagcagacagttttattgttcatgatgatatatttttatcttgtgcaatgtaacatcagagattttgagacacaacgtggctttgttgaataaatcgaacttttgctgagttgaaggatcagCTCGAGaGCAGTTCAACCTGTTGATAGtacgtactaagctctcatgtttcacgtactaagctctcatgtttaacgtactaagctctcatgtttaacgaactaaaccctcatggctaacgtactaagctctcatggctaacgtactaagctctcatgtttcacgtactaagctctcatgtttgaacaataaaattaatataaatcagcaacttaaatagcctctaaggttttaagttttataagaaaaaaaagaatatataaggcttttaaagcttttaaggtttaacggttgtggacaacaagccagggatgtaacgcactgagaagcccttagagcctctcaaagcaattttgagtgacacaggaacacttaacggctgacatgggaattagccatgggcccgtgcgaatcaccctaggTGTAAAACGACGGCCAGTCTTAAGCTCGGGCCCCAAATAATGATTTTATTTTGACTGATAGTGACCTGTTCGTTGCAACAAATTGATGAGCAATGCTTTTTTATAATGCCAACTTTGTACAAAAAAGCAGGCTCCGAATTGgtatcacgaggcagaatttcagataaaaaaaatCCTTAGCTTTCGCTAAGGATCTGAAGTGgaattcatgA", "plasmid", "pth7035K_brp038")
	pLEFT = DNA("GATCTTTTATAGCTTGCTCAGTCCTAGGTACAATGCTTGCTACCTAGTAGACATAAAAACGGCAAAGTATGagcacaaaaaagaaaccattaacacaagagcagcttgaggacgcacgtcgccttaaagcaatttatgaaaaaaagaaaaatgaacttggcttatcccaggaatctgtcgcagacaagatggggatggggcagtcaggcgttggtgctttatttaatggcatcaatgcattaaatgcttataacgccgcattgcttgcaaaaattctcaaagttagcgttgaagaatttagcccttcaatcgccagagaaatctacgagatgtatgaagcggttagtatgcagccgtcacttagaagtgagtatgagtaccctgttttttctcatgttcaggcagggatgttctcacctgagcttagaacctttaccaaaggtgatgcggagagatgggtaagcacagctagcgagaccagtccggaaagtgaaacgtgatttcatgcgtcattttgaacattttgtaaatcttatttaataatgtgtgcggcaattcacatttaatttatgaatgttttcttaacatcgcggcaactcaagaaacggcaggttcGGATCTtagctactagagaaagaggagaaatactagatgcgtaaaggcgaagagctgttcactggtgtcgtccctattctggtggaactggatggtgatgtcaacggtcataagttttccgtgcgtggcgagggtgaaggtgacgcaactaatggtaaactgacgctgaagttcatctgtactactggtaaactgccggtaccttggccgactctggtaacgacgctgacttatggtgttcagtgctttgctcgttatccggaccatatgaagcagcatgacttcttcaagtccgccatgccggaaggctatgtgcaggaacgcacgatttcctttaaggatgacggcacgtacaaaacgcgtgcggaagtgaaatttgaaggcgataccctggtaaaccgcattgagctgaaaggcattgactttaaagaagacggcaatatcctgggccataagctggaatacaattttaacagccacaatgtttacatcaccgccgataaacaaaaaaatggcattaaagcgaattttaaaattcgccacaacgtggaggatggcagcgtgcagctggctgatcactaccagcaaaacactccaatcggtgatggtcctgttctgctgccagacaatcactatctgagcacgcaaagcgttctgtctaaagatccgaacgagaaacgcgatcatatggttctgctggagttcgtaaccgcagcgggcatcacgcatggtatggatgaactgtacaaatgaagtccgggtctcGGATCCACTGGCCGTCGTTTTACACctaggtgctcaaaaagacgccaaaagggcgctgttatctgataaggcttatctggtatcattttgcgaggtctgggtcacattttaattttcggtagtacgtcgctcgactgatgcctaatgcctcccacggtttcagcgaacgtgctgatgtaggaactgctgcgcgcttagatttagttccgcccttgcgaccgcgagcggcctgtacagcggaaaatccctctggtgagaatttcctgtgtgtatatttcgcaatgctcttgccaatagcccgacattcagccggagaaagcggaacgggaagcgaagcgttgtacatttcgacacgctggataacggcatcaagccattgtgagaatacaggccagccctgacgaatcgctctgtaggcccatttacggaccttttcgaacagatggtagtttcgccccagcccgtaatttttatcgacgctacggcgcgctgaggcgtactcgaggattatcaaaaaggatcttcacctagatccttttaaattaaaaatgaagttttaaatcaatctaaagtatatatgagtaaacttggtctgacagttaccaatgcttaatcagtgaggcacctatctcagcgatctgtctatttcgttcatccatagttgcctgactccccgtcgtgtagataactacgatacgggagggcttaccatctggccccagtgctgcaatgataccgcgggacccacgctcaccggctccagatttatcagcaataaaccagccagccggaagggccgagcgcagaagtggtcctgcaactttatccgcctccatccagtctattaattgttgccgggaagctagagtaagtagttcgccagttaatagtttgcgcaacgttgttgccattgctacaggcatcgtggtgtcacgctcgtcgtttggtatggcttcattcagctccggttcccaacgatcaaggcgagttacatgatcccccatgttgtgcaaaaaagcggttagctccttcggtcctccgatcgttgtcagaagtaagttggccgcagtgttatcactcatggttatggcagcactgcataattctcttactgtcatgccatccgtaagatgcttttctgtgactggtgagtactcaaccaagtcattctgagaatagtgtatgcggcgaccgagttgctcttgcccggcgtcaatacgggataataccgcgccacatagcagaactttaaaagtgctcatcattggaaaacgttcttcggggcgaaaactctcaaggatcttaccgctgttgagatccagttcgatgtaacccactcgtgcacccaactgatcttcagcatcttttactttcaccagcgtttctgggtgagcaaaaacaggaaggcaaaatgccgcaaaaaagggaataagggcgacacggaaatgttgaatactcatactcttcctttttcaatattattgaagcatttatcagggttattgtctcatgagcggatacatatttgaatgtatttagaaaaataaacaaataggggttccgcgcacatttccccgaaaaGTGCCACCTGACGTCTAAGTCTAGAcGAGGAGtaatcaagtcagcaacttaaatagcctctaaggttttaagttttataagaaaaaaaagaatatataaggcttttaaagcttttaaggtttaacggttgtggacaacaagccagggatgtaacgcactgagaagcccttagagcctctcaaagcaattttgagtgacacaggaacacttaacggctgacatgggaattagccatgggcccgtgcgaatcaccctaggTGTAAAACGACGGCCAGTCTTAAGCTCGGGCCCCAAATAATGATTTTATTTTGACTGATAGTGACCTGTTCGTTGCAACAAATTGATGAGCAATGCTTTTTTATAATGCCAACTTTGTACAAAAAAGCAGGCTCCGAATTGgtatcacgaggcagaatttcagataaaaaaaatCCTTAGCTTTCGCTAAGGATCTGAAGTGgaattcatgA", "plasmid", "pLEFT")
	pRIGHT = DNA("gctagcgagaccagtccggaaagtgaaacgtgatttcatgcgtcattttgaacattttgtaaatcttatttaataatgtgtgcggcaattcacatttaatttatgaatgttttcttaacatcgcggcaactcaagaaacggcaggttcGGATCTtagctactagagaaagaggagaaatactagatgcgtaaaggcgaagagctgttcactggtgtcgtccctattctggtggaactggatggtgatgtcaacggtcataagttttccgtgcgtggcgagggtgaaggtgacgcaactaatggtaaactgacgctgaagttcatctgtactactggtaaactgccggtaccttggccgactctggtaacgacgctgacttatggtgttcagtgctttgctcgttatccggaccatatgaagcagcatgacttcttcaagtccgccatgccggaaggctatgtgcaggaacgcacgatttcctttaaggatgacggcacgtacaaaacgcgtgcggaagtgaaatttgaaggcgataccctggtaaaccgcattgagctgaaaggcattgactttaaagaagacggcaatatcctgggccataagctggaatacaattttaacagccacaatgtttacatcaccgccgataaacaaaaaaatggcattaaagcgaattttaaaattcgccacaacgtggaggatggcagcgtgcagctggctgatcactaccagcaaaacactccaatcggtgatggtcctgttctgctgccagacaatcactatctgagcacgcaaagcgttctgtctaaagatccgaacgagaaacgcgatcatatggttctgctggagttcgtaaccgcagcgggcatcacgcatggtatggatgaactgtacaaatgaagtccgggtctcgGATCCtaaCTCGCTCaggcttcctcgctcactgactcgctgcgctcggtcgttcggctgcggcgagcggtatcagctcactcaaaggcggtaatCAATTCGACCCAGCTTTCTTGTACAAAGTTGGCATTATAAAAAATAATTGCTCATCAATTTGTTGCAACGAACAGGTCACTATCAGTCAAAATAAAATCATTATTTGCCATCCAGCTGATATCCCCTATAGTGAGTCGTATTACATGGTCATAGCTGTTTCCTGGCAGCTCTGGCCCGTGTCTCAAAATCTCTGATGTTACATTGCACAAGATAAAAATATATCATCATGCTCTAGAgtgttacaaccaattaaccaattctgattagaaaaactcatcgagcatcaaatgaaactgcaatttattcatatcaggattatcaataccatatttttgaaaaagccgtttctgtaatgaaggagaaaactcaccgaggcagttccataggatggcaagatcctggtatcggtctgcgattccgactcgtccaacatcaatacaacctattaatttcccctcgtcaaaaataaggttatcaagtgagaaatcaccatgagtgacgactgaatccggtgagaatggcaaaagcttatgcatttctttccagacttgttcaacaggccagccattacgctcgtcatcaaaatcactcgcatcaaccaaaccgttattcattcgtgattgcgcctgagcgagacgaaatacgcgatcgctgttaaaaggacaattacaaacaggaatcgaatgcaaccggcgcaggaacactgccagcgcatcaacaatattttcacctgaatcaggatattcttctaatacctggaatgctgttttcccggggatcgcagtggtgagtaaccatgcatcatcaggagtacggataaaatgcttgatggtcggaagaggcataaattccgtcagccagtttagtctgaccatctcatctgtaacatcattggcaacgctacctttgccatgtttcagaaacaactctggcgcatcgggcttcccatacaatcgatagattgtcgcacctgattgcccgacattatcgcgagcccatttatacccatataaatcagcatccatgttggaatttaatcgcggcctggagcaagacgtttcccgttgaatatggctcataacaccccttgtattactgtttatgtaagcagacagttttattgttcatgatgatatatttttatcttgtgcaatgtaacatcagagattttgagacacaacgtggctttgttgaataaatcgaacttttgctgagttgaaggatcagCTCGAGaGCAGTTCAACCTGTTGATAGtacgtactaagctctcatgtttcacgtactaagctctcatgtttaacgtactaagctctcatgtttaacgaactaaaccctcatggctaacgtactaagctctcatggctaacgtactaagctctcatgtttcacgtactaagctctcatgtttgaacaataaaattaatataaatccttgattaCTCCTCaTATAGAGCGCCTCAGCGCGCcgtagcgtcgataaaaattacgggctggggcgaaactaccatctgttcgaaaaggtccgtaaatgggcctacagagcgattcgtcagggctggcctgtattctcacaatggcttgatgccgttatccagcgtgtcgaaatgtacaacgcttcgcttcccgttccgctttctccggctgaatgtcgggctattggcaagagcattgcgaaatatacacacaggaaattctcaccagagggattttccgctgtacaggccgctcgcggtcgcaagggcggaactaaatctaagcgcgcagcagttcctacatcagcacgttcgctgaaaccgtgggaggcattaggcatcagtcgagcgacgtactaccgaaaattaaaatgtgacccagacctcgcaaaataagaccagataagccttatcagataacagcgcccttttggcgtctttttgagcacctaggTGTAAAACGACGGCCAGTT", "plasmid", "pLEFT")
	prod1 = PCR(olib001, olib002, pth7035K_nd033)
	print "PCR Product:"
	prod1.prettyPrint()
	ins = Digest(prod1, [EnzymeDictionary["BsaI"]])
	print 'Insert DNA Digest:'
	for insert in ins:
		insert.prettyPrint()
	vec_digest = Digest(pLEFT, [EnzymeDictionary["BsaI"]])
	#Gel purify large band for vec, and pcr purify for ins
	vec = GelAndZymoPurify(vec_digest,'L')
	print "===> Vector Digest:"
	for v in vec:
		v.prettyPrint()
	jtk161 = Strain("jtk161", "pUC,P15A,ColE2", "", )
	
	ligation_products = Ligate(ins+vec)
	print 'Ligation Products:'
	for l in ligation_products:
		l.prettyPrint()

	LIB002_LEFT_RND1 = TransformPlateMiniprep(ligation_products, jtk161, "Amp")
	#product should be TAAAGGTCTCGCTAGCGGTAGCGGCAGTAGTGCCAATGAAAAcaacctgatttggatcgatcttgagatgaccggtctggatcccgagcgcgatcgcattattgagattgccacgctggtgaccgatgccnnknnkaatattctggcagaagggccgaccattgcagtacaccagtctgatgaacagctggcgctgatggatgactggaacgtgcgcacccataccgccagcgggctggtagagcgcgtgaaagcgagcacgatgggcgatcgggaagctgaactggcaacgctcgaatttttaaaacagtgggtgcctgcgggaaaatcgccgatttgcggtaacagcatcggtcaggaccgtcgtttcctgtttaaatacatgccggagctggaagcctacttccactaccgttatctcgatgtcagcaccctgaaagagnnkgcgcgccgcnnkAAGCCGGAAATTCTGGATGGTTAGGCATCTCCTCGGATCCGAGACCTTT
	#inside the pth7035K vector (nhei/bamhi positions)
	print 'Miniprep product:'
	LIB002_LEFT_RND1[0].prettyPrint()
	prod2 = PCR(olib003, olib004, LIB002_LEFT_RND1[0])
	print 'Final amplification product:'
	prod2.prettyPrint()
