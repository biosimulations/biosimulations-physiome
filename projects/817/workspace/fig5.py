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



start, stop, step = -100, 100, 5

Vm_plot = np.arange(start, stop + step, step)
Vm_plot = Vm_plot.reshape((1, Vm_plot.shape[0]))


file = load_sedml("Current_Ito.sedml")


def run_sim1(Vm_step, protocol, r_0, r_1, r_2, r_5, r_6, s_1, s_2, s_5, s_6, tau_r_const, tau_s_const):


    if protocol == 1: #Ma
        period = [500, 500, 1000, 50]
        step1 = -50 #mV
        step2 = -50 #mV
        stepf = -50 #mV
    elif protocol ==2: #cordiero
        period = [1000, 10, 500, 50]
        step1 = -80
        step2 = -50
        stepf = -50
    else: #veerman
        period = [1000, 5, 400, 50]
        step1 = -80
        step2 = -40
        stepf = -50

    col1 = step1 * np.ones(Vm_step.T.shape)
    col2 = step2 * np.ones(Vm_step.T.shape)
    col3 = Vm_step.T
    col4 = stepf * np.ones(Vm_step.T.shape)

    Vm_mat = np.hstack((col1, col2, col3, col4))

    Y = np.array((-80, 0, 1)).reshape(3, 1)

    Ito = 0.01 * np.ones((sum(period) * 100, len(Vm_step.T)))
    Time = sum(period) * np.ones((sum(period) * 100, len(Vm_step.T)))

    # sedml file
    data = file.data()
    Ito_IV = []

    x_act = np.zeros(Vm_step.T.shape)
    x_inact = np.zeros(Vm_step.T.shape)
    tau_act = np.zeros(Vm_step.T.shape)
    tau_inact = np.zeros(Vm_step.T.shape)
    for j in range(len(Vm_step.T)):
        print(j)
        file.reset(True)
        file.clear_results()
        if protocol == 1:
            data.constants()["Current_Ito/Ki"] = 150  # Ma
        elif protocol == 2:
            data.constants()["Current_Ito/Ki"] = 135  # Cordiero
        else:
            data.constants()["Current_Ito/Ki"] = 125  # veerman

        data.constants()["Current_Ito/Ko"] = 5.4
        data.constants()["Current_Ito/r_0"] = r_0
        data.constants()["Current_Ito/r_1"] = r_1
        data.constants()["Current_Ito/r_2"] = r_2
        data.constants()["Current_Ito/r_5"] = r_5
        data.constants()["Current_Ito/r_6"] = r_6
        data.constants()["Current_Ito/s_1"] = s_1
        data.constants()["Current_Ito/s_2"] = s_2
        data.constants()["Current_Ito/s_5"] = s_5
        data.constants()["Current_Ito/s_6"] = s_6
        data.constants()["Current_Ito/tau_r_const"] = tau_r_const
        data.constants()["Current_Ito/tau_s_const"] = tau_s_const

        # for v in Vm_step:
        data.states()["Current_Ito/v"] = Vm_step.T[j]

        data.set_starting_point(0)
        data.set_ending_point(10)
        data.set_point_interval(10)
        file.run()

        ds = file.results().data_store()
        x_to_inf_act = ds.voi_and_variables()["Current_Ito/x_to_inf_act"].values()
        x_to_inf_inact = ds.voi_and_variables()["Current_Ito/x_to_inf_inact"].values()
        tau_to_act = ds.voi_and_variables()["Current_Ito/tau_to_act"].values()
        tau_to_inact = ds.voi_and_variables()["Current_Ito/tau_to_inact"].values()

        x_act[j] = x_to_inf_act[-1]
        x_inact[j] = x_to_inf_inact[-1]
        tau_act[j] = tau_to_act[-1]
        tau_inact[j] = tau_to_inact[-1]

        Y_init = Y.flatten()

        for i in range(len(period)):
            Y_init[0] = Vm_mat[j, i].T

            timespan = [sum(period[0:(i)]), sum(period[0:i+1])]

            # file = load_sedml(filename)
            file.reset(True)
            file.clear_results()
            if protocol == 1:
                data.constants()["Current_Ito/Ki"] = 150 #Ma
            elif protocol == 2:
                data.constants()["Current_Ito/Ki"] = 135 #Cordiero
            else:
                data.constants()["Current_Ito/Ki"] = 125 #veerman


            data.constants()["Current_Ito/Ko"] = 5.4
            data.constants()["Current_Ito/r_0"] = r_0
            data.constants()["Current_Ito/r_1"] = r_1
            data.constants()["Current_Ito/r_2"] = r_2
            data.constants()["Current_Ito/r_5"] = r_5
            data.constants()["Current_Ito/r_6"] = r_6
            data.constants()["Current_Ito/s_1"] = s_1
            data.constants()["Current_Ito/s_2"] = s_2
            data.constants()["Current_Ito/s_5"] = s_5
            data.constants()["Current_Ito/s_6"] = s_6
            data.constants()["Current_Ito/tau_r_const"] = tau_r_const
            data.constants()["Current_Ito/tau_s_const"] = tau_s_const

            data.states()["Current_Ito/X_to_act"] = Y_init[2]
            data.states()["Current_Ito/X_to_inact"] = Y_init[1]
            # data.constants()["main/k_new"] = k_new
            data.states()["Current_Ito/v"] = Y_init[0]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(0.1)
            file.run()
            ds = file.results().data_store()
            dX_to_act = ds.voi_and_variables()["Current_Ito/X_to_act"].values()
            dX_to_inact = ds.voi_and_variables()["Current_Ito/X_to_inact"].values()
            i_to = ds.voi_and_variables()["Current_Ito/i_to"].values()
            dv = ds.voi_and_variables()["Current_Ito/v"].values()
            x_to_inf_act = ds.voi_and_variables()["Current_Ito/x_to_inf_act"].values()
            x_to_inf_inact = ds.voi_and_variables()["Current_Ito/x_to_inf_inact"].values()
            Time_hold = (ds.voi_and_variables()["Current_Ito/t"].values()).T
            Time_hold = Time_hold.reshape(Time_hold.shape[0], 1)
            results = np.stack((dv, dX_to_inact, dX_to_act))
            values_hold = results.T
            Y_init = results.T[-1, :]


            print()

            Ito_hold = np.zeros(Time_hold.shape)


            for k in range(0, 50):

                timespan1 = [0, 50]


                # file.reset(True)
                # file.clear_results()
                if protocol == 1:
                    data.constants()["Current_Ito/Ki"] = 150  # Ma
                elif protocol == 2:
                    data.constants()["Current_Ito/Ki"] = 135  # Cordiero
                else:
                    data.constants()["Current_Ito/Ki"] = 125  # veerman

                data.constants()["Current_Ito/Ko"] = 5.4
                data.constants()["Current_Ito/r_0"] = r_0
                data.constants()["Current_Ito/r_1"] = r_1
                data.constants()["Current_Ito/r_2"] = r_2
                data.constants()["Current_Ito/r_5"] = r_5
                data.constants()["Current_Ito/r_6"] = r_6
                data.constants()["Current_Ito/s_1"] = s_1
                data.constants()["Current_Ito/s_2"] = s_2
                data.constants()["Current_Ito/s_5"] = s_5
                data.constants()["Current_Ito/s_6"] = s_6
                data.constants()["Current_Ito/tau_r_const"] = tau_r_const
                data.constants()["Current_Ito/tau_s_const"] = tau_s_const

                data.states()["Current_Ito/X_to_act"] = values_hold[k][2]
                data.states()["Current_Ito/X_to_inact"] = values_hold[k][1]
                # data.constants()["main/k_new"] = k_new
                data.states()["Current_Ito/v"] = values_hold[k][0]

                data.set_starting_point(timespan1[0])
                data.set_ending_point(timespan1[1])
                data.set_point_interval(10)
                file.run()
                ds = file.results().data_store()
                dX_to_act = ds.voi_and_variables()["Current_Ito/X_to_act"].values()
                dX_to_inact = ds.voi_and_variables()["Current_Ito/X_to_inact"].values()
                i_to = ds.voi_and_variables()["Current_Ito/i_to"].values()

                Ito_hold[k] = i_to[0]

            if i == 0:
                Time_j = Time_hold
                Ito_j = Ito_hold
            else:
                Time_j = np.vstack((Time_j, Time_hold))
                Ito_j = np.vstack((Ito_j, Ito_hold))

        c = Time[0:len(Time_j), j].reshape((1, (Time[0:len(Time_j), j]).shape[-1]))
        c = Time_j
        d = Ito[0:len(Ito_j), j].reshape((1, (Ito[0:len(Ito_j), j]).shape[-1]))
        d = Ito_j
        Ito_IV.append(np.max(d))


    Ito_IV = np.array(Ito_IV)
    Ito_IV = (Ito_IV.reshape((1, Ito_IV.shape[0]))).T


    return Ito_IV, x_act, x_inact, tau_act, tau_inact


