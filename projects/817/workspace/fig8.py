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


def get_data(filename):
    data = filename.data()
    data.set_ending_point(100)
    data.set_point_interval(1)
    return data


def run_sim(data, filename, Ki):
    ik1_list = []


    voltage = np.arange(-150, 51, 1)

    var1_list = [0.0229, 0.0841, 0.1338, 0.3745, 0.185]
    var2_list = [0.0012, 0.0861, 0.4780, 0.1815, 1.6433]
    var3_list = [1.2173, 93.9391, 27.2428, 10.5111, 0.3036]
    var4_list = [8.5590, 9.5527, 4.9250, 0.0448, 1.5436]
    var5_list = [0.1162, 23.0096, 8.7222, 0.0203, 0.1132]
    var6_list = [77.5571, 5.8902, 56.6362, 89.1151, 53.9824]
    key_ids = ["one", "two", "three", "four", "five"]
    results1 = {}
    file = load_sedml(filename)
    for var1, var2, var3, var4, var5, var6, index in zip(var1_list, var2_list, var3_list, var4_list, var5_list, var6_list, key_ids):
        file.reset(True)
        file.clear_results()
        data.constants()["Current_Ik1/var_1"] = var1
        data.constants()["Current_Ik1/var_2"] = var2
        data.constants()["Current_Ik1/var_3"] = var3
        data.constants()["Current_Ik1/var_4"] = var4
        data.constants()["Current_Ik1/var_5"] = var5
        data.constants()["Current_Ik1/var_6"] = var6
        results1[index] = []

        for v in voltage:
            data.constants()["Current_Ik1/Ki"] = Ki
            data.constants()["Current_Ik1/v"] = v
            file.run()
            ds = file.results().data_store()
            value1 = ds.voi_and_variables()["Current_Ik1/i_k1"].values()[-1]
            results1[index].append(value1)

    return results1


if __name__ == '__main__':
    Channel_file = "Current_Ik1.sedml"

    Channel = load_sedml(Channel_file)

    data = get_data(Channel)

    Ik1_kurokawa_list = run_sim(data, Channel_file, 125)
    Ik1_ma_list = run_sim(data, Channel_file, 150)
    Ik1_baseline_list = run_sim(data, Channel_file, 148)
    Jalife_Mature_IK1_list = run_sim(data, Channel_file, 148)
    Jalife_Immature_IK1_list = run_sim(data, Channel_file, 148)

    voltage = np.arange(-150, 51, 1)

    plt.figure(figsize=(7, 6))
    plt.plot(voltage, Jalife_Mature_IK1_list["four"], color='green', linewidth=3, label='Jalife Mature')
    plt.plot(voltage, Jalife_Immature_IK1_list["five"], color='purple', linewidth=3, label='Jalife Immature')
    plt.plot(voltage, Ik1_ma_list['two'], color='blue', linewidth=3, label='Ma et al.')
    plt.plot(voltage, Ik1_kurokawa_list['one'], color='orangered', linewidth=3, label='Kurokawa Lab')
    plt.plot(voltage, Ik1_baseline_list["three"], color='black', linewidth=3, label='Baseline Model')

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('I$_{K1}$ (pA/pF)', fontsize=18)
    plt.xticks(np.arange(-150, 51, 50))
    plt.yticks((np.arange(-20, 5.1, 5)))
    plt.xlim(-150, 50)
    plt.ylim(-20, 5)
    plt.tick_params(axis='both', labelsize='18')
    plt.legend(fontsize='14')

    plt.tick_params(axis='both', labelsize='18')
    plt.xlabel('Voltage (mV)', size='18')
    plt.ylabel('I$_{k1}$ (pA/pF)', size='18')
    plt.subplots_adjust(left=0.2,
                        bottom=0.2,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)


    plt.savefig('Figure08.png')

    stop = timeit.default_timer()
    print('Time: ', stop - start)