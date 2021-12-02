About this model
====================

:Original publication: `Hodgkin & Huxley (1952)`_: ‘A Quantitative Description of Membrane Current and its Application to Conduction and Excitation in Nerve’, J. Physiol. 117: 500-544.

:DOI: https://doi.org/10.1113/jphysiol.1952.sp004764

.. _`Hodgkin & Huxley (1952)`: http://www.ncbi.nlm.nih.gov/pubmed/12991237

Model status
=============

The current CellML model implementation runs in OpenCOR_.
The results have been validated against the data extracted from the figures in the published `Hodgkin & Huxley (1952)`_.
The model structure, simulation results and limitation have been detailed in the following sections.

Model overview
===================
This workspace holds a CellML_ encoding of the `Hodgkin & Huxley (1952)`_ model. 
The `Hodgkin & Huxley (1952)`_ (HH) model is one of the foundational models of cellular electrophysiology. 
It defined the “standard” gating kinetics still used in many models today. 
The model includes potassium, sodium, and ‘leakage’ currents as well and the transmembrane electrical potential. 
The HH model was originally developed to investigate flow of electric charge in giant nerve axons in squid.

.. figure::  doc/math-overview.png
   :width: 85%
   :align: center
   :alt: Schematics of the model

   A diagrammatic representation of the Hodgkin & Huxley (1952) model.

.. _CellML: https://www.cellml.org/

Modular description
===================

Components
----------

CellML divides the mathematical model into distinct components, which are able to be re-used.
The main CellML components are:

- `Membrane potential component <components/stimulated.cellml/view>`_
  
- `Membrane current component <components/clamped_current.cellml/view>`_ (the ionic current during a voltage clamp)
  
- `Propagated action potential component <components/propagated_AP.cellml/view>`_
  
- `Potassium current component <components/IK.cellml>`_
  
- `Sodium current component <components/INa.cellml>`_
  
- `Leakage current component <components/Ileak.cellml>`_
  
- `Gating kinetics component <components/gating-variable.cellml>`_ – a single definition instantiated three times for the n, m, and h gates
  
- Gating rates components (open/close rates for n, m, and h gates respectively)
  
- `Gate initialization components <components/gate_initials.cellml/view>`_ (steady state values of n, m, and h gates for specified membrane potentials)
  
- `Temperature component <components/temperature_factor.cellml/view>`_
  
- `Time component <experiments/time.cellml/view>`_ 

Each of these blocks is itself a CellML model, which enables us to reuse the various components in future studies and models.

Experiments
---------------------

Following best practices, this model separates the mathematics from the parameterisation of the model. The mathematical model is imported into a specific parameterised instance in order to perform numerical simulations. 
The parameterisation would include defining the stimulus protocol to be applied.

This workspace has three sets of experiments:

1. `Periodic stimulation <experiments/periodic-stimulus.cellml/view>`_     

2. `Voltage clamp experiment <experiments/voltage_clamp_experiment.cellml/view>`_ 

3. `Action potential propagation along 1D cable model <experiments/AP_propagation_experiment.cellml/view>`_ (please see `Known issues`_) 

Simulation settings 
-------------------
Simulation settings are encoded in SED-ML_ documents for experiment execution. 
The python scripts to run simulation and reproduce the figures in the original paper are also included.

.. _SED-ML: http://sed-ml.org/

Model history
=================== 

The original model implementation is from `VPH-MIP case study`_. The main modification is summarized as follows:

1. Add the `temperature component`_ to enable the simulation at different temperatures.
   
2. Add  `membrane current component`_,  `voltage clamp <experiments/voltage_clamp_protocol.cellml>`_ and `voltage clamp experiment`_ to simulate a membrane current during a voltage clamp.

3. Add `gate initialization components`_ to enable the simulation of anode break excitation. 
   
4. Add `propagated action potential model <components/propagated_AP.cellml/view>`_ and `action potential propagation experiment <experiments/AP_propagation_experiment.cellml>`_ to simulate a propagated action potential (please see `Known issues`_).   

5. Add the python scripts to run simulation and reproduce the figures in the original paper.   

.. _`VPH-MIP case study`: https://models.physiomeproject.org/w/andre/VPH-MIP

Known issues
===================

1.  The voltage clamp value cannot be -10 mV as the :math:`\alpha_n` would be infinity.
   
2.  The `propagated action potential model`_ does not work, which needs further investigation in future.
   
3.  The temperature unit is set to Kelvin in the CellML models. If you want to simulate the model behavior at temperature T with unit Celsius, you do not need to do conversion as the offset is cancelled in the mathematical expressions including temperature factor. 
   
4.  You need to set appropriate parameters and initial values in the CellML files, if you want to run simulation using OpenCOR_ rather than the provided Python scripts.

5. The :math:`V` in the model is defined relative to the resting potential, while the inward current is positive. This is different from the convention of modern physiological modelling.

.. _OpenCOR: https://opencor.ws/

