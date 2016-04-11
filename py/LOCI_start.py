import random

def LOCI_start(aux_loci_struc):
    '''
    This function defines the basic structure of the loci/alleles of individuals in a given simulation and randomly initializes
    the gene struture for an individual
    Input:
    - aux_loci_struc: list showing the genetic structure of an individual - loci and alleles per loci, 
      in the form: [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0],[0,0],[0,0,0,0,0,0]] 
      (the numbers inside brackets are not important, only the number of brackets and number of elements inside them)
    Output:
    - aux_LOCI: random genetic structure for an individual 
    '''
    
    number_of_loci=len(aux_loci_struc)
    aux_LOCI=[]
    for locus_ID in range(number_of_loci):
        locus_alleles = aux_loci_struc[locus_ID]
        aux_alleles=[]
        for allelle in range(len(locus_alleles)):
            random_value=random.uniform(0,1) # aqui da pra melhorar isso e colocar direto um random sample entre 0 e 1
            random_value_binary=int(round(random_value,0))
            aux_alleles.append(random_value_binary)
        aux_LOCI.append(aux_alleles)
    return aux_LOCI