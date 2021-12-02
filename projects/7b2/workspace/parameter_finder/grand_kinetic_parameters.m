% Kinetic rate constants for composite model of FCU-AC 
% they must be computed together because of the presence of new potential closed loops

% order: {'cAMP','LRGbinding_B1AR','LRGbinding_M2','GsProtein','GiProtein'}

function [k_kinetic, N_cT, K_C, W] = grand_kinetic_parameters(M, include_type2_reactions, dims, V, noLRG)

    num_cols = dims.num_cols;
    num_rows = dims.num_rows;

    % shared large/small constants
    bigNum = 1e5;
    fastKineticConstant = bigNum;
    smallReverse = 1e0;
    
% cAMP
    K1_m = 1.03e3;        % uM
    k1cat = 0.2;          % 1/s
    K2_m = 3.15e+2;       % uM
    k2cat = 8.5;          % 1/s
    K3_m = 8.60e+2;       % uM
    k3cat = 1e-16;        % 1/s
    K4_m = 1.30;          % uM
    k4cat = 5;            % 1/s
    K5_m = 30;            % uM
    K6_m = 0.4;           % uM
    K7_m = 44;            % uM
    KGiAC_m = 10; % made up value % uM

    % initialise arrays
    vkap = zeros(4,1);
    vkam = zeros(4,1);
    vkbp = zeros(4,1);
    vkbm = zeros(4,1);
    vkm2 = zeros(4,1);
    vkp2 = zeros(4,1);
    vK_m = [K1_m,K2_m,K3_m,K4_m,K5_m,K6_m,K7_m,KGiAC_m];
    vkcat = [k1cat,k2cat,k3cat,k4cat];

    kap_mult = [0.93, 0.1, 1, 1,0.1]; % finding rates from literature?

    % include the Gi reaction to remove it from the system in inhibited
    % form
    iks = 1:4;
    for i=1:4
        vkap(i) = kap_mult(i)*fastKineticConstant;
        vkam(i) = vkap(i)*vK_m(iks(i)) - vkcat(i);
        vkbp(i) = vkcat(i);
        vkbm(i) = (vkap(i)*vkbp(i))/vkam(i);
    end
    iks = 5:8;
    for i= 1:4
        vkm2(i) = fastKineticConstant;
        vkp2(i) = vkm2(i)/vK_m(iks(i));
    end


