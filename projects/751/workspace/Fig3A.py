# To reproduce Figure 3 in the associated Physiome paper,
# execute this script from the command line:

#   cd [PathToThisFile]
#   [PathToOpenCOR]/pythonshell Figure3A.py

import os

import matplotlib

matplotlib.use('agg')

import numpy as np
import matplotlib.pyplot as plt

import opencor as opencor

root = "C:/Users/nafs080/work/BG-python-project/resources"
simulation = opencor.open_simulation(os.path.join(root, 'AE1-BG.sedml'))
data = simulation.data()
data.set_ending_point(10)
data.set_point_interval(1)
result = []
q_HCO3_i_vec = [0,5,10,15,20,25,30,35,40,45,50,60]
for q in q_HCO3_i_vec:
    simulation.reset(True)
    simulation.clear_results()
    data.constants()["AE1/q_Cl_o"] = 114
    data.constants()["AE1/q_Cl_i"] = 29
    data.constants()["AE1/q_HCO3_o"] = 26
    data.constants()["AE1/K_Cl_o"] = 1.34784535e+00
    data.constants()["AE1/K_Cl_i"] = 1.34809503e+00
    data.constants()["AE1/K_HCO3_i"] = 8.37243345e-01
    data.constants()["AE1/K_HCO3_o"] = 8.37398440e-01
    data.constants()["AE1/K_E_o"] = 3.42812779e+00
    data.constants()["AE1/K_E_i"] = 3.71610024e-01
    data.constants()["AE1/K_ECl_o"] = 2.30943735e+02
    data.constants()["AE1/K_ECl_i"] = 2.50575623e+01
    data.constants()["AE1/K_EHCO3_o"] = 5.68610961e+02
    data.constants()["AE1/K_EHCO3_i"] = 6.15805309e+01

    data.constants()["AE1/K_Re1"] = 2.16462852e+01
    data.constants()["AE1/K_Re2"] = 2.43394395e+00
    data.constants()["AE1/K_Re3"] = 1.99577523e+02
    data.constants()["AE1/K_Re4"] = 3.21470643e+02
    data.constants()["AE1/K_Re5"] = 2.19265742e+00
    data.constants()["AE1/K_Re6"] = 3.48281500e+01

    data.states()["AE1/q_E_o"] = 0.01738
    data.states()["AE1/q_E_i"] = 0.473
    data.states()["AE1/q_ECl_o"] = 0.0396
    data.states()["AE1/q_ECl_i"] = 0.274
    data.states()["AE1/q_EHCO3_i"] = 0.0621
    data.states()["AE1/q_EHCO3_o"] = 0.00228
    data.constants()["AE1/q_HCO3_i"] = q
    simulation.run()
    ds = simulation.results().data_store()
    value = ds.voi_and_variables()["AE1/v_Re5"].values()[-1]
    result.append(value)
# print(result)


simulation1 = opencor.open_simulation(os.path.join(root, 'Weinstein_2000_AE1_Fig3.sedml'))
data1 = simulation1.data()
data1.set_ending_point(10)
data1.set_point_interval(1)
result_cellml = []
for q in q_HCO3_i_vec:
    simulation1.reset(True)
    simulation1.clear_results()
    data1.states()["concentrations/HCO3_int"] = q
    simulation1.run()
    ds = simulation1.results().data_store()
    value1 = ds.voi_and_variables()["fluxes/J_AE1_HCO3"].values()
    result_cellml.append(value1)

# print(result_cellml)



plt.plot(q_HCO3_i_vec, result, color= 'green')
plt.plot(q_HCO3_i_vec, result_cellml, color= 'blue')
plt.xlabel('HCO3_i')
plt.ylabel('HCO3 flux')
plt.savefig("Figure3A.png")
# plt.show()




