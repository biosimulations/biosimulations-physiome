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


start, stop, step = -100.1, 50.1, 2

Vm_plot = np.arange(start, stop + step, step)
Vm_plot = Vm_plot.reshape((1, Vm_plot.shape[0]))


file = load_sedml("Current_Ica.sedml")

def run_sim1(Vm_step, protocol, d_0, d_1, d_2, d_5, d_6, f_1, f_2, f_5, f_6, tau_d_const, tau_f_const):
    Y = np.array((-70, 0.3, 0, 0, 1, 1)).reshape(6, 1)

    period = [3000, 4000, 1000]
    step1 = -40
    stepf = -40

    if protocol == 1: #Ma
        period = [1000, 3000, 100, 100]
        step1 = -80 #mV
        step2 = -50
        stepf = -50 #mV
    elif protocol == 2: #Es-Salah_lamoureaux
        period = [1000, 3000, 125, 100]
        step1 = -80  # mV
        step2 = -50
        stepf = -50
    else: #Veerman
        period = [500, 500, 300, 100]
        step1 = -80  # mV
        step2 = -80
        stepf = -80


    col1 = step1 * np.ones(Vm_step.T.shape)
    col2 = step2 * np.ones(Vm_step.T.shape)
    col3 = Vm_step.T
    col4 = stepf * np.ones(Vm_step.T.shape)

    Vm_mat = np.hstack((col1, col2, col3, col4))


    Time = sum(period) * np.ones((sum(period) * 100, len(Vm_step.T)))
    ICaL = 0.01 * np.ones((sum(period) * 100, len(Vm_step.T)))
    IV_cal = np.zeros(Vm_step.T.shape)


    # sedml file
    data = file.data()

    x_act = np.zeros(Vm_step.T.shape)
    x_inact = np.zeros(Vm_step.T.shape)
    x_fca_inact = np.zeros(Vm_step.T.shape)
    tau_act = np.zeros(Vm_step.T.shape)
    tau_inact = np.zeros(Vm_step.T.shape)
    tau_fca = np.zeros(Vm_step.T.shape)
    for j in range(len(Vm_step.T)):
        print(j)

        file.reset(True)
        file.clear_results()
        if protocol == 1:
            data.constants()["Current_IcaL/Ki"] = 0  # Ma
            data.constants()["Current_IcaL/Ko"] = 0
            data.constants()["Current_IcaL/Na_i"] = 5
            data.constants()["Current_IcaL/Nao"] = 0
            data.constants()["Current_IcaL/Cao"] = 5
        elif protocol == 2:
            data.constants()["Current_IcaL/Ki"] = 0  # Es Salah
            data.constants()["Current_IcaL/Ko"] = 0
            data.constants()["Current_IcaL/Na_i"] = 5
            data.constants()["Current_IcaL/Nao"] = 0
            data.constants()["Current_IcaL/Cao"] = 5
        elif protocol == 4:
            data.constants()["Current_IcaL/Ki"] = 0
            data.constants()["Current_IcaL/Ko"] = 0
            data.constants()["Current_IcaL/Na_i"] = 0
            data.constants()["Current_IcaL/Nao"] = 0
            data.constants()["Current_IcaL/Cao"] = 2.5
        else:
            data.constants()["Current_IcaL/Ki"] = 0  # Veerman
            data.constants()["Current_IcaL/Ko"] = 0
            data.constants()["Current_IcaL/Na_i"] = 0
            data.constants()["Current_IcaL/Nao"] = 0
            data.constants()["Current_IcaL/Cao"] = 1.8

        data.constants()["Current_IcaL/d_0"] = d_0
        data.constants()["Current_IcaL/d_1"] = d_1
        data.constants()["Current_IcaL/d_2"] = d_2
        data.constants()["Current_IcaL/d_5"] = d_5
        data.constants()["Current_IcaL/d_6"] = d_6
        data.constants()["Current_IcaL/f_1"] = f_1
        data.constants()["Current_IcaL/f_2"] = f_2
        data.constants()["Current_IcaL/f_5"] = f_5
        data.constants()["Current_IcaL/f_6"] = f_6
        data.constants()["Current_IcaL/tau_d_const"] = tau_d_const
        data.constants()["Current_IcaL/tau_f_const"] = tau_f_const

        # for v in Vm_step:
        data.states()["Current_IcaL/v"] = Vm_step.T[j]

        data.set_starting_point(0)
        data.set_ending_point(10)
        data.set_point_interval(10)
        file.run()
        ds = file.results().data_store()

        x_inf_act = ds.voi_and_variables()["Current_IcaL/x_ca_inf_act"].values()
        x_inf_inact = ds.voi_and_variables()["Current_IcaL/x_ca_inf_inact"].values()
        x_fca_inf_inact = ds.voi_and_variables()["Current_IcaL/x_fca_inf_inact"].values()
        tau_ca_act = ds.voi_and_variables()["Current_IcaL/tau_ca_act"].values()
        tau_ca_inact = ds.voi_and_variables()["Current_IcaL/tau_ca_inact"].values()
        tau_fca_inact = ds.voi_and_variables()["Current_IcaL/tau_fca"].values()

        x_act[j] = x_inf_act[-1]
        x_inact[j] = x_inf_inact[-1]
        x_fca_inact[j] = x_fca_inf_inact[-1]
        tau_act[j] = tau_ca_act[-1]
        tau_inact[j] = tau_ca_inact[-1]
        tau_fca[j] = tau_fca_inact[-1]

        Y_init = Y.flatten()

        for i in range(len(period)):
            Y_init[0] = Vm_mat[j, i].T

            timespan = [sum(period[0:(i)]), sum(period[0:i+1])]

            # file = load_sedml(filename)
            file.reset(True)
            file.clear_results()
            if protocol == 1:
                data.constants()["Current_IcaL/Ki"] = 0 #Ma
                data.constants()["Current_IcaL/Ko"] = 0
                data.constants()["Current_IcaL/Na_i"] = 5
                data.constants()["Current_IcaL/Nao"] = 0
                data.constants()["Current_IcaL/Cao"] = 5
            elif protocol == 2:
                data.constants()["Current_IcaL/Ki"] = 0  #Es Salah
                data.constants()["Current_IcaL/Ko"] = 0
                data.constants()["Current_IcaL/Na_i"] = 5
                data.constants()["Current_IcaL/Nao"] = 0
                data.constants()["Current_IcaL/Cao"] = 5
            elif protocol == 4:
                data.constants()["Current_IcaL/Ki"] = 0
                data.constants()["Current_IcaL/Ko"] = 0
                data.constants()["Current_IcaL/Na_i"] = 0
                data.constants()["Current_IcaL/Nao"] = 0
                data.constants()["Current_IcaL/Cao"] = 2.5
            else:
                data.constants()["Current_IcaL/Ki"] = 0 #Veerman
                data.constants()["Current_IcaL/Ko"] = 0
                data.constants()["Current_IcaL/Na_i"] = 0
                data.constants()["Current_IcaL/Nao"] = 0
                data.constants()["Current_IcaL/Cao"] = 1.8


            data.constants()["Current_IcaL/d_0"] = d_0
            data.constants()["Current_IcaL/d_1"] = d_1
            data.constants()["Current_IcaL/d_2"] = d_2
            data.constants()["Current_IcaL/d_5"] = d_5
            data.constants()["Current_IcaL/d_6"] = d_6
            data.constants()["Current_IcaL/f_1"] = f_1
            data.constants()["Current_IcaL/f_2"] = f_2
            data.constants()["Current_IcaL/f_5"] = f_5
            data.constants()["Current_IcaL/f_6"] = f_6
            data.constants()["Current_IcaL/tau_d_const"] = tau_d_const
            data.constants()["Current_IcaL/tau_f_const"] = tau_f_const

            # data.constants()["main/k_new"] = k_new
            data.states()["Current_IcaL/v"] = Y_init[0]
            data.states()["Current_IcaL/ca_SR"] = Y_init[1]
            data.states()["Current_IcaL/ca_i"] = Y_init[2]
            data.states()["Current_IcaL/X_ca_act"] = Y_init[3]
            data.states()["Current_IcaL/X_ca_inact"] = Y_init[4]
            data.states()["Current_IcaL/X_fca_inact"] = Y_init[5]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(1)
            file.run()
            ds = file.results().data_store()

            dv = ds.voi_and_variables()["Current_IcaL/v"].values()
            dca_SR = ds.voi_and_variables()["Current_IcaL/ca_SR"].values()
            dca_i = ds.voi_and_variables()["Current_IcaL/ca_i"].values()
            dX_ca_act = ds.voi_and_variables()["Current_IcaL/X_ca_act"].values()
            dX_ca_inact = ds.voi_and_variables()["Current_IcaL/X_ca_inact"].values()
            dX_fca_inact = ds.voi_and_variables()["Current_IcaL/X_fca_inact"].values()

            Time_hold = (ds.voi_and_variables()["Current_IcaL/t"].values()).T
            Time_hold = Time_hold.reshape(Time_hold.shape[0], 1)
            results = np.stack((dv, dca_SR, dca_i, dX_ca_act, dX_ca_inact, dX_fca_inact))
            values_hold = results.T
            Y_init = values_hold[-1, :]


            ICaL_hold = np.zeros(Time_hold.shape)

            for k in range(0,80):
                timespan1 = [0,80]


                # file.reset(True)
                # file.clear_results()
                if protocol == 1:
                    data.constants()["Current_IcaL/Ki"] = 0  # Ma
                    data.constants()["Current_IcaL/Ko"] = 0
                    data.constants()["Current_IcaL/Na_i"] = 5
                    data.constants()["Current_IcaL/Nao"] = 0
                    data.constants()["Current_IcaL/Cao"] = 5
                elif protocol == 2:
                    data.constants()["Current_IcaL/Ki"] = 0  # Es Salah
                    data.constants()["Current_IcaL/Ko"] = 0
                    data.constants()["Current_IcaL/Na_i"] = 5
                    data.constants()["Current_IcaL/Nao"] = 0
                    data.constants()["Current_IcaL/Cao"] = 5
                elif protocol == 4:
                    data.constants()["Current_IcaL/Ki"] = 0
                    data.constants()["Current_IcaL/Ko"] = 0
                    data.constants()["Current_IcaL/Na_i"] = 0
                    data.constants()["Current_IcaL/Nao"] = 0
                    data.constants()["Current_IcaL/Cao"] = 2.5
                else:
                    data.constants()["Current_IcaL/Ki"] = 0  # Veerman
                    data.constants()["Current_IcaL/Ko"] = 0
                    data.constants()["Current_IcaL/Na_i"] = 0
                    data.constants()["Current_IcaL/Nao"] = 0
                    data.constants()["Current_IcaL/Cao"] = 1.8

                data.constants()["Current_IcaL/d_0"] = d_0
                data.constants()["Current_IcaL/d_1"] = d_1
                data.constants()["Current_IcaL/d_2"] = d_2
                data.constants()["Current_IcaL/d_5"] = d_5
                data.constants()["Current_IcaL/d_6"] = d_6
                data.constants()["Current_IcaL/f_1"] = f_1
                data.constants()["Current_IcaL/f_2"] = f_2
                data.constants()["Current_IcaL/f_5"] = f_5
                data.constants()["Current_IcaL/f_6"] = f_6
                data.constants()["Current_IcaL/tau_d_const"] = tau_d_const
                data.constants()["Current_IcaL/tau_f_const"] = tau_f_const

                # data.constants()["main/k_new"] = k_new
                data.states()["Current_IcaL/v"] = values_hold[k][0]
                data.states()["Current_IcaL/ca_SR"] = values_hold[k][1]
                data.states()["Current_IcaL/ca_i"] = values_hold[k][2]
                data.states()["Current_IcaL/X_ca_act"] = values_hold[k][3]
                data.states()["Current_IcaL/X_ca_inact"] = values_hold[k][4]
                data.states()["Current_IcaL/X_fca_inact"] = values_hold[k][5]

                data.set_starting_point(timespan1[0])
                data.set_ending_point(timespan1[1])
                data.set_point_interval(80)
                file.run()
                ds = file.results().data_store()

                i_CaL = ds.voi_and_variables()["Current_IcaL/i_CaL"].values()

                ICaL_hold[k] = i_CaL[0]

            if i == 0:
                Time_j = Time_hold
                i_CaL_j = ICaL_hold
            else:
                Time_j = np.vstack((Time_j, Time_hold))
                i_CaL_j = np.vstack((i_CaL_j, ICaL_hold))

            if i == 2:
                start = 30
                index = np.count_nonzero((np.array(np.max(abs(ICaL_hold[start:-1])))))
                IV_cal[j] = ICaL_hold[index+start-1]


    return IV_cal, x_act, x_inact, x_fca_inact, tau_act, tau_inact, tau_fca


