import os
import math
import numpy as np
import matplotlib
matplotlib.use('agg')
import scipy
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from  ca_analysis import ca_analysis
import opencor as opencor
import timeit

# start = timeit.default_timer()
# root = "C:/Nima/ABI/Physiome Journal/pluripotent stem cell/src/cellml/Channels/"


def load_sedml(filename):
    return opencor.open_simulation(filename)

def get_data(filename):
    data = filename.data()
    data.set_ending_point(10)
    data.set_point_interval(1)
    return data

#

file = load_sedml("Channels.sedml")
data = get_data(file)


def sim_ik1(k_new, vm):
    # ik1_list = []


    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/k_new"] = k_new
    data.constants()["main/protocol"] = 0
    data.constants()["main/v"] = vm
    file.run()
    ds = file.results().data_store()
    ik1 = ds.voi_and_variables()["main/i_k1"].values()[0]

    return ik1

##
def sim_ikr(k_new, vm, X_kr_act, X_kr_inact):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_kr_act"] = X_kr_act
    data.constants()["main/X_kr_inact"] = X_kr_inact
    data.constants()["main/k_new"] = k_new
    data.constants()["main/v"] = vm
    data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_kr_act = ds.voi_and_variables()["main/dX_kr_act"].values()[0]
    dX_kr_inact = ds.voi_and_variables()["main/dX_kr_inact"].values()[0]
    ikr = ds.voi_and_variables()["main/i_Kr"].values()[0]

    return dX_kr_act, dX_kr_inact, ikr

##
def sim_iks(k_new, vm, X_ks_act):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_ks_act"] = X_ks_act

    data.constants()["main/k_new"] = k_new
    data.constants()["main/v"] = vm
    data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_ks_act = ds.voi_and_variables()["main/dX_ks_act"].values()[0]

    iks = ds.voi_and_variables()["main/i_Ks"].values()[0]

    return dX_ks_act, iks
##

def sim_ito(k_new, vm, X_to_act, X_to_inact):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_to_act"] = X_to_act
    data.constants()["main/X_to_inact"] = X_to_inact
    data.constants()["main/k_new"] = k_new
    data.constants()["main/v"] = vm
    data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_to_act = ds.voi_and_variables()["main/dX_to_act"].values()[0]
    dX_to_inact = ds.voi_and_variables()["main/dX_to_inact"].values()[0]
    ito = ds.voi_and_variables()["main/i_to"].values()[0]

    return dX_to_act, dX_to_inact, ito
##

def sim_ica(k_new, vm, ca_i, Na_i, X_ca_act, X_ca_inact, X_fca_inact):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_ca_act"] = X_ca_act
    data.constants()["main/X_ca_inact"] = X_ca_inact
    data.constants()["main/X_fca_inact"] = X_fca_inact
    data.constants()["main/k_new"] = k_new
    data.constants()["main/v"] = vm
    data.constants()["main/ca_i"] = ca_i
    data.constants()["main/Na_i"] = Na_i
    # data.constants()["main/K_i"] = K_i
    data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_ca_act = ds.voi_and_variables()["main/dX_ca_act"].values()[0]
    dX_ca_inact = ds.voi_and_variables()["main/dX_ca_inact"].values()[0]
    dX_fca_inact = ds.voi_and_variables()["main/dX_fca_inact"].values()[0]
    iCaL = ds.voi_and_variables()["main/i_CaL"].values()[0]
    ibarca = ds.voi_and_variables()["main/ibarca"].values()[0]
    ibarna = ds.voi_and_variables()["main/ibarna"].values()[0]
    ibark = ds.voi_and_variables()["main/ibark"].values()[0]

    return dX_ca_act, dX_ca_inact, dX_fca_inact, iCaL, ibarca, ibarna, ibark

##
def sim_icat(vm, X_cat_act, X_cat_inact):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_cat_act"] = X_cat_act
    data.constants()["main/X_cat_inact"] = X_cat_inact
    # data.constants()["main/k_new"] = k_new
    # data.constants()["main/Cai"] = Cai
    data.constants()["main/v"] = vm
    # data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_cat_act = ds.voi_and_variables()["main/dX_cat_act"].values()[0]
    dX_cat_inact = ds.voi_and_variables()["main/dX_cat_inact"].values()[0]
    i_cat = ds.voi_and_variables()["main/i_cat"].values()[0]

    return dX_cat_act, dX_cat_inact, i_cat
