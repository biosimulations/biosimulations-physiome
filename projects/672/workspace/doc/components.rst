Components
----------

CellML divides the mathematical model into distinct components, which are able to be re-used.
The main CellML components are:

- `Membrane potential component <../components/stimulated.cellml/view>`_
- `Membrane current component <../components/clamped_current.cellml/view>`_ (the ionic current during a voltage clamp)
- `Propagated action potential component <../components/propagated_AP.cellml/view>`_
- `Potassium current component <../components/IK.cellml>`_
- `Sodium current component <../components/INa.cellml>`_
- `Leakage current component <../components/Ileak.cellml>`_
- `Gating kinetics component <../components/gating-variable.cellml>`_ – a single definition instantiated three times for the n, m, and h gates
- Gating rates components (open/close rates for n, m, and h gates respectively)
- `Gate initialization components <../components/gate_initials.cellml/view>`_ (steady state values of n, m, and h gates under boundary conditions)
- `Temperature component <../components/temperature_factor.cellml/view>`_
- `Time component <../experiments/time.cellml/view>`_ 

Each of these blocks is itself a CellML model, which enables us to reuse the various components in future studies and models.
