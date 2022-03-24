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
    algebraicVariableCount =55;
end
% There are a total of 19 entries in each of the rate and state variable arrays.
% There are a total of 59 entries in the constant variable array.
%

function [VOI, STATES, ALGEBRAIC, CONSTANTS] = solveModel()
    [LEGEND_STATES, LEGEND_ALGEBRAIC, legend_VOI, LEGEND_CONSTANTS, LEGEND_RATES] = createLegends();
    % Create ALGEBRAIC of correct size
    global algebraicVariableCount;  algebraicVariableCount = getAlgebraicVariableCount();

    % Set timespan to solve over
    tspan = [0, 15];

    % Set numerical accuracy options for ODE solver
    options = odeset('RelTol', 1e-06, 'AbsTol', 1e-06, 'MaxStep', 5e-5);

    % extra options for stimuli [ L_B1 ] and other settings 
    st = struct;
    st.stimHolding = 1e-9;
    st.stimMag = 1e1; 
    st.stimSt = 3e0;
    st.tR = 5e-1; % seconds for rAMP start
    st.stimDur = 2e0;
    st.m = st.stimMag/st.tR;
    % st.qR_init = 0.04579000;
    % st.qGs_init = 1.45;
    st.vRsynth = 1e5;
    p = [st.stimHolding, st.stimMag, st.stimSt, st.tR, st.stimDur, st.m, st.vRsynth];
        
    stlabels = {'stimHolding in component environment (fmol)',...
    'stimMag in component environment (fmol)',...
    'stimSt in component environment (second)',...
    'tR in component environment (second)',...
    'stimDur in component environment (second)',...
    'm in component environment (fmol_per_sec)'...
    'v_Rsynthesis in component GPCR_B1AR_reduced (fmol_per_sec)'};
    
    [i_stp, ~,~] = find_indices(stlabels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));

    % Initialise constants and state variables
    [INIT_STATES, CONSTANTS] = initConsts(p,i_stp);
    % Solve model with ODE solver
    [VOI, STATES] = ode15s(@(VOI, STATES)computeRates(VOI, STATES, CONSTANTS), tspan, INIT_STATES, options);

    % Compute algebraic variables
    [RATES, ALGEBRAIC] = computeRates(VOI, STATES, CONSTANTS);
    ALGEBRAIC = computeAlgebraic(ALGEBRAIC, CONSTANTS, STATES, VOI);

    labels = {'q_LB1 in component environment (fmol)', ... 
            'q_RB1_inactive in component environment (fmol)'...
            'q_RB1 in component environment (fmol)'...
            'q_L_RB1_inactive in component environment (fmol)', ...
            'q_L_RB1 in component environment (fmol)', ...
            'q_L_RB1_Gs in component environment (fmol)', ...
            'q_RB1_Gs in component environment (fmol)', ...
            'q_Gsa_GTP in component environment (fmol)',...
            'conserv_R_T in component environment (fmol)'};
    [i_con, i_st, i_alg] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
    if i_st
        plot_selected(i_st,VOI,STATES,legend_VOI,LEGEND_STATES,'STATES',ceil(sqrt(length(i_st))))
    end
    if i_con
        plot_selected(i_con,VOI,repmat(CONSTANTS, length(VOI)),legend_VOI,LEGEND_CONSTANTS,'CONSTANTS',ceil(sqrt(length(i_con))))
    end
    plot_selected(i_alg,VOI,ALGEBRAIC,legend_VOI,LEGEND_ALGEBRAIC,'ALGEBRAIC',ceil(sqrt(length(i_alg))))

    % velocities
    if true
        vlabels = {'v_C_B1 in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_R_B1 in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_L_B1 in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_Act1_Gs in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_Act2_Gs in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_Hyd_Gs in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_Reassoc_Gs in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_InternR_B1 in component GPCR_B1AR_reduced (fmol_per_sec)',...
    'v_InternLR_B1 in component GPCR_B1AR_reduced (fmol_per_sec)'};
        [~, ~, i_alg] = find_indices(vlabels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        plot_selected(i_alg,VOI,ALGEBRAIC,legend_VOI,LEGEND_ALGEBRAIC,'REACTION FLUXES',ceil(sqrt(length(i_alg))))
    end
        
    % debug nonincreasing effect of L stim
    if false
        labels = {'mu_L_RB1 in component GPCR_B1AR_reduced (J_per_mol)',...
            'mu_Gs in component GPCR_B1AR_reduced (J_per_mol)',...
            'mu_L_RB1_Gs in component GPCR_B1AR_reduced (J_per_mol)',...
            'v_R_B1 in component GPCR_B1AR_reduced (fmol_per_sec)'};
        [~, i_st, i_alg] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
%         plot_selected(i_st,VOI,STATES,legend_VOI,LEGEND_STATES,'STATES',ceil(sqrt(length(i_st))))
        plot_selected(i_alg,VOI,ALGEBRAIC,legend_VOI,LEGEND_ALGEBRAIC,'v_R',ceil(sqrt(length(i_alg))))
    end
    
    % plot rates of variables
    labels = {'d/dt q_LB1 in component GPCR_B1AR_reduced (fmol)', ... 
        'd/dt q_RB1_inactive in component GPCR_B1AR_reduced (fmol)'...
        'd/dt q_RB1 in component GPCR_B1AR_reduced (fmol)'...
        'd/dt q_L_RB1_inactive in component GPCR_B1AR_reduced (fmol)', ...
        'd/dt q_L_RB1 in component GPCR_B1AR_reduced (fmol)', ...
        'd/dt q_L_RB1_Gs in component GPCR_B1AR_reduced (fmol)', ...
        'd/dt q_RB1_Gs in component GPCR_B1AR_reduced (fmol)', ...
        'd/dt q_Gsa_GTP in component GPCR_B1AR_reduced (fmol)'};
    [~, i_r, ~] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_RATES), cellstr(LEGEND_ALGEBRAIC));
    plot_selected(i_r,VOI,RATES',legend_VOI,LEGEND_STATES,'RATES',ceil(sqrt(length(i_r))))

    % debug R moieties
    if false
        labels = {'conserv_R_T in component environment (fmol)',...
                    'total_R_init in component environment (fmol)'...
                    'q_RB1_inactive in component environment (fmol)'...
                    'q_RB1 in component environment (fmol)'...
                    'q_L_RB1_inactive in component environment (fmol)', ...
                    'q_L_RB1 in component environment (fmol)', ...
                    'q_L_RB1_Gs in component environment (fmol)', ...
                    'q_RB1_Gs in component environment (fmol)', ...
                    'q_RB1_tag in component environment (fmol)',...
                    'q_L_RB1_tag in component environment (fmol)',...
                    'q_RB1_GRKArr in component environment (fmol)',...
                    'q_L_RB1_GRKArr in component environment (fmol)'};
        [i_con, i_st, i_alg] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        plot_selected(i_alg,VOI,ALGEBRAIC,legend_VOI,LEGEND_ALGEBRAIC,'R moieties',ceil(sqrt(length(i_alg))))
    end
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

function [] = plot_2per(i_alg0,id0,ids,x,y0,y,legend_y,legend_y_con,titlestr,ns)
    istart = 30;
    figure();
%     plot 2 per subplot
    if i_alg0
        idoffset = length(i_alg0);
        for i = 1:idoffset
            subplot(ns,ns,i)
            plot(x(istart:end), y(istart:end,i_alg0(i)),'x-'); hold on;
            plot(x(istart:end), y(istart:end,ids(i)));
            xlabel('time (s)');
            diff = mean(abs(y(istart:end,i_alg0(i)) - y(istart:end,ids(i))));
            str = split(legend_y(i_alg0(i),:),' in');
            title([str(1), strcat('avg abs error = ', num2str(diff))]);
    %         legend('init','sumspecies');
            str1 = split(legend_y(i_alg0(i),:),' ');
            str2 = split(legend_y(ids(i),:),' ');
            legend(str1(1),str2(1));
        end
    else
        idoffset = 0;
    end
    for i = (idoffset+1):length(ids)
        subplot(ns,ns,i)
        plot(x(istart:end), ones(length(x)-istart+1,1)*y0(id0(i-idoffset)),'x-'); hold on;
        plot(x(istart:end), y(istart:end,ids(i)));
        diff = abs(mean(y(istart:end,ids(i))) - y0(id0(i-idoffset)));
        xlabel('time (s)');
        str = split(legend_y(ids(i),:),' in');
        title([str(1), strcat('avg abs error = ', num2str(diff))]);
        legend(legend_y_con(id0(i-idoffset),:),legend_y(ids(i),:));
    end
    suptitle(strcat(titlestr,' eps = ',num2str(eps)))    
end
function [LEGEND_STATES, LEGEND_ALGEBRAIC, LEGEND_VOI, LEGEND_CONSTANTS, LEGEND_RATES] = createLegends()
    LEGEND_STATES = ''; LEGEND_ALGEBRAIC = ''; LEGEND_VOI = ''; LEGEND_CONSTANTS = '';
    LEGEND_VOI = strpad('time in component environment (second)');
    LEGEND_CONSTANTS(:,1) = strpad('q_RB1_inactive_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,2) = strpad('q_L_RB1_inactive_init in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,1) = strpad('q_LB1_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,3) = strpad('q_RB1_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,4) = strpad('q_Gs_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,5) = strpad('q_RB1_Gs_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,6) = strpad('q_L_RB1_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,7) = strpad('q_L_RB1_Gs_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,8) = strpad('q_Gsa_GTP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,9) = strpad('q_Gsbetagamma_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,10) = strpad('q_Gsa_GDP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,11) = strpad('q_GTP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,12) = strpad('q_GDP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,13) = strpad('q_Pi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,14) = strpad('q_RB1_tag_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,15) = strpad('q_L_RB1_tag_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,16) = strpad('q_RB1_GRKArr_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,17) = strpad('q_L_RB1_GRKArr_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,18) = strpad('q_GRKArr_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,19) = strpad('stimSt in component environment (second)');
    LEGEND_CONSTANTS(:,20) = strpad('stimDur in component environment (second)');
    LEGEND_CONSTANTS(:,21) = strpad('tR in component environment (second)');
    LEGEND_CONSTANTS(:,22) = strpad('stimMag in component environment (fmol)');
    LEGEND_CONSTANTS(:,23) = strpad('stimHolding in component environment (fmol)');
    LEGEND_CONSTANTS(:,58) = strpad('m in component environment (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,2) = strpad('q_RB1_inactive in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,3) = strpad('q_L_RB1_inactive in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,4) = strpad('q_LB1 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,5) = strpad('q_RB1 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,6) = strpad('q_Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,7) = strpad('q_RB1_Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,8) = strpad('q_L_RB1 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,9) = strpad('q_L_RB1_Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,10) = strpad('q_Gsa_GTP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,11) = strpad('q_Gsbetagamma in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,12) = strpad('q_Gsa_GDP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,14) = strpad('q_GTP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,15) = strpad('q_GDP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,16) = strpad('q_Pi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,17) = strpad('q_RB1_tag in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,18) = strpad('q_L_RB1_tag in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,19) = strpad('q_RB1_GRKArr in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,20) = strpad('q_L_RB1_GRKArr in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,23) = strpad('q_GRKArr in component environment (fmol)');
    LEGEND_STATES(:,1) = strpad('q_RB1_inactive in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,2) = strpad('q_L_RB1_inactive in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,3) = strpad('q_LB1 in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,4) = strpad('q_RB1 in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,5) = strpad('q_Gs in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,6) = strpad('q_RB1_Gs in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,7) = strpad('q_L_RB1 in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,8) = strpad('q_L_RB1_Gs in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,9) = strpad('q_Gsa_GTP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,10) = strpad('q_Gsbetagamma in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,11) = strpad('q_Gsa_GDP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,12) = strpad('q_GTP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,13) = strpad('q_GDP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,14) = strpad('q_Pi in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,15) = strpad('q_RB1_tag in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,16) = strpad('q_L_RB1_tag in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,17) = strpad('q_RB1_GRKArr in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,18) = strpad('q_L_RB1_GRKArr in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES(:,19) = strpad('q_GRKArr in component GPCR_B1AR_reduced (fmol)');
    LEGEND_ALGEBRAIC(:,21) = strpad('conserv_R_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,22) = strpad('conserv_L_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,13) = strpad('conserv_G_T in component environment (fmol)');
    LEGEND_CONSTANTS(:,59) = strpad('total_R_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,24) = strpad('kappa_Rswitch_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,25) = strpad('kappa_LRswitch_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,26) = strpad('kappa_C_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,27) = strpad('kappa_R_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,28) = strpad('kappa_L_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,29) = strpad('kappa_L_actR in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,30) = strpad('kappa_Act1_Gs in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,31) = strpad('kappa_Act2_Gs in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,32) = strpad('kappa_Hyd_Gs in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,33) = strpad('kappa_Reassoc_Gs in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,34) = strpad('kappa_InternR_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,35) = strpad('kappa_InternLR_B1 in component GPCR_B1AR_reduced_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,36) = strpad('K_RB1_inactive in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,37) = strpad('K_L_RB1_inactive in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,38) = strpad('K_LB1 in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,39) = strpad('K_RB1 in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,40) = strpad('K_Gs in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,41) = strpad('K_RB1_Gs in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,42) = strpad('K_L_RB1 in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,43) = strpad('K_L_RB1_Gs in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,44) = strpad('K_Gsa_GTP in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,45) = strpad('K_Gsbetagamma in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,46) = strpad('K_Gsa_GDP in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,47) = strpad('K_GTP in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,48) = strpad('K_GDP in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,49) = strpad('K_Pi in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,50) = strpad('K_RB1_tag in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,51) = strpad('K_L_RB1_tag in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,52) = strpad('K_RB1_GRKArr in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,53) = strpad('K_L_RB1_GRKArr in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,54) = strpad('K_GRKArr in component GPCR_B1AR_reduced_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,55) = strpad('R in component constants (J_per_K_per_mol)');
    LEGEND_CONSTANTS(:,56) = strpad('T in component constants (kelvin)');
    LEGEND_ALGEBRAIC(:,24) = strpad('mu_RB1_inactive in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,25) = strpad('mu_L_RB1_inactive in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,26) = strpad('mu_LB1 in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,27) = strpad('mu_RB1 in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,28) = strpad('mu_Gs in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,29) = strpad('mu_RB1_Gs in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,30) = strpad('mu_L_RB1 in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,31) = strpad('mu_L_RB1_Gs in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,32) = strpad('mu_Gsa_GTP in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,33) = strpad('mu_Gsbetagamma in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,34) = strpad('mu_Gsa_GDP in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,35) = strpad('mu_GTP in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,36) = strpad('mu_GDP in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,37) = strpad('mu_Pi in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,38) = strpad('mu_RB1_tag in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,39) = strpad('mu_L_RB1_tag in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,40) = strpad('mu_RB1_GRKArr in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,41) = strpad('mu_L_RB1_GRKArr in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,42) = strpad('mu_GRKArr in component GPCR_B1AR_reduced (J_per_mol)');
    LEGEND_ALGEBRAIC(:,43) = strpad('v_Rswitch_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,44) = strpad('v_LRswitch_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,45) = strpad('v_C_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,46) = strpad('v_R_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,47) = strpad('v_L_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,49) = strpad('v_L_actR in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,48) = strpad('v_Act1_Gs in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,50) = strpad('v_Act2_Gs in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,51) = strpad('v_Hyd_Gs in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,54) = strpad('v_Reassoc_Gs in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,52) = strpad('v_InternR_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,55) = strpad('v_InternLR_B1 in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,53) = strpad('v_Rsynthesis in component GPCR_B1AR_reduced (fmol_per_sec)');
    LEGEND_CONSTANTS(:,57) = strpad('F in component constants (C_per_mol)');
    LEGEND_RATES(:,1) = strpad('d/dt q_RB1_inactive in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,2) = strpad('d/dt q_L_RB1_inactive in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,3) = strpad('d/dt q_LB1 in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,4) = strpad('d/dt q_RB1 in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,5) = strpad('d/dt q_Gs in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,6) = strpad('d/dt q_RB1_Gs in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,7) = strpad('d/dt q_L_RB1 in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,8) = strpad('d/dt q_L_RB1_Gs in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,9) = strpad('d/dt q_Gsa_GTP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,10) = strpad('d/dt q_Gsbetagamma in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,11) = strpad('d/dt q_Gsa_GDP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,12) = strpad('d/dt q_GTP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,13) = strpad('d/dt q_GDP in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,14) = strpad('d/dt q_Pi in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,15) = strpad('d/dt q_RB1_tag in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,16) = strpad('d/dt q_L_RB1_tag in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,17) = strpad('d/dt q_RB1_GRKArr in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,18) = strpad('d/dt q_L_RB1_GRKArr in component GPCR_B1AR_reduced (fmol)');
    LEGEND_RATES(:,19) = strpad('d/dt q_GRKArr in component GPCR_B1AR_reduced (fmol)');
    LEGEND_STATES  = LEGEND_STATES';
    LEGEND_ALGEBRAIC = LEGEND_ALGEBRAIC';
    LEGEND_RATES = LEGEND_RATES';
    LEGEND_CONSTANTS = LEGEND_CONSTANTS';
end

function [STATES, CONSTANTS] = initConsts(p, i_stp)
    [LEGEND_STATES, LEGEND_ALGEBRAIC, legend_VOI, LEGEND_CONSTANTS,~] = createLegends();
    VOI = 0; CONSTANTS = []; STATES = []; ALGEBRAIC = [];
    CONSTANTS(:,1) = 0.0004579000e0;
    CONSTANTS(:,2) = 1e-18;
    CONSTANTS(:,3) = 1e-18;
    CONSTANTS(:,4) = 0.1455400000;
    CONSTANTS(:,5) = 1e-18;
    CONSTANTS(:,6) = 1e-18;
    CONSTANTS(:,7) = 1e-18;
    CONSTANTS(:,8) = 0.01;
    CONSTANTS(:,9) = 0.02;
    CONSTANTS(:,10) = 0.01;
    CONSTANTS(:,11) = 2.2;
    CONSTANTS(:,12) = 1.1;
    CONSTANTS(:,13) = 570;
    CONSTANTS(:,14) = 1e-18;
    CONSTANTS(:,15) = 1e-18;
    CONSTANTS(:,16) = 1e-18;
    CONSTANTS(:,17) = 1e-18;
    CONSTANTS(:,18) = 1e-3;
    CONSTANTS(:,19) = 2.5;
    CONSTANTS(:,20) = 5e-1;
    CONSTANTS(:,21) = 1e0;
    CONSTANTS(:,22) = 1e0;
    CONSTANTS(:,23) = 1e-8;
    STATES(:,1) = 1e-16;
    STATES(:,2) = 1e-16;
    STATES(:,3) = 1e-16;
    STATES(:,4) = 1e-16;
    STATES(:,5) = 1e-16;
    STATES(:,6) = 1e-16;
    STATES(:,7) = 1e-16;
    STATES(:,8) = 1e-16;
    STATES(:,9) = 1e-16;
    STATES(:,10) = 1e-16;
    STATES(:,11) = 1e-16;
    STATES(:,12) = 1e-16;
    STATES(:,13) = 1e-16;
    STATES(:,14) = 1e-16;
    STATES(:,15) = 1e-16;
    STATES(:,16) = 1e-16;
    STATES(:,17) = 1e-16;
    STATES(:,18) = 1e-16;
    STATES(:,19) = 1e-16;
    CONSTANTS(:,24) = 1036.38;
    CONSTANTS(:,25) = 1.83921e-07;
    CONSTANTS(:,26) = 891573;
    CONSTANTS(:,27) = 1.58222e+06;
    CONSTANTS(:,28) = 0;
    CONSTANTS(:,29) = 52417.5;
    CONSTANTS(:,30) = 0.000610519;
    CONSTANTS(:,31) = 0.576677;
    CONSTANTS(:,32) = 0.0661821;
    CONSTANTS(:,33) = 8.60273e-06;
    CONSTANTS(:,34) = 0.00230556;
    CONSTANTS(:,35) = 2.17775;
    CONSTANTS(:,36) = 28.0492;
    CONSTANTS(:,37) = 1.58056e+11;
    CONSTANTS(:,38) = 0.0574759;
    CONSTANTS(:,39) = 0.280492;
    CONSTANTS(:,40) = 0.00337913;
    CONSTANTS(:,41) = 1.07597;
    CONSTANTS(:,42) = 0.158056;
    CONSTANTS(:,43) = 0.00113911;
    CONSTANTS(:,44) = 0.00878478;
    CONSTANTS(:,45) = 736.699;
    CONSTANTS(:,46) = 161.34;
    CONSTANTS(:,47) = 823.314;
    CONSTANTS(:,48) = 3.61368e-10;
    CONSTANTS(:,49) = 7.91408e-11;
    CONSTANTS(:,50) = 0.500146;
    CONSTANTS(:,51) = 0.000529497;
    CONSTANTS(:,52) = 1.26086e-05;
    CONSTANTS(:,53) = 1.33485e-08;
    CONSTANTS(:,54) = 732843;
    CONSTANTS(:,55) = 8.31;
    CONSTANTS(:,56) = 310;
    CONSTANTS(:,57) = 96485;
    CONSTANTS(:,58) = CONSTANTS(:,22)./CONSTANTS(:,21);
    CONSTANTS(:,59) = CONSTANTS(:,1)+CONSTANTS(:,2)+CONSTANTS(:,3)+CONSTANTS(:,5)+CONSTANTS(:,6)+CONSTANTS(:,7);
    % modify values at indices i_stp with values stored in struct p
    for i = 1:length(i_stp)
        CONSTANTS(:,i_stp(i)) = p(i);
    end
    
    % HACK
    if false
        disp('HACKILY INCREASING KAPPA BY 1E6');
        for i=26:34
            CONSTANTS(:,i) = CONSTANTS(:,i)*1e6;
        end
    end
    
    if false
        % set some ICs to zero for debugging R conservation
        labels = {...
            'q_RB1_inactive_init in component environment (fmol)'...
            'q_RB1_init in component environment (fmol)'...
            'q_L_RB1_inactive_init in component environment (fmol)', ...
            'q_L_RB1_init in component environment (fmol)', ...
            'q_L_RB1_Gs_init in component environment (fmol)', ...
            'q_RB1_Gs_init in component environment (fmol)', ...
            'q_RB1_aby_init in component environment (fmol)',...
            'q_L_RB1_aby_init in component environment (fmol)',...
            'q_RB1_abyT_init in component environment (fmol)',...
            'q_L_RB1_abyT_init in component environment (fmol)',...
            'q_RB1_tag_init in component environment (fmol)',...
            'q_L_RB1_tag_init in component environment (fmol)',...
            'q_RB1_GRKArr_init in component environment (fmol)',...
            'q_L_RB1_GRKArr_init in component environment (fmol)'};
        labels_st = {...
            'q_RB1_inactive in component GPCR_B1AR_reduced (fmol)'...
            'q_RB1 in component GPCR_B1AR_reduced (fmol)'...
            'q_L_RB1_inactive in component GPCR_B1AR_reduced (fmol)', ...
            'q_L_RB1 in component GPCR_B1AR_reduced (fmol)', ...
            'q_L_RB1_Gs in component GPCR_B1AR_reduced (fmol)', ...
            'q_RB1_Gs in component GPCR_B1AR_reduced (fmol)', ...
            'q_RB1_aby in component GPCR_B1AR_reduced (fmol)',...
            'q_L_RB1_aby in component GPCR_B1AR_reduced (fmol)',...
            'q_RB1_abyT in component GPCR_B1AR_reduced (fmol)',...
            'q_L_RB1_abyT in component GPCR_B1AR_reduced (fmol)',...
            'q_RB1_tag in component GPCR_B1AR_reduced (fmol)',...
            'q_L_RB1_tag in component GPCR_B1AR_reduced (fmol)',...
            'q_RB1_GRKArr in component GPCR_B1AR_reduced (fmol)',...
            'q_L_RB1_GRKArr in component GPCR_B1AR_reduced (fmol)'};
        [i_Rinits, ~,~] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        [~, i_RSTinits,~] = find_indices(labels_st, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        disp('HACKILY MAKING R MOIETIES ZERO IC');
        for i=1:length(i_Rinits)
            CONSTANTS(:,i_Rinits(i)) = 0;
        end
        for i=1:length(i_RSTinits)
            STATES(:,i_RSTinits(i)) = 0;
        end
    end
    
    if (isempty(STATES)), warning('Initial values for states not set');, end
end

function [RATES, ALGEBRAIC] = computeRates(VOI, STATES, CONSTANTS)
disp(VOI)         
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
    ALGEBRAIC(:,3) = STATES(:,2)+CONSTANTS(:,2);
    ALGEBRAIC(:,25) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,37).*ALGEBRAIC(:,3));
    ALGEBRAIC(:,8) = STATES(:,7)+CONSTANTS(:,6);
    ALGEBRAIC(:,30) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,42).*ALGEBRAIC(:,8));
    ALGEBRAIC(:,44) =  CONSTANTS(:,25).*(exp(ALGEBRAIC(:,25)./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,30)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,2) = STATES(:,1)+CONSTANTS(:,1);
    ALGEBRAIC(:,24) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,36).*ALGEBRAIC(:,2));
    ALGEBRAIC(:,1) = piecewise({VOI<CONSTANTS(:,19)&VOI>CONSTANTS(:,19) - CONSTANTS(:,21), CONSTANTS(:,23)+ CONSTANTS(:,58).*((VOI - CONSTANTS(:,19))+CONSTANTS(:,21)) , VOI>=CONSTANTS(:,19)&VOI<CONSTANTS(:,19)+CONSTANTS(:,20), CONSTANTS(:,22)+CONSTANTS(:,23) , VOI<CONSTANTS(:,19)+CONSTANTS(:,21)+CONSTANTS(:,20)&VOI>=CONSTANTS(:,19)+CONSTANTS(:,20), CONSTANTS(:,23)+  - CONSTANTS(:,58).*(((VOI - CONSTANTS(:,19)) - CONSTANTS(:,21)) - CONSTANTS(:,20)) }, CONSTANTS(:,23));
    ALGEBRAIC(:,4) = STATES(:,3)+ALGEBRAIC(:,1);
    ALGEBRAIC(:,26) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,38).*ALGEBRAIC(:,4));
    ALGEBRAIC(:,47) =  CONSTANTS(:,28).*(exp((ALGEBRAIC(:,24)+ALGEBRAIC(:,26))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,25)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,2) =  - ALGEBRAIC(:,44)+ALGEBRAIC(:,47);
                                    
    ALGEBRAIC(:,5) = STATES(:,4)+CONSTANTS(:,3);
    ALGEBRAIC(:,27) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,39).*ALGEBRAIC(:,5));
                                                                                                                                                                                                                              
                                                    
                                    
                                                
                                                                                               
                                                                                                                                                                
    ALGEBRAIC(:,6) = STATES(:,5)+CONSTANTS(:,4);
    ALGEBRAIC(:,28) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,40).*ALGEBRAIC(:,6));
    ALGEBRAIC(:,7) = STATES(:,6)+CONSTANTS(:,5);
    ALGEBRAIC(:,29) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,41).*ALGEBRAIC(:,7));
    ALGEBRAIC(:,45) =  CONSTANTS(:,26).*(exp((ALGEBRAIC(:,27)+ALGEBRAIC(:,28))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,29)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
                                                   
                                                      
                                                                                   
                                                
                                                                                               
                                                                                                                                                                                                                              
                                                   
    ALGEBRAIC(:,10) = STATES(:,9)+CONSTANTS(:,8);
    ALGEBRAIC(:,32) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,44).*ALGEBRAIC(:,10));
    ALGEBRAIC(:,11) = STATES(:,10)+CONSTANTS(:,9);
    ALGEBRAIC(:,33) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,45).*ALGEBRAIC(:,11));
    ALGEBRAIC(:,14) = STATES(:,12)+CONSTANTS(:,11);
    ALGEBRAIC(:,35) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,47).*ALGEBRAIC(:,14));
    ALGEBRAIC(:,15) = STATES(:,13)+CONSTANTS(:,12);
    ALGEBRAIC(:,36) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,48).*ALGEBRAIC(:,15));
    ALGEBRAIC(:,17) = STATES(:,15)+CONSTANTS(:,14);
    ALGEBRAIC(:,38) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,50).*ALGEBRAIC(:,17));
    ALGEBRAIC(:,48) =  CONSTANTS(:,30).*(exp((ALGEBRAIC(:,29)+ALGEBRAIC(:,35))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp((ALGEBRAIC(:,32)+ALGEBRAIC(:,33)+ALGEBRAIC(:,38)+ALGEBRAIC(:,36))./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,6) = ALGEBRAIC(:,45) - ALGEBRAIC(:,48);
    ALGEBRAIC(:,49) =  CONSTANTS(:,29).*(exp((ALGEBRAIC(:,27)+ALGEBRAIC(:,26))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,30)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,3) =  - ALGEBRAIC(:,47) - ALGEBRAIC(:,49);
    ALGEBRAIC(:,43) =  CONSTANTS(:,24).*(exp(ALGEBRAIC(:,24)./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,27)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,4) = (ALGEBRAIC(:,43) - ALGEBRAIC(:,45)) - ALGEBRAIC(:,49);
    ALGEBRAIC(:,9) = STATES(:,8)+CONSTANTS(:,7);
    ALGEBRAIC(:,31) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,43).*ALGEBRAIC(:,9));
    ALGEBRAIC(:,46) =  CONSTANTS(:,27).*(exp((ALGEBRAIC(:,30)+ALGEBRAIC(:,28))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,31)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,7) = (ALGEBRAIC(:,44) - ALGEBRAIC(:,46))+ALGEBRAIC(:,49);
    ALGEBRAIC(:,18) = STATES(:,16)+CONSTANTS(:,15);
    ALGEBRAIC(:,39) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,51).*ALGEBRAIC(:,18));
    ALGEBRAIC(:,50) =  CONSTANTS(:,31).*(exp((ALGEBRAIC(:,31)+ALGEBRAIC(:,35))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp((ALGEBRAIC(:,32)+ALGEBRAIC(:,33)+ALGEBRAIC(:,39)+ALGEBRAIC(:,36))./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,8) = ALGEBRAIC(:,46) - ALGEBRAIC(:,50);
    RATES(:,12) =  - ALGEBRAIC(:,48) - ALGEBRAIC(:,50);
    RATES(:,13) = ALGEBRAIC(:,48)+ALGEBRAIC(:,50);
    ALGEBRAIC(:,53) = ALGEBRAIC(:,43)+ALGEBRAIC(:,49);
    RATES(:,1) = ( - ALGEBRAIC(:,43) - ALGEBRAIC(:,47))+ 0.000000.*ALGEBRAIC(:,53);
    ALGEBRAIC(:,12) = STATES(:,11)+CONSTANTS(:,10);
    ALGEBRAIC(:,34) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,46).*ALGEBRAIC(:,12));
    ALGEBRAIC(:,16) = STATES(:,14)+CONSTANTS(:,13);
    ALGEBRAIC(:,37) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,49).*ALGEBRAIC(:,16));
    ALGEBRAIC(:,51) =  CONSTANTS(:,32).*(exp(ALGEBRAIC(:,32)./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp((ALGEBRAIC(:,34)+ALGEBRAIC(:,37))./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,9) = (ALGEBRAIC(:,48)+ALGEBRAIC(:,50)) - ALGEBRAIC(:,51);
    RATES(:,14) = ALGEBRAIC(:,51);
    ALGEBRAIC(:,19) = STATES(:,17)+CONSTANTS(:,16);
    ALGEBRAIC(:,40) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,52).*ALGEBRAIC(:,19));
    ALGEBRAIC(:,23) = STATES(:,19)+CONSTANTS(:,18);
    ALGEBRAIC(:,42) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,54).*ALGEBRAIC(:,23));
                                                                                                                                                                                                                              
                                                    
                                  
    ALGEBRAIC(:,52) =  CONSTANTS(:,34).*(exp((ALGEBRAIC(:,38)+ALGEBRAIC(:,42))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,40)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
                                                                        
                                                                      
    RATES(:,15) = ALGEBRAIC(:,48) - ALGEBRAIC(:,52);
    RATES(:,17) = ALGEBRAIC(:,52);
    ALGEBRAIC(:,54) =  CONSTANTS(:,33).*(exp((ALGEBRAIC(:,34)+ALGEBRAIC(:,33))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,28)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,5) = ( - ALGEBRAIC(:,45) - ALGEBRAIC(:,46))+ALGEBRAIC(:,54);
    RATES(:,10) = (ALGEBRAIC(:,48)+ALGEBRAIC(:,50)) - ALGEBRAIC(:,54);
    RATES(:,11) = ALGEBRAIC(:,51) - ALGEBRAIC(:,54);
    ALGEBRAIC(:,20) = STATES(:,18)+CONSTANTS(:,17);
    ALGEBRAIC(:,41) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,53).*ALGEBRAIC(:,20));
    ALGEBRAIC(:,55) =  CONSTANTS(:,35).*(exp((ALGEBRAIC(:,39)+ALGEBRAIC(:,42))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,41)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    RATES(:,16) = ALGEBRAIC(:,50) - ALGEBRAIC(:,55);
    RATES(:,18) = ALGEBRAIC(:,55);
    RATES(:,19) =  - ALGEBRAIC(:,52) - ALGEBRAIC(:,55);
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
    ALGEBRAIC(:,3) = STATES(:,2)+CONSTANTS(:,2);
    ALGEBRAIC(:,25) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,37).*ALGEBRAIC(:,3));
    ALGEBRAIC(:,8) = STATES(:,7)+CONSTANTS(:,6);
    ALGEBRAIC(:,30) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,42).*ALGEBRAIC(:,8));
    ALGEBRAIC(:,44) =  CONSTANTS(:,25).*(exp(ALGEBRAIC(:,25)./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,30)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,2) = STATES(:,1)+CONSTANTS(:,1);
    ALGEBRAIC(:,24) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,36).*ALGEBRAIC(:,2));
    ALGEBRAIC(:,1) = piecewise({VOI<CONSTANTS(:,19)&VOI>CONSTANTS(:,19) - CONSTANTS(:,21), CONSTANTS(:,23)+ CONSTANTS(:,58).*((VOI - CONSTANTS(:,19))+CONSTANTS(:,21)) , VOI>=CONSTANTS(:,19)&VOI<CONSTANTS(:,19)+CONSTANTS(:,20), CONSTANTS(:,22)+CONSTANTS(:,23) , VOI<CONSTANTS(:,19)+CONSTANTS(:,21)+CONSTANTS(:,20)&VOI>=CONSTANTS(:,19)+CONSTANTS(:,20), CONSTANTS(:,23)+  - CONSTANTS(:,58).*(((VOI - CONSTANTS(:,19)) - CONSTANTS(:,21)) - CONSTANTS(:,20)) }, CONSTANTS(:,23));
    ALGEBRAIC(:,4) = STATES(:,3)+ALGEBRAIC(:,1);
    ALGEBRAIC(:,26) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,38).*ALGEBRAIC(:,4));
    ALGEBRAIC(:,47) =  CONSTANTS(:,28).*(exp((ALGEBRAIC(:,24)+ALGEBRAIC(:,26))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,25)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,5) = STATES(:,4)+CONSTANTS(:,3);
    ALGEBRAIC(:,27) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,39).*ALGEBRAIC(:,5));
                                                                                                                                                                                                                              
                                                
                                                                                               
                                                                                                                                                                
    ALGEBRAIC(:,6) = STATES(:,5)+CONSTANTS(:,4);
    ALGEBRAIC(:,28) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,40).*ALGEBRAIC(:,6));
    ALGEBRAIC(:,7) = STATES(:,6)+CONSTANTS(:,5);
    ALGEBRAIC(:,29) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,41).*ALGEBRAIC(:,7));
    ALGEBRAIC(:,45) =  CONSTANTS(:,26).*(exp((ALGEBRAIC(:,27)+ALGEBRAIC(:,28))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,29)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
                                                      
                                                
                                                                                               
                                                                                                                                                                                                                              
    ALGEBRAIC(:,10) = STATES(:,9)+CONSTANTS(:,8);
    ALGEBRAIC(:,32) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,44).*ALGEBRAIC(:,10));
    ALGEBRAIC(:,11) = STATES(:,10)+CONSTANTS(:,9);
    ALGEBRAIC(:,33) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,45).*ALGEBRAIC(:,11));
    ALGEBRAIC(:,14) = STATES(:,12)+CONSTANTS(:,11);
    ALGEBRAIC(:,35) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,47).*ALGEBRAIC(:,14));
    ALGEBRAIC(:,15) = STATES(:,13)+CONSTANTS(:,12);
    ALGEBRAIC(:,36) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,48).*ALGEBRAIC(:,15));
    ALGEBRAIC(:,17) = STATES(:,15)+CONSTANTS(:,14);
    ALGEBRAIC(:,38) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,50).*ALGEBRAIC(:,17));
    ALGEBRAIC(:,48) =  CONSTANTS(:,30).*(exp((ALGEBRAIC(:,29)+ALGEBRAIC(:,35))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp((ALGEBRAIC(:,32)+ALGEBRAIC(:,33)+ALGEBRAIC(:,38)+ALGEBRAIC(:,36))./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,49) =  CONSTANTS(:,29).*(exp((ALGEBRAIC(:,27)+ALGEBRAIC(:,26))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,30)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,43) =  CONSTANTS(:,24).*(exp(ALGEBRAIC(:,24)./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,27)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,9) = STATES(:,8)+CONSTANTS(:,7);
    ALGEBRAIC(:,31) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,43).*ALGEBRAIC(:,9));
    ALGEBRAIC(:,46) =  CONSTANTS(:,27).*(exp((ALGEBRAIC(:,30)+ALGEBRAIC(:,28))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,31)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,18) = STATES(:,16)+CONSTANTS(:,15);
    ALGEBRAIC(:,39) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,51).*ALGEBRAIC(:,18));
    ALGEBRAIC(:,50) =  CONSTANTS(:,31).*(exp((ALGEBRAIC(:,31)+ALGEBRAIC(:,35))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp((ALGEBRAIC(:,32)+ALGEBRAIC(:,33)+ALGEBRAIC(:,39)+ALGEBRAIC(:,36))./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,53) = ALGEBRAIC(:,43)+ALGEBRAIC(:,49);
    ALGEBRAIC(:,12) = STATES(:,11)+CONSTANTS(:,10);
    ALGEBRAIC(:,34) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,46).*ALGEBRAIC(:,12));
    ALGEBRAIC(:,16) = STATES(:,14)+CONSTANTS(:,13);
    ALGEBRAIC(:,37) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,49).*ALGEBRAIC(:,16));
    ALGEBRAIC(:,51) =  CONSTANTS(:,32).*(exp(ALGEBRAIC(:,32)./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp((ALGEBRAIC(:,34)+ALGEBRAIC(:,37))./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,19) = STATES(:,17)+CONSTANTS(:,16);
    ALGEBRAIC(:,40) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,52).*ALGEBRAIC(:,19));
    ALGEBRAIC(:,23) = STATES(:,19)+CONSTANTS(:,18);
    ALGEBRAIC(:,42) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,54).*ALGEBRAIC(:,23));
    ALGEBRAIC(:,52) =  CONSTANTS(:,34).*(exp((ALGEBRAIC(:,38)+ALGEBRAIC(:,42))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,40)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,54) =  CONSTANTS(:,33).*(exp((ALGEBRAIC(:,34)+ALGEBRAIC(:,33))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,28)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,20) = STATES(:,18)+CONSTANTS(:,17);
    ALGEBRAIC(:,41) =  CONSTANTS(:,55).*CONSTANTS(:,56).*log( CONSTANTS(:,53).*ALGEBRAIC(:,20));
    ALGEBRAIC(:,55) =  CONSTANTS(:,35).*(exp((ALGEBRAIC(:,39)+ALGEBRAIC(:,42))./( CONSTANTS(:,55).*CONSTANTS(:,56))) - exp(ALGEBRAIC(:,41)./( CONSTANTS(:,55).*CONSTANTS(:,56))));
    ALGEBRAIC(:,13) = ALGEBRAIC(:,6)+ALGEBRAIC(:,7)+ALGEBRAIC(:,9)+ALGEBRAIC(:,10)+ALGEBRAIC(:,12);
    ALGEBRAIC(:,21) = ALGEBRAIC(:,2)+ALGEBRAIC(:,3)+ALGEBRAIC(:,5)+ALGEBRAIC(:,7)+ALGEBRAIC(:,8)+ALGEBRAIC(:,9)+ALGEBRAIC(:,17)+ALGEBRAIC(:,18)+ALGEBRAIC(:,19)+ALGEBRAIC(:,20);
    ALGEBRAIC(:,22) = ALGEBRAIC(:,3)+ALGEBRAIC(:,4)+ALGEBRAIC(:,8)+ALGEBRAIC(:,9)+ALGEBRAIC(:,18)+ALGEBRAIC(:,20);
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

