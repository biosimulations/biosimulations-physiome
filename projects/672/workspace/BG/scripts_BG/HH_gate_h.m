function [alpha_h,beta_h]=HH_gate_h(V,phi)

alpha_h = 0.07 .* exp( V ./ 20 ) .* phi;
beta_h = phi ./ (exp( (V + 30) ./10 ) + 1);
end
