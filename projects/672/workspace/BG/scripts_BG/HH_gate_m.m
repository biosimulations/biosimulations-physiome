function [alpha_m,beta_m]=HH_gate_m(V,phi)

alpha_m = 0.1 .* (V + 25) .* phi ./ (exp( (V + 25) ./ 10) -1 );
beta_m = 4 .* exp( V ./ 18 ) .* phi;
TF = isnan(alpha_m); % handle /0
alpha_m(TF)=1;
end