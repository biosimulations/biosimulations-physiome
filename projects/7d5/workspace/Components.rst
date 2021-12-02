About this model
====================

:Original publication: `Kernik et al. (2019)`_:
  "A computational model of induced pluripotent stem-cell derived cardiomyocytes \
  incorporating experimental variability from multiple data sources" J  Physiol. 2019 Sep 1; 597(17): 4533-4564.

:DOI: https://dx.doi.org/10.1113%2FJP277724

.. _`Kernik et al. (2019)`: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6767694/

************
CellML files
************

CellML can build a model in a modular way which divides the model
into distinct modules, which can be re-used.
The main CellML files:

- `Components <Components>`_ which include:
    - Main file that put all the other required files together: `Channels <https://models.physiomeproject.org/e/7c7/Components/Channels.cellml/view>`_

         this file is the main CellML file which is the top model in the hierarchical modular
         presentation and rest of the files need to be imported here in order to run the simulation.
    - These files have the formulation for calculating each channel's current (for instance: *Current_Ik1*): `Current_Ik1 <https://models.physiomeproject.org/e/7c7/Components/Current_Ik1.cellml/view>`_
    - This file contains the formulation for Nernst potential: `Nernst_potential <https://models.physiomeproject.org/e/7c7/Components/Nernst_potential.cellml/view>`_
    - Different protocol to choose a value for intracellular potassium: `Protocol <https://models.physiomeproject.org/e/7c7/Components/Protocol.cellml/view>`_
    - Probability of channels gates being open or close: `act_inact <https://models.physiomeproject.org/e/7c7/Components/act_inact.cellml/view>`_

        this file is the main CellML file for calculation the probability of channels gates being
        open or close and also the activation/inactivation time constants.
        some other files need to be imported here in order to run the simulation.
    - Hodgkin-Huxley-type gating formulations are provided in a single module here: `gatting <https://models.physiomeproject.org/e/7c7/Components/gatting.cellml/view>`_
    - some of the channels have different gating formulation which is collected in specific file (for instance: *gating_Ik1*): `gating_Ik1 <https://models.physiomeproject.org/e/7c7/Components/gating_Ik1.cellml/view>`_
    - General file for required parameters: `parameter <https://models.physiomeproject.org/e/7c7/Components/parameter.cellml/view>`_
        This file is a general file, specific parameters for calculating the probability of each channel's gate being
        open or close are presented in associated python script.
    - some of the channels have their own parameters which are collected in specific file (for instance: *parameter_Ik1*): `parameter_Ik1 <https://models.physiomeproject.org/e/7c7/Components/parameter_Ik1.cellml/view>`_
    - All the required units for this simulation: `unit <https://models.physiomeproject.org/e/7c7/Components/unit.cellml/view>`_









