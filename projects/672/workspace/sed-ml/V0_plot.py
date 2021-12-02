import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'V0'
# Figure name
prefig = 'V0'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 12, 9
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 5, 2
ax, lns = {}, {}
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
plotindex = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
x_name = 'outputs/time'
y_names =['outputs/minus_V','outputs/m','outputs/h','outputs/gNa','outputs/INa',
'outputs/n','outputs/gK','outputs/IK','outputs/Ileak','outputs/Ii']
y_labels =['-V (mV)','m','h','$g_{Na}$','$I_{Na}$','n','$g_{K}$','$I_{K}$','$I_{l}$','$I_{i}$']
rol=int(20*1000)
filename ='%s.csv' % (prefilename)
data = pd.read_csv(filename)
for i, y_name in enumerate(y_names):  
    x_data = data[x_name][0:rol]   
    y_data = data[y_name][0:rol]
    ax[i] = fig.add_subplot(subpRow, subpCol, plotindex[i])
    ax[i].plot(x_data, y_data, color=cycle[0])
    ax[i].tick_params(direction='in', axis='both')   
    ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)
    ax[i].grid(linestyle='-.')
    
    if plotindex[i] in [9,10]: 
        ax[i].set_xlabel ('time(ms)', fontsize= labelfontsize)
    else:
        ax[i].set_xticklabels([])
    
plt.savefig(figfile)        
plt.show()