##

def sim_ina(vm, X_na_h_inact, X_na_j_inact, X_na_m_act):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_na_m_act"] = X_na_m_act
    data.constants()["main/X_na_h_inact"] = X_na_h_inact
    data.constants()["main/X_na_j_inact"] = X_na_j_inact
    # data.constants()["main/k_new"] = k_new
    data.constants()["main/v"] = vm
    # data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_na_m_act = ds.voi_and_variables()["main/dX_na_m_act"].values()[0]
    dX_na_h_inact = ds.voi_and_variables()["main/dX_na_h_inact"].values()[0]
    dX_na_j_inact = ds.voi_and_variables()["main/dX_na_j_inact"].values()[0]
    ina = ds.voi_and_variables()["main/i_na"].values()[0]

    return dX_na_h_inact, dX_na_j_inact, dX_na_m_act, ina

##

def sim_if(vm, X_f_act):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/X_f_act"] = X_f_act
    # data.constants()["main/k_new"] = k_new
    data.constants()["main/v"] = vm
    # data.constants()["main/protocol"] = 0
    file.run()
    ds = file.results().data_store()
    dX_f_act = ds.voi_and_variables()["main/dX_f_act"].values()[0]
    i_fNa = ds.voi_and_variables()["main/i_fNa"].values()[0]
    i_fK = ds.voi_and_variables()["main/i_fK"].values()[0]
    i_f = ds.voi_and_variables()["main/i_f"].values()[0]

    return dX_f_act, i_fNa, i_fK, i_f
##

def sim_inaca(vm, ca_i, Na_i):
    # ik1_list = []


    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/v"] = vm
    data.constants()["main/ca_i"] = ca_i
    data.constants()["main/Na_i"] = Na_i
    file.run()
    ds = file.results().data_store()
    inaca = ds.voi_and_variables()["main/i_naca"].values()[0]

    return inaca

def sim_inak(vm, Na_i):
    # ik1_list = []


    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/v"] = vm
    data.constants()["main/Na_i"] = Na_i
    file.run()
    ds = file.results().data_store()
    inak = ds.voi_and_variables()["main/i_nak"].values()[0]

    return inak


def sim_iup(ca_i):
    # ik1_list = []


    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/ca_i"] = ca_i
    file.run()
    ds = file.results().data_store()
    iup = ds.voi_and_variables()["main/i_up"].values()[0]

    return iup

def sim_leak(ca_SR, ca_i):
    # ik1_list = []


    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()
    data.constants()["main/ca_SR"] = ca_SR
    data.constants()["main/ca_i"] = ca_i
    file.run()
    ds = file.results().data_store()
    j_leak = ds.voi_and_variables()["main/j_leak"].values()[0]

    return j_leak


def sim_rel(ca_SR, ca_i, C, O, I):
    # ik1_list = []


    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()
    data.constants()["main/ca_SR"] = ca_SR
    data.constants()["main/ca_i"] = ca_i
    data.constants()["main/C"] = C
    data.constants()["main/O"] = O
    data.constants()["main/I"] = I
    file.run()
    ds = file.results().data_store()
    # CI = ds.voi_and_variables()["main/CI"].values()[0]
    dC = ds.voi_and_variables()["main/dC"].values()[0]
    dO = ds.voi_and_variables()["main/dO"].values()[0]
    dI = ds.voi_and_variables()["main/dI"].values()[0]
    j_rel = ds.voi_and_variables()["main/j_rel"].values()[0]

    return dC, dO, dI, j_rel

def sim_ibna(vm):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/v"] = vm
    file.run()
    ds = file.results().data_store()
    i_b_na = ds.voi_and_variables()["main/i_b_Na"].values()[0]

    return i_b_na

def sim_ibca(vm, ca_i):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/v"] = vm
    data.constants()["main/ca_i"] = ca_i
    file.run()
    ds = file.results().data_store()
    i_b_Ca = ds.voi_and_variables()["main/i_b_Ca"].values()[0]

    return i_b_Ca

def sim_ipca(ca_i):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    # data.constants()["main/v"] = vm
    data.constants()["main/ca_i"] = ca_i
    file.run()
    ds = file.results().data_store()
    i_PCa = ds.voi_and_variables()["main/i_PCa"].values()[0]

    return i_PCa

