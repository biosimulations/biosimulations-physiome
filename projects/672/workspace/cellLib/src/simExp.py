# Simulate experiments
import opencor as oc
import numpy as np
def simExp(simfile, savefiles,start, ending, pointInterval,indexStart,indexEnd,varSet,varLoop,varSave):
   # Allow one variable to loop
   if len(varLoop)>1:
       sys.exit("The number of the variables to loop is greater than 1") 
   # Load the simulation file   
   simulation = oc.open_simulation(simfile)
   # The data object houses all the relevant information
   # and pointers to the OpenCOR internal data representations
   data = simulation.data()
   data.set_starting_point(start)
   data.set_ending_point(ending)
   data.set_point_interval(pointInterval) 
   # If need to save peak value
   peak=False
   getallSave = list(varSave.values()) 
   for i,geti in enumerate(getallSave):
      if True in geti.values():   
         peak=True
   # Variable to loop
   loopVar=list(varLoop)[0]
   loopPair = list(varLoop.values())[0]
   loopType=list(loopPair)[0]
   loopValues=list(loopPair.values())[0]
   print(loopVar,loopValues)
   # Data to save
   varName = np.array(list(varSave))
   vars = np.reshape(varName, (1, len(varName)))
   # Create a matrix r to save the data   
   rows=indexEnd-indexStart
   if len(savefiles)==1 and (rows==1 or peak==True):
       r = np.zeros((len(loopValues),len(varName)))
       finalSave=True 
   else:
       r = np.zeros((rows,len(varName)))
       finalSave=False
   # Run the simulation
   for k, ivalue in enumerate(loopValues):
       # Reset states and parameters
       simulation.reset(True)
       # Set parameter values
       if loopType=='constants':
          data.constants()[loopVar] = ivalue          
       elif loopType=='algebraic':
          data.algebraic()[loopVar] = ivalue
       elif loopType=='states':
          data.states()[loopVar] = ivalue
       else:
           sys.exit("Wrong type of the variable") 
       for setVar, setPair  in varSet.items():
           setType = list(setPair)[0]
           setValue= list(setPair.values())[0]
           if setType=='constants':
              data.constants()[setVar] = setValue
           elif setType=='algebraic':
              data.algebraic()[setVar] = setValue
           elif setType=='states':
              data.states()[setVar] = setValue
           else:
              sys.exit("Wrong type of the variable")         
       simulation.run()
       # Access simulation results
       results = simulation.results()
       # Grab specific variable results
       m=0       
       for saveVar, savePair  in varSave.items():
           saveType = list(savePair)[0]
           fpeak = list(savePair.values())[0]              
           if saveType =='constants':
              tempr = results.constants()[saveVar].values()[indexStart:indexEnd]              
           elif saveType =='algebraic':
              tempr = results.algebraic()[saveVar].values()[indexStart:indexEnd]
           elif saveType =='states':
              tempr = results.states()[saveVar].values()[indexStart:indexEnd]
           elif saveType =='voi':
              tempr = results.voi().values()[indexStart:indexEnd] 
           else:
              sys.exit("Wrong type of the variable")                      
           if finalSave==False:
              r[:,m] = tempr              
           else:
              if fpeak == True:
                 index_max = np.argmax(abs(tempr))
                 r[k,m] = tempr[index_max]
              else:                 
                 r[k,m] = tempr[-1] 
           m=m+1
       if finalSave==False:
          # Save the simulation result of the last run       
          filename='%s.csv' % (savefiles[k])
          np.savetxt(filename, vars, fmt='%s',delimiter=",")
          with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
          f.close
       # clear the results
       simulation.clear_results() 

   if finalSave==True:    
      # Save the simulation result for all       
      filename='%s.csv' % (savefiles[0])
      np.savetxt(filename, vars, fmt='%s',delimiter=",")
      with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
      f.close

   print(filename)

