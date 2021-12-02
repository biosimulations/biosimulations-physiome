About this model
====================

:Original publication: `Kernik et al. (2019)`_:
  "A computational model of induced pluripotent stem-cell derived cardiomyocytes
  incorporating experimental variability from multiple data sources" J  Physiol. 2019 Sep 1; 597(17): 4533-4564.

:DOI: https://dx.doi.org/10.1113%2FJP277724

.. _`Kernik et al. (2019)`: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6767694/

************
Figure 06
************
Transient outward potassium current (:math:`I_to`) model optimization
****************************************************************************
The voltage dependent activation and inactivation gating variables were modeled here.
experimental iPSC‐CM data collected from `Ma et al. (2011)`_, `Cordeiro et al. (2013)`_
and `Veerman et al. (2016)`_ in order to optimize data specific model.
Since non of the datasets had both steady-state activation and inactivation data therefore,
Inactivation time constant parameters of `Veerman et al. (2016)`_ model were optimized with time
constant activation from `Ma et al. (2011)`_. `Cordeiro et al. (2013)`_ model parameters were optimized
with steady-state activation parameters from `Ma et al. (2011)`_ and steady-state inactivation
data from `Cordeiro et al. (2013)`_ were used to optimize the model of `Ma et al. (2011)`_. All the
results are presented in Fig. 6. D.
Time constant activation parameters were optimized to `ten Tusscher (2004)`_ model which is shown
in Fig. 6 C.


`act_inact.cellml`_ is the main CellML file which shows the probability of
transient outward potassium channel being open or\
close. Its associated SED-ML file contains all the simulation settings.
All the CellML files and SED-ML files need to be download in a same folder (act_inact, gating, parameter, unit)
as well as python script (`fig6-new.py`_). In the python script, required SED-ML file is loaded
into the script and by running the code following figure is reproduced. `fig6-new.py`_ is used to
generate the simulation and reproduces the graph shown in Figure 6 in the original study.
In order to reproduce Figure 6, once all the files are downloaded to the same folder,
execute the following script from the command line (command prompt):

cd [PathToThisFile]

[PathToOpenCOR]/pythonshell fig6-new.py

.. figure::  Experiments/Figure06.png
   :width: 85%
   :align: center
   :alt: Transient outward potassium current model optimization

A, optimized activation with dataset-specific model fits. Different colour represent experimental
iPSC-CM data from multiple laboratories. C, Time constant of :math:`I_to` activation gate. D,
Time constant of :math:`I_to` inactivation gate.

.. _`ten Tusscher (2004)`: https://journals.physiology.org/doi/full/10.1152/ajpheart.00794.2003/
.. _`Ma et al. (2011)`: https://pubmed.ncbi.nlm.nih.gov/21890694/
.. _`Veerman et al. (2016)`: https://www.nature.com/articles/srep30967/
.. _`Cordeiro et al. (2013)`: https://pubmed.ncbi.nlm.nih.gov/23542310/
.. _`act_inact.cellml`: https://models.physiomeproject.org/workspace/702/rawfile/2a5d36a02c5e82d6a97c237aa20a7f15d2624862/Components/act_inact.cellml
.. _`fig6-new.py`: https://models.physiomeproject.org/workspace/702/rawfile/2a5d36a02c5e82d6a97c237aa20a7f15d2624862/Experiments/fig6-new.py






