# LRGbinding module - for muscarinic receptor as GPCR
# Based on Iancu 2007

#     return (k_kinetic, N_cT, K_C, W) kinetic parameters, constraints, and vector of volumes in each
# compartment (pL) (1 if gating variable, or in element corresponding to
# kappa)

import numpy as np 

def kinetic_parameters(M, include_type2_reactions, dims, V):
    # Set the kinetic rate constants.
    # original model had reactions that omitted enzymes as substrates e.g. BARK
    # convert unit from 1/s to 1/uM.s by dividing by conc of enzyme
    # all reactions were irreversible, made reversible by letting kr ~= 0
    
    num_cols = dims['num_cols']
    num_rows = dims['num_rows']

    # concentration of BARK = 0.6uM (crude approx from litsearch, for GRK)
    bigNum = 1e6
    fastKineticConstant = bigNum
    
    Ksig1 = 30    # uM  Kc
    Ksig2 = 0.16  # uM  Kh
    Ksig4 = 11    # uM  Kl
    ksig1p = fastKineticConstant
    ksig1m = ksig1p*Ksig1
    ksig2p = fastKineticConstant
    ksig2m = ksig2p*Ksig2
    ksig4p = fastKineticConstant
    ksig4m = ksig4p*Ksig4
    ksig3p = fastKineticConstant
    # find ksig4m using detailed balance
    ksig3m = ksig1m*ksig2m*ksig3p*ksig4p/(ksig1p*ksig2p*ksig4m)
        
    k_kinetic = [
        ksig1p, ksig2p, ksig3p, ksig4p,
        ksig1m, ksig2m, ksig3m, ksig4m
        ]

    # CONSTRAINTS
    N_cT = []
    K_C = []

    # volume vector
    W = list(np.append([1] * num_cols, [V['V_myo']] * num_rows))

    return (k_kinetic, [N_cT], K_C, W) 