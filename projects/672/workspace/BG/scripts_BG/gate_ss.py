# importing modules
from asyncio import constants
import sys as sys
import os 
import numpy
import opencor as oc
import pandas as pd 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))  # scripts_BG
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current) # BG
gparent = os.path.dirname(parent) # VPH-MIP
mpath = gparent + '\\cellLib\\src'
# appending a path
sys.path.append(mpath)
import simExp


filename = current+'\\kineticGHK.csv'
data = pd.read_csv(filename)
q_data = data['Channels($fmol$)']   
qNa_data = q_data[0]
qK_data = q_data[1]

print(qNa_data,qK_data)

simfile = parent+'\\gate_n4_BG_ss.sedml'
savefiles=[current+'\\gate_n4_BG_ss']
simulation = oc.open_simulation(simfile)
data = simulation.data()
ending=data.ending_point()
indexStart = int(ending/data.point_interval())
indexEnd = indexStart + 1 
varSet = {'initials/q_S0_init':{'constants':qK_data},'outputs/q_S0':{'states':qK_data}}
varLoop = {'boundary_conditions/V_m':{'constants':1e-3*numpy.arange(-105, 66, 1)}}
varSave = {'boundary_conditions/V_m':{'constants':False},'outputs/q_S0':{'states':False},'outputs/q_S1':{'states':False},'outputs/q_S2':{'states':False},
'outputs/q_S3':{'states':False},'outputs/q_S4':{'states':False},'outputs/q_S4_norm':{'algebraic':False},}

simExp.simExp(simfile, savefiles,ending,indexStart,indexEnd,varSet,varLoop,varSave)

simfile = parent+'\\gate_m3h_BG_ss.sedml'
savefiles=[current+'\\gate_m3h_BG_ss']
simulation = oc.open_simulation(simfile)
data = simulation.data()
ending=data.ending_point()
indexStart = int(ending/data.point_interval())
indexEnd = indexStart + 1 
varSet = {'initials/q_S00_init':{'constants':qNa_data},'outputs/q_S00':{'states':qNa_data}}
varLoop = {'boundary_conditions/V_m':{'constants':1e-3*numpy.arange(-90, 41, 1)}}
varSave = {'boundary_conditions/V_m':{'constants':False},'outputs/q_S00':{'states':False},'outputs/q_S01':{'states':False},
'outputs/q_S10':{'states':False},'outputs/q_S11':{'states':False},
'outputs/q_S20':{'states':False},'outputs/q_S21':{'states':False},
'outputs/q_S30':{'states':False},'outputs/q_S31':{'states':False},'outputs/q_S31_norm':{'algebraic':False},}

simExp.simExp(simfile, savefiles,ending,indexStart,indexEnd,varSet,varLoop,varSave)