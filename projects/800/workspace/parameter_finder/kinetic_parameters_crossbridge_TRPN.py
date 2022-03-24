# crossbridge model from S.Land et al 2017

import numpy as np 

def kinetic_parameters(M, include_all_reactions, dims, V):
    # Set the kinetic rate constants.
    # all reactions are reversible. no closed loops.

    num_cols = dims['num_cols']
    num_rows = dims['num_rows']

    # CONVERT TO fM 
    bigNum = 1e6
    fastKineticConstant = bigNum
    smallReverse = fastKineticConstant/(pow(bigNum,2))

    rs = 0.25
    rw = 0.5

    k_TRPN_on = 100e3 # [=] 1/mM.s
    k_TRPN_off = 200  # [=] 1/s

    kBUm = 1e3      # [=] 1/s
    kBUp = kBUm/(1-rs-((1-rs)*rw)) # [=] 1/s
    kUWp = 26       # [=] 1/s
    kUWm = 170      # [=] 1/s
    kWSp = 4        # [=] 1/s
    kWSm = smallReverse # [=] 1/s
    kSUp = 18       # [=] 1/s

    # use detailed balance to find kSUm
    if True:
        kSUm = kUWp*kWSp*kSUp/(kUWm*kWSm)
    else:
        kSUm = smallReverse # [=] 1/s

    k_kinetic = [k_TRPN_on,kBUp,kUWp,kWSp,kSUp,
                k_TRPN_off,kBUm,kUWm,kWSm,kSUm]

    # CONSTRAINTS
    N_cT = []
    K_C = []
    
    # volume vector
    W = list(np.append([1] * num_cols, [V['V_myo']] * num_rows))

    return (k_kinetic, [N_cT], K_C, W)











