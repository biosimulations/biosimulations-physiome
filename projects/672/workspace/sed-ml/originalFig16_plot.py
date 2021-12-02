import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig13'
# Figure name
prefig = 'Fig16'
figfile = 'original%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 6
fig = plt.figure(figsize=(fw,fh))
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
subpRow, subpCol = 1, 1
ax1 = fig.add_subplot(111)
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# Read original data

filename ='fig16_v.csv'
odata = pd.read_csv(filename)
vt = odata['x']   
v = odata['Curve1']  

filename ='fig16_g.csv'
odata = pd.read_csv(filename)
gt = odata['x']   
g = odata['Curve1']

# Read simulation data from the files
V_initial = [-15]
x_name = 'outputs/time'
y_name = 'outputs/minus_V'
g_name = 'outputs/g'

for i, iV_initial in enumerate(V_initial):
    filename ='%s_(%d)mV.csv' % (prefilename, iV_initial)
    data = pd.read_csv(filename)
    x_data = data[x_name]   
    y_data = data[y_name]
    g_data = data[g_name]
    T_data = data['parameters/T']
    lns1 = ax1.plot(x_data, y_data, color=cycle[0], label = 'CellML -V @ %d mV, %0.1f ℃' % (iV_initial, T_data[1] ) )
    lns2 = ax1.plot(vt, v, '.', color=cycle[0], label = 'HH  -V @ %d mV, %0.1f ℃' % (iV_initial, T_data[1] ) )
    ax2 = ax1.twinx()
    lns3 = ax2.plot(x_data, g_data, color=cycle[1], label = 'CellML  g @ %d mV, %0.1f ℃' % (iV_initial, T_data[1] ) )
    lns4 = ax2.plot(gt, g, '.', color=cycle[1], label = 'HH  g @ %d mV, %0.1f ℃' % (iV_initial, T_data[1] ) )
    
# Align 0
ax1_ylims = ax1.axes.get_ylim()           # Find y-axis limits set by the plotter
ax1_yratio = ax1_ylims[0] / ax1_ylims[1]  # Calculate ratio of lowest limit to highest limit
ax2_ylims = ax2.axes.get_ylim()           # Find y-axis limits set by the plotter
ax2_yratio = ax2_ylims[0] / ax2_ylims[1]  # Calculate ratio of lowest limit to highest limit
if ax1_yratio < ax2_yratio: 
    ax2.set_ylim(bottom = ax2_ylims[1]*ax1_yratio)
else:
    ax1.set_ylim(bottom = ax1_ylims[1]*ax2_yratio)
    
plt.tick_params(direction='in', axis='both')    
# added these three lines
lns = lns1 + lns2 + lns3 + lns4
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, frameon=False, loc= 'best')
plt.xlabel ('time(ms)', fontsize= labelfontsize)
ax1.set_ylabel ('-V (mV)', fontsize= labelfontsize)
ax2.set_ylabel ('g (mS/$cm^2$)', fontsize= labelfontsize)
ax1.set_title('%s in the primary publication' % (prefig))
plt.axhline(y=0.0, color="black", linestyle="--")
plt.savefig(figfile)        
plt.show()




