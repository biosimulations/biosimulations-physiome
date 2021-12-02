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
    x1_list = [0.0024, 0.0051, 0.0028, 0.0126, 0.0057, 0.0125]
    x2_list = [12.1564, 9.9823, 16.4121, 15.9432, 13.6235, -25.9945]
    x5_list = [0.1168, 0.0192, 0.044, 0.0152, 0.0476, 37.3426]
    x6_list = [-7.1218, -5.5038, -7.8373, -7.8094, -7.0681, 22.092]
    x7_list = [50, 50, 50, 50, 50, 0]
    key_ids = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
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
    plt.plot(voltage, act_inact_list[0]['one'], color='orange', label= 'Wu Lab',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['six'], color='orange',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['two'], color='blue', label= 'Ma et al.',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['six'], color='blue',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['three'], color= 'purple', label= 'Es Salah', linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['six'], color= 'purple', linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['four'], color='green', label= 'Bellin et al.',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['six'], color='green',  linewidth= 4)
    plt.plot(voltage, act_inact_list[0]['five'], color='black', label='Baseline Model', linewidth=4)
    plt.plot(voltage, act_inact_list[0]['six'], color='black',  linewidth= 4)

    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Normalized I$_{Kr}$', fontsize= 18)
    plt.tick_params(axis='both', labelsize='18')
    plt.xlim(-150,50,50)
    plt.ylim(0,1,0.5)
    plt.title('A', fontsize=18)
    plt.legend(fontsize= '15')

    plt.subplot(2,2,3)
    plt.plot(voltage, act_inact_list[1]['one'], color='orange', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['two'], color='blue', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['three'], color='purple', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['four'], color='green', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['five'], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Tau$_{act}$ (ms)', fontsize= 18)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.xlim(-150,50,50)
    plt.ylim(0,1000,500)
    plt.title('C', fontsize= '18')

    #
    plt.subplot(2,2,4)
    plt.plot(voltage, act_inact_list[1]['six'], color='orange', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['six'], color='blue', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['six'], color='purple', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['six'], color='green', linewidth=4)
    plt.plot(voltage, act_inact_list[1]['six'], color='black', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Tau$_{inact}$ (ms)', fontsize= 18)
    plt.tick_params(axis= 'both', labelsize= '18')
    plt.xlim(-150,50,50)
    plt.ylim(0,3,1)
    plt.title('D', fontsize=18)

    # plt.show()
    plt.savefig('Figure05.png')
