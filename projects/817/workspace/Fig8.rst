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
Inward rectifier potassium current (:math:`I_{K1}`) model optimization
****************************************************************************

The slow delayed rectifier potassium current was modeled here.
experimental iPSC-CM data collected from `Ma et al. (2011)`_ , Kurokawa Lab (`Li et al. (2017)`_),
and the Jalife Lab (`Herron et al. (2016)`_) in order to optimize data specific model.

`Current_Ik1.cellml`_  is the main CellML files which has all the formulation for Inward rectifier potassium current,
Its associated Sedml file contains all the simulation settings.

All the CellML files and SED-ML files related to this channel need to be downloaded in a same folder (Current_Ik1, gating_Ik1, parameter_Ik1, parameter, unit)
as well as python script (`fig8.py`_). In the python script, required Sedml file (Current_Ik1.sedml) is loaded
into the script and by running the code following figure is reproduced.`fig8.py`_ is used to
generate the simulation and reproduces the graph shown in Figure 9 in the original study.
In order to reproduce Figure 9, once all the files are downloaded to the same folder,
execute the following script from the command line (command prompt):

cd [PathToThisFile]

[PathToOpenCOR]/pythonshell fig8.py

.. figure:: Figure08.png
   :width: 85%
   :align: center
   :alt: I-V curve with dataset-specific model fits. Different colour represent experimental
    iPSC-CM data from multiple laboratories


.. _`Ma et al. (2011)`: https://pubmed.ncbi.nlm.nih.gov/21890694/
.. _`Li et al. (2017)`: https://pubmed.ncbi.nlm.nih.gov/28615142/
.. _`Herron et al. (2016)`: https://www.ahajournals.org/doi/full/10.1161/CIRCEP.113.003638

.. _`Current_Ik1.cellml`: https://models.physiomeproject.org/workspace/702/rawfile/a619946dc2f89d6d787cebfbd9b1f2a54f5aa227/Current_Ik1.cellml
.. _`fig8.py`: https://models.physiomeproject.org/workspace/702/rawfile/a619946dc2f89d6d787cebfbd9b1f2a54f5aa227/fig8.py





