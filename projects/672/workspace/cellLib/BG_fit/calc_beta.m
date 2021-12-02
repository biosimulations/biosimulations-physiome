function beta = calc_beta(params,V,T)
% params: [kf, zf, kr, zr];
R = 8.314;
F = 96485;

beta = params(3)*exp(params(4)*F*V/R/T);

end