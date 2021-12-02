import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'Ist_10ms'
suf=['-10','-50',]
# Figure name
prefig = 'Ist2_IV'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 6
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 1, 1
ax, lns = {}, {}
lfontsize, labelfontsize = 10, 10 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
x_name = 'outputs/minus_V'
y_name ='outputs/Ii'
y_name1 ='outputs/Istim'
y_labels =['$I_i(\mu A/cm^2)$']

ax = fig.add_subplot(subpRow, subpCol, 1)
rol=int(6*1000)
for i, suffix in enumerate(suf):
    filename ='%s%smV.csv' % (prefilename,suffix)
    data = pd.read_csv(filename)       
    x_data = data[x_name][0:rol]   
    y_data = data[y_name][0:rol] 
    y_data1 = data[y_name1][0:rol] 

    ax.plot(x_data, y_data, color=cycle[i],label='$I_{st}$=%s $\mu A/cm^2$, $I_i$' % (suffix))
    ax.plot(x_data, y_data+y_data1, '-.', color=cycle[i], label='$I_{st}$=%s $\mu A/cm^2$, $I_i+I_{stim}$' % (suffix))
    
ax.tick_params(direction='in', axis='both')   
ax.set_ylabel (y_labels[0], fontsize= labelfontsize)
ax.grid(linestyle='-.')
ax.set_xlabel ('-V (mV)', fontsize= labelfontsize)   
ax.legend(loc = 'best', fontsize=lfontsize, frameon=False)   
plt.savefig(figfile)        
plt.show()




