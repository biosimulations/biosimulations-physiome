clear;
clc;
close all;
addpath(genpath('../../cellLib/BG_fit/'))
T = 279.45;
phi = 3^((T - 6.3-273.15) / 10);

%% Steady-state gating parameters and time constants
V = transpose(-120:1:60); % unit mV
[alpha,beta]=HH_gate_m(-(V+75),phi);
TF = isnan(alpha);
alpha(TF)=1;
tau = calc_tau(alpha,beta);
g_ss = calc_gss(alpha,beta);
%% Fit bond graph parameters to model
% params: [kf, zf, kr, zr];
error_func_alpha = @(params) square_error(alpha - calc_alpha(params,V/1000,T));
error_func_beta = @(params) square_error(beta - calc_beta(params,V/1000,T));
error_func_gss = @(params) square_error(g_ss - p2gss(params,V,T));
error_func_tau = @(params) square_error(tau- p2tau(params,V,T));
error_func = @(params) error_func_alpha(params) + error_func_beta(params) + error_func_gss(params) + error_func_tau(params);
lb = [0; -10; 0; -10];
ub = [Inf; 10; Inf; 10];
options_ps = optimoptions('particleswarm','UseParallel',true,'HybridFcn',@fmincon,'SwarmSize',200,'FunctionTolerance',1e-8);
[params_vec,fval,exitflag,output] = particleswarm(error_func,4,lb,ub,options_ps);
save(['Na_m_parameters.mat'],'params_vec');
%% Plot
h = figure;
x0=100;
y0=50;
height=350*2;
width=400*2;
set(gcf,'position',[x0,y0,width,height])
gate_plot(alpha,beta,g_ss,tau,params_vec,V,T,'m',fval);
filename='m_gate.fig';
savefig(h,filename)

function [alpha_m,beta_m]=HH_gate_m(V,phi)

alpha_m = 0.1 .* (V + 25) .* phi ./ (exp( (V + 25) ./ 10) -1 );
beta_m = 4 .* exp( V ./ 18 ) .* phi;
end


