
import numpy as np

def initialize_genetics(Na, n_loci = 5, n_alelles = [2], diploid = True):
    # Include groups
    # how should related individuals be realed genetically in the beginning of the simulation?
    # Implement if it is not diploid, 1 strain instead of 2

    if len(n_alelles) == 1:
        
        # structure is (number of individual, two strains, allele for each locus)
        genetics = np.random.random_integers(n_alelles[0], size = (Na, 2, n_loci))
        
    elif len(n_alelles) == n_loci:

        gen_rand = np.random.rand(Na, 2, n_loci)*n_alelles
        genetics = np.ceil(gen_rand).astype(np.int8)
    else:
        raise ValueError('There is some problem with the genetics structure. \
        Number of loci: '+str(n_loci)+'; Number of alleles:'+str(len(n_alleles)))
    
    return genetics


def reproduce_genetics(Nind, individual_id, individual_genetics, who_is_dad, who_is_mom):
    '''
    
    This is basen only on simple Mendelian genetics. But it is also possible to increment
    that to include mutations, recombination, and other microgenetic processes.
    
    Input: 
    Nind: int; offspring size.
    individual_genetics: genetics of all individuals before offsprings were born.
    who_is_dad: index of individuals who are dad of each cub.
    who_is_mom: index of individuals who are mom of each cub.
    '''
    
    # condition = not same zigot
    
    # Select indexes (0,1) for random alelle from fater and mother
    random_alelle_dad = np.random.randint(2, size=Nind)
    random_alelle_mom = np.random.randint(2, size=Nind)
    
    # Indexes of dads and mom
    #dad_index = np.in1d(individual_id, who_is_dad).nonzero()[0]
    #mom_index = np.in1d(individual_id, who_is_mom).nonzero()[0]
    dad_index = np.where(individual_id == who_is_dad[:,None])[1]
    mom_index = np.where(individual_id == who_is_mom[:,None])[1]
    
    # Sample these alelle strains
    a = individual_genetics[dad_index,random_alelle_dad]
    b = individual_genetics[mom_index,random_alelle_mom]
    
    # Concatenate and change the dimensions to (Ninds, 2 strains, n_alelles)
    new_inds_genetics = np.transpose(np.dstack((a,b)), axes = (0,2,1))
    
    # Return the array of genetics for the new individuals
    return new_inds_genetics