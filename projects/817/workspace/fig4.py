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




start, stop, step = -150, 50, 5

Vm_plot = np.arange(start, stop + step, step)
Vm_plot = Vm_plot.reshape((1, Vm_plot.shape[0]))



file = load_sedml("Current_Ikr.sedml")


def run_sim1(Vm_step, protocol, Xr1_0, Xr1_1, Xr1_2, Xr1_5, Xr1_6, Xr2_1, Xr2_2, Xr2_5, Xr2_6, Xr1_7, Xr2_7):
    period = [3000, 4000, 1000]
    step1 = -40
    stepf = -40

    if protocol == 1: #bellin (4) % ma (1)
        period = [3000, 4000, 1000]
        step1 = -40 #mV
        stepf = -40 #mV
    elif protocol == 2: #Es-Salah_lamoureaux
        period = [3000, 4000, 1000]
        step1 = -50
        stepf = -50
    elif protocol == 3: #Wu
        period =  [3000, 2500, 1000]
        step1 = -50
        stepf = -40
    elif protocol == 4: #bellin (4) % ma (1)
        period = [3000, 4000, 1000]
        step1 = -40 #mV
        stepf = -40 #mV


    col1 = step1 * np.ones(Vm_step.T.shape)
    col2 = Vm_step.T
    col3 = stepf * np.ones(Vm_step.T.shape)

    Vm_mat = np.hstack((col1, col2, col3))

    Y = np.array((-40, 0, 1)).reshape(3, 1)

    IKr_tail = np.zeros(Vm_step.shape)
    time_tail = np.zeros(Vm_step.shape)

    Ikr = np.ones((sum(period) * 100, len(Vm_step.T)))
    Time = sum(period) * np.ones((sum(period) * 100, len(Vm_step.T)))

    # sedml file
    data = file.data()
    Ikr_IV = []

    x_act = np.zeros(Vm_step.T.shape)
    x_inact = np.zeros(Vm_step.T.shape)
    tau_act = np.zeros(Vm_step.T.shape)
    tau_inact = np.zeros(Vm_step.T.shape)
    for j in range(len(Vm_step.T)):
        print(j)

        file.reset(True)
        file.clear_results()
        if protocol == 1:
            data.constants()["Current_Ikr/Ki"] = 150  # Ma
            data.constants()["Current_Ikr/Ko"] = 5.4
        elif protocol == 2:
            data.constants()["Current_Ikr/Ki"] = 145  # Es-Salah_lamoureaux
            data.constants()["Current_Ikr/Ko"] = 4
        elif protocol == 3:
            data.constants()["Current_Ikr/Ki"] = 150  # WU
            data.constants()["Current_Ikr/Ko"] = 5.4
        elif protocol == 4:
            data.constants()["Current_Ikr/Ki"] = 145  # Bellin
            data.constants()["Current_Ikr/Ko"] = 5.4

        data.constants()["Current_Ikr/Xr1_0"] = Xr1_0
        data.constants()["Current_Ikr/Xr1_1"] = Xr1_1
        data.constants()["Current_Ikr/Xr1_2"] = Xr1_2
        data.constants()["Current_Ikr/Xr1_5"] = Xr1_5
        data.constants()["Current_Ikr/Xr1_6"] = Xr1_6
        data.constants()["Current_Ikr/Xr2_1"] = Xr2_1
        data.constants()["Current_Ikr/Xr2_2"] = Xr2_2
        data.constants()["Current_Ikr/Xr2_5"] = Xr2_5
        data.constants()["Current_Ikr/Xr2_6"] = Xr2_6
        data.constants()["Current_Ikr/Xr1_7"] = Xr1_7
        data.constants()["Current_Ikr/Xr2_7"] = Xr2_7

        # for v in Vm_step:
        data.states()["Current_Ikr/v"] = Vm_step.T[j]

        data.set_starting_point(0)
        data.set_ending_point(10)
        data.set_point_interval(10)
        file.run()

        ds = file.results().data_store()
        x_inf_act = ds.voi_and_variables()["Current_Ikr/x_inf_act"].values()
        x_inf_inact = ds.voi_and_variables()["Current_Ikr/x_inf_inact"].values()
        tau_kr_act = ds.voi_and_variables()["Current_Ikr/tau_kr_act"].values()
        tau_kr_inact = ds.voi_and_variables()["Current_Ikr/tau_kr_inact"].values()

        x_act[j] = x_inf_act[-1]
        x_inact[j] = x_inf_inact[-1]
        tau_act[j] = tau_kr_act[-1]
        tau_inact[j] = tau_kr_inact[-1]

        Y_init = Y.flatten()
        tail_max = 0

        for i in range(len(period)):
            Y_init[0] = Vm_mat[j, i].T
            # if i == 0:
                # Time_forVmi = 0
            #     timespan = [sum(period[0:i]), Time_forVmi + period[i]]
            # else:
            timespan = [sum(period[0:(i)]), sum(period[0:i+1])]

            # file = load_sedml(filename)
            file.reset(True)
            file.clear_results()
            if protocol == 1:
                data.constants()["Current_Ikr/Ki"] = 150 #Ma
                data.constants()["Current_Ikr/Ko"] = 5.4
            elif protocol == 2:
                data.constants()["Current_Ikr/Ki"] = 145 #Es-Salah_lamoureaux
                data.constants()["Current_Ikr/Ko"] = 4
            elif protocol == 3:
                data.constants()["Current_Ikr/Ki"] = 150 #WU
                data.constants()["Current_Ikr/Ko"] = 5.4
            elif protocol == 4:
                data.constants()["Current_Ikr/Ki"] = 145 #Bellin
                data.constants()["Current_Ikr/Ko"] = 5.4

            data.constants()["Current_Ikr/Xr1_0"] = Xr1_0
            data.constants()["Current_Ikr/Xr1_1"] = Xr1_1
            data.constants()["Current_Ikr/Xr1_2"] = Xr1_2
            data.constants()["Current_Ikr/Xr1_5"] = Xr1_5
            data.constants()["Current_Ikr/Xr1_6"] = Xr1_6
            data.constants()["Current_Ikr/Xr2_1"] = Xr2_1
            data.constants()["Current_Ikr/Xr2_2"] = Xr2_2
            data.constants()["Current_Ikr/Xr2_5"] = Xr2_5
            data.constants()["Current_Ikr/Xr2_6"] = Xr2_6
            data.constants()["Current_Ikr/Xr1_7"] = Xr1_7
            data.constants()["Current_Ikr/Xr2_7"] = Xr2_7

            data.states()["Current_Ikr/X_kr_act"] = Y_init[2]
            data.states()["Current_Ikr/X_kr_inact"] = Y_init[1]
            # data.constants()["main/k_new"] = k_new
            data.states()["Current_Ikr/v"] = Y_init[0]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(1)
            file.run()
            ds = file.results().data_store()
            dX_kr_act = ds.voi_and_variables()["Current_Ikr/X_kr_act"].values()
            dX_kr_inact = ds.voi_and_variables()["Current_Ikr/X_kr_inact"].values()
            # i_to = ds.voi_and_variables()["Current_Ikr/i_to"].values()
            dv = ds.voi_and_variables()["Current_Ikr/v"].values()
            Time_hold = (ds.voi_and_variables()["Current_Ikr/t"].values()).T
            Time_hold = Time_hold.reshape(Time_hold.shape[0], 1)
            results = np.stack((dv, dX_kr_inact, dX_kr_act))
            values_hold = results.T
            Y_init = values_hold[-1, :]


            IKr_hold = np.zeros(Time_hold.shape)

            for k in range(0,60):

                timespan1 = [0, 60]

                # file.reset(True)
                # file.clear_results()
                if protocol == 1:
                    data.constants()["Current_Ikr/Ki"] = 150  # Ma
                    data.constants()["Current_Ikr/Ko"] = 5.4
                elif protocol == 2:
                    data.constants()["Current_Ikr/Ki"] = 145  # Es-Salah_lamoureaux
                    data.constants()["Current_Ikr/Ko"] = 4
                elif protocol == 3:
                    data.constants()["Current_Ikr/Ki"] = 150  # WU
                    data.constants()["Current_Ikr/Ko"] = 5.4
                elif protocol == 4:
                    data.constants()["Current_Ikr/Ki"] = 145  # Bellin
                    data.constants()["Current_Ikr/Ko"] = 5.4

                data.constants()["Current_Ikr/Xr1_0"] = Xr1_0
                data.constants()["Current_Ikr/Xr1_1"] = Xr1_1
                data.constants()["Current_Ikr/Xr1_2"] = Xr1_2
                data.constants()["Current_Ikr/Xr1_5"] = Xr1_5
                data.constants()["Current_Ikr/Xr1_6"] = Xr1_6
                data.constants()["Current_Ikr/Xr2_1"] = Xr2_1
                data.constants()["Current_Ikr/Xr2_2"] = Xr2_2
                data.constants()["Current_Ikr/Xr2_5"] = Xr2_5
                data.constants()["Current_Ikr/Xr2_6"] = Xr2_6
                data.constants()["Current_Ikr/Xr1_7"] = Xr1_7
                data.constants()["Current_Ikr/Xr2_7"] = Xr2_7

                data.states()["Current_Ikr/X_kr_act"] = values_hold[k][2]
                data.states()["Current_Ikr/X_kr_inact"] = values_hold[k][1]
                # data.constants()["main/k_new"] = k_new
                data.states()["Current_Ikr/v"] = values_hold[k][0]

                data.set_starting_point(timespan1[0])
                data.set_ending_point(timespan1[1])
                data.set_point_interval(60)
                file.run()
                ds = file.results().data_store()
                dX_kr_act = ds.voi_and_variables()["Current_Ikr/X_kr_act"].values()
                dX_kr_inact = ds.voi_and_variables()["Current_Ikr/X_kr_inact"].values()
                i_Kr = ds.voi_and_variables()["Current_Ikr/i_Kr"].values()

                IKr_hold[k] = i_Kr[0]


                if i == 2 and Time_hold[k] < sum(period[0:2])+10:
                    if abs(IKr_hold[k]) > tail_max:

                        print(j,i,k)
                        time_tail[0][j] = Time_hold[k]

                        IKr_tail[0][j] = IKr_hold[k]
                        tail_max = abs(IKr_hold[k])


            if i == 0:
                Time_j = Time_hold
                Ikr_j = IKr_hold
            else:
                Time_j = np.vstack((Time_j, Time_hold))
                Ikr_j = np.vstack((Ikr_j, IKr_hold))



    return IKr_tail, x_act, x_inact, tau_act, tau_inact


