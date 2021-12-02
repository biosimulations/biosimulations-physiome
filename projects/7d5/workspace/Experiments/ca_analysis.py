import numpy as np
# import scipy as sp
from scipy.integrate import cumtrapz
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

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
    plt.figure(figsize= (14,8))
    plt.subplot(1,2,1)
    plt.plot((time[inds1:inds2] - time[inds1])/ 1000, Ca[inds1: inds2]*1e6, color= 'red')
    plt.xlim(0, 1, 0.2)
    plt.title('A', fontsize=18)
    plt.ylabel('[Ca$^{2+}$] (nM)')
    plt.xlabel('Time (ms)')
    # plt.show()

    # % % plot figure 10 C
    plt.subplot(1,2,2)
    plt.plot((Time_flux - time[inds1]), fluxJserca_norm)
    plt.plot((Time_flux-time[inds1]), fluxIncx_ca_norm, color= 'red')
    plt.plot((Time_flux-time[inds1]), fluxIpca_norm, color= 'orange')
    plt.xlim(0, 1000, 200)
    plt.title('B', fontsize=18)

    plt.ylabel('Ca flux normalized')
    plt.xlabel('Time (ms)')

    # plt.show()
    plt.savefig('Figure10.png')

    return None
