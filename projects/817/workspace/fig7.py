import os

import matplotlib
matplotlib.use('agg')

import numpy as np
import matplotlib.pyplot as plt

import opencor as opencor

import timeit

start = timeit.default_timer()

def load_sedml(filename):
    return opencor.open_simulation(filename)



start, stop, step = -150, 0, 2

Vm_plot = np.arange(start, stop + step, step)
Vm_plot = Vm_plot.reshape((1, Vm_plot.shape[0]))



def load_sedml(filename):
    return opencor.open_simulation(filename)

file = load_sedml("Current_If.sedml")


def run_sim1(Vm_step, protocol, g_f, xf_1, xf_2, xf_5, xf_6, xf_const):
    Y = np.array((-70, 0.1)).reshape(2, 1)
    print()

    if protocol == 1:
        period = [2000, 3000, 100]
        V1 = -35
        Vend = -125
    else:  # ma
        period = [2000, 2000, 100]
        V1 = -40
        Vend = -125

    col1 = V1 * np.ones(Vm_step.T.shape)
    col2 = Vm_step.T
    col3 = Vend * np.ones(Vm_step.T.shape)
    Vm_mat = np.hstack((col1, col2, col3))

    xy = 2  # variables in y

    values = np.zeros((sum(period) * 100, len(Vm_step.T) * xy))
    Time = sum(period) * np.ones((sum(period) * 100, len(Vm_step.T)))
    IF_IV = np.zeros(Vm_step.T.shape)
    x_act = np.zeros(Vm_step.T.shape)
    tau_act = np.zeros(Vm_step.T.shape)

    #sedml file
    data = file.data()

    for j in range(len(Vm_step.T)):
        print(j)
        Y_init = Y.flatten()

        for i in range(len(period)):
            Y_init[0] = Vm_mat[j, i].T
            if i == 0:
                Time_forVmi = 0
                timespan = [Time_forVmi, Time_forVmi + period[i]]
            else:
                timespan = [Time_forVmi[-1], Time_forVmi[-1] + period[i]]

            # file = load_sedml(filename)
            file.reset(True)
            file.clear_results()
            if protocol == 1:
                data.constants()["Current_If/Ki"] = 140
            else:
                data.constants()["Current_If/Ki"] = 150

            data.constants()["Current_If/Na_i"] = 5
            data.constants()["Current_If/Ko"] = 5.4
            data.constants()["Current_If/Nao"] = 135
            data.constants()["Current_If/g_f"] = g_f
            data.constants()["Current_If/xf_1"] = xf_1
            data.constants()["Current_If/xf_2"] = xf_2
            data.constants()["Current_If/xf_5"] = xf_5
            data.constants()["Current_If/xf_6"] = xf_6
            data.constants()["Current_If/xf_const"] = xf_const

            data.states()["Current_If/X_f_act"] = Y[1]
            # data.constants()["main/k_new"] = k_new
            data.states()["Current_If/v"] = Y_init[0]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(0.992063)
            file.run()
            ds = file.results().data_store()
            dX_f_act = ds.voi_and_variables()["Current_If/X_f_act"].values()
            i_f = ds.voi_and_variables()["Current_If/i_f"].values()
            dv = ds.voi_and_variables()["Current_If/v"].values()
            Time_hold = (ds.voi_and_variables()["Current_If/t"].values()).T
            Time_hold = Time_hold.reshape(Time_hold.shape[0], 1)
            results = np.stack((dv, dX_f_act))
            values_hold = results.T
            Y_init = results.T[-1,:]


            if i == 0:
                Time_forVmi = Time_hold
                values_forVmi = values_hold
            else:
                values_forVmi = np.vstack((values_forVmi, values_hold))
                Time_forVmi = np.vstack((Time_forVmi, Time_hold))

            if i == 1:
