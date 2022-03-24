function [alpha_n,beta_n]=HH_gate_n(V,phi)

alpha_n = 0.01 .* (V + 10) .* phi ./ (exp( (V + 10) ./ 10) -1 );

beta_n = 0.125 .* exp( V ./ 80 ) .* phi;

TF = isnan(alpha_n); % handle /0;
alpha_n(TF)=0.1;
end