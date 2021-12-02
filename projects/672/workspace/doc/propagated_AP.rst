Propagated action potential model
---------------------------------

The `propagated_AP.cellml <../components/propagated_AP.cellml>`_ defines the `equation of a propagated action potential <../components/propagated_AP.cellml/cellml_math>`_.
It combines the imported ionic current components:

- Potassium current component
  
The `IK.cellml <../components/IK.cellml>`_ defines the equation of the potassium current.
It instantiates the imported `gating kinetics component <../components/gating-variable.cellml>`_ for n gate, while the n gate rate is defined in `IK-gating-rates.cellml <../components/IK-gating-rates.cellml>`_.

- Sodium current component
  
The `INa.cellml <../components/INa.cellml>`_ defines the equation of the sodium current.
It instantiates the imported `gating kinetics component`_ for m and h gates, while the gate rates are defined in `INa-gating-rates.cellml <../components/INa-gating-rates.cellml>`_.

- Leakage current component
  
The `Ileak.cellml <../components/Ileak.cellml>`_ defines the equation of the leakage current.