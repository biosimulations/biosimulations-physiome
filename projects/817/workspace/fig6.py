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


start, stop, step = -100, 100, 2

Vm_plot = np.arange(start, stop + step, step)
Vm_plot = Vm_plot.reshape((1, Vm_plot.shape[0]))



file = load_sedml("Current_Iks.sedml")



def run_sim1(Vm_step, protocol, ks_0, ks_1, ks_2, ks_5, ks_6, tau_ks_const):
    Y = np.array((-70, 0)).reshape(2, 1)
    print()


    col1 = -40 * np.ones(Vm_step.T.shape)
    col2 = Vm_step.T
    col3 = -40 * np.ones(Vm_step.T.shape)

    period = [2000, 5000, 100]
    Vm_mat = np.hstack((col1, col2, col3))


    xy = 2  # variables in y

    values = np.zeros((sum(period) * 100, len(Vm_step.T) * xy))
    Time = sum(period) * np.ones((sum(period) * 100, len(Vm_step.T)))
    IV_place = np.zeros(Vm_step.T.shape)
    x_act = np.zeros(Vm_step.T.shape)
    tau_act = np.zeros(Vm_step.T.shape)

    # sedml file
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
                data.constants()["Current_Iks/Ki"] = 130 #Ma Wei
            else:
                data.constants()["Current_Iks/Ki"] = 145 #Ma


            data.constants()["Current_Iks/Ko"] = 5.4
            data.constants()["Current_Iks/ks_0"] = ks_0
            data.constants()["Current_Iks/ks_1"] = ks_1
            data.constants()["Current_Iks/ks_2"] = ks_2
            data.constants()["Current_Iks/ks_5"] = ks_5
            data.constants()["Current_Iks/ks_6"] = ks_6
            data.constants()["Current_Iks/tau_ks_const"] = tau_ks_const

            data.states()["Current_Iks/X_ks_act"] = Y[1]

            data.states()["Current_Iks/v"] = Y_init[0]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(0.992063)
            file.run()
            ds = file.results().data_store()
            dX_ks_act = ds.voi_and_variables()["Current_Iks/X_ks_act"].values()
            i_Ks = ds.voi_and_variables()["Current_Iks/i_Ks"].values()
            dv = ds.voi_and_variables()["Current_Iks/v"].values()
            Time_hold = (ds.voi_and_variables()["Current_Iks/t"].values()).T
            Time_hold = Time_hold.reshape(Time_hold.shape[0], 1)
            results = np.stack((dv, dX_ks_act))

            values_hold = results.T
            Y_init = results.T[-1, :]

            print()

            if i == 0:
                Time_forVmi = Time_hold
                values_forVmi = values_hold
            else:
                values_forVmi = np.vstack((values_forVmi, values_hold))
                Time_forVmi = np.vstack((Time_forVmi, Time_hold))

            if i == 1:
                timespan1 = [0, 1]

                if protocol == 1:
                    data.constants()["Current_Iks/Ki"] = 140
                else:
                    data.constants()["Current_Iks/Ki"] = 150

                data.constants()["Current_Iks/Ko"] = 5.4
                data.constants()["Current_Iks/ks_0"] = ks_0
                data.constants()["Current_Iks/ks_1"] = ks_1
                data.constants()["Current_Iks/ks_2"] = ks_2
                data.constants()["Current_Iks/ks_5"] = ks_5
                data.constants()["Current_Iks/ks_6"] = ks_6
                data.constants()["Current_Iks/tau_ks_const"] = tau_ks_const

                data.states()["Current_Iks/X_ks_act"] = values_hold[-1][1]
                # data.constants()["main/k_new"] = k_new
                data.states()["Current_Iks/v"] = values_hold[-1][0]

                data.set_starting_point(timespan1[0])
                data.set_ending_point(timespan1[1])
                data.set_point_interval(1)
                file.run()
                ds = file.results().data_store()
                x_ks_inf_act = ds.voi_and_variables()["Current_Iks/x_ks_inf_act"].values()
                tau_ks_act = ds.voi_and_variables()["Current_Iks/tau_ks_act"].values()
                i_ks = ds.voi_and_variables()["Current_Iks/i_Ks"].values()
                #
                IV_place[j] = i_ks[-1]
                x_act[j] = x_ks_inf_act[-1]
                tau_act[j] = tau_ks_act[-1]

        if j == 75:
            print()
        Time[0: len(Time_forVmi), j] = Time_forVmi[:, 0]
        values[0: len(Time_forVmi), ((j * xy) - (xy - 2)): (j * xy) + 2] = values_forVmi

    return IV_place, x_act, tau_act


