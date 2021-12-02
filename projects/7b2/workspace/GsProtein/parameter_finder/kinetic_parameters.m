% Gs protein module following Saucerman and Iancu: act1 and act2 with LR
% and LRG as substrates (G is already bound, so there is only one substrate
% to each act reaction)

% Gs is associated with B1AR proteins

% Return kinetic parameters, constraints, and vector of volumes in each
% compartment (pL) (1 if gating variable, or in element corresponding to
% kappa)

% 14Oct21: adding phosphate binding reaction to RG and LRG as separate
% reactions. Only RG_Pi and LRG_Pi proceed to Act reactions. 

function [k_kinetic, N_cT, K_C, W] = kinetic_parameters(M, include_type2_reactions, dims, V)
    % Set the kinetic rate constants.
    % original model had reactions that omitted enzymes as substrates e.g. BARK
    % convert unit from 1/s to 1/uM.s by dividing by conc of enzyme
    % all reactions were irreversible, made reversible by letting kr ~= 0

    num_cols = dims.num_cols;
    num_rows = dims.num_rows;

    bigNum = 1e3;
    fastKineticConstant = bigNum;
    smallReverse = fastKineticConstant/(bigNum^2);
    
    kPhosRGp = fastKineticConstant;
    kPhosRGm = fastKineticConstant;
    kPhosLRGp = fastKineticConstant;
    kPhosLRGm = fastKineticConstant;
    kAct1p = 16;                 % 1/s
    kAct1m = smallReverse;           % 1/s            
    kAct2p = 16;                 % 1/s
    kAct2m = smallReverse;           % 1/s            
    kHydp = 0.8;                    % 1/s      
    kHydm = smallReverse;           % 1/s
    kReassocp = 1.21e3;             % 1/uM.s
    kReassocm = kReassocp/bigNum;   % 1/s
    
    % ensure that the closed loop formed by Act1 & Act2 obey detailed
    % balance
    kAct2m = kAct1m * kAct2p / kAct1p;
    % CLOSED LOOP involving G - aGTP - aGDP - G
    % use detailed balance to find kReasocm with either Act (as they have
    % same equilibrium constant
    if true
        kReassocm = kAct1p*kHydp*kReassocp/(kAct1m*kHydm);
    end

    k_kinetic = [
        kPhosRGp, kPhosLRGp, kAct1p, kAct2p, kHydp, kReassocp...
        kPhosRGm, kPhosLRGm, kAct1m, kAct2m, kHydm, kReassocm
        ]';

    % CONSTRAINTS
    N_cT = zeros(1,size(M,2)); 
    
    % LR.G = aGTP.betaGamma
    if false                                                          
        N_cT(2,num_cols + 3) = 1;
        N_cT(2,num_cols + 4) = 1;
        N_cT(2,num_cols + 5) = -1;
        N_cT(2,num_cols + 6) = -1;
    end
    % [a-GTP] + [a-GDP] = [beta.gamma]                              **SMALL_ERROR**
    if true 
        N_cT(1,num_cols + 7) = 1;   % beta_gamma
        N_cT(1,num_cols + 8) = -1;  % a_GTP
        N_cT(1,num_cols + 10) = -1;  % a_GDP
    end
    
    K_C = [1];

    % volume vector
    W = [ones(num_cols,1); V.V_myo*ones(num_rows,1)];

return 