if __name__ == '__main__':
    r_0_list = [0.025, 0.15, 0.1785, 0.1178]
    r_1_list = [0.0478, 0.0591, 0.0591, 0.0554]
    r_2_list = [15.1653, 9.9437, 9.9436, 11.6842]
    r_5_list = [5.2098, 3.3787, 3.3789, 3.9892]
    r_6_list = [-14.6505, -9.2455, -9.2454, -11.0471]
    s_1_list = [1.5665e-4, 3.9748e-4, 4.7856e-4, 3.4423e-4]
    s_2_list = [-11.3965, -21.8363, -19.6705, -17.6345]
    s_5_list = [235.6863, 247.8116, 76.7837, 186.7605]
    s_6_list = [7.3083, 7.2455, 9.989, 8.1809]
    tau_r_const_list = [0.3680, 0.8611, 0.8611, 0.6968]
    tau_s_const_list = [9.1434, 15.3766, 9.1533, 11.2245]

    #
    plt.figure(figsize=(15, 13))

    plt.subplot(2, 2, 1)

    protocol = 1
    Iks_IV1 = run_sim1(Vm_plot, protocol, r_0_list[0], r_1_list[0], r_2_list[0], r_5_list[0], r_6_list[0], s_1_list[0],
                       s_2_list[0], s_5_list[0], s_6_list[0], tau_r_const_list[0], tau_s_const_list[0])
    plt.plot(Vm_plot.T, Iks_IV1[1], color='blue', label='Ma et al.', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV1[2], color='blue', linewidth=4)

    protocol = 2
    Iks_IV2 = run_sim1(Vm_plot, protocol, r_0_list[1], r_1_list[1], r_2_list[1], r_5_list[1], r_6_list[1], s_1_list[1],
                       s_2_list[1], s_5_list[1], s_6_list[1], tau_r_const_list[1], tau_s_const_list[1])
    plt.plot(Vm_plot.T, Iks_IV2[1], color='green', label='Cordeiro et al.', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV2[2], color='green', linewidth=4)
    # # #
    # # #
    protocol = 3
    Iks_IV3 = run_sim1(Vm_plot, protocol, r_0_list[2], r_1_list[2], r_2_list[2], r_5_list[2], r_6_list[2], s_1_list[2],
                       s_2_list[2], s_5_list[2], s_6_list[2], tau_r_const_list[2], tau_s_const_list[2])
    plt.plot(Vm_plot.T, Iks_IV3[1], color='orangered', label='Veerman et al.', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV3[2], color='orangered', linewidth=4)
    #
    protocol = 2
    Iks_IV4 = run_sim1(Vm_plot, protocol, r_0_list[3], r_1_list[3], r_2_list[3], r_5_list[3], r_6_list[3], s_1_list[3],
                       s_2_list[3], s_5_list[3], s_6_list[3], tau_r_const_list[3], tau_s_const_list[3])
    plt.plot(Vm_plot.T, Iks_IV4[1], color='black', label='Baseline Model', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV4[2], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Normalized I$_{to}$', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 1.1, 0.5))
    plt.xlim(-100, 100, 50)
    plt.ylim(0, 1, 0.5)
    plt.title('A', fontsize=18)
    plt.legend(fontsize='15', loc= 'best')

    plt.subplot(2, 2, 3)

    plt.plot(Vm_plot.T, Iks_IV1[3], color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[3], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[3], color='green', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[3], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{act}$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 6.1, 2))
    plt.xlim(-100, 100)
    plt.ylim(0, 6)
    plt.title('C', fontsize='18')

    plt.subplot(2, 2, 4)

    plt.plot(Vm_plot.T, Iks_IV1[4], color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[4], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[4], color='green', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[4], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{inact}$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 301, 100))
    plt.xlim(-100, 100)
    plt.ylim(0, 300)
    plt.title('D', fontsize=18)

    plt.subplot(2, 2, 2)

    plt.plot(Vm_plot.T, Iks_IV1[0], color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[0], color='green', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[0], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[0], color='black', linewidth=4)

    plt.xticks(np.arange(-100, 101, 50))
    plt.yticks(np.arange(0, 21, 10))
    plt.xlim(-100, 100)
    plt.ylim(0, 20)
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{to}$ (pA/pF)', size='18')
    plt.tick_params(axis='both', labelsize='18')
    plt.title('B', fontsize=18)

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)

    stop = timeit.default_timer()

    print('Time: ', stop - start)

    # plt.show()
    plt.savefig('Figure05.png')
