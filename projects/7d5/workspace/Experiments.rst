About this model
******************

:Original publication: `Kernik et al. (2019)`_:
  "A computational model of induced pluripotent stem-cell derived cardiomyocytes \
  incorporating experimental variability from multiple data sources" J  Physiol. 2019 Sep 1; 597(17): 4533-4564.

:DOI: https://dx.doi.org/10.1113%2FJP277724

.. _`Kernik et al. (2019)`: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6767694/

**************
Experiments
**************
Here the model run the simulation for each channel in the primary paper in order to reproduce the figures.
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

1. :math:`I_Na` : `Sodium current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig3-new.py/view>`_

2. :math:`I_CaL` : `Calcium current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig4-new.py/view>`_

3. :math:`I_Kr` : `Rapid delayed rectifier potassium current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig5-new.py/view>`_

4. :math:`I_to` : `Transient outward potassium current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig6-new.py/view>`_

5. :math:`I_Ks` : `Slow delayed rectifier potassium current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig7-new.py/view>`_

6. :math:`I_f` : `Pacemaker/funny current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig8-new.py/view>`_

7. :math:`I_{K1}` : `Inward rectifier potassium current model optimization <https://models.physiomeproject.org/e/7c7/Experiments/fig9-new.py/view>`_

8. Calcium Analysis :  `Optimization of calcium handling in the iPSC-CM baseline model <https://models.physiomeproject.org/e/7c7/Experiments/fig10-new.py/view>`_

9. baseline model AP: `Action potential in the iPSC-CM baseline model <https://models.physiomeproject.org/e/7c7/Experiments/fig11-new.py/view>`_

Simulation settings
*********************
Simulation settings (solver, duration of the simulation, etc) are stored in SED-ML files.
The Python scripts contains the required parameters and conditions for each channel
to run simulation and then plot the results with Matplotlib library to reproduce the figures
in the original paper. The name of each scripts presents the Figure number in the primary paper.
fig3-new.py is used to generate the simulation and reproduces the graph shown in
Figure 3 in the original study.
In order to reproduce Figure 3, once all the files are downloaded to the same folder,
execute the following script from the command line (command prompt):

cd [PathToThisFile]

[PathToOpenCOR]/pythonshell fig3-new.py






