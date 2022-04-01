# Plot experiment results
import matplotlib.pyplot as plt

def plotExp(figs,subfigs,figfiles):
   # Set figure dimension (width, height) in inches.
   fig, axs = plt.subplots(figs['rows'],figs['cols'],figsize=(figs['width'],figs['height']))
   plt.subplots_adjust(left=figs['left'], bottom=figs['bottom'], right=figs['right'], top=figs['top'], wspace=figs['wspace'], hspace=figs['hspace']) 
   # Set the subfigures  
   for subfig in subfigs.values():       
       rid=subfig['rowid']
       cid=subfig['colid']
       traces=subfig['traces']
       if figs['rows']==1 and figs['cols']==1:
           ax=axs
       elif figs['rows']==1 or figs['cols']==1:
           ax=axs [rid]
       else:
           ax=axs [rid,cid]           
       ax.set_xlabel (subfig['xlabel'], fontsize= subfig['labelfont'])
       ax.set_ylabel (subfig['ylabel'], fontsize= subfig['labelfont'])
       ax.grid(visible=subfig['grid'],  axis=subfig['gridaxis'])
       if subfig['twiny']==True:
           tax = ax.twinx()
           tax.tick_params(axis='y', labelcolor=trace['linecolor'])
           tax.set_ylabel (subfig['ylabel2'], fontsize= subfig['labelfont'],color=subfig['labelcolor'])
           # draw the traces   
           for trace in traces.values():
               if trace['y2']==True:
                   tax.plot(trace['dataX'], trace['dataY'], ls=trace['linestyle'], marker=trace['marker'], color=trace['linecolor'], label = trace['lname'])
               else:
                   ax.plot(trace['dataX'], trace['dataY'], ls=trace['linestyle'], marker=trace['marker'], color=trace['linecolor'], label = trace['lname'])                     
       else:
           # draw the traces
           for trace in traces.values():
               ax.plot(trace['dataX'], trace['dataY'], ls=trace['linestyle'], marker=trace['marker'], color=trace['linecolor'], label = trace['lname'])

       if subfig['lgdshow']==True:
           if subfig['twiny']==True:
               lines, labels = ax.get_legend_handles_labels()
               lines2, labels2 = tax.get_legend_handles_labels()
               ax.legend(lines + lines2, labels + labels2, loc = subfig['lgdloc'], fontsize=subfig['lgdfont'], frameon=False,ncol=subfig['lgdncol'])
           else:
               ax.legend(loc = subfig['lgdloc'], fontsize=subfig['lgdfont'], frameon=False,ncol=subfig['lgdncol'])   
       
       if subfig['setlim']==True:
           ax.set(xlim=(subfig['xmin'], subfig['xmax']), ylim=(subfig['ymin'], subfig['ymax']))   
              
   plt.savefig(figfiles)
   plt.show()
   return fig,axs