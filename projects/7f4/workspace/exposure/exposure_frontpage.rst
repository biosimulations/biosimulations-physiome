About this model
====================

This is a bond-graph model of the metabolism of the G-protein coupled receptor (:math:`{\beta}`-1 adrenergic receptor, R) and the associated Gs protein in the cardiac cell.

    **INPUTS:** 
        - Ligand (L) stimulus e.g. isoproterenol 
        
    **OUTPUTS:** 
        - Change in molar amount of Gs\ :math:`{\alpha}`\ :sub:`GTP`\
        
    **REACTIONS:** 
        - R\ :sub:`switch`\ : Spontaneous activation of R from an inactivate state to a state that can bind a Gs protein
        - LR\ :sub:`switch`\ : Similar to R\ :sub:`switch`\ , but with substrate of inactive complex LR
        - R\ :sub:`L`\ : the binding of L to R
        - R\ :sub:`C`\ : the binding of Gs to R
        - R\ :sub:`R`\ : the binding of Gs to complex LR
        - Act1: Bundled reactions representing the transient exchange of GDP for GTP on the active RG complex, which forms Gs\ :math:`{\alpha}`\ :sub:`GTP`\, Gs\ :math:`{\beta\gamma}`, GDP and R\ :sub:`tag`\. The latter is the R protein tagged for internalisation
        - Act2: Similar to Act1, but with substrate LRG and product LR\ :sub:`tag`\
        - Hyd: Hydration of GTP on Gs\ :math:`{\alpha}` :sub:`GTP`\, forming Gs\ :math:`{\alpha}`\ :sub:`GDP` and phosphate
        - Reassoc: Binding of Gs\ :math:`{\alpha}`\ :sub:`GDP` and Gs\ :math:`{\beta\gamma}` to reform Gs
        - Intern\ :sub:`R`\ : Internalisation of R\ :sub:`tag` by the GRK and arrestin proteins
        - Intern\ :sub:`LR`\ : Similar to Intern\ :sub:`R`\, but for substrate LR :sub:`tag`\
        

Model status
=============

The current CellML implementation runs in OpenCOR.


Model overview
===================
This model is based on existing kinetic model, where the mathematics are translated into the bond-graph formalism. This describes the model in energetic terms and forces adherence to the laws of thermodynamics. 


For the following figures, all enzymes are shown in maroon.


.. figure:: exposure/BG_GPCR_B1AR.png
   :width: 100%
   :align: center
   :alt: BG PKACI reaction
   
   Fig. 1. Bond-graph formulation of the GPCR-\ :math:`{\beta}`\ 1AR network


|

For the above bond-graphs, a '0' node refers to a junction where all chemical potentials are the same. A '1' node refers to all fluxes being the same going in and out of the junction.

.. csv-table:: List of chemical species
   :header: "Abbreviation", "Name"
   :widths: 5, 15 
   
   "Gs", "Gs protein"
   "Gs\ :math:`{\alpha}`\", "Alpha subunit of the Gs protein"
   "Gs\ :math:`{\beta\gamma}`\", "Beta and gamma subunits of the Gs protein"
   "GDP", "Guanosine diphosphate"
   "GRK", "G protein-coupled receptor kinase"
   "GTP", "Guanosine triphosphate"
   "L", "Ligand"
   "P\ :sub:`i`", "Phosphate"
   "R", "Receptor (:math:`{\beta}`-1 adrenergic receptor)"
   "R\ :sub:`i`", "Receptor (inactive form)"
   "R\ :sub:`tag`", "Receptor tagged for internalisation by GRK"
   
Parameter finding
~~~~~~~~~~~~~~~~~
A description of the process to find bond-graph parameters is shown in the folder    `parameter_finder <parameter_finder>`_, which relies on the:

1. stoichiometry of system

2. kinetic constants for forward/reverse reactions

  - If not already, all reactions are made reversible by assigning a small value to the reverse  direction.
  
3. `linear algebra script <https://models.physiomeproject.org/workspace/7dc/rawfile/29d84125387d3b09137c8a01e76721eda14cae33/parameter_finder/kinetic_parameters_GPCR_B1AR_reduced.py>`_. 

Here, this solve process is performed in Python.


Original kinetic model
======================
Saucerman et al: `Modeling beta-adrenergic control of cardiac myocyte contractility in silico. <https://models.physiomeproject.org/exposure/9766d9bd0325c31e47a31b291e26ccad>`_

Additional detail on receptor internalisation were provided by Stephen Duffull et al. (University of Otago). 

