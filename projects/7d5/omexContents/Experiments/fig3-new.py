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
    x1_list = [99.1744, 1.1541e+03, 1.080458e+02, 1.169173e+02, 0.0063, 0.0037, 0.0036, 9.6060e-04, 6.4626e-04, 6.1214e-04, 5.1226e-04, 2.7837e-04]
    x2_list = [12.8324, 7.9836, 13.1070, 13.3819, -21.6256, -20.7042, -19.8394, -17.1882, -69.4174, -70.7590, -66.5838, -59.575]
    x5_list = [0.0039, 2.2902e-04, 0.0023, 7.8562e-04, 1.7575e4, 4.04e3, 9.6633e+03, 8.0546e3, 1.7575e+04, 4.0423e3, 9.6633e+03, 8.0546e+03]
    x6_list = [-8.2139, -6.4445, -7.9177, -7.6216, 6.7241, 8.7507, 7.3955, 8.8259, 6.7241, 8.7507, 7.3955, 8.8259]
    x7_list = [0.0374, 0.0289, 0.0320, 0.0296, 0.2, 0.1496, 0.1673, 0.1524, 1.3219, 0.78967, 0.9511, 0.7417]
    key_ids = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
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

            value1 = (ds.voi_and_variables()["main/%s" % var1].values()[-1])
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
    # inact_list = run_sim(data2, inact_file,'inact', 'tau_h')

    # tau_m_list = run_sim(data1, act_file, 'tau_m')
    # tau_h_list = run_sim(data2, inact_file, 'tau_h')


    voltage = np.arange(-150, 51, 1)

    for i in voltage:
        act_inact_list[0]['one'][i] = (act_inact_list[0]['one'][i])**3
        act_inact_list[0]['two'][i] = (act_inact_list[0]['two'][i]) ** 3
        act_inact_list[0]['three'][i] = (act_inact_list[0]['three'][i]) ** 3
        act_inact_list[0]['four'][i] = (act_inact_list[0]['four'][i]) ** 3
        act_inact_list[0]['five'][i] = (act_inact_list[0]['five'][i]) ** 2
        act_inact_list[0]['six'][i] = (act_inact_list[0]['six'][i]) ** 2
        act_inact_list[0]['seven'][i] = (act_inact_list[0]['seven'][i]) ** 2
        act_inact_list[0]['eight'][i] = (act_inact_list[0]['eight'][i]) ** 2

    plt.figure(figsize= (15,13))
    plt.subplot(2,2,1)
    plt.plot(voltage, (act_inact_list[0]['one']), color='blue', label= 'Ma et al.',  linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['five']), color= 'blue', linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['two']), color='purple', label= 'Jalife Immature',  linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['six']), color='purple', linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['three']), color= 'black', label= 'Baseline Model', linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['seven']), color='black', linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['four']), color='green', label= 'Jalife Mature',  linewidth= 4)
    plt.plot(voltage, (act_inact_list[0]['eight']), color='green', linewidth= 4)
    plt.xlabel('Voltage (mV)', fontsize= 18)
    plt.ylabel('Normalized I$_{Na}$', fontsize= 18)
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150,50,50)
    plt.ylim(0,1,0.1)
    plt.title('A', fontsize=18)
    plt.legend(fontsize= '15')

    plt.subplot(2,2,2)
    plt.plot(voltage,  act_inact_list[1]['one'], color='blue', label='Ma et al.', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['two'], color='purple', label='Jalife Immature', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['three'], color='black', label='Baseline Model', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['four'], color='green', label='Jalife Mature', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_m$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50, 50)
    plt.ylim(0, 0.5, 0.05)
    plt.title('C', fontsize=18)
    #
    plt.subplot(2,2,3)
    plt.plot(voltage,  act_inact_list[1]['five'], color='blue', label='Ma et al.', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['six'], color='purple', label='Jalife Immature', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['seven'], color='black', label='Baseline Model', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['eight'], color='green', label='Jalife Mature', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_h$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50, 50)
    plt.ylim(0, 6, 1)
    plt.title('D', fontsize=18)
    #
    plt.subplot(2,2,4)
    plt.plot(voltage,  act_inact_list[1]['nine'], color='blue', label='Ma et al.', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['ten'], color='purple', label='Jalife Immature', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['eleven'], color='black', label='Baseline Model', linewidth=4)
    plt.plot(voltage,  act_inact_list[1]['twelve'], color='green', label='Jalife Mature', linewidth=4)

    plt.xlabel('Voltage (mV)', fontsize=18)
    plt.ylabel('Tau$_j$ (ms)', fontsize=18)
    plt.tick_params(axis='both', labelsize=18)
    plt.xlim(-150, 50, 50)
    plt.ylim(0, 700, 100)
    plt.title('E', fontsize= 18)



    # plt.show()
    plt.savefig('Figure03.png')
