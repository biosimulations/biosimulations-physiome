function g_ss = p2gss(params,V,T)
[alpha,beta] = calc_gate_transitions(params,V/1000,T);
g_ss = calc_gss(alpha,beta);
end