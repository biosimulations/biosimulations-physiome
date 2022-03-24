import os
import math
import numpy as np
import matplotlib
matplotlib.use('agg')
import scipy
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import opencor as opencor

import timeit

start = timeit.default_timer()

def load_sedml(filename):
    return opencor.open_simulation(filename)


file = load_sedml("Channels.sedml")


print()


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


print()


plt.figure(figsize=(8, 5))
plt.plot(sim()[1], sim()[0], color= 'red', linewidth= 3)
plt.yticks(np.arange(-100, 51, 50))
plt.xticks(np.arange(0, 3001, 1000))
plt.xlim(0, 3000)
plt.ylim(-100, 50)
plt.xlabel('Time (ms)', fontsize= 18)
plt.ylabel('Voltage (mV)', fontsize= 18)
plt.tick_params(axis='both', labelsize='18')
plt.subplots_adjust(left=0.2,
                        bottom=0.2,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)

stop = timeit.default_timer()
print('Time: ', stop - start)
plt.savefig('Figure10.png')
