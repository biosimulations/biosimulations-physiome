import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'gating'
# Figure name
prefig = 'gating'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 10, 9
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 2, 2
ax, lns = {}, {}
lfontsize, labelfontsize = 10, 10 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
filename ='%s.csv' % (prefilename)
data = pd.read_csv(filename)
x_name = 'outputs/minus_V'
y_names =[['outputs/tau_m','outputs/tau_h','outputs/tau_n'],
['outputs/m_inf','outputs/h_inf','outputs/n_inf'],
['outputs/m3_inf','outputs/h_inf','outputs/n4_inf',],
['outputs/m3h_inf',]]
legends = [['$\\tau_m$ (ms)', '$\\tau_h$ (ms)', '$\\tau_n$ (ms)'],
['$m_\infty$', '$h_\infty$','$n_\infty$', ],
['$m_\infty^3$', '$h_\infty$','$n_\infty^4$' ],
['$m_\infty^3h_\infty$']]

plotindex = [1, 3, 2, 4,]

x_data = data[x_name]
y_labels =['(A)time constant (ms)', '(B) activation/inactivation (single)',
'(C) activation/inactivation (group)', '(D) activation/inactivation (sodium)']

for i, y_label in enumerate(y_labels):
    ax[i] = fig.add_subplot(subpRow, subpCol, plotindex[i])

    for j, y_name in enumerate(y_names[i]):              
       y_data = data[y_name]
       ax[i].plot(x_data, y_data, color=cycle[j], label = legends[i][j])

    ax[i].grid(linestyle='-.')
    ax[i].tick_params(direction='in', axis='both')   
    ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)
    ax[i].set_xlabel ('-V (mV)', fontsize= labelfontsize) 
    ax[i].legend(loc = 'best', fontsize=lfontsize, frameon=False)               

plt.savefig(figfile)        
plt.show()




