import os
import math
import numpy as np
import matplotlib
matplotlib.use('agg')
import scipy
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.integrate import cumtrapz
from scipy.interpolate import make_interp_spline
import opencor as opencor

import timeit

start = timeit.default_timer()

def load_sedml(filename):
    return opencor.open_simulation(filename)


file = load_sedml("Channels.sedml")


def sim ():
    # sedml file
    data = file.data()

    timespan = [0, 3e3]


    data.states()["main/v"] = -75.5966016388547
    data.states()["main/ca_SR"] = 0.3350867967323261
    data.states()["main/ca_i"] = 0.000219191642424964
    data.states()["main/Na_i"] = 7.16928091250999
    data.states()["main/Ki"] = 104.748824394112
    data.states()["main/ca_ligand"] = 0
    data.states()["main/X_ca_act"] = 0.000394925342652924
    data.states()["main/X_ca_inact"] = 0.170990105585540
    data.states()["main/X_fca_inact"] = 0.877798946134089
    data.states()["main/X_kr_act"] = 0.309767485715433
    data.states()["main/X_kr_inact"] = 0.450577185148519
    data.states()["main/X_ks_act"] = 0.153788281650949
    data.states()["main/X_na_h_inact"] = 0.739543607812429
    data.states()["main/X_na_j_inact"] = 0.124515982574505
    data.states()["main/X_na_m_act"] = 0.0297549962926414
    data.states()["main/X_f_act"] = 0.00640338504912616
    data.states()["main/X_to_inact"] = 0.746802810614006
    data.states()["main/X_to_act"] = 0.000267597833344161
    data.states()["main/X_cat_act"] = 0.000270195573471577
    data.states()["main/X_cat_inact"] = 0.756032904368393
    data.states()["main/C"] = 0.0113120363433751
    data.states()["main/O"] = 0.000165045105312396
    data.states()["main/I"] = 0.0142153622323012



    data.set_starting_point(timespan[0])
    data.set_ending_point(timespan[1])
    data.set_point_interval(1)
    file.run()
    ds = file.results().data_store()
    v = ds.voi_and_variables()["main/v"].values()
    Time_hold = (ds.voi_and_variables()["main/t"].values())
    INaCa = ds.voi_and_variables()["main/i_naca"].values()
    IpCa = ds.voi_and_variables()["main/i_PCa"].values()
    Iup = ds.voi_and_variables()["main/i_up"].values()
    cai = ds.voi_and_variables()["main/ca_i"].values()
    Cai_buf = ds.voi_and_variables()["main/Cai_buf"].values()
    i_leak = ds.voi_and_variables()["main/j_leak"].values()
    i_CaL = ds.voi_and_variables()["main/i_CaL"].values()


    return v, Time_hold, INaCa, IpCa, Iup, cai, Cai_buf, i_leak, i_CaL


sim()
time = sim()[1]
INaCa = sim()[2]
IpCa = sim()[3]
Iup = sim()[4]
cai = sim()[5]

def ca_analysis(time, Iup, INaCa, IpCa, Ca):
    # % Constants(copied from ipsc_function)
    V_tot = 3960 #% um ^ 3 from hwang et al.
    Vc_tenT = 16404
    VSR_tenT = 1094
    V_tot_tenT = Vc_tenT + VSR_tenT
    Vc = V_tot * (Vc_tenT / V_tot_tenT)
    Cm = 60 #% pF
    F = 96.4853415 #% coulomb_per_mmole( in model_parameters)

    # % % Find first beat to analyze
    inds_time_800 = np.where(time>800)[0][0]
    inds_time_1600 = np.where(time>1600)[0][0]

    inds1 = np.argmin(Ca[0:inds_time_800])
    inds2 = np.argmin(Ca[inds_time_800:inds_time_1600]) + inds_time_800

    # % % Calculate Normalized Ca2 + flux
    # % take integral
    intJserca = cumtrapz(Iup, time)
    intIncx_ca = cumtrapz(-INaCa * 2 * Cm / (2.0 * Vc * F), time)
    intIpca = cumtrapz(IpCa * Cm / (2.0 * Vc * F), time)

    # % integral for first beat
    fluxJserca = intJserca[inds1:inds2]-intJserca[inds1]
    fluxIncx_ca = intIncx_ca[inds1:inds2]-intIncx_ca[inds1]
    fluxIpca = intIpca[inds1:inds2]-intIpca[inds1]

    # % Normalize flux
    flux_total = fluxJserca + fluxIncx_ca + fluxIpca
    ref = np.amax(flux_total)
    fluxJserca_norm = fluxJserca / ref
    fluxIncx_ca_norm = fluxIncx_ca / ref
    fluxIpca_norm = fluxIpca / ref
    Time_flux = time[inds1:inds2]

    # % % plot figure 10A
    plt.figure(figsize= (14,7))
    plt.subplot(1,2,1)
    plt.plot((time[inds1:inds2] - time[inds1])/ 1000, Ca[inds1: inds2]*1e6, color= 'red', label= 'Baseline Model', linewidth = 4)

    plt.xticks(np.arange(0, 1.1, 0.5))
    plt.yticks(np.arange(0, 801, 200))
    plt.xlim(0, 1)
    plt.ylim(0, 800)
    plt.tick_params(axis='both', labelsize='18')
    plt.ylabel('[Ca$^{2+}$] (nM)', fontsize=18)
    plt.xlabel('Time (s)', fontsize=18)
    plt.legend(fontsize= '14', loc='best')
    plt.title('A', fontsize=18)
    # % % plot figure 10 C

    plt.subplot(1,2,2)
    plt.plot((Time_flux - time[inds1])/1000, fluxJserca_norm, color= 'blue', label= 'SERCA', linewidth = 4)
    plt.plot((Time_flux-time[inds1])/1000, fluxIncx_ca_norm, color= 'orangered', label= 'NCX', linewidth = 4)
    plt.plot((Time_flux-time[inds1])/1000, fluxIpca_norm, color= 'gold', label= 'non-NCX (SL-pump)', linewidth = 4)
    plt.xticks(np.arange(0, 1.1, 0.5))
    plt.yticks(np.arange(0, 8.1, 0.2))
    plt.xlim(0, 1)
    plt.ylim(0, 0.8)
    plt.tick_params(axis='both', labelsize='18')
    plt.title('B', fontsize=18)

    plt.ylabel('Ca$^{2+}$ flux normalized', fontsize = 18)
    plt.xlabel('Time (s)', fontsize = 18)
    plt.legend(fontsize='14', loc='best')

    plt.subplots_adjust(left=0.2,
                        bottom=0.2,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)

    plt.savefig('Figure10.png')
    return None

ca_analysis(time, Iup, INaCa, IpCa, cai)


stop = timeit.default_timer()
print('Time: ', stop - start)
plt.savefig('Figure09.png')