def sim_ca_sr(ca_SR, ca_i):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    # data.constants()["main/v"] = vm
    data.constants()["main/ca_SR"] = ca_SR
    data.constants()["main/ca_i"] = ca_i
    # data.constants()["main/i_up"] = i_up
    # data.constants()["main/j_rel"] = j_rel
    # data.constants()["main/j_leak"] = j_leak
    file.run()
    ds = file.results().data_store()
    Ca_SR_bufSR = ds.voi_and_variables()["main/Ca_SR_bufSR"].values()[0]

    return Ca_SR_bufSR

def sim_ca_buf(ca_i):
    # file = load_sedml(filename)
    file.reset(True)
    file.clear_results()

    data.constants()["main/ca_i"] = ca_i

    file.run()
    ds = file.results().data_store()
    Cai_buf = ds.voi_and_variables()["main/Cai_buf"].values()[0]

    return Cai_buf

##
def ipsc_function(time, Y):

    # differential equations for Kernik iPSC-CM model
    # solved by ODE15s in main_ipsc.m

    # State variable definitions:

    # %1: Vm (millivolt)
    #
    # % Ionic Flux: -------------------------------------------------------------
    # % 2: Ca_SR (millimolar)
    # % 3: Cai (millimolar)
    # % 4: Nai (millimolar)
    # % 5: Ki (millimolar)
    # % 6: Ca_ligand (millimolar)
    #
    # % Current Gating (dimensionless):------------------------------------------
    # % 7: d     (activation in i_CaL)
    # % 8: f1    (inactivation in i_CaL)
    # % 9: fCa   (calcium-dependent inactivation in i_CaL)
    # % 10: Xr1   (activation in i_Kr)
    # % 11: Xr2  (inactivation in i_Kr
    # % 12: Xs   (activation in i_Ks)
    # % 13: h    (inactivation in i_Na)
    # % 14: j    (slow inactivation in i_Na)
    # % 15: m    (activation in i_Na)
    # % 16: Xf   (inactivation in i_f)
    # % 17: s    (inactivation in i_to)
    # % 18: r    (activation in i_to)
    # % 19: dCaT (activation in i_CaT)
    # % 20: fCaT (inactivation in i_CaT)
    # % 21: R (in Irel)
    # % 22: O (in Irel)
    # % 23: I (in Irel)

    dY = np.zeros((len(Y), 1))

    # %Current parameter values:
    x_scale_conductance = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # x_K1 = np.array([0.133785777797606, 0.477994972217041, 27.2427558793487, 4.925023317814123,
    #                  8.72223760006882, 56.63619749982442])
    # x_KR = np.array([0.218025, 0.00574885237435, 13.623492636257568, 0.047630571181836,
    #                  -7.068087429655488, 0.012456640526827, -25.994458164437674, 37.342633150104064,
    #                  22.091964235390165, 50.0, 0.0])
    x_IKS = np.array([0.0077, 0.00116558448, 66726.83867589361, 0.28045890824999997,
                      -18.86697157291, 4.7411499999999995E-6])
    xTO = np.array([0.1178333333333, 0.055361418171300004, 11.6842023429669, 3.9891810803774996,
                    -11.0471393012032, 3.442309443E-4, -17.6344722898096, 186.76053690969502,
                    8.1809338733227, 0.6967584211715, 11.2244577239469])
    x_cal = np.array([0.308027691379, 12.966294189722, 7.0791459647109996, 0.044909415507,
                      -6.909880369242, 5.12589826E-4, -49.50571203387, 1931.211223514319,
                      5.730027499698999, 1.65824694683, 100.462559171103])
    x_cat = 0.185
    x_NA = np.array([9.720613409241, 108.04584638481799, 13.107015733941, 0.0023269143669999996,
                     -7.917726289513, 0.003626598864, -19.839358860026, 9663.294977114741,
                     7.395503564613, 5.122571819999999E-4, -66.583755502652, 0.031977580384,
                     0.167331502516, 0.951088724962])
    x_F = np.array([0.0435, 5.7897E-7, -14.589712170199999, 20086.650237884372, 10.202352845280002,
                    23.94529134653])
    #
    # %Flags:
    stim_flag = 0.0  # dimensionless (in stim_mode)
    voltageclamp = 0.0  # %square pulses if =1
    #
    # % -------------------------------------------------------------------------------
    # %%  Constants for flag protocols:
    #
    # % for stim:
    cyclelength = 800  # 1000ms = 1hz beating
    i_stim_Amplitude = 3  # pA/pF (in stim_mode)
    i_stim_End = 10e3  # milisecond (in stim_mode)
    i_stim_PulseDuration = 5  # milisecond (in stim_mode)
    i_stim_Start = 0  # milisecond (in stim_mode)
    #
    # % for square pulse voltage clamp:
    v_clamp_step = 0
    v_clamp_rest = -65
    steplength = 100
    R_clamp = 0.02
    # %-------------------------------------------------------------------------------
    # %% Cell geometry
    Cm = 60  # pF
    V_tot = 3960  # um^3
    Vc_tenT = 16404
    VSR_tenT = 1094
    V_tot_tenT = Vc_tenT + VSR_tenT  # V_total data from Hwang et al., V_c and V_SR  proportionally scaled from Ten Tusscher 2004 values
    Vc = V_tot * (Vc_tenT / V_tot_tenT)  # =3712.4 um^3 (93.7% total volume)
    V_SR = V_tot * (VSR_tenT / V_tot_tenT)  # =247.6 um^3 (6.3% total volume)
    #
    # % -------------------------------------------------------------------------------
    # %% Constants
    T = 310.0  # kelvin (in model_parameters)'
    R = 8.314472  # joule_per_mole_kelvin (in model_parameters)
    F = 96.4853415  # coulomb_per_mmole (in model_parameters)
    Ko = 5.4  # millimolar (in model_parameters)
    Cao = 1.8  # millimolar (in model_parameters
    Nao = 140  # millimolar (in model_parameters)
    #
    # % -------------------------------------------------------------------------------
    # %% Reversal Potentials:
    E_Ca = 0.5 * R * T / F * np.log(Cao / Y[2])  # millivolt
    E_Na = R * T / F * np.log(Nao / Y[3])  # millivolt
    E_K = R * T / F * np.log(Ko / Y[4])  # millivolt
    #
    # % -------------------------------------------------------------------------------
    # %% Inward Rectifier K+ current (Ik1):
    #
    # results_file = "Channels-new1.sedml"
    # results = load_sedml(results_file)
    # data1 = get_data(results)
    i_K1 = sim_ik1(Y[4], Y[0])

    # %-------------------------------------------------------------------------------
    # %% Rapid Delayed Rectifier Current (Ikr):

    dY[9] = sim_ikr(Y[4], Y[0], Y[9], Y[10])[0]
    dY[10] = sim_ikr(Y[4], Y[0], Y[9], Y[10])[1]
    i_Kr = sim_ikr(Y[4], Y[0], Y[9], Y[10])[2]

    # %----------------------------------------------------------------------------
    # %% Slow delayed rectifier current (IKs):

    dY[11] = sim_iks(Y[4], Y[0], Y[11])[0]
    i_Ks = sim_iks(Y[4], Y[0], Y[11])[1]
    #
    #
    # %-------------------------------------------------------------------------------
    # %% Transient outward current (Ito):
    #

    dY[16] = sim_ito(Y[4], Y[0], Y[16], Y[17])[0]
    dY[17] = sim_ito(Y[4], Y[0], Y[16], Y[17])[1]
    i_to = sim_ito(Y[4], Y[0], Y[16], Y[17])[2]
    #
    # %-------------------------------------------------------------------------------
    # %% L-type Ca2+ current (ICaL):
    # %define parameters from x_cal

    dY[6] = sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[0]
    dY[7] = sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[1]
    dY[8] = sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[2]
    i_CaL = sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[3]
    i_CaL_Ca = (sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[4]) * Y[6] * Y[7] * Y[8]
    i_CaL_Na = (sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[5]) * Y[6] * Y[7] * Y[8]
    i_CaL_K = (sim_ica(Y[4], Y[0], Y[2], Y[3], Y[6], Y[7], Y[8])[6]) * Y[6] * Y[7] * Y[8]

    # %-------------------------------------------------------------------------------
    # %% T-type Calcium Current (ICaT):
    # %SAN T-TYPE CA2+ model (Demir et al., Maltsev-Lakatta ), G_CaT determined by fit to Kurokawa IV:

    dY[18] = sim_icat(Y[0], Y[18], Y[19])[0]
    dY[19] = sim_icat(Y[0],  Y[18], Y[19])[1]
    i_CaT = sim_icat(Y[0], Y[18], Y[19])[2]
    #
    # % -------------------------------------------------------------------------------
    # %% Sodium Current (INa):
    # %define parameters from x_Na

    dY[12] = sim_ina(Y[0], Y[12], Y[13], Y[14])[0]
    dY[13] = sim_ina(Y[0], Y[12], Y[13], Y[14])[1]
    dY[14] = sim_ina(Y[0], Y[12], Y[13], Y[14])[2]
    i_Na = sim_ina(Y[0], Y[12], Y[13], Y[14])[3]

    #
    # %-------------------------------------------------------------------------------%-------------------------------------------------------------------------------
    # %% Funny/HCN current (If):
    # %define parameters from x_F

    dY[15] = sim_if(Y[0], Y[15])[0]
    i_fNa = sim_if(Y[0], Y[15])[1]
    i_fK = sim_if(Y[0], Y[15])[2]
    i_f = sim_if(Y[0], Y[15])[3]
    #
    # %-------------------------------------------------------------------------------
    # %% Na+/Ca2+ Exchanger current (INaCa):
    # % Ten Tusscher formulation

    i_NaCa = sim_inaca(Y[0], Y[2], Y[3])


    # %% Na+/K+ pump current (INaK):
    # % Ten Tusscher formulation

    i_NaK = sim_inak(Y[0], Y[3])

    # %-------------------------------------------------------------------------------
    # %% SR Uptake/SERCA (J_up):
    # % Ten Tusscher formulation
    #

    i_up = sim_iup(Y[2])
    # %-------------------------------------------------------------------------------
    # %% SR Leak (J_leak):
    # % Ten Tusscher formulation

    i_leak = sim_leak(Y[1], Y[2])
    #
    # %-------------------------------------------------------------------------------
    # %% SR Release/RYR (J_rel):
    # % re-fit parameters. scaled to account for differences in calcium concentration in
    # % cleft (cleft is used in shannon-bers model geometry, not in this model geometry)

    dY[20] = sim_rel(Y[1], Y[2], Y[20], Y[21], Y[22])[0]
    dY[21] = sim_rel(Y[1], Y[2], Y[20], Y[21], Y[22])[1]
    dY[22] = sim_rel(Y[1], Y[2], Y[20], Y[21], Y[22])[2]
    i_rel = sim_rel(Y[1], Y[2], Y[20], Y[21], Y[22])[3]

    # % % Background Sodium(I_bNa):
    # % Ten Tusscher formulation

    i_b_Na = sim_ibna(Y[0])
    #
    # % -------------------------------------------------------------------------------
    # % % Background Calcium(I_bCa):
    # % Ten Tusscher formulation
    i_b_Ca = sim_ibca(Y[0], Y[2])
    #
    # % -------------------------------------------------------------------------------
    # % % Calcium SL Pump(I_pCa):
    # % Ten Tusscher formulation

    i_PCa = sim_ipca(Y[2])

    # % -------------------------------------------------------------------------------
    # % % 2: CaSR(millimolar)
    # % rapid equilibrium approximation equations - -not as formulated in ten Tusscher 2004 text

    Ca_SR_bufSR = sim_ca_sr(Y[1], Y[2])
    dY[1] = Ca_SR_bufSR * Vc / V_SR * (i_up - (i_rel + i_leak))
    #
    # % -------------------------------------------------------------------------------
    # % % 3: Cai(millimolar)
    # % rapid equilibrium approximation equations - - not as formulated in ten Tusscher 2004 text

    Cai_bufc = sim_ca_buf(Y[2])
    dY[2] = (Cai_bufc) * (
            i_leak - i_up + i_rel - dY[5] - (i_CaL_Ca + i_CaT + i_b_Ca + i_PCa - 2 * i_NaCa) * Cm / (2.0 * Vc * F))

    #
    # % -------------------------------------------------------------------------------
    # % % 4: Nai(millimolar)( in sodium_dynamics)
    dY[3] = -Cm * (i_Na + i_b_Na + i_fNa + 3.0 * i_NaK + 3.0 * i_NaCa + i_CaL_Na) / (F * Vc)
    #
    if stim_flag == 1:
        dY[3] = 0
    else:
        pass
    # end
    #
    # % -------------------------------------------------------------------------------
    # % % 5: Ki(millimolar)( in potatssium_dynamics)
    dY[4] = -Cm * (i_K1 + i_to + i_Kr + i_Ks + i_fK - 2.0 * i_NaK + i_CaL_K) / (F * Vc)
    #
    if stim_flag == 1:
        dY[4] = 0
    else:
        pass
    # end
    #
    # % -------------------------------------------------------------------------------
    # % % 1: Vm(Membrane voltage)
    #
    # % I_stim:
    if (time >= i_stim_Start) and (time <= i_stim_End) and (
            ((time - i_stim_Start - 100) % cyclelength) < i_stim_PulseDuration):
        i_stim = stim_flag * i_stim_Amplitude
    else:
        i_stim = 0.0
    # end
    #
    # % Voltage Clamp:
    if voltageclamp == 0:
        v_clamp = Y[0]  # set i_voltageclamp to 0
    elif voltageclamp == 1:  # train of square pulse:
        if (time % cyclelength) < cyclelength - steplength:
            v_clamp = v_clamp_rest
        else:
            v_clamp = v_clamp_step
    # end
    # end
    #
    i_voltageclamp = (v_clamp - Y[0]) / R_clamp
    #
    dY[0] = -(
            i_K1 + i_to + i_Kr + i_Ks + i_CaL + i_CaT + i_NaK + i_Na + i_NaCa + i_PCa + i_f + i_b_Na + i_b_Ca - i_stim - i_voltageclamp)
    dY = dY.flatten()

    currents = [i_K1, i_to, i_Kr, i_Ks, i_CaL, i_NaK, i_Na, i_NaCa, i_PCa, i_f, i_b_Na, i_b_Ca, i_rel, i_up, i_leak,
                i_stim, i_CaT]
    currents = np.asarray(currents)

    dY[23:] = currents

    return dY


