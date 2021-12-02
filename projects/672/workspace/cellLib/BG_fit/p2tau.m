function tau = p2tau(params,V,T)
[alpha,beta] = calc_gate_transitions(params,V/1000,T);
tau = calc_tau(alpha,beta);
end