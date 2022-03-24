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


start, stop, step = -150, 50, 2

Vm_plot = np.arange(start, stop + step, step)
Vm_plot = Vm_plot.reshape((1, Vm_plot.shape[0]))

file = load_sedml("Current_Ina.sedml")


def run_sim1(Vm_step, protocol, g_Na, m_1, m_2, m_5, m_6, h_1, h_2, h_5, h_6, j_1, j_2, tau_m_const, tau_h_const, tau_j_const):
    Y = np.array((-70, 0.75, 0, 0.75)).reshape(4, 1)


    if protocol == 1: #Jalife

        col1 = -120 * np.ones(Vm_step.T.shape)
        col2 = Vm_step.T

        Vm_mat = np.hstack((col1, col2))
        period = [2000, 200]

    else:
        col1 = -80 * np.ones(Vm_step.T.shape) #Ma
        col2 = Vm_step.T

        Vm_mat = np.hstack((col1, col2))
        period = [2000, 40]

    xy = len(Y)

    values = np.zeros((sum(period)*100, len(Vm_step.T)*xy))
    Time = np.zeros((sum(period)*100, len(Vm_step.T)))

    # sedml file
    data = file.data()

    for j in range(len(Vm_step.T)):
        print(j)
        Time_forVmi = 0
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
                data.constants()["Current_Ina/Na_i"] = 5 #Jalife
                data.constants()["Current_Ina/Nao"] = 20

            else:
                data.constants()["Current_Ina/Na_i"] = 10  #Ma
                data.constants()["Current_Ina/Nao"] = 50



            data.constants()["Current_Ina/g_Na"] = g_Na
            data.constants()["Current_Ina/m_1"] = m_1
            data.constants()["Current_Ina/m_2"] = m_2
            data.constants()["Current_Ina/m_5"] = m_5
            data.constants()["Current_Ina/m_6"] = m_6
            data.constants()["Current_Ina/h_1"] = h_1
            data.constants()["Current_Ina/h_2"] = h_2
            data.constants()["Current_Ina/h_5"] = h_5
            data.constants()["Current_Ina/h_6"] = h_6
            data.constants()["Current_Ina/j_1"] = j_1
            data.constants()["Current_Ina/j_2"] = j_2
            data.constants()["Current_Ina/tau_m_const"] = tau_m_const
            data.constants()["Current_Ina/tau_h_const"] = tau_h_const
            data.constants()["Current_Ina/tau_j_const"] = tau_j_const

            data.states()["Current_Ina/v"] = Y_init[0]
            data.states()["Current_Ina/X_na_h_inact"] = Y_init[1]
            data.states()["Current_Ina/X_na_m_act"] = Y_init[2]
            data.states()["Current_Ina/X_na_j_inact"] = Y_init[3]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(0.02)
            file.run()
            ds = file.results().data_store()

            dv = ds.voi_and_variables()["Current_Ina/v"].values()

            dX_na_h_inact = ds.voi_and_variables()["Current_Ina/X_na_h_inact"].values()
            dX_na_m_act = ds.voi_and_variables()["Current_Ina/X_na_m_act"].values()
            dX_na_j_inact = ds.voi_and_variables()["Current_Ina/X_na_j_inact"].values()
            INaa = ds.voi_and_variables()["Current_Ina/i_na"].values()
            Time_hold = (ds.voi_and_variables()["Current_Ina/t"].values()).T
            Time_hold = Time_hold.reshape(Time_hold.shape[0], 1)
            results = np.stack((dv, dX_na_h_inact, dX_na_m_act, dX_na_j_inact))

            values_hold = results.T
            Y_init = values_hold[-1, :].reshape((values_hold[-1, :].shape[0]),1)



            if i == 0:
                Time_forVmi = Time_hold
                values_forVmi = values_hold
            else:
                values_forVmi = np.vstack((values_forVmi, values_hold))
                Time_forVmi = np.vstack((Time_forVmi, Time_hold))

            if i == 1:
                Time[0: len(Time_hold), j] = Time_hold[:,0]
                Time_hold = Time_hold.reshape((Time_hold.shape[0], 1))

                values[0: np.max(values_hold.shape), (((j+1) * xy) - (xy)): ((j+1) * xy)] = values_hold


    Time = Time[(values != 0).any(axis=1)]
    values = values[(values != 0).any(axis=1)]
    #
    Vm = values[0,:]
    INa = np.zeros(Time.shape)
    INa_peak = np.zeros((1, Time.shape[1]))


    x_h_inact = np.zeros(Vm_step.T.shape)
    x_m_act = np.zeros(Vm_step.T.shape)
    x_j_inact = np.zeros(Vm_step.T.shape)
    tau_h_inact = np.zeros(Vm_step.T.shape)
    tau_m_act = np.zeros(Vm_step.T.shape)
    tau_j_inact = np.zeros(Vm_step.T.shape)
    for j in range(Time.shape[1]):
        # Time_forVmi = 0
        for i in range(0,100):

            timespan = [0, 10]
    #
            file.reset(True)
            file.clear_results()
            if protocol == 1:
                data.constants()["Current_Ina/Na_i"] = 5  # Jalife
                data.constants()["Current_Ina/Nao"] = 20
    #
            else:
                data.constants()["Current_Ina/Na_i"] = 10  # Ma
                data.constants()["Current_Ina/Nao"] = 50

            data.constants()["Current_Ina/g_Na"] = g_Na
            data.constants()["Current_Ina/m_1"] = m_1
            data.constants()["Current_Ina/m_2"] = m_2
            data.constants()["Current_Ina/m_5"] = m_5
            data.constants()["Current_Ina/m_6"] = m_6
            data.constants()["Current_Ina/h_1"] = h_1
            data.constants()["Current_Ina/h_2"] = h_2
            data.constants()["Current_Ina/h_5"] = h_5
            data.constants()["Current_Ina/h_6"] = h_6
            data.constants()["Current_Ina/j_1"] = j_1
            data.constants()["Current_Ina/j_2"] = j_2
            data.constants()["Current_Ina/tau_m_const"] = tau_m_const
            data.constants()["Current_Ina/tau_h_const"] = tau_h_const
            data.constants()["Current_Ina/tau_j_const"] = tau_j_const


            data.states()["Current_Ina/v"] = values[i, (((j+1)*xy)-(xy)):((j+1)*(xy))][0]
            data.states()["Current_Ina/X_na_h_inact"] = values[i, (((j+1)*xy)-(xy)):((j+1)*(xy))][1]
            data.states()["Current_Ina/X_na_m_act"] = values[i, (((j+1)*xy)-(xy)):((j+1)*(xy))][2]
            data.states()["Current_Ina/X_na_j_inact"] = values[i, (((j+1)*xy)-(xy)):((j+1)*(xy))][3]

            data.set_starting_point(timespan[0])
            data.set_ending_point(timespan[1])
            data.set_point_interval(10)
            file.run()
            ds = file.results().data_store()
            INa[i,j] = ds.voi_and_variables()["Current_Ina/i_na"].values()[0]
            x_na_h_inf_inact = ds.voi_and_variables()["Current_Ina/x_na_h_inf_inact"].values()
            x_na_m_inf_act = ds.voi_and_variables()["Current_Ina/x_na_m_inf_act"].values()
            x_na_j_inf_inact = ds.voi_and_variables()["Current_Ina/x_na_j_inf_inact"].values()
            tau_na_h_inact = ds.voi_and_variables()["Current_Ina/tau_na_h_inact"].values()
            tau_na_m_act = ds.voi_and_variables()["Current_Ina/tau_na_m_act"].values()
            tau_na_j_inact = ds.voi_and_variables()["Current_Ina/tau_na_j_inact"].values()

            if abs(INa_peak[0][j]) < abs(INa[i,j]):
                INa_peak[0][j] = INa[i,j]
            x_h_inact[j] = x_na_h_inf_inact[-1]
            x_m_act[j] = x_na_m_inf_act[-1]
            x_j_inact[j] = x_na_j_inf_inact[-1]
            tau_h_inact[j] = tau_na_h_inact[-1]
            tau_m_act[j] = tau_na_m_act[-1]
            tau_j_inact[j] = tau_na_j_inact[-1]

    return INa_peak, x_h_inact, x_m_act, x_j_inact, tau_h_inact, tau_m_act, tau_j_inact



