# This script calculates the bond graph parameters for all reactions of the
# a given module. Specify the directory.
# based on SERCA model of Pan et al, which is based on Tran et al. (2009). 
# Parameters calculated in module's directory, by using the kinetic
# parameters and stoichiometric matrix.

# 19 Jul INITIAL CONDITIONS
# given dq/dt = A.q + c where A is a square matrix, use null(A) to find ICs
# of q. 
# A is constructed from linearising equations through lm, and
# contains BG parameters 
# K kappa are contained in c, but disregarding this
# as this is not dependent on q.

# return W from kinetic_parameters

import os
import csv
import json
import math
import numpy as np
import sympy
from scipy.linalg import null_space
from kinetic_parameters_cAMP import kinetic_parameters


def read_IDs(path):
    data = []
    with open(path,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
    return data


def load_matrix(stoich_path):
    matrix = []
    with open(stoich_path,'r') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            matrix.append([int(r) for r in row])
        f.close()
    return matrix


if __name__ == "__main__":

    ## booleans
    write_parameters_file = True
    include_constraints = True
    include_type2_reactions = True

    ## Set directories
    current_dir = os.getcwd()
    data_dir = current_dir + '\data'
    output_dir = current_dir + '\output'
    modname = os.path.dirname(current_dir).split('\\')[-1].split('_')[-1]

    if ('beta1' in current_dir) and False:
        matstr = '_withR_LR_scheme4'
    else:
        matstr = ''

    ## Define volumes
    V_myo = 34.4 # pL
    V = dict()
    V['V_myo'] = V_myo

    ## Load forward matrix
    if include_type2_reactions:
        stoich_path = data_dir + '\\all_forward_matrix%s.txt'%matstr
    else:
        stoich_path = data_dir + '\\all_noType2_forward_matrix.txt'

    N_f = load_matrix(stoich_path)


    ## Load reverse matrix
    if include_type2_reactions:
        stoich_path = data_dir + '\\all_reverse_matrix%s.txt'%matstr
    else:
        stoich_path = data_dir + '\\all_noType2_reverse_matrix.txt'
    
    N_r = load_matrix(stoich_path)

    N_fT = np.transpose(N_f)
    N_rT = np.transpose(N_r)

    ## Calculate stoichiometric matrix
    # I matrix to align with placement of kappa down the column.
    # x-axis of stoich matrix (R1a, R1b etc) coincides with the kp km of that kinetic reaction
    N = [[N_r[j][i] - N_f[j][i] for i in range(len(N_f[0]))] for j in range(len(N_f))]
    N_T = [[N_rT[j][i] - N_fT[j][i] for i in range(len(N_fT[0]))] for j in range(len(N_fT))]

    num_rows = len(N)
    num_cols = len(N[0])
    dims = dict()
    dims['num_rows'] = num_rows
    dims['num_cols'] = num_cols

    I = np.identity(num_cols)

    M = np.append(np.append(I, N_fT,1), np.append(I, N_rT,1),0)

    # addpath(current_dir)
    # addpath(data_dir)
    [k_kinetic, N_cT, K_C, W] = kinetic_parameters(M, include_type2_reactions, dims, V) ################
    if not include_constraints:
        N_cT = []

    try:
        M = np.append(M, N_cT,0)
        k = np.append(k_kinetic, K_C, 0)
    except:
        k = k_kinetic

    # Calculate bond graph constants from kinetic parameters
    # Note: units of kappa are fmol/s, units of K are fmol^-1
    lambda_expo = np.matmul(np.linalg.pinv(M), [math.log(ik) for ik in k])
    lambdaW = [math.exp(l) for l in lambda_expo]


    # Check that kinetic parameters are reproduced by bond graph parameters
    k_est = np.matmul(M,[math.log(k) for k in lambdaW])
    k_est = [math.exp(k) for k in k_est]
    diff = [(k[i] - k_est[i])/k[i] for i in range(len(k))]

    error = np.sum([abs(d) for d in diff])


    # Check that there is a detailed balance constraint
    Z = null_space(np.transpose(M))

    N_rref = sympy.Matrix(N).rref()
    R_mat = null_space(N)
    kf = k_kinetic[:num_cols]
    kr = k_kinetic[num_cols:]
    K_eq = [kf[i]/kr[i] for i in range(len(kr))]
    zero_est = np.matmul(np.transpose(R_mat),K_eq)
    zero_est_log = np.matmul(np.transpose(R_mat),[math.log(k) for k in K_eq])

    # if not R_mat:
    #     warning('R_mat is empty: matrix is full rank')
    
    lambdak = [lambdaW[i]/W[i] for i in range(len(W))]
    kappa = lambdak[:len(N[0])]
    K = lambdak[len(N[0]):]

    rxnID = read_IDs('data\\rxnID.txt')
    Kname = read_IDs('data\\Kname.txt')


    # ### print outputs ###
    for ik in range(len(kappa)):
        print('var kappa_%s: fmol_per_sec {init: %g, pub: out};' %(rxnID[ik],kappa[ik]))
    for ik in range(len(Kname)):
        print('var K_%s: per_fmol {init: %g, pub: out};' %(Kname[ik],K[ik]))

    file = open(output_dir + '/all_parameters_out.json', 'w')
    data = { "K": K, "kappa": kappa, "k_kinetic": k_kinetic }
    json.dump(data, file)


    if True:
        if False:
            for j in range(len(K)):
                print('var q_%s: fmol {init: 1e-13};'%Kname[j])
            for j in range(len(kappa)):
                print('var v%s: fmol_per_sec;'%rxnID[j])
            for j in range(len(K)):
                print('var mu_%s: J_per_mol;'%Kname[j])
            for j in range(len(kappa)):
                print('v%s = kappa_%s*exp(mu_a/(R*T));'%rxnID[j], rxnID[j])
            for j in range(len(K)):
                print('ode(q_%s, time) = p;'%Kname[j])
        print('\n')
        print('// Global value')
        for j in range(len(K)):
            print('var q_%s: fmol {pub: out};'%Kname[j])
        print('// From submodule')
        for j in range(len(K)):
            print('var q_%s_m%s: fmol {pub: in};'%(Kname[j], modname))

        for j in range(len(K)):
            print('q_%s = q_%s_m%s + q_%s_init;'%(Kname[j], Kname[j],
                modname,Kname[j]))
        print('\n')
        print('// Input from global environment')
        for j in range(len(K)):
            print('var q_%s_global: fmol {pub: in};'%Kname[j])
        print('// Output to global environment')
        for j in range(len(K)):
            print('var q_%s: fmol {init: 1e-16, pub: out};'%(Kname[j]))
        
        for j in range(len(K)):
            print('mu_%s = R*T*ln(K_%s*q_%s_global);'%(Kname[j],Kname[j],Kname[j]))
        print('\n')
        print('def map between environment and %s for'%modname)
        print('vars time and time;')
        for j in range(len(K)):
            print('vars q_%s_m%s and q_%s;'%(Kname[j], modname,Kname[j]))
            print('vars q_%s and q_%s_global;'%(Kname[j], Kname[j]))
        print('enddef;')



