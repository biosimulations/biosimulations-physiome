function [P,kf,kr]=GHK_cal(T,z,cXi,cXe,nX,W_i,W_e,G)
%cXi/cXe intracelluar/extracelluar concentration, mM
%W_i/W_e intracelluar/extracelluar volume, pL
%nX, channel numbers
%G, conductance of the open channel, mS
%% Define constants
R = 8.314; % unit J/mol/K
F = 96485; % C/mol
N_A = 6.022e23;
E_X = R*T/F*log(cXe/cXi); %Nernst potential
E_X_norm = F*E_X/(R*T);
G_GHK = 2*G*(1-exp(E_X_norm))/(cXi - cXe*exp(E_X_norm))*R*T/F/(z^2); % Unit mA/mM
P = G_GHK/F * 1e12; % Unit pL/s

X=nX/N_A*1e15; % unit fmol
kf=P/(W_i*X); % s^-1 fmol^1
kr=P/(W_e*X); % s^-1 fmol^1