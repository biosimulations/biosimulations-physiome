# Gs protein module following Saucerman and Iancu: act1 and act2 with LR
# and LRG as substrates (G is already bound, so there is only one substrate
# to each act reaction)

# Gs is associated with B1AR proteins

#     return (k_kinetic, N_cT, K_C, W) kinetic parameters, constraints, and vector of volumes in each
# compartment (pL) (1 if gating variable, or in element corresponding to
# kappa)

# 14Oct21: adding phosphate binding reaction to RG and LRG as separate
# reactions. Only RG_Pi and LRG_Pi proceed to Act reactions. 

import numpy as np 

def kinetic_parameters(M, include_type2_reactions, dims, V):
    # Set the kinetic rate constants.
    # original model had reactions that omitted enzymes as substrates e.g. BARK
    # convert unit from 1/s to 1/uM.s by dividing by conc of enzyme
    # all reactions were irreversible, made reversible by letting kr ~= 0

    num_cols = dims['num_cols']
    num_rows = dims['num_rows']

    bigNum = 1e3
    fastKineticConstant = bigNum
    smallReverse = fastKineticConstant/(pow(bigNum,2))

    k_Doff1p = fastKineticConstant
    k_Doff1m = smallReverse
    k_Ton1p = fastKineticConstant
    k_Ton1m = smallReverse
    k_Doff2p = fastKineticConstant
    k_Doff2m = smallReverse
    k_Ton2p = fastKineticConstant
    k_Ton2m = smallReverse
    kAct1p = 16                 # 1/s
    kAct1m = smallReverse           # 1/s            
    kAct2p = 16                 # 1/s
    kAct2m = smallReverse           # 1/s            
    kHydp = 0.8                    # 1/s      
    kHydm = smallReverse           # 1/s
    kReassocp = 1.21e3             # 1/uM.s
    kReassocm = kReassocp/bigNum   # 1/s
    # phosphorylation of GDP by NDPK (nucleoside diphosphate kinase) - omitting MM enzyme
    kPiPhosp = fastKineticConstant
    kPiPhosm = smallReverse

    # ensure that the closed loop formed by Act1 & Act2 obey detailed
    # balance
    kAct2m = kAct1m * kAct2p / kAct1p
    # CLOSED LOOP involving G - aGTP - aGDP - G
    # use detailed balance to find kReasocm with either Act (as they have
    # same equilibrium constant
    if True:
        kReassocm = kAct1p*kHydp*kReassocp/(kAct1m*kHydm)
    

    k_kinetic = [
        k_Doff1p, k_Ton1p, kAct1p, k_Doff2p, k_Ton2p, kAct2p, kHydp, kReassocp, #kPiPhosp,
        k_Doff1m, k_Ton1m, kAct1m, k_Doff2m, k_Ton2m, kAct2m, kHydm, kReassocm #,kPiPhosm
        ]

    # CONSTRAINTS
    N_cT = []
    
    # LR.G = aGTP.betaGamma
    if False:                                                          
        N_cT[1][num_cols + 2] = 1
        N_cT[1][num_cols + 3] = 1
        N_cT[1][num_cols + 4] = -1
        N_cT[1][num_cols + 5] = -1
    
    # [a-GTP] + [a-GDP] = [beta.gamma]                              **SMALL_ERROR**
    if True:
        N_cT = np.zeros(len(M[0]))
        N_cT[num_cols + 6] = 1   # beta_gamma
        N_cT[num_cols + 5] = -1  # a_GTP
        N_cT[num_cols + 7] = -1  # a_GDP

    K_C = [1]

    # volume vector
    W = list(np.append([1] * num_cols, [V['V_myo']] * num_rows))

    return (k_kinetic, [N_cT], K_C, W) 











