import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig13'
# Figure name
prefig = 'Fig19'
figfile = 'original%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 8, 9
fig = plt.figure(figsize=(fw,fh))
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
subpRow, subpCol = 2, 1
ax = {}
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# For reading original data derived from the paper
filesuffix=['v','gK','h']
filepre = 'fig19'
ox_data, oy_data = {}, {}
for i, ifile in enumerate(filesuffix):
    filename ='%s_%s.csv' % (filepre, ifile)
    odata = pd.read_csv(filename)
    ox_data[i] = odata['x']   
    oy_data[i] = odata['Curve1']

# Read data from the files
V_initial = -15
x_name = 'outputs/time'
y_name = 'outputs/minus_V'
g_name = 'outputs/gK'
h_name = 'outputs/h'

filename ='%s_(%d)mV.csv' % (prefilename, V_initial)
data = pd.read_csv(filename)
x_data = data[x_name]   
y_data = data[y_name]
g_data = data[g_name]
h_data = data[h_name]
T_data = data['parameters/T']

ax[1] = fig.add_subplot(subpRow, subpCol, 1)
ax[1].plot(x_data, y_data, color=cycle[0], label = 'CellML model -V @ %d mV, %0.1f ℃' % (V_initial, T_data[1] ) )
ax[1].plot(ox_data[0], oy_data[0], '.', color=cycle[0], label = 'HH model -V @ %d mV, %0.1f ℃' % (V_initial, T_data[1] ) )
ax[1].set_ylabel ('-V (mV)', fontsize= labelfontsize)

ax[1].legend(frameon=False,loc= 'best')

ax[2] = fig.add_subplot(subpRow, subpCol, 2)
label1 = 'CellML model g @ %d mV, %0.1f ℃' % (V_initial, T_data[1] ) 
lns1 = ax[2].plot(x_data, g_data,  color=cycle[0] )
label2 = 'HH model g @ %d mV, %0.1f ℃' % (V_initial, T_data[1] )
lns2 = ax[2].plot(ox_data[1], oy_data[1], '.', color=cycle[0] )
ax[2].set_ylabel ('g (mS/$cm^2$)', fontsize= labelfontsize)

ax[3] = ax[2].twinx()
label3 = 'CellML model h @ %d mV, %0.1f ℃' % (V_initial, T_data[1] )
lns3 = ax[3].plot(x_data, h_data,  color=cycle[1])
label4 = 'HH model h @ %d mV, %0.1f ℃' % (V_initial, T_data[1] )
lns4 = ax[3].plot(ox_data[2], oy_data[2], '.', color=cycle[1])
ax[3].set_ylabel ('h', fontsize= labelfontsize)

ax[3].set_xlabel ('time(ms)', fontsize= labelfontsize)
lns = lns1 + lns2 + lns3 + lns4
ax[2].legend(lns, [label1, label2, label3, label4], frameon=False, loc= 'center right')

plt.savefig(figfile)        
plt.show()