% B1AR composite: LRG_B1AR + GsProtein
    
    kPhosRGp = fastKineticConstant;
    kPhosRGm = fastKineticConstant;
    kPhosLRGp = fastKineticConstant;
    kPhosLRGm = fastKineticConstant;
    Ksig1 = 33;    % uM  Kc
    Ksig2 = 0.285; % uM  Kl
    Ksig3 = 0.062; % uM  Kr
    ksig1p = fastKineticConstant;
    ksig1m = ksig1p*Ksig1;
    ksig2p = fastKineticConstant;
    ksig2m = ksig2p*Ksig2;
    ksig3p = fastKineticConstant;
    ksig3m = ksig3p*Ksig3;
    ksig4p = fastKineticConstant;
    % find ksig4m using detailed balance
    ksig4m = ksig1m*ksig2m*ksig3p*ksig4p/(ksig1p*ksig2p*ksig3m);
    
    kAct1p = 16;                 % 1/s
    kAct1m = smallReverse;           % 1/s            
    kAct2p = 16;                 % 1/s
    kAct2m = smallReverse;           % 1/s            
    kHydp = 0.8;                    % 1/s      
    kHydm = smallReverse;           % 1/s
    kReassocp = 1.21e3;             % 1/uM.s
    kReassocm = kReassocp/fastKineticConstant;   % 1/s
    
    % Loop1: find kact1m using detailed balance
    kAct1m = (kAct1p*ksig1p)/ksig1m;
    % Loop2: find kact1m using detailed balance
    kAct2m = (kAct2p*ksig3p)/ksig3m;

    % Big Loop: find ksig3p or kact2m using detailed balance
    % *** unnecessary ***
    ksig3m = kAct1p*ksig2m*ksig3p*ksig4p/(kAct1m*ksig2p*ksig4m);
    
    % CLOSED LOOP involving G - aGTP - aGDP - G
    % use detailed balance to find kReasocm with either Act (as they have
    % same equilibrium constant
    if true
        kReassocm = kAct1p*kHydp*kReassocp/(kAct1m*kHydm);
    end


% M2 composite: LRG_M2 + GiProtein
    
    K_M2sig1 = 30;    % uM  Kc
    K_M2sig2 = 0.16;  % uM  Kh
    K_M2sig4 = 11;    % uM  Kl
    k_M2sig1p = fastKineticConstant;
    k_M2sig1m = k_M2sig1p*K_M2sig1;
    k_M2sig2p = fastKineticConstant;
    k_M2sig2m = k_M2sig2p*K_M2sig2;
    k_M2sig4p = fastKineticConstant;
    k_M2sig4m = k_M2sig4p*K_M2sig4;
    k_M2sig3p = fastKineticConstant;
    k_M2sig3m = k_M2sig1m*k_M2sig2m*k_M2sig3p*k_M2sig4p/(k_M2sig1p*k_M2sig2p*k_M2sig4m); % interim?
    
    k_M2PhosRGp = fastKineticConstant;
    k_M2PhosRGm = fastKineticConstant;
    k_M2PhosLRGp = fastKineticConstant;
    k_M2PhosLRGm = fastKineticConstant;
    k_M2Act1p = 2.5;                   % 1/s
    k_M2Act1m = smallReverse;          % 1/s            
    k_M2Act2p = 0.05;                  % 1/s
    k_M2Act2m = smallReverse;          % 1/s            
    k_M2Hydp = 0.8;                    % 1/s      
    k_M2Hydm = smallReverse;           % 1/s
    k_M2Reassocp = 1.21e3;             % 1/uM.s
    k_M2Reassocm = k_M2Reassocp/fastKineticConstant;   % 1/s
    
    % Loop1: find kact1m using detailed balance
    k_M2Act1m = (k_M2Act1p*k_M2sig1p)/k_M2sig1m;
    % Loop2: find kact1m using detailed balance
    k_M2Act2m = (k_M2Act2p*k_M2sig3p)/k_M2sig3m;

    % Big Loop: find k_M2sig3p or kact2m using detailed balance
    % *** unnecessary ***
    k_M2sig3m = k_M2Act1p*k_M2sig2m*k_M2sig3p*k_M2sig4p/(k_M2Act1m*k_M2sig2p*k_M2sig4m);
    
    % CLOSED LOOP involving G - aGTP - aGDP - G
    % use detailed balance to find kReasocm with either Act (as they have
    % same equilibrium constant
    if true
        k_M2Reassocm = k_M2Act1p*k_M2Hydp*k_M2Reassocp/(k_M2Act1m*k_M2Hydm);
    end
    
% TOTAL    
    %  order: {'cAMP','LRGbinding_B1AR','LRGbinding_M2','GsProtein','GiProtein'}
% forwaard first, then reverse!
    k_kinetic = [vkap(1) vkbp(1) ... %cAMP
        vkap(2) vkbp(2) ...
        vkap(3) vkbp(3) ...
        vkap(4) vkbp(4) ...
        vkp2(1:4)' ...
        ksig1p, ksig2p, ksig3p, ksig4p... %LRG B1AR
        k_M2sig1p, k_M2sig2p, k_M2sig3p, k_M2sig4p...% LRG_M2
        kPhosRGp, kPhosLRGp, kAct1p, kAct2p, kHydp, kReassocp... %GsProtein
        k_M2PhosRGp, k_M2PhosLRGp, k_M2Act1p, k_M2Act2p, k_M2Hydp, k_M2Reassocp... %GiProtein
        vkam(1) vkbm(1) ...
        vkam(2) vkbm(2) ...
        vkam(3) vkbm(3) ...
        vkam(4) vkbm(4) ...
        vkm2(1:4)'...
        ksig1m, ksig2m, ksig3m, ksig4m...
        k_M2sig1m, k_M2sig2m, k_M2sig3m, k_M2sig4m...
        kPhosRGm, kPhosLRGm, kAct1m, kAct2m, kHydm, kReassocm...
        k_M2PhosRGm, k_M2PhosLRGm, k_M2Act1m, k_M2Act2m, k_M2Hydm, k_M2Reassocm
        ]';
    if noLRG
            k_kinetic = [vkap(1) vkbp(1) ... %cAMP
            vkap(2) vkbp(2) ...
            vkap(3) vkbp(3) ...
            vkap(4) vkbp(4) ...
            vkp2(1:4)' ...
            kPhosRGp, kPhosLRGp, kAct1p, kAct2p, kHydp, kReassocp... %GsProtein
            k_M2PhosRGp, k_M2PhosLRGp, k_M2Act1p, k_M2Act2p, k_M2Hydp, k_M2Reassocp... %GiProtein
            vkam(1) vkbm(1) ...
            vkam(2) vkbm(2) ...
            vkam(3) vkbm(3) ...
            vkam(4) vkbm(4) ...
            vkm2(1:4)'...
            kPhosRGm, kPhosLRGm, kAct1m, kAct2m, kHydm, kReassocm...
            k_M2PhosRGm, k_M2PhosLRGm, k_M2Act1m, k_M2Act2m, k_M2Hydm, k_M2Reassocm
            ]';
    end
    
    if false % Gs and LRG_B1 only
            k_kinetic = [ksig1p, ksig2p, ksig3p, ksig4p... %LRG B1AR
            kAct1p, kAct2p, kHydp, kReassocp... %GsProtein
            ksig1m, ksig2m, ksig3m, ksig4m...
            kAct1m, kAct2m, kHydm, kReassocm...
            ]';
    end
    
    if false
            k_kinetic = [k_M2sig1p, k_M2sig2p, k_M2sig3p, k_M2sig4p...% LRG_M2
        k_M2Act1p, k_M2Act2p, k_M2Hydp, k_M2Reassocp... %GiProtein
        k_M2sig1m, k_M2sig2m, k_M2sig3m, k_M2sig4m...
        k_M2Act1m, k_M2Act2m, k_M2Hydm, k_M2Reassocm
        ]';
    end

    % CONSTRAINTS
    N_cT = [];
    if false
        N_cT = zeros(1,size(M,2)); 
        % substrate B1ARp is in eqlm with product B1ARtot
        N_cT(1,num_cols + 1) = 1;
        N_cT(1,num_cols + 2) = -1;
    end
    K_C = ones(1,size(N_cT,1));

    % volume vector
    W = [ones(num_cols,1); V.V_myo*ones(num_rows,1)];

return 