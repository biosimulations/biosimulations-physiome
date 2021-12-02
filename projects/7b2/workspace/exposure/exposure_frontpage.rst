About this model
====================

This is a Functional Cell Unit for adenylyl cyclase metabolism in the cardiac cell. 

This is a composite module, composed of several individual modules, and merged together in a modular fashion.

    **INPUTS:** 
        - Ligands for beta-1 adrenergic and muscarinic receptors.
        
    **OUTPUTS:** 
        - Change in molar amount of cyclic AMP.

Model status
=============

The current CellML implementation runs in OpenCOR.

Model overview
===================
All components are presented in `bond-graph` form.
Components are made by converting an existing kinetic model and translating into bond-graph form. 

.. figure:: exposure/FCU_picture.png
   :width: 25%
   :align: center
   :alt: Components of the model

   Components of the model.
    
A description of the process to find bond-graph parameter is shown in the folder    `parameter_finder <parameter_finder>`_, which relies on the:

1. stoichiometry of system

2. kinetic constants for forward/reverse reactions

  - If not already, all reactions are made reversible by assigning a small value to the reverse  direction.
  
3. `linear algebra script <https://models.physiomeproject.org/workspace/705/file/e2e0d90970a2ee0be95efad22e7c7ab266bf8f84/parameter_finder/find_BG_parameters_composite.py>`_. 

Here, this solve process is performed in Python.


Modular description
===================

Components
----------

CellML divides the mathematical model into distinct components, which are able to be re-used in other composite models.
These CellML components are:

- `beta-1 adrenergic receptor <https://models.physiomeproject.org/workspace/6f7>`_ ( :math:`{\beta}` 1AR)
- `Gs Protein <https://models.physiomeproject.org/workspace/6f8>`_
- `muscarinic receptor <https://models.physiomeproject.org/workspace/707>`_  (M2)
- `Gi Protein <https://models.physiomeproject.org/workspace/6f9>`_
- `cyclic AMP <https://models.physiomeproject.org/workspace/674>`_ (cAMP)
   
.. csv-table:: Origin of kinetic model components
   :header: "Source", "Components"
   :widths: 15, 30   
   
   "`Saucerman et al. <https://models.physiomeproject.org/exposure/9766d9bd0325c31e47a31b291e26ccad>`_", ":math:`{\beta}` 1AR, Gs Protein, cAMP"
   "`Iancu et al. <https://models.physiomeproject.org/exposure/f67b68f901fc3986fcea0dcfceb503f9>`_", "M2, Gs Protein"
   
Each of these blocks is itself a CellML model, complete with bond-graph parameters appropriate for the isolated system.


