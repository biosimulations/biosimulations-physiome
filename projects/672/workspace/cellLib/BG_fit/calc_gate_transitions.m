function [alpha,beta] = calc_gate_transitions(params,V,T)
% params: [kf, zf, kr, zr];
R = 8.314;
F = 96485;

alpha = params(1)*exp(params(2)*F*V/R/T);
beta = params(3)*exp(params(4)*F*V/R/T);

end