if __name__ == '__main__':

    ks_0_list = [0.0030, 0.0096, 0.0105, 0.0077]
    ks_1_list = [9.384e-4, 0.0013, 0.0013, 0.0012]
    ks_2_list = [180.5160, 1e5, 1e5, 6.6727e4]
    ks_5_list = [0.3532, 0.2614, 0.2268, 0.2805]
    ks_6_list = [-14.6633, -22.0906, -19.847, -18.8670]
    tau_ks_const_list = [1.4223e-5, 2e-11, 2e-11, 4.7411e-6]

    plt.figure(figsize=(19, 7))
    plt.subplot(1, 3, 1)

    protocol = 0
    Iks_IV1 = run_sim1(Vm_plot, protocol, ks_0_list[0], ks_1_list[0], ks_2_list[0], ks_5_list[0], ks_6_list[0],
                      tau_ks_const_list[0])
    x_act = np.array(Iks_IV1[1])

    plt.plot(Vm_plot.T, x_act, color='blue', label= 'Ma et al.',  linewidth=4)

    protocol = 1
    Iks_IV2 = run_sim1(Vm_plot, protocol, ks_0_list[1], ks_1_list[1], ks_2_list[1], ks_5_list[1], ks_6_list[1],
                      tau_ks_const_list[1])

    x_act = np.array(Iks_IV2[1])

    plt.plot(Vm_plot.T, x_act, color='orangered', label='Ma, Wei et al. patient', linewidth=4)

    protocol = 1
    Iks_IV3 = run_sim1(Vm_plot, protocol, ks_0_list[2], ks_1_list[2], ks_2_list[2], ks_5_list[2], ks_6_list[2],
                      tau_ks_const_list[2])
    x_act = np.array(Iks_IV3[1])
    plt.plot(Vm_plot.T, x_act, color='purple', label= 'Ma, Wie et al. iCell', linewidth=4)

    protocol = 0
    Iks_IV4 = run_sim1(Vm_plot, protocol, ks_0_list[3], ks_1_list[3], ks_2_list[3], ks_5_list[3], ks_6_list[3],
                      tau_ks_const_list[3])

    x_act = np.array(Iks_IV4[1])
    plt.plot(Vm_plot.T, x_act, color='black', label= 'Baseline Model', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Normalized I$_{Ks}$', fontsize= 18)
    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 1.1, 0.5))
    plt.xlim(-100,100)
    plt.ylim(0,1)
    plt.tick_params(axis='both', labelsize='18')
    plt.title('A', fontsize=18)
    plt.legend(fontsize= '14', loc = 'best')

    plt.subplot(1, 3, 2)

    tau_act = np.array(Iks_IV1[2])

    plt.plot(Vm_plot.T, tau_act, color='blue', linewidth=4)

    tau_act = np.array(Iks_IV2[2])

    plt.plot(Vm_plot.T, tau_act, color='orangered', linewidth=4)

    tau_act = np.array(Iks_IV3[2])
    plt.plot(Vm_plot.T, tau_act, color='purple', linewidth=4)

    tau_act = np.array(Iks_IV4[2])
    plt.plot(Vm_plot.T, tau_act, color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Tau$_{act},I_{Ks}$ (ms)', fontsize= 18)
    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 1001, 500))
    plt.xlim(-100,100)
    plt.ylim(0,1000)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.title('B', fontsize=18)

    plt.subplot(1, 3, 3)


    plt.plot(Vm_plot.T, Iks_IV1[0], color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[0], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[0], color='purple', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[0], color='black', linewidth=4)
    #
    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 2.1, 0.5))
    plt.xlim(-100, 100)
    plt.ylim(0, 2)
    plt.tick_params(axis='both', labelsize='18')
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{ks}$ (pA/pF)', size='18')
    plt.title('C', fontsize=18)

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)


    plt.savefig('Figure06.png')
    stop = timeit.default_timer()
    print('Time: ', stop - start)