if __name__ == '__main__':
    plt.figure(figsize=(15, 13))

    d_0_list = [0.19016464505208927, 0.38010243347999983, 0.484048813248, 0.17779487373692016, 0.30802769137925234]
    d_1_list = [7.724718062981113, 14.567438770685602, 8.770648120828913, 15.560795677650413, 12.966294189721642]
    d_2_list = [6.388825030309134, 7.501436625497612, 7.8748150063959255, 5.861186262240001, 7.07914596471118]
    d_5_list = [0.08803087507239495, 0.032552967698800464, 0.062165144462064205, 0.04001013436000526,
                0.044909415506956644]
    d_6_list = [-6.265773108811118, -7.305350518436171, - 7.6680726347258314, - 5.756217954563908, - 6.909880369241971]
    f_1_list = [0.001644383040759749, 3.454960428030549E-4, 5.925134493322452E-4, 5.997599860362688E-4,
                5.125898260571896E-4]
    f_2_list = [-82.46034376474563, -43.41688999393955, - 52.77826478681527, - 52.32198132085614, - 49.50571203387032]
    f_5_list = [818.2069824654249, 1580.8554165474573, 729.0226806467049, 3483.7555733487948, 1931.2112235143188]
    f_6_list = [4.35226624639966, 6.131075895743708, 6.1849082640235915, 4.874098339328655, 5.730027499698651]
    tau_d_const_list = [1.736167780874709, 1.6122826510533983, 1.6664595173798702, 1.6959986720577191,
                        1.6582469468303291]
    tau_f_const_list = [97.74237390031138, 99.52320589734498, 97.14763412621564, 104.71683748974891, 100.46255917110318]

    plt.subplot(2, 2, 1)

    protocol = 1
    ICaL_IV1 = run_sim1(Vm_plot, protocol, d_0_list[0], d_1_list[0], d_2_list[0], d_5_list[0], d_6_list[0], f_1_list[0],
                        f_2_list[0], f_5_list[0], f_6_list[0],
                        tau_d_const_list[0], tau_f_const_list[0])
    plt.plot(Vm_plot[0], ICaL_IV1[1], color='blue', label='Ma', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV1[2], color='blue', linewidth=4)

    protocol = 3
    ICaL_IV2 = run_sim1(Vm_plot, protocol, d_0_list[1], d_1_list[1], d_2_list[1], d_5_list[1], d_6_list[1], f_1_list[1],
                        f_2_list[1], f_5_list[1], f_6_list[1],
                        tau_d_const_list[1], tau_f_const_list[1])
    plt.plot(Vm_plot[0], ICaL_IV2[1], color='orangered', label='Veerman1', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV2[2], color='orangered', linewidth=4)

    protocol = 3
    ICaL_IV3 = run_sim1(Vm_plot, protocol, d_0_list[2], d_1_list[2], d_2_list[2], d_5_list[2], d_6_list[2], f_1_list[2],
                        f_2_list[2], f_5_list[2], f_6_list[2],
                        tau_d_const_list[2], tau_f_const_list[2])
    plt.plot(Vm_plot[0], ICaL_IV3[1], color='purple', label='Veerman2', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV3[2], color='purple', linewidth=4)

    protocol = 2
    ICaL_IV4 = run_sim1(Vm_plot, protocol, d_0_list[3], d_1_list[3], d_2_list[3], d_5_list[3], d_6_list[3], f_1_list[3],
                        f_2_list[3], f_5_list[3], f_6_list[3],
                        tau_d_const_list[3], tau_f_const_list[3])
    plt.plot(Vm_plot[0], ICaL_IV4[1], color='green', label='EsSalah', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV4[2], color='green', linewidth=4)

    protocol = 4
    ICaL_IV5 = run_sim1(Vm_plot, protocol, d_0_list[4], d_1_list[4], d_2_list[4], d_5_list[4], d_6_list[4], f_1_list[4],
                        f_2_list[4], f_5_list[4], f_6_list[4],
                        tau_d_const_list[4], tau_f_const_list[4])
    plt.plot(Vm_plot[0], ICaL_IV5[1], color='black', label='Baseline', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV5[2], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Normalized I$_{CaL}$', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-100, 51, 50))
    plt.yticks(np.arange(0, 1.1, 0.5))
    plt.xlim(-100, 50)
    plt.ylim(0, 1)
    plt.title('A', fontsize=18)
    plt.legend(fontsize='15')

    plt.subplot(2, 2, 2)

    plt.plot(Vm_plot[0], ICaL_IV1[0].T[0], color='blue', label='Ma', linewidth=4)

    plt.plot(Vm_plot[0], ICaL_IV2[0].T[0], color='orangered', label='Veerman1', linewidth=4)

    plt.plot(Vm_plot[0], ICaL_IV3[0].T[0], color='purple', label='Veerman2', linewidth=4)

    plt.plot(Vm_plot[0], ICaL_IV4[0].T[0], color='green', label='EsSalah', linewidth=4)

    plt.plot(Vm_plot[0], ICaL_IV5[0].T[0], color='black', label='Baseline', linewidth=4)

    plt.xticks(np.arange(-100, 51, 50))
    plt.yticks(np.arange(-65, 21, 20))
    plt.xlim(-100, 50)
    plt.ylim(-70, 20)

    plt.tick_params(axis='both', labelsize='18')
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{ICaL}$ (pA/pF)', size='18')
    plt.title('B', fontsize=18)

    plt.subplot(2, 2, 3)

    plt.plot(Vm_plot[0], ICaL_IV1[4], color='blue', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV2[4], color='orangered', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV3[4], color='purple', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV4[4], color='green', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV5[4], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{act},I_{CaL}$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-100, 51, 50))
    plt.yticks(np.arange(1.5, 3.6, 0.5))
    plt.xlim(-100, 50)
    plt.ylim(1.5, 3.5)
    plt.title('C', fontsize=18)

    plt.subplot(2, 2, 4)

    plt.plot(Vm_plot[0], ICaL_IV1[5], color='blue', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV2[5], color='orangered', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV3[5], color='purple', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV4[5], color='green', linewidth=4)
    plt.plot(Vm_plot[0], ICaL_IV5[5], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{inact},I_{CaL}$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-100, 51, 50))
    plt.yticks(np.arange(0, 1001, 500))
    plt.xlim(-100, 50)
    plt.ylim(0, 1000)
    plt.title('D', fontsize=18)

    plt.tick_params(axis='both', labelsize='18')
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{ICaL}$ (pA/pF)', size='18')
    plt.title('B', fontsize=18)
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)

    stop = timeit.default_timer()

    print('Time: ', stop - start)
    plt.savefig('Figure03.png')

