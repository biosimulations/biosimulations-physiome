About this model
====================

:Original publication: `Kernik et al. (2019)`_:
  "A computational model of induced pluripotent stem-cell derived cardiomyocytes
  incorporating experimental variability from multiple data sources" J  Physiol. 2019 Sep 1; 597(17): 4533-4564.

:DOI: https://dx.doi.org/10.1113%2FJP277724

.. _`Kernik et al. (2019)`: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6767694/

************
Figure 08
************
Pacemaker/funny current (:math:`I_f`) model optimization
****************************************************************************

The voltage dependent activation gating variables were modeled here.
experimental iPSC‐CM data collected from `Ma et al. (2011)`_ and Kurokawa Lab `Li et al. (2017)`_
in order to optimize data specific model. Activation gate parameters were
optimized using the steady-state activation and activation time constants from experimental data
(Fig. 8. A and B).


`act_inact.cellml`_ is the main CellML file which shows the probability of
transient outward potassium channel being open or\
close. Its associated SED-ML file contains all the simulation settings.
All the CellML files and SED-ML files need to be download in a same folder (act_inact, gating, parameter, unit)
as well as python script (`fig8-new.py`_). In the python script, required SED-ML file is loaded
into the script and by running the code following figure is reproduced. `fig8-new.py`_ is used to
generate the simulation and reproduces the graph shown in Figure 8 in the original study.
In order to reproduce Figure 8, once all the files are downloaded to the same folder,
execute the following script from the command line (command prompt):

cd [PathToThisFile]

[PathToOpenCOR]/pythonshell fig8-new.py

.. figure::  Experiments/Figure08.png
   :width: 85%
   :align: center
   :alt: Pacemaker/funny current model optimization

A, optimized steady-state activation with dataset-specific model fits. Different colour represent experimental
iPSC-CM data from multiple laboratories. B, Time constant of :math:`I_f` activation gate.

.. _`Ma et al. (2011)`: https://pubmed.ncbi.nlm.nih.gov/21890694/
.. _`Li et al. (2017)`: https://pubmed.ncbi.nlm.nih.gov/28615142/
.. _`act_inact.cellml`: https://models.physiomeproject.org/workspace/702/rawfile/2a5d36a02c5e82d6a97c237aa20a7f15d2624862/Components/act_inact.cellml
.. _`fig8-new.py`: https://models.physiomeproject.org/workspace/702/rawfile/2a5d36a02c5e82d6a97c237aa20a7f15d2624862/Experiments/fig8-new.py






