tic;    
[VOI, STATES, ALGEBRAIC, CONSTANTS] = mainFunction();
toc;

function [VOI, STATES, ALGEBRAIC, CONSTANTS] = mainFunction()
    % This is the "main function".  In Matlab, things work best if you rename this function to match the filename.
   [VOI, STATES, ALGEBRAIC, CONSTANTS] = solveModel();
end

function [algebraicVariableCount] = getAlgebraicVariableCount()
    % Used later when setting a global variable with the number of algebraic variables.
    % Note: This is not the "main method".
    algebraicVariableCount =39;
end
% There are a total of 11 entries in each of the rate and state variable arrays.
% There are a total of 48 entries in the constant variable array.
%

function [VOI, STATES, ALGEBRAIC, CONSTANTS] = solveModel()
    [LEGEND_STATES, LEGEND_ALGEBRAIC, LEGEND_VOI, LEGEND_CONSTANTS] = createLegends();
    % Create ALGEBRAIC of correct size
    global algebraicVariableCount;  algebraicVariableCount = getAlgebraicVariableCount();
    % Initialise constants and state variables
    [INIT_STATES, CONSTANTS] = initConsts;

    % Set timespan to solve over
    tspan = [0, 1];

    % Set numerical accuracy options for ODE solver
    options = odeset('RelTol', 1e-06, 'AbsTol', 1e-06, 'MaxStep', 1e-3);

    % Solve model with ODE solver
    [VOI, STATES] = ode15s(@(VOI, STATES)computeRates(VOI, STATES, CONSTANTS), tspan, INIT_STATES, options);

    % Compute algebraic variables
    [RATES, ALGEBRAIC] = computeRates(VOI, STATES, CONSTANTS);
    ALGEBRAIC = computeAlgebraic(ALGEBRAIC, CONSTANTS, STATES, VOI);

    vlabels = {'q_Ca_TRPN in component environment (fmol)',...
        'q_B in component environment (fmol)',...
        'q_U in component environment (fmol)',...
        'q_W in component environment (fmol)',...
        'q_S in component environment (fmol)',...
        'G_w in component crossbridge_TRPN (metre)',...
        'G_s in component crossbridge_TRPN (metre)',...
        'T_active in component crossbridge_TRPN (kPa)',...
        'T_passive in component crossbridge_TRPN (kPa)',...
        'T_total in component crossbridge_TRPN (kPa)'};
    [~, i_st, i_alg] = find_indices(vlabels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
    if i_st
        plot_selected(i_st,VOI,STATES,'s',LEGEND_STATES,'STATES',ceil(sqrt(length(i_st))))
    end
    plot_selected(i_alg,VOI,ALGEBRAIC,'s',LEGEND_ALGEBRAIC,'ALGEBRAIC',ceil(sqrt(length(i_alg))))
end            


function [i_con, i_st, i_alg] = find_indices(labels, LEGEND_CONSTANTS, LEGEND_STATES, LEGEND_ALGEBRAIC)
% return the indices for the selected labels
    all_legends = [LEGEND_CONSTANTS; LEGEND_STATES; LEGEND_ALGEBRAIC];
    
    i_con = [];
    for i = 1:length(labels)
        i_con = [i_con; find(strcmp(labels{i},LEGEND_CONSTANTS))];
    end
    i_st = [];
    for i = 1:length(labels)
        i_st = [i_st; find(strcmp(labels{i},LEGEND_STATES))];
    end
    i_alg = [];
    for i = 1:length(labels)
        i_alg = [i_alg; find(strcmp(labels{i},LEGEND_ALGEBRAIC))];
    end
    
    if length(i_con) + length(i_st) + length(i_alg) < length(labels)
        error('missing index');
    end
end


function [] = plot_selected(ids,x,y,legend_x,legend_y,titlestr,ns)
    istart = 1;
    figure();
%     plot stimuli
    for i = 1:length(ids)
        subplot(ns,ns,i)
        plotting_x = x(istart:end);
        plotting_y = y(istart:end,ids(i));
        if isempty(plotting_y) % probably a constant scalar
            plotting_y = repmat(y(ids(i)),2);
            plotting_x = [x(istart), x(end)];
        end
        plot(plotting_x, plotting_y);
        xlabel('time (s)');
        str = split(legend_y(ids(i),:), ' ');
        str = legend_y(ids(i),:);
        l = legend(str);
        set(l,'interpreter','none');
    end
    suptitle(titlestr)    
end


function [LEGEND_STATES, LEGEND_ALGEBRAIC, LEGEND_VOI, LEGEND_CONSTANTS] = createLegends()
    LEGEND_STATES = ''; LEGEND_ALGEBRAIC = ''; LEGEND_VOI = ''; LEGEND_CONSTANTS = '';
    LEGEND_VOI = strpad('time in component environment (second)');
    LEGEND_CONSTANTS(:,1) = strpad('q_Cai_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,2) = strpad('q_TRPN_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,3) = strpad('q_Ca_TRPN_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,4) = strpad('q_B_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,5) = strpad('q_U_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,6) = strpad('q_W_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,7) = strpad('q_S_init in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,3) = strpad('q_TRPN in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,6) = strpad('q_Cai in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,9) = strpad('q_Ca_TRPN in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,10) = strpad('q_B in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,11) = strpad('q_U in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,12) = strpad('q_W in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,13) = strpad('q_S in component environment (fmol)');
    LEGEND_STATES(:,1) = strpad('q_TRPN in component crossbridge_TRPN (fmol)');
    LEGEND_STATES(:,2) = strpad('q_Cai in component crossbridge_TRPN (fmol)');
    LEGEND_STATES(:,3) = strpad('q_Ca_TRPN in component crossbridge_TRPN (fmol)');
    LEGEND_STATES(:,4) = strpad('q_B in component crossbridge_TRPN (fmol)');
    LEGEND_STATES(:,5) = strpad('q_U in component crossbridge_TRPN (fmol)');
    LEGEND_STATES(:,6) = strpad('q_W in component crossbridge_TRPN (fmol)');
    LEGEND_STATES(:,7) = strpad('q_S in component crossbridge_TRPN (fmol)');
    LEGEND_ALGEBRAIC(:,36) = strpad('T_total in component crossbridge_TRPN (kPa)');
    LEGEND_STATES(:,8) = strpad('SL in component crossbridge_TRPN (metre)');
    LEGEND_CONSTANTS(:,8) = strpad('kappa_R_TRPNCa in component crossbridge_TRPN_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,9) = strpad('kappa_R_BU in component crossbridge_TRPN_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,10) = strpad('kappa_R_UW in component crossbridge_TRPN_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,11) = strpad('kappa_R_WS in component crossbridge_TRPN_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,12) = strpad('kappa_R_SU in component crossbridge_TRPN_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,13) = strpad('K_TRPN in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,14) = strpad('K_Cai in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,15) = strpad('K_Ca_TRPN in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,16) = strpad('K_B in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,17) = strpad('K_U in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,18) = strpad('K_W in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,19) = strpad('K_S in component crossbridge_TRPN_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,20) = strpad('R in component constants (J_per_K_per_mol)');
    LEGEND_CONSTANTS(:,21) = strpad('T in component constants (kelvin)');
    LEGEND_CONSTANTS(:,22) = strpad('n_Tm in component crossbridge_TRPN (dimensionless)');
    LEGEND_ALGEBRAIC(:,14) = strpad('mu_TRPN in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,15) = strpad('mu_Cai in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,16) = strpad('mu_Ca_TRPN in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,17) = strpad('mu_B in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,19) = strpad('mu_U in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,21) = strpad('mu_W in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,23) = strpad('mu_S in component crossbridge_TRPN (J_per_mol)');
    LEGEND_ALGEBRAIC(:,39) = strpad('v_R_TRPNCa in component crossbridge_TRPN (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,25) = strpad('v_R_BU in component crossbridge_TRPN (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,31) = strpad('v_R_UW in component crossbridge_TRPN (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,33) = strpad('v_R_WS in component crossbridge_TRPN (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,35) = strpad('v_R_SU in component crossbridge_TRPN (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,37) = strpad('tension in component crossbridge_TRPN (N_per_mm2)');
    LEGEND_ALGEBRAIC(:,38) = strpad('mu_tension in component crossbridge_TRPN (J_per_mol)');
    LEGEND_CONSTANTS(:,23) = strpad('kf_coeff in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,44) = strpad('n in component crossbridge_TRPN (J_per_mol)');
    LEGEND_CONSTANTS(:,24) = strpad('hh in component crossbridge_TRPN (mm2_per_N)');
    LEGEND_CONSTANTS(:,25) = strpad('SL_0 in component crossbridge_TRPN (metre)');
    LEGEND_CONSTANTS(:,26) = strpad('q_MS in component crossbridge_TRPN (fmol)');
    LEGEND_CONSTANTS(:,27) = strpad('r_s in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,28) = strpad('r_w in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,29) = strpad('A_eff in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,30) = strpad('phi in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,31) = strpad('k_uw in component crossbridge_TRPN (per_sec)');
    LEGEND_CONSTANTS(:,32) = strpad('k_ws in component crossbridge_TRPN (per_sec)');
    LEGEND_STATES(:,9) = strpad('G_w in component crossbridge_TRPN (metre)');
    LEGEND_STATES(:,10) = strpad('G_s in component crossbridge_TRPN (metre)');
    LEGEND_CONSTANTS(:,41) = strpad('c_w in component crossbridge_TRPN (per_sec)');
    LEGEND_CONSTANTS(:,42) = strpad('c_s in component crossbridge_TRPN (per_sec)');
    LEGEND_CONSTANTS(:,43) = strpad('A_w in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,45) = strpad('A_s in component crossbridge_TRPN (dimensionless)');
    LEGEND_ALGEBRAIC(:,4) = strpad('mu_1 in component crossbridge_TRPN (J_per_m)');
    LEGEND_CONSTANTS(:,46) = strpad('mu_2 in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,1) = strpad('mu_3 in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,5) = strpad('mu_4 in component crossbridge_TRPN (J_per_m)');
    LEGEND_CONSTANTS(:,47) = strpad('mu_5 in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,2) = strpad('mu_6 in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,7) = strpad('v_1 in component crossbridge_TRPN (m_per_s)');
    LEGEND_CONSTANTS(:,33) = strpad('v_2 in component crossbridge_TRPN (m_per_s)');
    LEGEND_ALGEBRAIC(:,8) = strpad('v_4 in component crossbridge_TRPN (m_per_s)');
    LEGEND_CONSTANTS(:,34) = strpad('v_to_mu in component crossbridge_TRPN (Js_per_m2)');
    LEGEND_ALGEBRAIC(:,24) = strpad('T_active in component crossbridge_TRPN (kPa)');
    LEGEND_CONSTANTS(:,35) = strpad('T_ref in component crossbridge_TRPN (kPa)');
    LEGEND_ALGEBRAIC(:,22) = strpad('mu_T_a in component crossbridge_TRPN (kPa)');
    LEGEND_ALGEBRAIC(:,18) = strpad('mu_T_S in component crossbridge_TRPN (kPa)');
    LEGEND_ALGEBRAIC(:,20) = strpad('mu_T_W in component crossbridge_TRPN (kPa)');
    LEGEND_STATES(:,11) = strpad('Cdd in component crossbridge_TRPN (metre)');
    LEGEND_ALGEBRAIC(:,26) = strpad('eta in component crossbridge_TRPN (per_sec)');
    LEGEND_CONSTANTS(:,36) = strpad('eta_l in component crossbridge_TRPN (per_sec)');
    LEGEND_CONSTANTS(:,37) = strpad('eta_s in component crossbridge_TRPN (per_sec)');
    LEGEND_CONSTANTS(:,38) = strpad('k in component crossbridge_TRPN (dimensionless)');
    LEGEND_CONSTANTS(:,39) = strpad('alpha in component crossbridge_TRPN (kPa)');
    LEGEND_ALGEBRAIC(:,30) = strpad('v_Cdd in component crossbridge_TRPN (m_per_s)');
    LEGEND_ALGEBRAIC(:,27) = strpad('mu_d in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,28) = strpad('mu_k in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,29) = strpad('mu_f in component crossbridge_TRPN (J_per_m)');
    LEGEND_ALGEBRAIC(:,32) = strpad('mu_T_passive in component crossbridge_TRPN (kPa)');
    LEGEND_ALGEBRAIC(:,34) = strpad('T_passive in component crossbridge_TRPN (kPa)');
    LEGEND_CONSTANTS(:,40) = strpad('F in component constants (C_per_mol)');
    LEGEND_RATES(:,2) = strpad('d/dt q_Cai in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,1) = strpad('d/dt q_TRPN in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,3) = strpad('d/dt q_Ca_TRPN in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,4) = strpad('d/dt q_B in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,5) = strpad('d/dt q_U in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,6) = strpad('d/dt q_W in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,7) = strpad('d/dt q_S in component crossbridge_TRPN (fmol)');
    LEGEND_RATES(:,9) = strpad('d/dt G_w in component crossbridge_TRPN (metre)');
    LEGEND_RATES(:,8) = strpad('d/dt SL in component crossbridge_TRPN (metre)');
    LEGEND_RATES(:,10) = strpad('d/dt G_s in component crossbridge_TRPN (metre)');
    LEGEND_RATES(:,11) = strpad('d/dt Cdd in component crossbridge_TRPN (metre)');
    LEGEND_STATES  = LEGEND_STATES';
    LEGEND_ALGEBRAIC = LEGEND_ALGEBRAIC';
    LEGEND_RATES = LEGEND_RATES';
    LEGEND_CONSTANTS = LEGEND_CONSTANTS';
end


function [STATES, CONSTANTS] = initConsts()
    VOI = 0; CONSTANTS = []; STATES = []; ALGEBRAIC = [];
    CONSTANTS(:,1) = 6.82e-1;
    CONSTANTS(:,2) = 2.57;
    CONSTANTS(:,3) = 1e-6;
    CONSTANTS(:,4) = 1;
    CONSTANTS(:,5) = 0;
    CONSTANTS(:,6) = 0;
    CONSTANTS(:,7) = 0;
    STATES(:,1) = 1e-16;
    STATES(:,2) = 1e-16;
    STATES(:,3) = 1e-16;
    STATES(:,4) = 1e-16;
    STATES(:,5) = 1e-16;
    STATES(:,6) = 1e-16;
    STATES(:,7) = 1e-16;
    STATES(:,8) = 1e-6;
    CONSTANTS(:,8) = 52.0453;
    CONSTANTS(:,9) = 2.90875;
    CONSTANTS(:,10) = 0.332501;
    CONSTANTS(:,11) = 0.00782356;
    CONSTANTS(:,12) = 140824;
    CONSTANTS(:,13) = 1.27424;
    CONSTANTS(:,14) = 1.27424;
    CONSTANTS(:,15) = 0.11171;
    CONSTANTS(:,16) = 6.06164;
    CONSTANTS(:,17) = 2.27312;
    CONSTANTS(:,18) = 14.8627;
    CONSTANTS(:,19) = 3.71567e-06;
    CONSTANTS(:,20) = 8.31;
    CONSTANTS(:,21) = 310;
    CONSTANTS(:,22) = 1.1;
    CONSTANTS(:,23) = -0.0118;
    CONSTANTS(:,24) = 1;
    CONSTANTS(:,25) = 2e-6;
    CONSTANTS(:,26) = 1e-6;
    CONSTANTS(:,27) = 0.25;
    CONSTANTS(:,28) = 0.5;
    CONSTANTS(:,29) = 25;
    CONSTANTS(:,30) = 2.23;
    CONSTANTS(:,31) = 26;
    CONSTANTS(:,32) = 4;
    STATES(:,9) = 1e-6;
    STATES(:,10) = 1e-6;
    CONSTANTS(:,33) = 0;
    CONSTANTS(:,34) = 1;
    CONSTANTS(:,35) = 40.5;
    STATES(:,11) = 0;
    CONSTANTS(:,36) = 200e3;
    CONSTANTS(:,37) = 20e3; % eta_s
    CONSTANTS(:,38) = 7;
    CONSTANTS(:,39) = 2.1;
    CONSTANTS(:,40) = 96485;
    CONSTANTS(:,41) = ( CONSTANTS(:,30).*CONSTANTS(:,31).*(1.00000 - CONSTANTS(:,28)))./CONSTANTS(:,28);
    CONSTANTS(:,42) = ( CONSTANTS(:,30).*CONSTANTS(:,32).*(1.00000 - CONSTANTS(:,27)).*CONSTANTS(:,28))./CONSTANTS(:,27);
    CONSTANTS(:,43) = ( CONSTANTS(:,29).*CONSTANTS(:,27))./( (1.00000 - CONSTANTS(:,27)).*CONSTANTS(:,28)+CONSTANTS(:,27));
    CONSTANTS(:,44) =  CONSTANTS(:,23).*CONSTANTS(:,20).*CONSTANTS(:,21);
    % CONSTANTS(:,47) = CONSTANTS(:,33);
    CONSTANTS(:,45) = CONSTANTS(:,43);
    CONSTANTS(:,46) =   - CONSTANTS(:,43).*CONSTANTS(:,33).*CONSTANTS(:,34);
    CONSTANTS(:,47) =   - CONSTANTS(:,45).*CONSTANTS(:,33).*CONSTANTS(:,34);
    if (isempty(STATES)), warning('Initial values for states not set');, end
end

function [RATES, ALGEBRAIC] = computeRates(VOI, STATES, CONSTANTS)
disp(VOI);
    global algebraicVariableCount;
    statesSize = size(STATES);
    statesColumnCount = statesSize(2);
    if ( statesColumnCount == 1)
        STATES = STATES';
        ALGEBRAIC = zeros(1, algebraicVariableCount);
        utilOnes = 1;
    else
        statesRowCount = statesSize(1);
        ALGEBRAIC = zeros(statesRowCount, algebraicVariableCount);
        RATES = zeros(statesRowCount, statesColumnCount);
        utilOnes = ones(statesRowCount, 1);
    end
    RATES(:,8) = CONSTANTS(:,47);
    ALGEBRAIC(:,1) =  CONSTANTS(:,41).*STATES(:,9).*CONSTANTS(:,34);
    ALGEBRAIC(:,4) =  - CONSTANTS(:,46) - ALGEBRAIC(:,1);
    ALGEBRAIC(:,7) = ALGEBRAIC(:,4)./CONSTANTS(:,34);
    RATES(:,9) = ALGEBRAIC(:,7);
    ALGEBRAIC(:,2) =  CONSTANTS(:,42).*STATES(:,10).*CONSTANTS(:,34);
    ALGEBRAIC(:,5) =  - CONSTANTS(:,47) - ALGEBRAIC(:,2);
    ALGEBRAIC(:,8) = ALGEBRAIC(:,5)./CONSTANTS(:,34);
    RATES(:,10) = ALGEBRAIC(:,8);
    ALGEBRAIC(:,9) = STATES(:,3)+CONSTANTS(:,3);
    ALGEBRAIC(:,16) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,15).*ALGEBRAIC(:,9));
    ALGEBRAIC(:,10) = STATES(:,4)+CONSTANTS(:,4);
    ALGEBRAIC(:,17) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,16).*ALGEBRAIC(:,10));
    ALGEBRAIC(:,11) = STATES(:,5)+CONSTANTS(:,5);
    ALGEBRAIC(:,19) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,17).*ALGEBRAIC(:,11));
    ALGEBRAIC(:,25) =  CONSTANTS(:,9).*(exp((ALGEBRAIC(:,17)+ CONSTANTS(:,22).*ALGEBRAIC(:,16))./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp((ALGEBRAIC(:,19)+ CONSTANTS(:,22).*ALGEBRAIC(:,16))./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    RATES(:,4) =  - ALGEBRAIC(:,25);
    [CONSTANTS, STATES, ALGEBRAIC] = rootfind_0(VOI, CONSTANTS, STATES, ALGEBRAIC);
    ALGEBRAIC(:,30) = ALGEBRAIC(:,27)./CONSTANTS(:,34);
    RATES(:,11) = ALGEBRAIC(:,30);
    ALGEBRAIC(:,12) = STATES(:,6)+CONSTANTS(:,6);
    ALGEBRAIC(:,21) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,18).*ALGEBRAIC(:,12));
    ALGEBRAIC(:,31) =  CONSTANTS(:,10).*(exp(ALGEBRAIC(:,19)./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp(ALGEBRAIC(:,21)./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    ALGEBRAIC(:,13) = STATES(:,7)+CONSTANTS(:,7);
    ALGEBRAIC(:,23) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,19).*ALGEBRAIC(:,13));
    ALGEBRAIC(:,33) =  CONSTANTS(:,11).*(exp(ALGEBRAIC(:,21)./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp(ALGEBRAIC(:,23)./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    RATES(:,6) = ALGEBRAIC(:,31) - ALGEBRAIC(:,33);
    ALGEBRAIC(:,35) =  CONSTANTS(:,12).*(exp(ALGEBRAIC(:,23)./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp(ALGEBRAIC(:,19)./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    RATES(:,5) = (ALGEBRAIC(:,25) - ALGEBRAIC(:,31))+ALGEBRAIC(:,35);
    RATES(:,7) = ALGEBRAIC(:,33) - ALGEBRAIC(:,35);
    ALGEBRAIC(:,3) = STATES(:,1)+CONSTANTS(:,2);
    ALGEBRAIC(:,14) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,13).*ALGEBRAIC(:,3));
    ALGEBRAIC(:,6) = STATES(:,2)+CONSTANTS(:,1);
    ALGEBRAIC(:,15) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,14).*ALGEBRAIC(:,6));
    ALGEBRAIC(:,18) =  (CONSTANTS(:,35)./( CONSTANTS(:,25).*CONSTANTS(:,26).*CONSTANTS(:,27))).*STATES(:,7).*(STATES(:,10)+CONSTANTS(:,25));
    ALGEBRAIC(:,20) =  (CONSTANTS(:,35)./( CONSTANTS(:,25).*CONSTANTS(:,26).*CONSTANTS(:,27))).*STATES(:,6).*STATES(:,9);
    ALGEBRAIC(:,22) = ALGEBRAIC(:,18)+ALGEBRAIC(:,20);
    ALGEBRAIC(:,24) = ALGEBRAIC(:,22);
    ALGEBRAIC(:,32) =  (( CONSTANTS(:,39).*ALGEBRAIC(:,26))./CONSTANTS(:,25)).*ALGEBRAIC(:,30);
    ALGEBRAIC(:,34) = ALGEBRAIC(:,32);
    ALGEBRAIC(:,36) = ALGEBRAIC(:,24)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,37) =  ALGEBRAIC(:,36).*1000.00;
    ALGEBRAIC(:,38) =  CONSTANTS(:,24).*CONSTANTS(:,44).*ALGEBRAIC(:,37);
    ALGEBRAIC(:,39) =  CONSTANTS(:,8).*(exp((ALGEBRAIC(:,15)+ALGEBRAIC(:,14))./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp((ALGEBRAIC(:,16)+ALGEBRAIC(:,38))./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    RATES(:,2) =  - ALGEBRAIC(:,39);
    RATES(:,1) =  - ALGEBRAIC(:,39);
    RATES(:,3) = ALGEBRAIC(:,39);
   RATES = RATES';
end

% Calculate algebraic variables
function ALGEBRAIC = computeAlgebraic(ALGEBRAIC, CONSTANTS, STATES, VOI)
    statesSize = size(STATES);
    statesColumnCount = statesSize(2);
    if ( statesColumnCount == 1)
        STATES = STATES';
        utilOnes = 1;
    else
        statesRowCount = statesSize(1);
        utilOnes = ones(statesRowCount, 1);
    end
    ALGEBRAIC(:,1) =  CONSTANTS(:,41).*STATES(:,9).*CONSTANTS(:,34);
    ALGEBRAIC(:,4) =  - CONSTANTS(:,46) - ALGEBRAIC(:,1);
    ALGEBRAIC(:,7) = ALGEBRAIC(:,4)./CONSTANTS(:,34);
    ALGEBRAIC(:,2) =  CONSTANTS(:,42).*STATES(:,10).*CONSTANTS(:,34);
    ALGEBRAIC(:,5) =  - CONSTANTS(:,47) - ALGEBRAIC(:,2);
    ALGEBRAIC(:,8) = ALGEBRAIC(:,5)./CONSTANTS(:,34);
    ALGEBRAIC(:,9) = STATES(:,3)+CONSTANTS(:,3);
    ALGEBRAIC(:,16) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,15).*ALGEBRAIC(:,9));
    ALGEBRAIC(:,10) = STATES(:,4)+CONSTANTS(:,4);
    ALGEBRAIC(:,17) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,16).*ALGEBRAIC(:,10));
    ALGEBRAIC(:,11) = STATES(:,5)+CONSTANTS(:,5);
    ALGEBRAIC(:,19) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,17).*ALGEBRAIC(:,11));
    ALGEBRAIC(:,25) =  CONSTANTS(:,9).*(exp((ALGEBRAIC(:,17)+ CONSTANTS(:,22).*ALGEBRAIC(:,16))./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp((ALGEBRAIC(:,19)+ CONSTANTS(:,22).*ALGEBRAIC(:,16))./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    ALGEBRAIC(:,30) = ALGEBRAIC(:,27)./CONSTANTS(:,34);
    ALGEBRAIC(:,12) = STATES(:,6)+CONSTANTS(:,6);
    ALGEBRAIC(:,21) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,18).*ALGEBRAIC(:,12));
    ALGEBRAIC(:,31) =  CONSTANTS(:,10).*(exp(ALGEBRAIC(:,19)./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp(ALGEBRAIC(:,21)./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    ALGEBRAIC(:,13) = STATES(:,7)+CONSTANTS(:,7);
    ALGEBRAIC(:,23) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,19).*ALGEBRAIC(:,13));
    ALGEBRAIC(:,33) =  CONSTANTS(:,11).*(exp(ALGEBRAIC(:,21)./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp(ALGEBRAIC(:,23)./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    ALGEBRAIC(:,35) =  CONSTANTS(:,12).*(exp(ALGEBRAIC(:,23)./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp(ALGEBRAIC(:,19)./( CONSTANTS(:,20).*CONSTANTS(:,21))));
    ALGEBRAIC(:,3) = STATES(:,1)+CONSTANTS(:,2);
    ALGEBRAIC(:,14) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,13).*ALGEBRAIC(:,3));
    ALGEBRAIC(:,6) = STATES(:,2)+CONSTANTS(:,1);
    ALGEBRAIC(:,15) =  CONSTANTS(:,20).*CONSTANTS(:,21).*log( CONSTANTS(:,14).*ALGEBRAIC(:,6));
    ALGEBRAIC(:,18) =  (CONSTANTS(:,35)./( CONSTANTS(:,25).*CONSTANTS(:,26).*CONSTANTS(:,27))).*STATES(:,7).*(STATES(:,10)+CONSTANTS(:,25));
    ALGEBRAIC(:,20) =  (CONSTANTS(:,35)./( CONSTANTS(:,25).*CONSTANTS(:,26).*CONSTANTS(:,27))).*STATES(:,6).*STATES(:,9);
    ALGEBRAIC(:,22) = ALGEBRAIC(:,18)+ALGEBRAIC(:,20);
    ALGEBRAIC(:,24) = ALGEBRAIC(:,22);
    ALGEBRAIC(:,32) =  (( CONSTANTS(:,39).*ALGEBRAIC(:,26))./CONSTANTS(:,25)).*ALGEBRAIC(:,30);
    ALGEBRAIC(:,34) = ALGEBRAIC(:,32);
    ALGEBRAIC(:,36) = ALGEBRAIC(:,24)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,37) =  ALGEBRAIC(:,36).*1000.00;
    ALGEBRAIC(:,38) =  CONSTANTS(:,24).*CONSTANTS(:,44).*ALGEBRAIC(:,37);
    ALGEBRAIC(:,39) =  CONSTANTS(:,8).*(exp((ALGEBRAIC(:,15)+ALGEBRAIC(:,14))./( CONSTANTS(:,20).*CONSTANTS(:,21))) - exp((ALGEBRAIC(:,16)+ALGEBRAIC(:,38))./( CONSTANTS(:,20).*CONSTANTS(:,21))));
end

% Functions required for solving differential algebraic equation
function [CONSTANTS, STATES, ALGEBRAIC] = rootfind_0(VOI, CONSTANTS_IN, STATES_IN, ALGEBRAIC_IN)
    ALGEBRAIC = ALGEBRAIC_IN;
    CONSTANTS = CONSTANTS_IN;
    STATES = STATES_IN;
    global initialGuess_0;
    if (length(initialGuess_0) ~= 4), initialGuess_0 = [0.1,0.1,0.1,0.1];, end
    options = optimset('Display', 'off', 'TolX', 1E-6);
    if length(VOI) == 1
        residualfn = @(algebraicCandidate)residualSN_0(algebraicCandidate, ALGEBRAIC, VOI, CONSTANTS, STATES);
        soln = fsolve(residualfn, initialGuess_0, options);
        initialGuess_0 = soln;
        ALGEBRAIC(:,26) = soln(1);
        ALGEBRAIC(:,27) = soln(2);
        ALGEBRAIC(:,28) = soln(3);
        ALGEBRAIC(:,29) = soln(4);
    else
        SET_ALGEBRAIC(:,26) = logical(1);
        SET_ALGEBRAIC(:,27) = logical(1);
        SET_ALGEBRAIC(:,28) = logical(1);
        SET_ALGEBRAIC(:,29) = logical(1);
        for i=1:length(VOI)
            residualfn = @(algebraicCandidate)residualSN_0(algebraicCandidate, ALGEBRAIC(i,:), VOI(i), CONSTANTS, STATES(i,:));
            soln = fsolve(residualfn, initialGuess_0, options);
            initialGuess_0 = soln;
            TEMP_ALGEBRAIC(:,26) = soln(1);
            TEMP_ALGEBRAIC(:,27) = soln(2);
            TEMP_ALGEBRAIC(:,28) = soln(3);
            TEMP_ALGEBRAIC(:,29) = soln(4);
            ALGEBRAIC(i,SET_ALGEBRAIC) = TEMP_ALGEBRAIC(SET_ALGEBRAIC);
        end
    end
end

function resid = residualSN_0(algebraicCandidate, ALGEBRAIC, VOI, CONSTANTS, STATES)
    ALGEBRAIC(:,26) = algebraicCandidate(1);
    ALGEBRAIC(:,27) = algebraicCandidate(2);
    ALGEBRAIC(:,28) = algebraicCandidate(3);
    ALGEBRAIC(:,29) = algebraicCandidate(4);
    resid(1) = ALGEBRAIC(:,26) - piecewise({ALGEBRAIC(:,27)>0.000000, CONSTANTS(:,36) }, CONSTANTS(:,37));
    resid(2) = ALGEBRAIC(:,28) -  (CONSTANTS(:,38)./ALGEBRAIC(:,26)).*STATES(:,11).*CONSTANTS(:,34);
    resid(3) = ALGEBRAIC(:,29) -  (CONSTANTS(:,38)./ALGEBRAIC(:,26)).*(STATES(:,8) - CONSTANTS(:,25)).*CONSTANTS(:,34);
    resid(4) = ALGEBRAIC(:,27) - ( - ALGEBRAIC(:,28)+ALGEBRAIC(:,29));
end

% Compute result of a piecewise function
function x = piecewise(cases, default)
    set = [0];
    for i = 1:2:length(cases)
        if (length(cases{i+1}) == 1)
            x(cases{i} & ~set,:) = cases{i+1};
        else
            x(cases{i} & ~set,:) = cases{i+1}(cases{i} & ~set);
        end
        set = set | cases{i};
        if(set), break, end
    end
    if (length(default) == 1)
        x(~set,:) = default;
    else
        x(~set,:) = default(~set);
    end
end

% Pad out or shorten strings to a set length
function strout = strpad(strin)
    req_length = 160;
    insize = size(strin,2);
    if insize > req_length
        strout = strin(1:req_length);
    else
        strout = [strin, blanks(req_length - insize)];
    end
end

