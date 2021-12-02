About this model
*****************

:Original publication: `Kernik et al. (2019)`_:
  "A computational model of induced pluripotent stem-cell derived cardiomyocytes \
  incorporating experimental variability from multiple data sources" J  Physiol. 2019 Sep 1; 597(17): 4533-4564.

:DOI: https://doi.org/10.1113/JP277724


Model status
**************

The current CellML model implementation runs OpenCOR_.
The simulation settings are saved in SED-ML file. \
SED-ML files then loaded into OpenCOR using Python scripts in order for the code to iterate \
over different initial conditions and inputs and capture the results.
The CellML and SED-ML files and Python scripts can reproduce \
results presented in the primary published paper.


Model overview
*****************
This workspace holds a CellML_ and Python encoding of the `Kernik et al. (2019)`_
model. The original model developed a whole cell model of
induced pluripotent stem cell-derived cardiomyocytes (iPSC-CMs)
composed of simple model components comprising ion channel models with single exponential
voltage-dependent gating variable rate constants. The model were parameterized to fit experimental
iPSC-CM data from multiple laboratories for all major ionic currents. The resulting population
of cellular models predicts robust inter-subject variability in iPSC-CMs.
This approach links molecular mechanisms to known cellular-level iPSC-CM phenotypes,
as shown by comparing immature and mature subpopulations of models to analyse the contributing
factors underlying each phenotype.

.. figure::  schematic-diagram.jpg
   :width: 85%
   :align: center
   :alt: Schematics of the model

   A diagrammatic representation of the Kernik et al. (2019) model.

.. _CellML: https://www.cellml.org/
.. _OpenCOR: https://opencor.ws/
.. _GitHub: https://github.com/ClancyLabUCD/IPSC-model/


Modular description
********************

Components
----------

CellML enables models to be encoded in a modular manner such that each module can be independently tested priort to
composing the modules into larger models to address specific aims.
The main modules for this model are:

- `Components <Components>`_ which include:
    - Main module that assembles the membrane channels: `Channels <Components/Channels.cellml/view>`_. This file is the main CellML file which is the top model in the hierarchical modular presentation and rest of the files need to be imported here in order to run the simulation.
    - These files have the formulation for calculating each channel's current (for example: *Current_Ik1*): `Current_Ik1 <Components/Current_Ik1.cellml/view>`_
    - This file contains the formulation for Nernst potential: `Nernst_potential <Components/Nernst_potential.cellml/view>`_
    - Different protocol to choose a value for intracellular potassium: `Protocol <Components/Protocol.cellml/view>`_
    - Probability of channels gates being open or close: `act_inact <Components/act_inact.cellml/view>`_. This file is the main CellML file for calculation the probability of channels gates being open or close and also the activation/inactivation time constants. Some other files need to be imported here in order to run the simulation.
    - Hodgkin-Huxley-type gating formulations are provided in a single module here: `gating <Components/gatting.cellml/view>`_
    - some of the channels have different gating formulation which is collected in specific file (for example: *gating_Ik1*): `gating_Ik1 <Components/gating_Ik1.cellml/view>`_
    - General file for required parameters: `parameter <Components/parameter.cellml/view>`_. This file is a general file, specific parameters for calculating the probability of each channel's gate being open or close are presented in associated python script.
    - some of the channels have their own parameters which are collected in specific file (for instance: *parameter_Ik1*): `parameter_Ik1 <Components/parameter_Ik1.cellml/view>`_
    - All the required units for this simulation: `unit <Components/unit.cellml/view>`_



Experiments
-----------

Here in the `Experiments <Experiments>`_ folder, the model run the simulation for each channel in the primary paper in order to reproduce the figures.
In each section in the navigation panel, simulation calculates
the probability of that channel being open or close. Each figure includes one python script
which can load the SED-ML file and provide the
simulation results. In each figure parameters for voltage-dependent activation and inactivation gates
were optimized to  iPSC-CM experimental data from various laboratories. baseline model calculate all the
current through different channels and needs its own python script in order to plot the action potential of developed model.
Calcium analysis needs the python script for the baseline model as well as other function saved in different script in order to show
the calcium analysis.

This workspace has nine sets of experiments and corresponding simulation results, we just provided
the simulation results here in order to check the reproducibility of figures in the primary paper:

1. :math:`I_Na` : `Sodium current model optimization <Experiments/fig3-new.py/view>`_

2. :math:`I_CaL` : `Calcium current model optimization <Experiments/fig4-new.py/view>`_

3. :math:`I_Kr` : `Rapid delayed rectifier potassium current model optimization <Experiments/fig5-new.py/view>`_

4. :math:`I_to` : `Transient outward potassium current model optimization <Experiments/fig6-new.py/view>`_

5. :math:`I_Ks` : `Slow delayed rectifier potassium current model optimization <Experiments/fig7-new.py/view>`_

6. :math:`I_f` : `Pacemaker/funny current model optimization <Experiments/fig8-new.py/view>`_

7. :math:`I_{K1}` : `Inward rectifier potassium current model optimization <Experiments/fig9-new.py/view>`_

8. Calcium Analysis :  `Optimization of calcium handling in the iPSC-CM baseline model <Experiments/fig10-new.py/view>`_

9. baseline model AP: `Action potential in the iPSC-CM baseline model <Experiments/fig11-new.py/view>`_

Simulation settings
-------------------

Simulation settings (solver, duration of the simulation, etc) are stored in SED-ML files.
The Python scripts contains the required parameters and conditions for each channel
to run simulation and then plot the results with Matplotlib library to reproduce the figures
in the original paper. The name of each scripts presents the Figure number in the primary paper.
For example, fig3-new.py is used to generate the simulation and reproduces the graph shown in
Figure 3 in the original study.
In order to reproduce Figure 3, once all the files are downloaded to the same folder,
execute the following script from the command line (command prompt):

cd [PathToThisFile]

[PathToOpenCOR]/pythonshell fig3-new.py

Model History
*************

The original model of **induced pluripotent stem-cell derived cardiomyocytes incorporating
experimental variability from multiple data sources** was built in MATLAB which can be
downloaded from GitHub_.

.. _`Kernik et al. (2019)`: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6767694/