if __name__ == '__main__':
    plt.figure(figsize=(15, 13))

    g_Na_list = [14.123076923076923, 5.891490255824878, 3.3149, 9.7206]
    m_1_list = [99.17442902064411, 116.91726374899146, 1154.108, 108.0458]
    m_2_list = [12.832120283197101, 13.381911184684302, 7.9836, 13.107]
    m_5_list = [0.0038682060291308777, 7.856227043863586E-4, 2.29e-4, 0.00232]
    m_6_list = [- 8.213861508384595, - 7.621591070642387, -6.4445, -7.9177]
    h_1_list = [0.006260500413808546, 9.606028351312509E-4, 0.00365, 0.0036266]
    h_2_list = [- 21.625645364933558, - 17.188238822805108, -20.704, -19.8393]
    h_5_list = [17575.454260436643, 8054.601979288204, 4042.19, 9663.295]
    h_6_list = [6.7241405330309645, 8.825873829432854, 8.7506, 7.3955]
    j_1_list = [6.462635563325624E-4, 2.783705796579095E-4, 6.1213e-4, 5.1225e-4]
    j_2_list = [- 69.41735067912443, - 59.57496548991692, -70.7589, -66.5837]
    tau_m_const_list = [0.037438327480079026, 0.02961757, 0.0288, 0.031977]
    tau_h_const_list = [0.19996250245492342, 0.1524029, 0.1496, 0.16733]
    tau_j_const_list = [1.3218743933806125, 0.74171729, 0.78967, 0.951088]

    plt.subplot(3, 2, 1)

    protocol = 0
    INa_IV1 = run_sim1(Vm_plot, protocol, g_Na_list[0], m_1_list[0], m_2_list[0], m_5_list[0], m_6_list[0], h_1_list[0],
                       h_2_list[0], h_5_list[0],
                       h_6_list[0], j_1_list[0], j_2_list[0], tau_m_const_list[0], tau_h_const_list[0],
                       tau_j_const_list[0])
    plt.plot(Vm_plot.T, INa_IV1[1], color='blue', label='Ma et al.', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV1[2], color='blue', linewidth=4)

    protocol = 1
    INa_IV2 = run_sim1(Vm_plot, protocol, g_Na_list[1], m_1_list[1], m_2_list[1], m_5_list[1], m_6_list[1], h_1_list[1],
                       h_2_list[1], h_5_list[1],
                       h_6_list[1], j_1_list[1], j_2_list[1], tau_m_const_list[1], tau_h_const_list[1],
                       tau_j_const_list[1])
    plt.plot(Vm_plot.T, INa_IV2[1], color='green', label='Jalife Mature', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV2[2], color='green', linewidth=4)
    # #
    #
    protocol = 1
    INa_IV3 = run_sim1(Vm_plot, protocol, g_Na_list[2], m_1_list[2], m_2_list[2], m_5_list[2], m_6_list[2], h_1_list[2],
                       h_2_list[2], h_5_list[2],
                       h_6_list[2], j_1_list[2], j_2_list[2], tau_m_const_list[2], tau_h_const_list[2],
                       tau_j_const_list[2])
    plt.plot(Vm_plot.T, INa_IV3[1], color='purple', label='Jalife Immature', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV3[2], color='purple', linewidth=4)
    #
    protocol = 0
    INa_IV4 = run_sim1(Vm_plot, protocol, g_Na_list[3], m_1_list[3], m_2_list[3], m_5_list[3], m_6_list[3], h_1_list[3],
                       h_2_list[3], h_5_list[3],
                       h_6_list[3], j_1_list[3], j_2_list[3], tau_m_const_list[3], tau_h_const_list[3],
                       tau_j_const_list[3])
    plt.plot(Vm_plot.T, INa_IV4[1], color='black', label='Baseline Model', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV4[2], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Normalized I$_{Na}$', fontsize=18)
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 1.1, 0.5))
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50)
    plt.ylim(0, 1)
    plt.title('A', fontsize=18)
    plt.legend(fontsize='14')

    plt.subplot(3, 2, 2)

    plt.plot(Vm_plot[0], INa_IV1[0][0], color='blue', linewidth=4)

    plt.plot(Vm_plot[0], INa_IV2[0][0], color='green', linewidth=4)

    plt.plot(Vm_plot[0], INa_IV3[0][0], color='purple', linewidth=4)

    plt.plot(Vm_plot[0], INa_IV4[0][0], color='black', linewidth=4)

    plt.xlim(-150, 50)
    plt.ylim(-250, 50)
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(-250, 51, 50))
    plt.tick_params(axis='both', labelsize=18)
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{Na}$ (pA/pF)', size='18')
    plt.title('B', fontsize=18)

    plt.subplot(3, 2, 3)

    plt.plot(Vm_plot.T, INa_IV1[5], color='blue', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV2[5], color='green', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV3[5], color='purple', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV4[5], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_m$ (ms)', fontsize=18)
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 0.61, 0.2))
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50)
    plt.ylim(0, 0.6)
    plt.title('C', fontsize=18)

    plt.subplot(3, 2, 4)

    plt.plot(Vm_plot.T, INa_IV1[4], color='blue', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV2[4], color='green', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV3[4], color='purple', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV4[4], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_h$ (ms)', fontsize=18)
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 6.1, 2))
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50)
    plt.ylim(0, 6)
    plt.title('D', fontsize=18)

    plt.subplot(3, 2, 5)

    plt.plot(Vm_plot.T, INa_IV1[6], color='blue', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV2[6], color='green', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV3[6], color='purple', linewidth=4)
    plt.plot(Vm_plot.T, INa_IV4[6], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_j$ (ms)', fontsize=18)
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks(np.arange(0, 751, 250))
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50)
    plt.ylim(0, 750)
    plt.title('E', fontsize=18)

    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.5,
                        hspace=0.5)

    plt.savefig('Figure02.png')

    stop = timeit.default_timer()
    print('Time: ', stop - start)