function K_gating_n(T,phi,V)

rng default  % For reproducibility
%% Steady-state gating parameters and time constants of HH
[alpha,beta]=HH_gate_n(-(V+65),phi);
TF = isnan(alpha);
alpha(TF)=0.1;
tau = calc_tau(alpha,beta);
g_ss = calc_gss(alpha,beta);
%% Fit new kinetic parameters for the bond graph of state models
% params: [kf, zf, kr, zr];
error_func_alpha = @(params) square_error(alpha - calc_alpha(params,V/1000,T));
error_func_beta = @(params) square_error(beta - calc_beta(params,V/1000,T));
error_func_gss = @(params) square_error(g_ss - p2gss(params,V,T));
error_func_tau = @(params) square_error(tau- p2tau(params,V,T));
%error_func = @(params) error_func_alpha(params) + error_func_beta(params) + 10.* error_func_gss(params) + error_func_tau(params);
error_func = @(params) 1.*error_func_alpha(params) + 10.* error_func_beta(params) + 200.* error_func_gss(params) + 50.* error_func_tau(params);
lb = [0; -10; 0; -10];
ub = [Inf; 10; Inf; 10];
options_ps = optimoptions('particleswarm','UseParallel',true,'HybridFcn',@fmincon,'SwarmSize',200,'FunctionTolerance',1e-8);
[params_vec,fval,exitflag,output] = particleswarm(error_func,4,lb,ub,options_ps);
alpha_bg=calc_alpha(params_vec,V/1000,T);
beta_bg=calc_beta(params_vec,V/1000,T);
g_ss_bg=p2gss(params_vec,V,T);
tau_bg=p2tau(params_vec,V,T);
MSE = (square_error(alpha - alpha_bg) + square_error(beta - beta_bg)...
    + square_error(g_ss - g_ss_bg) +square_error(tau- tau_bg))/length(V);
save(['K_n_parameters.mat'],'params_vec','alpha','beta','g_ss','tau','alpha_bg','beta_bg','g_ss_bg','tau_bg','V','MSE');
%% Plot for comparison
h = figure;
x0=100;
y0=50;
height=350*2;
width=400*2;
set(gcf,'position',[x0,y0,width,height])
gate_plot(alpha,beta,g_ss,tau,alpha_bg,beta_bg,g_ss_bg,tau_bg,V,'n',MSE);
filename='gate_n';
savefig(h,sprintf('%s.fig',filename))
exportgraphics(h,sprintf('%s.eps',filename));





