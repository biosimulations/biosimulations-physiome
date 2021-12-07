
% Function to generate Cai transient

function Cai = getCai(t)

    tau1 = 20; %(ms)
    tau2 = 33; %(ms)
    Ca_amp = 1.5; %(uM)
    Ca_dias = 0.09; %(uM)
    t_start = 50; %(ms)
    
    beta = (tau1/tau2)^(-1/(tau1/tau2 -1)) - (tau1/tau2)^(-1/(1 - tau2/tau1));
    
    if (t>t_start)
        Cai = ((Ca_amp - Ca_dias)/beta)*(exp(-(t-t_start)/tau1) - exp(-(t-t_start)/tau2)) + Ca_dias;
    else
        Cai = Ca_dias;
    end
    
end
