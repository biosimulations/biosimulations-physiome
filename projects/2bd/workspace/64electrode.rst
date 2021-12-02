The plugins emulates a 64 electrode basket catheter. The plugin can use external structured data provided through a shared memory. It can also emulate observed potentials at an electrode for a specific electric potential pattern on the cardiac surface.
The electrode signals can be viewed, colored and a subset can be selected to determine the surface potential near the catheter surface based on the selected electrodes.
Snapshots from the UI interface are shown below.

.. image:: .\BCEVAll.png

.. image:: .\BCESel.png

.. image:: .\BCEctrl.png

Plugin listens to the following messages
----------------------------------------
UPDATESOURCE:{URL} 
URL is the url:port of the service from which the data for the electrodes are input.

EMULATE:{NORMAL|PACING|TACHY|ARRHTM}
Plugin emulates the electrode readings for the selected electrophysiological pattern. NORMAL - normal rhythm, PACING - 200 Hz, TACHY - Tachycardia, ARRHTM - Arrhythmia.

The software has been developed by The Cardiac Electrophysiology group at the Auckland Bioengineering Institute. The plugins are under MedTech CORE license and can be accessed by MedTech CORE community free of charge. Request for access to binaries should be directed to cardiacelectro at medtech dot ac dot nz.

Contact
-------
cardiacelectro at medtech dot ac dot nz