if __name__ == '__main__':
    plt.figure(figsize=(16, 13))

    Xr1_0_list = [0.2346, 0.1173, 0.1346, 0.3856, 0.2180]
    Xr1_1_list = [0.0024, 0.0051, 0.0028, 0.0126, 0.0057]
    Xr1_2_list = [12.1564, 9.9823, 16.4121, 15.9432, 13.6235]
    Xr1_5_list = [0.1168, 0.0192, 0.044, 0.0105, 0.0476]
    Xr1_6_list = [-7.1218, -5.5038, -7.8373, -7.8094, -7.0681]
    Xr2_1_list = [0.0125, 0.0125, 0.0125, 0.0125, 0.0125]
    Xr2_2_list = [-25.9945, -25.9945, -25.9945, -25.9945, -25.9945]
    Xr2_5_list = [37.3426, 37.3426, 37.3426, 37.3426, 37.3426]
    Xr2_6_list = [22.0920, 22.0920, 22.0920, 22.0920, 22.0920]
    Xr1_7_list = [50, 50, 50, 50, 50]
    Xr2_7_list = [0, 0, 0, 0, 0]
    plt.subplot(2, 2, 1)

    protocol = 3
    Ikr_IV1 = run_sim1(Vm_plot, protocol, Xr1_0_list[0], Xr1_1_list[0], Xr1_2_list[0], Xr1_5_list[0], Xr1_6_list[0],
                       Xr2_1_list[0],
                       Xr2_2_list[0], Xr2_5_list[0], Xr2_6_list[0], Xr1_7_list[0], Xr2_7_list[0])
    plt.plot(Vm_plot.T, Ikr_IV1[1], color='orangered', label='Wu Lab', linewidth=4)
    plt.plot(Vm_plot.T, Ikr_IV1[2], color='orangered', linewidth=4)

    protocol = 1
    Iks_IV2 = run_sim1(Vm_plot, protocol, Xr1_0_list[1], Xr1_1_list[1], Xr1_2_list[1], Xr1_5_list[1], Xr1_6_list[1],
                       Xr2_1_list[1],
                       Xr2_2_list[1], Xr2_5_list[1], Xr2_6_list[1], Xr1_7_list[1], Xr2_7_list[1])
    plt.plot(Vm_plot.T, Iks_IV2[1], color='blue', label='Ma et al.', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV2[2], color='blue', linewidth=4)

    protocol = 2
    Iks_IV3 = run_sim1(Vm_plot, protocol, Xr1_0_list[2], Xr1_1_list[2], Xr1_2_list[2], Xr1_5_list[2], Xr1_6_list[2],
                       Xr2_1_list[2],
                       Xr2_2_list[2], Xr2_5_list[2], Xr2_6_list[2], Xr1_7_list[2], Xr2_7_list[2])
    plt.plot(Vm_plot.T, Iks_IV3[1], color='purple', label='Es Salah', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV3[2], color='purple', linewidth=4)

    protocol = 4
    Iks_IV4 = run_sim1(Vm_plot, protocol, Xr1_0_list[3], Xr1_1_list[3], Xr1_2_list[3], Xr1_5_list[3], Xr1_6_list[3],
                       Xr2_1_list[3],
                       Xr2_2_list[3], Xr2_5_list[3], Xr2_6_list[3], Xr1_7_list[3], Xr2_7_list[3])
    plt.plot(Vm_plot.T, Iks_IV4[1], color='green', label='Bellin et al.', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV4[2], color='green', linewidth=4)
    protocol = 1
    Iks_IV5 = run_sim1(Vm_plot, protocol, Xr1_0_list[4], Xr1_1_list[4], Xr1_2_list[4], Xr1_5_list[4], Xr1_6_list[4],
                       Xr2_1_list[4],
                       Xr2_2_list[4], Xr2_5_list[4], Xr2_6_list[4], Xr1_7_list[4], Xr2_7_list[4])
    plt.plot(Vm_plot.T, Iks_IV5[1], color='black', label='Baseline Model', linewidth=4)
    plt.plot(Vm_plot.T, Iks_IV5[2], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Normalized I$_{Kr}$', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 1.1, 0.5))
    plt.xlim(-150, 50)
    plt.ylim(0, 1)
    plt.title('A', fontsize=18)
    plt.legend(fontsize='15', loc='best')

    plt.subplot(2, 2, 2)

    plt.plot(Vm_plot.T, Ikr_IV1[0].T, color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[0].T, color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[0].T, color='purple', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[0].T, color='green', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV5[0].T, color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{kr}$ (pA/pF)', size='18')
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 3.1, 1))
    plt.xlim(-150, 50)
    plt.ylim(-0.2, 3)
    plt.title('D', fontsize=18)

    plt.subplot(2, 2, 3)

    plt.plot(Vm_plot.T, Ikr_IV1[3], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[3], color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[3], color='purple', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[3], color='green', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV5[3], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{act}$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 1001, 500))
    plt.xlim(-150, 50)
    plt.ylim(0, 1000)
    plt.title('C', fontsize='18')

    plt.subplot(2, 2, 4)

    plt.plot(Vm_plot.T, Ikr_IV1[4], color='orangered', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV2[4], color='blue', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV3[4], color='purple', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV4[4], color='green', linewidth=4)

    plt.plot(Vm_plot.T, Iks_IV5[4], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_{inact}$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 3.1, 1))
    plt.xlim(-150, 50)
    plt.ylim(0, 3)
    plt.title('D', fontsize=18)

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.3)

    stop = timeit.default_timer()

    print('Time: ', stop - start)

    # plt.show()
    plt.savefig('Figure04.png')
