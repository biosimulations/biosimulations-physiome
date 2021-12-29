import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'Ist_20ms'
suf=['20','-10']
#suf=['20']
# Figure name
prefig = 'IstPositive'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 12, 9
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 5, 2
ax, lns = {}, {}
lfontsize, labelfontsize = 10, 12 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
plotindex = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
x_name = 'outputs/time'
y_names =['outputs/minus_V','outputs/m','outputs/h','outputs/gNa','outputs/INa',
'outputs/n','outputs/gK','outputs/IK','outputs/Ileak','outputs/Ii']
y_labels =['-V (mV)','m','h','$g_{Na}$','$I_{Na}$','n','$g_{K}$','$I_{K}$','$I_{l}$','$I_{i}$']
rol=int(20*1000)
lines=['-','--']
Ist=['$I_{st}=20$','$I_{st}=-10$']
for j, suffix in enumerate(suf):
   filename ='%s%smV.csv' % (prefilename,suffix)
   data = pd.read_csv(filename)
   for i, y_name in enumerate(y_names):          
       x_data = data[x_name][0:rol]   
       y_data = data[y_name][0:rol]

       if j ==0: 
          ax[i] = fig.add_subplot(subpRow, subpCol, plotindex[i])
       else:
          ax[i].grid(linestyle='-.')
          ax[i].tick_params(direction='in', axis='both')   
          ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)         

          if plotindex[i] in [9,10]: 
            ax[i].set_xlabel ('time(ms)', fontsize= labelfontsize)            
          else:
            ax[i].set_xticklabels([])
        
       ax[i].plot(x_data, y_data, color=cycle[j],linestyle=lines[j],label=Ist[j])
             
ax[i].legend(loc = 'best', fontsize=lfontsize, frameon=False)
plt.savefig(figfile)        
plt.show()




