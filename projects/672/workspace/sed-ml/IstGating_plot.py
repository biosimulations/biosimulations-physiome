import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'Ist_20ms'
suf=['-10']
# Figure name
prefig = 'IstGating'
figfile = '%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 9
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 3, 1
lns = {}
lfontsize, labelfontsize = 10, 10 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
plotindex = [1, 2, 3]
x_name = 'outputs/time'
y_names =[['outputs/minus_V','outputs/m','outputs/h','outputs/n',],['outputs/minus_V','outputs/gNa','outputs/gK',],
['outputs/minus_V','outputs/INa','outputs/IK','outputs/Ileak','outputs/Ii']]
yl_names =[['-V','m','h','n',],['-V','$g_{Na}$','$g_{K}$',],
['-V','$I_{Na}$','$I_{K}$','$I_{l}$','$I_{i}$']]
y_labels =[['-V (mV)','gating'], ['-V (mV)','conductance'], ['-V (mV)','Currents']]
rol=int(30*1000)
w, h = 2, len(y_labels)
ax = [[0 for x in range(w)] for y in range(h)]  

for j, iV_initial in enumerate(suf):
   filename ='%s%smV.csv' % (prefilename, iV_initial)
   data = pd.read_csv(filename)
   x_data = data[x_name][0:rol]
   for i, y_name in enumerate(y_names):
       for m, iy_name in enumerate(y_name):
           y_data = data[iy_name][0:rol]           
           if m == 0: 
              ax[i][0] = fig.add_subplot(subpRow, subpCol, plotindex[i])          
              ax[i][0].plot(x_data, y_data,'-.', color=cycle[m],label='%s' % (yl_names[i][m]))
              ax[i][0].set_ylabel (y_labels[i][0], fontsize= labelfontsize)
              ax[i][0].tick_params(direction='in', axis='both')
              ax[i][0].grid(axis='x',linestyle='-.')
           elif m == 1:               
              ax[i][1] = ax[i][0].twinx()
              lns[m]= ax[i][1].plot(x_data, y_data, color=cycle[m], label='%s' % (yl_names[i][m]))
              sumlns=lns[m]
              ax[i][1].set_ylabel (y_labels[i][1], fontsize= labelfontsize)
              ax[i][1].tick_params(direction='in', axis='both')               
           else:
              lns[m]= ax[i][1].plot(x_data, y_data, color=cycle[m], label='%s' % (yl_names[i][m])) 
              
              sumlns=sumlns+lns[m]

           if plotindex[i] in [3]: 
              ax[i][0].set_xlabel ('time(ms)', fontsize= labelfontsize)            
           else:
              ax[i][0].set_xticklabels([])

       ax[i][1].legend(sumlns, yl_names[i][1:], frameon=False, loc= 'upper right') 
   
plt.savefig(figfile)        
plt.show()




