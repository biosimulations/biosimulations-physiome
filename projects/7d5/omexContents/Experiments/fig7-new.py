import os

import matplotlib
matplotlib.use('agg')

import numpy as np
import matplotlib.pyplot as plt

import opencor as opencor


# root = "C:/Nima/ABI/Physiome Journal/pluripotent stem cell/src/cellml/Channels/"


def load_sedml(filename):
    return opencor.open_simulation(filename)

def get_data(filename):
    data = filename.data()
    data.set_ending_point(10)
    data.set_point_interval(1)
    return data


def run_sim(data, filename, var1, var2):

    voltage = np.arange(-100, 101, 1)


    x1_list = [9.3840e-4, 0.0013, 0.0013, 0.0012]
    x2_list = [180.5160, 1e5, 1e5, 6.6727e4]
    x5_list = [0.3532, 0.2614, 0.2268, 0.2805]
    x6_list = [-14.6633, -22.0906, -19.8509, -18.8670]
    x7_list = [1.4223e-05, 2e-11, 2e-11, 4.7411e-6]
    key_ids = ["one", "two", "three", "four"]
    results1 = {}
    results2 = {}
    file = load_sedml(filename)
    for x1, x2, x5, x6, x7, index in zip(x1_list, x2_list, x5_list, x6_list, x7_list, key_ids):
        file.reset(True)
        file.clear_results()
        data.constants()["main/x1"] = x1
        data.constants()["main/x2"] = x2
        data.constants()["main/x5"] = x5
        data.constants()["main/x6"] = x6
        data.constants()["main/x7"] = x7
        results1[index] = []
        results2[index] = []
        for v in voltage:
            data.constants()["main/v"] = v
            file.run()
            ds = file.results().data_store()

            value1 = ds.voi_and_variables()["main/%s" % var1].values()[-1]
            value2 = ds.voi_and_variables()["main/%s" % var2].values()[-1]
            results1[index].append(value1)
            results2[index].append(value2)
    return results1, results2


if __name__ == '__main__':
    act_inact_file = "act_inact.sedml"
    # inact_file = "inact.sedml"

    act_inact = load_sedml(act_inact_file)
    # inact = load_sedml(inact_file)

    data1 = get_data(act_inact)
    # data2 = get_data(inact)

    #
    act_inact_list = run_sim(data1, act_inact_file, 'act_inact', 'tau')
    # inact_list = run_sim(data2, inact_file, 'inact', 'tau_h')
    #
    # tau_m_list = run_sim(data1, act_file, 'tau_m')
    # tau_h_list = run_sim(data2, inact_file, 'tau_h')



    voltage = np.arange(-100, 101, 1)

    plt.figure(figsize= (16,7))
    plt.subplot(1,3,1)
    plt.plot(voltage, act_inact_list[0]['one'], color='blue', label= 'Ma et al.',  linewidth= 4)

    plt.plot(voltage, act_inact_list[0]['two'], color='orange', label='Ma, Wei et al. patient', linewidth=4)

    plt.plot(voltage, act_inact_list[0]['three'], color='purple', label= 'Ma, Wie et al. iCell',  linewidth= 4)

    plt.plot(voltage, act_inact_list[0]['four'], color='black', label= 'Baseline Model',  linewidth= 4)




    plt.xlabel('Voltage (mV)', fontsize= 14)
    plt.ylabel('Normalized I$_{Ks}$', fontsize= 14)
    plt.xlim(-100,100,50)
    plt.ylim(0,1,0.5)
    plt.tick_params(axis='both', labelsize='18')
    plt.title('A', fontsize=18)
    plt.legend(fontsize= '14')

    # #
    plt.subplot(1,3,2)
    plt.plot(voltage, act_inact_list[1]['one'], color='blue', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['three'], color='orange', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['two'], color='green', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['four'], color='black', linewidth=4)


    plt.xlabel('Voltage (mV)', fontsize= 14)
    plt.ylabel('Tau$_{act},I_{Ks}$ (ms)', fontsize= 14)
    plt.xlim(-100,100,50)
    plt.ylim(0,1000,500)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.title('B', fontsize=18)

    # plt.show()
    plt.savefig('Figure07.png')
