clear;
clc;
close all;
addpath(genpath('../../cellLib/BG_fit/'))
T = 279.45; % K
R = 8.314; % unit J/mol/K
F = 96485; % C/mol
phi = 3^((T - 6.3-273.15) / 10);
%% Define volumes (unit pL)
W_i = 4.24e6;
W_e = 6.06e5;
A_cap = 0.3; % Unit cm^2
%A_cap = 1; % Unit cm^2
Vm_HH=-15; % mV
V_m = -Vm_HH-65;%mV
%dNa=483e8; % Na channel density /cm^2
%dK=145e8; % K channel density /cm^2
dNa=1000e8; % Na channel density /cm^2
%dNa=1000e8*120/36; % Na channel density /cm^2
%% Get the kinetic paras, comment them out if the corresponding .mat files exist and nothing needs to change
% For GHK Na and K
GHK_IV_cal(T,R,F,dNa,W_i,W_e,A_cap,V_m);
% For m gate in Na
V = transpose(-120:1:40); % unit mV
%Na_gating_m(T,phi,V);
% For h gate in Na
V = transpose(-120:1:40); % unit mV
%Na_gating_h(T,phi,V);
% For n gate in Na
V = transpose(-120:1:40); % unit mV
%K_gating_n(T,phi,V);
%% Write the kinetic paras of gates m, h, and n to the file for documentation
M(1,:)={'Gate','$\alpha_0(s^{-1})$','$z^f_g$','$\beta_0(s^{-1})$','$z^r_g$',};
load(['Na_m_parameters.mat']);
M(2,:)=['m' compose('%g',params_vec)];
load(['Na_h_parameters.mat']);
M(3,:)=['h' compose('%g',params_vec)];
load(['K_n_parameters.mat']);
M(4,:)=['n' compose('%g',params_vec)];
writecell(M,'kineticGate.csv','Delimiter',',')