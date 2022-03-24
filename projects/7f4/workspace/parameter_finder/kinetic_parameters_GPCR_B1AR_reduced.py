# Merged GPCR module, which is a combination of GsProtein and LRGbinding_B1AR.
# following Saucerman and Iancu: act1 and act2 with LR
# and LRG as substrates (G is already bound, so there is only one substrate
# to each act reaction)

# Gs is associated with B1AR proteins

#     return (k_kinetic, N_cT, K_C, W) kinetic parameters, constraints, and vector of volumes in each
# compartment (pL) (1 if gating variable, or in element corresponding to
# kappa)

# 14Oct21: adding phosphate binding reaction to RG and LRG as separate
# reactions. Only RG_Pi and LRG_Pi proceed to Act reactions. 

# 23nov21 removed RG + L -> LRG (sig2)
# 24nov21: merged Gs and GPCR binding
# 24nov21: adding receptor internalisation after aGTP has dissociated from the RG/LRG complex

import numpy as np 

def kinetic_parameters(M, include_type2_reactions, dims, V):
    # Set the kinetic rate constants.
    # original model had reactions that omitted enzymes as substrates e.g. BARK
    # convert unit from 1/s to 1/uM.s by dividing by conc of enzyme
    # all reactions were irreversible, made reversible by letting kr ~= 0

    num_cols = dims['num_cols']
    num_rows = dims['num_rows']

    bigNum = 1e6
    fastKineticConstant = bigNum
    smallReverse = 1/bigNum
    medReverse = np.sqrt(smallReverse)

    k_Rswitchp = fastKineticConstant
    k_Rswitchm = k_Rswitchp*0.01  # assume that only 1% of receptors are constitutionally active
    k_LRswitchp = fastKineticConstant
    k_LRswitchm = smallReverse

    KRc = 33    # uM  Kc
    KRL = 0.285 # uM  Kl
    KRr = 0.062 # uM  Kr
    kRcp = fastKineticConstant
    kRcm = kRcp*KRc
    kRrp = fastKineticConstant
    kRrm = kRrp*KRr
    # kRLp = fastKineticConstant
    # kRLm = kRLp*KRL
    kRL_actRp = fastKineticConstant
    kRL_actRm = kRL_actRp*KRL

    mult = 4e1
    kAct1p = 16*mult                 # 1/s
    kAct1m = smallReverse           # 1/s
    kAct2p = 16*mult                 # 1/s
    kAct2m = smallReverse           # 1/s
    kHydp = 0.8/mult                    # 1/s
    kHydm = smallReverse           # 1/s
    kReassocp = 1.21e3             # 1/uM.s
    kReassocm = smallReverse   # 1/s
    # RECEPTOR INTERNALISATION
    k_interRp = fastKineticConstant
    k_interRm = smallReverse
    k_interLRp = fastKineticConstant
    k_interLRm = smallReverse

    # ensure that the closed loop formed by Act1 & Act2 obey detailed balance
    # CLOSED LOOP involving G - aGTP - aGDP - G
    # use detailed balance to find kReasocm with either Act (as they have
    # same equilibrium constant
    if False:
        kAct2m = kAct1m * kAct2p / kAct1p
        kReassocm = kRcp*kAct1p*kHydp*kReassocp/(kRcm*kAct1m*kHydm)

    k_kinetic = [
        k_Rswitchp,k_LRswitchp,kRcp, kRrp, kRL_actRp, kAct1p, kAct2p, kHydp, kReassocp, k_interRp, k_interLRp,
        k_Rswitchm,k_LRswitchm,kRcm, kRrm, kRL_actRm, kAct1m, kAct2m, kHydm, kReassocm, k_interRm, k_interLRm
        ]

    # CONSTRAINTS
    N_cT = []
    K_C = []


    # [a-GTP] + [a-GDP] = [beta.gamma]                              **SMALL_ERROR**
    if False:
        N_cT = np.zeros(len(M[0]))
        N_cT[num_cols + 6] = 1   # beta_gamma
        N_cT[num_cols + 5] = -1  # a_GTP
        N_cT[num_cols + 7] = -1  # a_GDP
        K_C = [1]

    # volume vector
    W = list(np.append([1] * num_cols, [V['V_myo']] * num_rows))

    return (k_kinetic, [N_cT], K_C, W) 