#
                file.reset(True)
                file.clear_results()
                if protocol == 1:
                    data.constants()["Current_If/Ki"] = 140
                else:
                    data.constants()["Current_If/Ki"] = 150

                data.constants()["Current_If/Na_i"] = 5
                data.constants()["Current_If/Ko"] = 5.4
                data.constants()["Current_If/Nao"] = 135


                data.constants()["Current_If/g_f"] = g_f
                data.constants()["Current_If/xf_1"] = xf_1
                data.constants()["Current_If/xf_2"] = xf_2
                data.constants()["Current_If/xf_5"] = xf_5
                data.constants()["Current_If/xf_6"] = xf_6
                data.constants()["Current_If/xf_const"] = xf_const

                data.states()["Current_If/X_f_act"] = values_hold[-1][1]
                data.states()["Current_If/v"] = values_hold[-1][0]

                data.set_starting_point(timespan[0])
                data.set_ending_point(timespan[1])
                data.set_point_interval(0.992063)
                file.run()
                ds = file.results().data_store()
                x_f_inf_act = ds.voi_and_variables()["Current_If/x_f_inf_act"].values()
                tau_f_act = ds.voi_and_variables()["Current_If/tau_f_act"].values()
                i_f = ds.voi_and_variables()["Current_If/i_f"].values()

#
                IF_IV[j] = i_f[-1]
                x_act[j] = x_f_inf_act[-1]
                tau_act[j] = tau_f_act[-1]
        if j == 75:
            print()
        Time[0: len(Time_forVmi), j] = Time_forVmi[:, 0]
        values[0: len(Time_forVmi), ((j * xy) - (xy - 2)): (j * xy) + 2] = values_forVmi

    return IF_IV, x_act, tau_act



if __name__ == '__main__':
    g_f_list = [0.045, 0.1, 0.0435]
    xf_1_list = [1.64393000000000e-06, 3.1273e-7, 5.7897e-7]
    xf_2_list = [-14.2824449986200, -14.6665, -14.5897]
    xf_5_list = [21211.4254177363, 1.9712e4, 2.0087e4]
    xf_6_list = [8.58286947845000, 10.7422, 10.2024]
    xf_const_list = [0.0308875647300000, 47.8597, 23.9453]

    plt.figure(figsize=(19, 7))
    plt.subplot(1, 3, 1)

    protocol = 2
    IF_IV1 = run_sim1(Vm_plot, protocol, g_f_list[0], xf_1_list[0], xf_2_list[0], xf_5_list[0], xf_6_list[0],
                      xf_const_list[0])
    plt.plot(Vm_plot.T, IF_IV1[1], color='orangered', label='Ma et al.', linewidth=4)

    protocol = 1
    IF_IV2 = run_sim1(Vm_plot, protocol, g_f_list[1], xf_1_list[1], xf_2_list[1], xf_5_list[1], xf_6_list[1],
                      xf_const_list[1])
    plt.plot(Vm_plot.T, IF_IV2[1], color='blue', label='Kurokawa Lab', linewidth=4)

    protocol = 1
    IF_IV3 = run_sim1(Vm_plot, protocol, g_f_list[2], xf_1_list[2], xf_2_list[2], xf_5_list[2], xf_6_list[2],
                      xf_const_list[2])
    plt.plot(Vm_plot.T, IF_IV3[1], color='black', label='Baseline Model', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Normalized I$_{f}$', fontsize=18)
    plt.xticks(np.arange(-150, 0.1, 50))
    plt.yticks(np.arange(0, 1.1, 0.5))
    plt.xlim(-150, 0)
    plt.ylim(0, 1)
    plt.tick_params(axis='both', labelsize='18')
    plt.title('A', fontsize=18)
    plt.legend(fontsize='14')

    plt.subplot(1, 3, 2)

    plt.plot(Vm_plot.T, IF_IV1[2], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, IF_IV2[2], color='blue', linewidth=4)
    #

    plt.plot(Vm_plot.T, IF_IV3[2], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{act},I_{f}$ (ms)', fontsize=18)
    plt.xticks(np.arange(-150, 0.1, 50))
    plt.yticks(np.arange(0, 1501, 500))
    plt.xlim(-150, 0)
    plt.ylim(0, 1500)
    plt.tick_params(axis='both', labelsize='18')
    plt.title('B', fontsize=18)

    plt.subplot(1, 3, 3)

    plt.plot(Vm_plot.T, IF_IV1[0], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, IF_IV2[0], color='blue', linewidth=4)
    #

    plt.plot(Vm_plot.T, IF_IV3[0], color='black', linewidth=4)

    plt.xticks(np.arange(-150, 0.1, 50))
    plt.yticks(np.arange(-14, 2.1, 4))
    plt.xlim(-150, 0)
    plt.ylim(-14, 2)
    plt.tick_params(axis='both', labelsize='18')
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_f$ (pA/pF)', size='18')
    plt.title('C', fontsize=18)
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)


    stop = timeit.default_timer()

    print('Time: ', stop - start)
    plt.savefig('Figure07.png')
