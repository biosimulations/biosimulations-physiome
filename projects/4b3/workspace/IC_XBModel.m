%% Initial State variable values

Nxb = 0.9997;  % Non-permissive fraction in overlap region
XBpreR = 0.0001;   % Fraction of XBs in pre-rotated state (Stiffness generation)
XBpostR = 0.0001;  % Fraction of XBS in post-rotated state (force generation)
x_XBpreR = 0;    % Strain of XBs in the pre-rotated state
x_XBpostR = 0.007;  % Strain of XBs in the post-rotated state
TropCaL = 0.0144; % Ca bound to the low affinity troponin site
TropCaH = 0.1276; % Ca bound to the high affinity troponin sit
IntegF = 0;
SL = 2.3; % This is changed in SBSolve.m

init = [Nxb XBpreR XBpostR x_XBpreR x_XBpostR TropCaL TropCaH IntegF SL];

