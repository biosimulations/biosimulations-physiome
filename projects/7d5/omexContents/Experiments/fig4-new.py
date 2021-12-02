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

    voltage = np.arange(-150, 51, 1)
    x1_list = [7.7247, 14.5675, 12.9663, 8.7706, 15.5608, 0.0016, 3.455e-04, 5.12589e-04, 5.9251e-04, 5.997599860362688e-04]
    x2_list = [6.3888, 7.5014, 7.0791, 7.8748, 5.8612, -82.4603, -43.4169, -49.5057, -52.7783, -52.321981320856140]
    x5_list = [0.088, 0.0326, 0.0449, 0.0622, 0.04, 8.18207e+02, 1.5809e+03, 1.9312e+03, 7.290227e+02, 3.483755573348795e+03]
    x6_list = [-6.2658, -7.3054, -6.9099, -7.6681, -5.7562, 4.3523, 6.1311, 5.73, 6.1849, 4.874098339328655]
    x7_list = [1.7362, 1.6123, 1.6582, 1.6665, 1.696, 97.7424, 99.5232, 100.4626, 97.1476, 104.716837489749]
    key_ids = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
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


    voltage = np.arange(-150, 51, 1)

    plt.figure(figsize= (15,13))
    plt.subplot(2,2,1)
    plt.plot(voltage, act_inact_list[0]['one'], color='blue', label= 'Ma et al.',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['six'], color= 'blue', linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['two'], color='orange', label= 'Veerman1',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['seven'], color='orange',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['three'], color= 'black', label= 'Baseline Model', linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['eight'], color= 'black', linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['four'], color='purple', label= 'Veerman2',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['nine'], color='purple', linewidth=4)
    plt.plot(voltage, act_inact_list[0]['five'], color='green', label='Essalah', linewidth=4)
    plt.plot(voltage, act_inact_list[0]['ten'], color='green', linewidth=4)
    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Normalized I$_{Na}$', fontsize= 18)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.xlim(-100,50,50)
    plt.ylim(0,1,0.1)
    plt.title('A', fontsize=18)
    plt.legend(fontsize= '15')

    plt.subplot(2,2,3)
    plt.plot(voltage, act_inact_list[1]['one'], color='blue', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['two'], color='orange', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['three'], color='black', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['four'], color='purple', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['five'], color='green', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_m$ (ms)', fontsize=18)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.xlim(-100, 50, 50)
    plt.ylim(1.5, 3.5, 0.5)
    plt.title('C', fontsize=18)
    #
    plt.subplot(2,2,4)
    plt.plot(voltage, act_inact_list[1]['six'], color='blue', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['seven'], color='orange', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['eight'], color='black', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['nine'], color='purple', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['ten'], color='green', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Tau$_{inact},I_{CaL}$ (ms)', fontsize= 18)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.xlim(-100,50,50)
    plt.ylim(0,1000,500)
    plt.title('D', fontsize=18)

    # plt.show()
    plt.savefig('Figure04.png')