#
# end


currents_init = np.zeros(17)
Y_init = np.array(
    [-75.59660163885468, 0.3350867967323261, 2.1919164242496442E-4, 7.169280912509992, 104.74882439411213, 0.0,
     3.9492534265292434E-4, 0.17099010558554026, 0.8777989461340886, 0.30976748571543317, 0.4505771851485186,
     0.15378828165094874, 0.7395436078124292, 0.12451598257450494, 0.02975499629264136, 0.006403385049126155,
     0.7468028106140061, 2.6759783334416056E-4, 2.701955734715772E-4, 0.7560329043683934, 0.01131203634337511,
     1.6504510531239642E-4, 0.014215362232301161])
# t = np.linspace(0, 3000)
# t = [0, 0.02, 0.04, 0.06, 0.26, 0.46, 0.66, 1.66, 2.66, 3.66, 4.66]
y0 = np.concatenate((Y_init, currents_init))
# scipy.integrate.ode(ipsc_function).set_integrator('vode', method='BDF', order=5)
sol = solve_ivp(ipsc_function, [0, 3e3], y0, method="BDF", first_step=2e-2, max_step=3.0)
values = sol.y[0:23]

time = sol.t
# print((sol.y[0:23]).shape)
print(time.shape)
# print(values)
vm = values[0, :]
# print(vm)
cai = values[2, :]
# print(cai)

# print(INaCa)
# print(len(values[0:]))

currents = sol.y[23:]
currents_list = np.zeros(17)

INaCa = np.zeros(time.shape)
IpCa = np.zeros(time.shape)
Iup = np.zeros(time.shape)


for t in range(0, currents.shape[1]):
    # print("Time: ", t)
    currents_new = np.concatenate((values[:,t], currents_list))
    update_step_i = ipsc_function(time[t], currents_new)
    update_step_i_new = update_step_i[23:]
    INaCa[t] = update_step_i_new[7]
    IpCa[t] = update_step_i_new[8]
    Iup[t] = update_step_i_new[13]

update_step_i_new = update_step_i[23:]


ca_analysis(time, Iup, INaCa, IpCa, cai)


# plt.plot(time, vm, color= 'red')
# plt.xlim(0,3000,500)
# # plt.show()
# plt.savefig('Figure11.png')
# # stop = timeit.default_timer()
# print('Time: ', stop - start)