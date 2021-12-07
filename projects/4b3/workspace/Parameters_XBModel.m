% Parameters and initial conditions for Rice 2008 model


%% Model parameters

% Metabolite reference concentrations
Pi_ref = 2; %mM
MgATP_ref = 5; %mM
MgADP_ref = 0.036; %mM

% MgADP dissociation constant
kdADP = 0.004; % uM

% Set metabolite concentrations and pH level
MgATP = 5; %mM
MgADP = 36e-3; %mM
Pi = 2; %mM
pH = 7.15;

% Competitive H binding parameters
kdHCa = 1e-5;
m = 1;
pH_ref = 7.15;
Href = 10^(-pH_ref)*1e3;

% Gas constant
R = 8.314;
TmpC = 23;

% Sarcomere geometry (um)
SL_max = 2.4;
SL_min = 1.4;
L_thick = 1.65;
L_hbare = 0.1;
L_thin = 1.2;

% Temperature dependence
%TmpC = 25;
Q_kon = 1.5;
Q_koff = 1.3;
Q_kn_p = 1.6;
Q_kp_n = 1.6;
Q_fapp = 6.25;
Q_gapp = 2.5;
Q_hf = 6.25;
Q_hb = 6.25;
Q_gxb = 6.25;

% Species parameter
Xsp = 1; %1.0 for rat, 0.2 for Guinea Pig

% XB density
rho = 0.25;

% No of ATP consumed per XB 
phi = 1;

% Ca binding to troponin and thin filament
kon = 50e-3;   % (uM-1 ms-1)
koffL = 250e-3; % (ms-1)
koffH = 25e-3;  % (ms-1)
perm50 = 0.5; 
n_perm = 15;
kn_p = 500e-3; % (ms-1) % kn_p and kp_n values were round the wrong way! Changed on Dec 15th 2016
kp_n = 50e-3; % (ms-1)  % when changed, causes force to be very low - orig. params appear to be wrong.

% Thin filament regulation and XB cycling
fapp = 500e-3; % (ms-1)
gapp = 70e-3;  % (ms-1)
gslmod = 6;
hf = 2000e-3;  % (ms-1)
hfmdc = 5;
hb = 400e-3;   % (ms-1)
gxb = 70e-3;   % (ms-1)
sigma_p = 0.1;
sigma_n = 1;   

% Mean strain of strongly-bond states
x0 = 0.007; % (um)
Psi = 2;

% Normalised active and passive force
SL_rest = 1.9;  % (um)
PCon_titin = 0.002; %(normalised force)
PExp_titin = 10; %(um-1)
SL_collagen = 2.25; %(uM)
PCon_collagen = 0.02; %(normalised force)
PExp_collagen  = 70; %(um-1)

% Calculation of complete muscle response
mass = 0.2*0.00025e6; % for Rat (normalised force ms^2 um-1)
viscosity = 0.003;  % (normalised force ms um-1) 
