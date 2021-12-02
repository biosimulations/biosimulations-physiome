tic;
[VOI, states, ALGEBRAIC, CONSTANTS, rates] = solvemodel();
toc;
                                                      

function [ALGEBRAICvariablecount] = getALGEBRAICvariablecount()
    % used later when setting a global variable with the number of ALGEBRAIC variables.
    % note: this is not the "main method".
    ALGEBRAICvariablecount =138;
end
% there are a total of 46 enp.stimduries in each of the rate and state variable arrays.
% there are a total of 116 enp.stimduries in the constant variable array.
%


function [VOI, states, ALGEBRAIC, CONSTANTS, rates] = solvemodel()

    [LEGEND_STATES, LEGEND_ALGEBRAIC, legend_VOI, LEGEND_CONSTANTS] = createLegends();

    % create ALGEBRAIC of correct size
    global ALGEBRAICvariablecount;  ALGEBRAICvariablecount = getALGEBRAICvariablecount();

    % change amoiunt of total givben chemical species available (labels) by a
    % multiplication factor (Gmult)
    labels = {'q_AC_init in component environment (fmol)', ...
        'q_cAMP_init in component environment (fmol)', ...
        'q_R_B1_init in component environment (fmol)', ...
        'q_Gs_init in component environment (fmol)', ...
        'q_R_M2_init in component environment (fmol)', ...
        'q_Gi_init in component environment (fmol)'};
%     labels = {'q_R_B1_init in component environment (fmol)', ...
%         'q_R_M2_init in component environment (fmol)'};
    [igs,~,~] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
    Gmult = 1; %1e3;
    [init_states, CONSTANTS] = initConsts(Gmult, igs);

    % ------------------------------------------
    % set timespan to solve over
    VOI = [0,1e-5]; % fast timescales due to fkc
%     VOI = [0 1e-3];
    % ------------------------------------------

    % set numerical accuracy options for ode solver
    options = odeset('reltol', 1e-07/3, 'abstol', 1e-07/3, 'maxstep', 1e-9); % step: 1e-4 % no need for step=1e-9. same as 1e-5

    % extra options for stimuli [ L_B1, L_M2 ] settings 
    p = struct;
%     p.stimtimes = [[1,20];[3,40]];
	p.stimthreshold = [-0.95, -0.95]; %[1e-3,1e-3];
    p.stimholding = [1e-9,1e-9];
    p.stimmag = [1.888e10,1.888e10]; %[1e6,1e6];
    p.stimstart = [1.2e-6,3e-6];
    p.trAMP = [1e-6,1e-6]; % seconds for rAMP start
    p.stimdur = [1,1];
    if true
        p.stimmag = [0,0];
    end
    p.freq = [1,1]; %[0.25,0.25]; % per second
    % solve model with ode solver
    [VOI, states] = ode15s(@(VOI, states)computeRates(VOI, states, CONSTANTS,p), VOI, init_states, options);

    % compute ALGEBRAIC variables
    [rates, ALGEBRAIC] = computeRates(VOI, states, CONSTANTS,p);
    ALGEBRAIC = computeAlgebraic(ALGEBRAIC, CONSTANTS, states, VOI,p);

    labels = {'q_L_B1_init in component environment (fmol)', ... 
                'q_L_M2_init in component environment (fmol)', ...
                'q_LR_B1Gs in component environment (fmol)', ...
                'q_LR_M2Gi in component environment (fmol)', ...
                'q_aGs_GTP in component environment (fmol)', ...
                'q_aGi_GTP in component environment (fmol)', ...
                'q_aGs_GTP_AC in component cAMP (fmol)', ...
                'q_AC in component environment (fmol)', ...
                'q_cAMP in component environment (fmol)', ...
                'q_ATP in component environment (fmol)'};
        
    if true
        [~, i_st, i_alg] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        plot_selected(i_st,VOI,states,legend_VOI,LEGEND_STATES,sprintf('LR_B1\nGmult=%g', Gmult),ceil(sqrt(length(i_st))))
        plot_selected(i_alg,VOI,ALGEBRAIC,legend_VOI,LEGEND_ALGEBRAIC,sprintf('LR_B1\nGmult=%g', Gmult),ceil(sqrt(length(i_alg))))
    end
      
    % plot chemostat concentrations: they should be constant, or machine
    % error order
    labels = {...
'L_B1_T in component environment (fmol)',...
'L_M2_T in component environment (fmol)',...
'R_B1_T in component environment (fmol)',...
'Gs_T in component environment (fmol)',...
'R_M2_T in component environment (fmol)',...
'Gi_T in component environment (fmol)',...
'adenosine_T in component environment (fmol)'
};
    labels_init = {...
'q_L_B1_init in component environment (fmol)',...
'q_L_M2_init in component environment (fmol)',...
'q_R_B1_init in component environment (fmol)',...
'q_Gs_init in component environment (fmol)',...
'q_R_M2_init in component environment (fmol)',...
'q_Gi_init in component environment (fmol)',...
'q_ATP_init in component environment (fmol)'
};
    [~, ~, i_alg] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
    [i_con, ~, i_algstim] = find_indices(labels_init, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
    plot_2per(i_algstim,i_con, i_alg,VOI,CONSTANTS,ALGEBRAIC,LEGEND_ALGEBRAIC,LEGEND_CONSTANTS,sprintf('chemostats\nGmult=%g', Gmult),3)
    
    % debug R_B1_t
    if false
        labels = {'q_R_B1 in component LRGbinding_B1AR (fmol)','q_R_B1 in component GsProtein (fmol)'};
        [~, i_st, ~] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        plot_selected(i_st,VOI,states,legend_VOI,LEGEND_STATES,sprintf('R_B1\nGmult=%g', Gmult),ceil(sqrt(length(i_st))))
    end
    
    % debug aGs_GTP and aGiGTP
    if true
        labels = {...
            'q_R_B1GsP in component environment (fmol)',...
            'q_R_M2GiP in component environment (fmol)',...
            'q_aGs_GTP in component environment (fmol)',...
            'q_aGi_GTP in component environment (fmol)',...
            'vphos_R_B1Gs in component GsProtein (fmol_per_sec)',...
            'vphos_LR_B1Gs in component GsProtein (fmol_per_sec)',...
            'vphos_R_M2Gi in component GiProtein (fmol_per_sec)',...
            'vphos_LR_M2Gi in component GiProtein (fmol_per_sec)',...
            'vact1_Gs in component GsProtein (fmol_per_sec)',...
            'vact2_Gs in component GsProtein (fmol_per_sec)',...
            'vact1_Gi in component GiProtein (fmol_per_sec)',...
            'vact2_Gi in component GiProtein (fmol_per_sec)',...
            'vhyd_Gs in component GsProtein (fmol_per_sec)',...
            'vhyd_Gi in component GiProtein (fmol_per_sec)',...
            'q_aGs_GTP in component GsProtein (fmol)',...
            'q_aGi_GTP in component GiProtein (fmol)',...
            };
        [~, i_st, i_alg] = find_indices(labels, cellstr(LEGEND_CONSTANTS), cellstr(LEGEND_STATES), cellstr(LEGEND_ALGEBRAIC));
        plot_selected(i_alg,VOI,ALGEBRAIC,legend_VOI,LEGEND_ALGEBRAIC,sprintf('ag_GTP\nGmult=%g', Gmult),ceil(sqrt(length(i_alg))))
        plot_selected(i_st,VOI,states,legend_VOI,LEGEND_STATES,sprintf('ag_GTP\nGmult=%g', Gmult),ceil(sqrt(length(i_st))))
    end
        
    % plot all q variables to confirm if we are ss
    if false
        figure();
        n = ceil(sqrt(size(states,2)));
        for i=1:size(states,2)
            subplot(n,n,i)
            plot(VOI, states(:,i));
            xlabel(legend_VOI);
            title(LEGEND_STATES(i,:));
        end
    end
end


function [] = plot_selected(ids,x,y,legend_x,legend_y,titlestr,ns)
    istart = 30;
    figure();
%     plot stimuli
    for i = 1:length(ids)
        subplot(ns,ns,i)
        plot(x(istart:end), y(istart:end,ids(i)));
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


function [LEGEND_STATES, LEGEND_ALGEBRAIC, LEGEND_VOI, LEGEND_CONSTANTS] = createLegends()
    LEGEND_STATES = ''; LEGEND_ALGEBRAIC = ''; LEGEND_VOI = ''; LEGEND_CONSTANTS = '';
    LEGEND_CONSTANTS(:,1) = strpad('kappa_1a in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,2) = strpad('kappa_1b in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,3) = strpad('kappa_2a in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,4) = strpad('kappa_2b in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,5) = strpad('kappa_3a in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,6) = strpad('kappa_3b in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,7) = strpad('kappa_4a in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,8) = strpad('kappa_4b in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,9) = strpad('kappa_5 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,10) = strpad('kappa_6 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,11) = strpad('kappa_7 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,12) = strpad('kappa_GiAC in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,13) = strpad('kappa_sig1_B1 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,14) = strpad('kappa_sig2_B1 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,15) = strpad('kappa_sig3_B1 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,16) = strpad('kappa_sig4_B1 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,17) = strpad('kappa_sig1_M2 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,18) = strpad('kappa_sig2_M2 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,19) = strpad('kappa_sig3_M2 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,20) = strpad('kappa_sig4_M2 in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,21) = strpad('kappa_phos_RGs in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,22) = strpad('kappa_phos_LRGs in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,23) = strpad('kappa_act1_Gs in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,24) = strpad('kappa_act2_Gs in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,25) = strpad('kappa_hyd_Gs in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,26) = strpad('kappa_reassoc_Gs in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,27) = strpad('kappa_phos_RGi in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,28) = strpad('kappa_phos_LRGi in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,29) = strpad('kappa_act1_Gi in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,30) = strpad('kappa_act2_Gi in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,31) = strpad('kappa_hyd_Gi in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,32) = strpad('kappa_reassoc_Gi in component BG_parameters (fmol_per_sec)');
    LEGEND_CONSTANTS(:,33) = strpad('K_ATP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,34) = strpad('K_cAMP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,35) = strpad('K_AC in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,36) = strpad('K_AC_ATP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,37) = strpad('K_aGs_GTP_AC in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,38) = strpad('K_aGs_GTP_AC_ATP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,39) = strpad('K_FSK_AC in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,40) = strpad('K_FSK_AC_ATP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,41) = strpad('K_PDE in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,42) = strpad('K_PDE_cAMP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,43) = strpad('K_five_AMP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,44) = strpad('K_IBMX in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,45) = strpad('K_PDEinh in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,46) = strpad('K_aGs_GTP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,47) = strpad('K_FSK in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,48) = strpad('K_aGi_GTP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,49) = strpad('K_ACinh in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,50) = strpad('K_PPi in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,51) = strpad('K_L_B1 in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,52) = strpad('K_R_B1 in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,53) = strpad('K_Gs in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,54) = strpad('K_LR_B1 in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,55) = strpad('K_R_B1Gs in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,56) = strpad('K_LR_B1Gs in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,57) = strpad('K_L_M2 in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,58) = strpad('K_R_M2 in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,59) = strpad('K_Gi in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,60) = strpad('K_LR_M2 in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,61) = strpad('K_R_M2Gi in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,62) = strpad('K_LR_M2Gi in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,63) = strpad('K_R_B1GsP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,64) = strpad('K_LR_B1GsP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,65) = strpad('K_beta_gamma_Gs in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,66) = strpad('K_aGs_GDP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,67) = strpad('K_Pi in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,68) = strpad('K_R_M2GiP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,69) = strpad('K_LR_M2GiP in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,70) = strpad('K_beta_gamma_Gi in component BG_parameters (per_fmol)');
    LEGEND_CONSTANTS(:,71) = strpad('K_aGi_GDP in component BG_parameters (per_fmol)');
    LEGEND_VOI = strpad('time in component environment (second)');
    LEGEND_CONSTANTS(:,72) = strpad('vol_myo in component environment (pL)');
    LEGEND_CONSTANTS(:,73) = strpad('freq in component environment (dimensionless)');
    LEGEND_CONSTANTS(:,74) = strpad('stimSt in component environment (second)');
    LEGEND_CONSTANTS(:,75) = strpad('stimSt2 in component environment (second)');
    LEGEND_CONSTANTS(:,76) = strpad('stimDur in component environment (second)');
    LEGEND_CONSTANTS(:,77) = strpad('tR in component environment (second)');
    LEGEND_CONSTANTS(:,78) = strpad('stimMag in component environment (fmol)');
    LEGEND_CONSTANTS(:,79) = strpad('stimHolding in component environment (fmol)');
    LEGEND_CONSTANTS(:,123) = strpad('m in component environment (fmol_per_sec)');
    LEGEND_CONSTANTS(:,80) = strpad('q_ATP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,81) = strpad('q_AC_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,82) = strpad('q_cAMP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,83) = strpad('q_AC_ATP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,84) = strpad('q_FSK_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,85) = strpad('q_FSK_AC_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,86) = strpad('q_FSK_AC_ATP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,87) = strpad('q_aGs_GTP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,88) = strpad('q_aGs_GTP_AC_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,89) = strpad('q_aGs_GTP_AC_ATP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,90) = strpad('q_PDE_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,91) = strpad('q_PDEinh_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,92) = strpad('q_PDE_cAMP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,93) = strpad('q_IBMX_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,94) = strpad('q_five_AMP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,95) = strpad('q_aGi_GTP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,96) = strpad('q_ACinh_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,97) = strpad('q_PPi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,98) = strpad('q_R_B1_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,99) = strpad('q_Gs_init in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,1) = strpad('q_L_B1_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,100) = strpad('q_LR_B1_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,101) = strpad('q_R_B1Gs_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,102) = strpad('q_LR_B1Gs_init in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,2) = strpad('q_L_M2_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,103) = strpad('q_R_M2_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,104) = strpad('q_Gi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,105) = strpad('q_LR_M2_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,106) = strpad('q_R_M2Gi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,107) = strpad('q_LR_M2Gi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,108) = strpad('q_beta_gamma_Gs_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,109) = strpad('q_aGs_GDP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,110) = strpad('q_Pi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,111) = strpad('q_beta_gamma_Gi_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,112) = strpad('q_aGi_GDP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,113) = strpad('q_R_B1GsP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,114) = strpad('q_LR_B1GsP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,115) = strpad('q_R_M2GiP_init in component environment (fmol)');
    LEGEND_CONSTANTS(:,116) = strpad('q_LR_M2GiP_init in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,36) = strpad('L_B1_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,60) = strpad('L_M2_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,37) = strpad('R_B1_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,61) = strpad('R_M2_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,82) = strpad('Gs_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,103) = strpad('Gi_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,17) = strpad('adenosine_T in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,3) = strpad('q_ATP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,4) = strpad('q_cAMP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,5) = strpad('q_AC in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,6) = strpad('q_AC_ATP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,7) = strpad('q_aGs_GTP_AC in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,8) = strpad('q_aGs_GTP_AC_ATP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,9) = strpad('q_FSK_AC in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,10) = strpad('q_FSK_AC_ATP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,11) = strpad('q_PDE in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,14) = strpad('q_PDE_cAMP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,15) = strpad('q_five_AMP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,18) = strpad('q_IBMX in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,19) = strpad('q_PDEinh in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,20) = strpad('q_aGs_GTP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,21) = strpad('q_FSK in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,23) = strpad('q_aGi_GTP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,24) = strpad('q_ACinh in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,26) = strpad('q_PPi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,25) = strpad('q_L_B1 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,27) = strpad('q_R_B1 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,28) = strpad('q_Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,30) = strpad('q_LR_B1 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,32) = strpad('q_R_B1Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,34) = strpad('q_LR_B1Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,38) = strpad('q_L_M2 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,45) = strpad('q_R_M2 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,48) = strpad('q_Gi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,51) = strpad('q_LR_M2 in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,54) = strpad('q_R_M2Gi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,57) = strpad('q_LR_M2Gi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,62) = strpad('q_R_B1GsP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,70) = strpad('q_LR_B1GsP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,74) = strpad('q_beta_gamma_Gs in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,78) = strpad('q_aGs_GDP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,83) = strpad('q_Pi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,87) = strpad('q_R_M2GiP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,94) = strpad('q_LR_M2GiP in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,98) = strpad('q_beta_gamma_Gi in component environment (fmol)');
    LEGEND_ALGEBRAIC(:,102) = strpad('q_aGi_GDP in component environment (fmol)');
    LEGEND_STATES(:,1) = strpad('q_ATP in component cAMP (fmol)');
    LEGEND_STATES(:,2) = strpad('q_cAMP in component cAMP (fmol)');
    LEGEND_STATES(:,3) = strpad('q_AC in component cAMP (fmol)');
    LEGEND_STATES(:,4) = strpad('q_AC_ATP in component cAMP (fmol)');
    LEGEND_STATES(:,5) = strpad('q_aGs_GTP_AC in component cAMP (fmol)');
    LEGEND_STATES(:,6) = strpad('q_aGs_GTP_AC_ATP in component cAMP (fmol)');
    LEGEND_STATES(:,7) = strpad('q_FSK_AC in component cAMP (fmol)');
    LEGEND_STATES(:,8) = strpad('q_FSK_AC_ATP in component cAMP (fmol)');
    LEGEND_STATES(:,9) = strpad('q_PDE in component cAMP (fmol)');
    LEGEND_STATES(:,10) = strpad('q_PDE_cAMP in component cAMP (fmol)');
    LEGEND_STATES(:,11) = strpad('q_five_AMP in component cAMP (fmol)');
    LEGEND_STATES(:,12) = strpad('q_IBMX in component cAMP (fmol)');
    LEGEND_STATES(:,13) = strpad('q_PDEinh in component cAMP (fmol)');
    LEGEND_STATES(:,14) = strpad('q_aGs_GTP in component cAMP (fmol)');
    LEGEND_STATES(:,15) = strpad('q_FSK in component cAMP (fmol)');
    LEGEND_STATES(:,16) = strpad('q_aGi_GTP in component cAMP (fmol)');
    LEGEND_STATES(:,17) = strpad('q_ACinh in component cAMP (fmol)');
    LEGEND_STATES(:,18) = strpad('q_PPi in component cAMP (fmol)');
    LEGEND_STATES(:,19) = strpad('q_L_B1 in component LRGbinding_B1AR (fmol)');
    LEGEND_STATES(:,20) = strpad('q_R_B1 in component LRGbinding_B1AR (fmol)');
    LEGEND_STATES(:,21) = strpad('q_Gs in component LRGbinding_B1AR (fmol)');
    LEGEND_STATES(:,22) = strpad('q_LR_B1 in component LRGbinding_B1AR (fmol)');
    LEGEND_STATES(:,23) = strpad('q_R_B1Gs in component LRGbinding_B1AR (fmol)');
    LEGEND_STATES(:,24) = strpad('q_LR_B1Gs in component LRGbinding_B1AR (fmol)');
    LEGEND_STATES(:,25) = strpad('q_L_M2 in component LRGbinding_M2 (fmol)');
    LEGEND_STATES(:,26) = strpad('q_R_M2 in component LRGbinding_M2 (fmol)');
    LEGEND_STATES(:,27) = strpad('q_Gi in component LRGbinding_M2 (fmol)');
    LEGEND_STATES(:,28) = strpad('q_LR_M2 in component LRGbinding_M2 (fmol)');
    LEGEND_STATES(:,29) = strpad('q_R_M2Gi in component LRGbinding_M2 (fmol)');
    LEGEND_STATES(:,30) = strpad('q_LR_M2Gi in component LRGbinding_M2 (fmol)');
    LEGEND_STATES(:,31) = strpad('q_R_B1 in component GsProtein (fmol)');
    LEGEND_STATES(:,32) = strpad('q_Gs in component GsProtein (fmol)');
    LEGEND_STATES(:,33) = strpad('q_R_B1Gs in component GsProtein (fmol)');
    LEGEND_STATES(:,34) = strpad('q_R_B1GsP in component GsProtein (fmol)');
    LEGEND_STATES(:,35) = strpad('q_LR_B1 in component GsProtein (fmol)');
    LEGEND_STATES(:,36) = strpad('q_LR_B1Gs in component GsProtein (fmol)');
    LEGEND_STATES(:,37) = strpad('q_LR_B1GsP in component GsProtein (fmol)');
    LEGEND_STATES(:,38) = strpad('q_aGs_GTP in component GsProtein (fmol)');
    LEGEND_STATES(:,39) = strpad('q_beta_gamma_Gs in component GsProtein (fmol)');
    LEGEND_STATES(:,40) = strpad('q_aGs_GDP in component GsProtein (fmol)');
    LEGEND_STATES(:,41) = strpad('q_Pi in component GsProtein (fmol)');
    LEGEND_STATES(:,42) = strpad('q_R_M2 in component GiProtein (fmol)');
    LEGEND_STATES(:,43) = strpad('q_Gi in component GiProtein (fmol)');
    LEGEND_STATES(:,44) = strpad('q_R_M2Gi in component GiProtein (fmol)');
    LEGEND_STATES(:,45) = strpad('q_R_M2GiP in component GiProtein (fmol)');
    LEGEND_STATES(:,46) = strpad('q_LR_M2 in component GiProtein (fmol)');
    LEGEND_STATES(:,47) = strpad('q_LR_M2Gi in component GiProtein (fmol)');
    LEGEND_STATES(:,48) = strpad('q_LR_M2GiP in component GiProtein (fmol)');
    LEGEND_STATES(:,49) = strpad('q_aGi_GTP in component GiProtein (fmol)');
    LEGEND_STATES(:,50) = strpad('q_beta_gamma_Gi in component GiProtein (fmol)');
    LEGEND_STATES(:,51) = strpad('q_aGi_GDP in component GiProtein (fmol)');
    LEGEND_STATES(:,52) = strpad('q_Pi in component GiProtein (fmol)');
    LEGEND_CONSTANTS(:,117) = strpad('R in component constants (J_per_K_per_mol)');
    LEGEND_CONSTANTS(:,118) = strpad('T in component constants (kelvin)');
    LEGEND_CONSTANTS(:,119) = strpad('F in component constants (C_per_mol)');
    LEGEND_ALGEBRAIC(:,99) = strpad('v1a in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,104) = strpad('v1b in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,109) = strpad('v2a in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,112) = strpad('v2b in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,115) = strpad('v3a in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,118) = strpad('v3b in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,121) = strpad('v4a in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,125) = strpad('v4b in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,129) = strpad('v5 in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,122) = strpad('v6 in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,126) = strpad('v7 in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,130) = strpad('vGiAC in component cAMP (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,29) = strpad('mu_ATP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,33) = strpad('mu_AC in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,31) = strpad('mu_cAMP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,35) = strpad('mu_AC_ATP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,84) = strpad('mu_FSK in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,49) = strpad('mu_FSK_AC in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,52) = strpad('mu_FSK_AC_ATP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,79) = strpad('mu_aGs_GTP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,39) = strpad('mu_aGs_GTP_AC in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,46) = strpad('mu_aGs_GTP_AC_ATP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,55) = strpad('mu_PDE in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,75) = strpad('mu_PDEinh in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,58) = strpad('mu_PDE_cAMP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,71) = strpad('mu_IBMX in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,63) = strpad('mu_five_AMP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,88) = strpad('mu_aGi_GTP in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,91) = strpad('mu_ACinh in component cAMP (J_per_mol)');
    LEGEND_ALGEBRAIC(:,95) = strpad('mu_PPi in component cAMP (J_per_mol)');
    LEGEND_CONSTANTS(:,120) = strpad('vol in component cAMP (pL)');
    LEGEND_ALGEBRAIC(:,12) = strpad('ATP_T in component cAMP (fmol)');
    LEGEND_ALGEBRAIC(:,13) = strpad('AC_T in component cAMP (fmol)');
    LEGEND_ALGEBRAIC(:,22) = strpad('Gs_T in component cAMP (fmol)');
    LEGEND_ALGEBRAIC(:,16) = strpad('cAMP_T in component cAMP (fmol)');
    LEGEND_ALGEBRAIC(:,40) = strpad('mu_L_B1 in component LRGbinding_B1AR (J_per_mol)');
    LEGEND_ALGEBRAIC(:,47) = strpad('mu_R_B1 in component LRGbinding_B1AR (J_per_mol)');
    LEGEND_ALGEBRAIC(:,50) = strpad('mu_Gs in component LRGbinding_B1AR (J_per_mol)');
    LEGEND_ALGEBRAIC(:,53) = strpad('mu_LR_B1 in component LRGbinding_B1AR (J_per_mol)');
    LEGEND_ALGEBRAIC(:,56) = strpad('mu_R_B1Gs in component LRGbinding_B1AR (J_per_mol)');
    LEGEND_ALGEBRAIC(:,59) = strpad('mu_LR_B1Gs in component LRGbinding_B1AR (J_per_mol)');
    LEGEND_ALGEBRAIC(:,64) = strpad('vsig1_B1 in component LRGbinding_B1AR (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,72) = strpad('vsig2_B1 in component LRGbinding_B1AR (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,76) = strpad('vsig3_B1 in component LRGbinding_B1AR (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,80) = strpad('vsig4_B1 in component LRGbinding_B1AR (fmol_per_sec)');
    LEGEND_CONSTANTS(:,121) = strpad('vol in component LRGbinding_B1AR (pL)');
    LEGEND_ALGEBRAIC(:,41) = strpad('L_T in component LRGbinding_B1AR (fmol)');
    LEGEND_ALGEBRAIC(:,42) = strpad('R_T in component LRGbinding_B1AR (fmol)');
    LEGEND_ALGEBRAIC(:,43) = strpad('Gs_T in component LRGbinding_B1AR (fmol)');
    LEGEND_ALGEBRAIC(:,65) = strpad('mu_L_M2 in component LRGbinding_M2 (J_per_mol)');
    LEGEND_ALGEBRAIC(:,73) = strpad('mu_R_M2 in component LRGbinding_M2 (J_per_mol)');
    LEGEND_ALGEBRAIC(:,77) = strpad('mu_Gi in component LRGbinding_M2 (J_per_mol)');
    LEGEND_ALGEBRAIC(:,81) = strpad('mu_LR_M2 in component LRGbinding_M2 (J_per_mol)');
    LEGEND_ALGEBRAIC(:,85) = strpad('mu_R_M2Gi in component LRGbinding_M2 (J_per_mol)');
    LEGEND_ALGEBRAIC(:,89) = strpad('mu_LR_M2Gi in component LRGbinding_M2 (J_per_mol)');
    LEGEND_ALGEBRAIC(:,92) = strpad('vsig1_M2 in component LRGbinding_M2 (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,96) = strpad('vsig2_M2 in component LRGbinding_M2 (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,100) = strpad('vsig3_M2 in component LRGbinding_M2 (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,105) = strpad('vsig4_M2 in component LRGbinding_M2 (fmol_per_sec)');
    LEGEND_CONSTANTS(:,122) = strpad('vol in component LRGbinding_M2 (pL)');
    LEGEND_ALGEBRAIC(:,66) = strpad('L_T in component LRGbinding_M2 (fmol)');
    LEGEND_ALGEBRAIC(:,67) = strpad('R_T in component LRGbinding_M2 (fmol)');
    LEGEND_ALGEBRAIC(:,68) = strpad('Gi_T in component LRGbinding_M2 (fmol)');
    LEGEND_ALGEBRAIC(:,131) = strpad('vphos_R_B1Gs in component GsProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,133) = strpad('vphos_LR_B1Gs in component GsProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,135) = strpad('vact1_Gs in component GsProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,137) = strpad('vact2_Gs in component GsProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,139) = strpad('vhyd_Gs in component GsProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,141) = strpad('vreassoc_Gs in component GsProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,90) = strpad('mu_R_B1 in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,93) = strpad('mu_Gs in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,97) = strpad('mu_R_B1Gs in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,101) = strpad('mu_R_B1GsP in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,106) = strpad('mu_LR_B1 in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,110) = strpad('mu_LR_B1Gs in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,113) = strpad('mu_LR_B1GsP in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,116) = strpad('mu_aGs_GTP in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,119) = strpad('mu_beta_gamma_Gs in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,123) = strpad('mu_aGs_GDP in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,127) = strpad('mu_Pi in component GsProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,44) = strpad('R_T in component GsProtein (fmol)');
    LEGEND_ALGEBRAIC(:,86) = strpad('Gs_T in component GsProtein (fmol)');
    LEGEND_ALGEBRAIC(:,140) = strpad('vphos_R_M2Gi in component GiProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,142) = strpad('vphos_LR_M2Gi in component GiProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,143) = strpad('vact1_Gi in component GiProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,144) = strpad('vact2_Gi in component GiProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,145) = strpad('vhyd_Gi in component GiProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,146) = strpad('vreassoc_Gi in component GiProtein (fmol_per_sec)');
    LEGEND_ALGEBRAIC(:,107) = strpad('mu_R_M2 in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,111) = strpad('mu_Gi in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,114) = strpad('mu_R_M2Gi in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,117) = strpad('mu_R_M2GiP in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,120) = strpad('mu_LR_M2 in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,124) = strpad('mu_LR_M2Gi in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,128) = strpad('mu_LR_M2GiP in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,132) = strpad('mu_aGi_GTP in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,134) = strpad('mu_beta_gamma_Gi in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,136) = strpad('mu_aGi_GDP in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,138) = strpad('mu_Pi in component GiProtein (J_per_mol)');
    LEGEND_ALGEBRAIC(:,69) = strpad('R_T in component GiProtein (fmol)');
    LEGEND_ALGEBRAIC(:,108) = strpad('Gi_T in component GiProtein (fmol)');
    LEGEND_RATES(:,1) = strpad('d/dt q_ATP in component cAMP (fmol)');
    LEGEND_RATES(:,3) = strpad('d/dt q_AC in component cAMP (fmol)');
    LEGEND_RATES(:,4) = strpad('d/dt q_AC_ATP in component cAMP (fmol)');
    LEGEND_RATES(:,2) = strpad('d/dt q_cAMP in component cAMP (fmol)');
    LEGEND_RATES(:,15) = strpad('d/dt q_FSK in component cAMP (fmol)');
    LEGEND_RATES(:,7) = strpad('d/dt q_FSK_AC in component cAMP (fmol)');
    LEGEND_RATES(:,8) = strpad('d/dt q_FSK_AC_ATP in component cAMP (fmol)');
    LEGEND_RATES(:,14) = strpad('d/dt q_aGs_GTP in component cAMP (fmol)');
    LEGEND_RATES(:,5) = strpad('d/dt q_aGs_GTP_AC in component cAMP (fmol)');
    LEGEND_RATES(:,6) = strpad('d/dt q_aGs_GTP_AC_ATP in component cAMP (fmol)');
    LEGEND_RATES(:,10) = strpad('d/dt q_PDE_cAMP in component cAMP (fmol)');
    LEGEND_RATES(:,9) = strpad('d/dt q_PDE in component cAMP (fmol)');
    LEGEND_RATES(:,12) = strpad('d/dt q_IBMX in component cAMP (fmol)');
    LEGEND_RATES(:,13) = strpad('d/dt q_PDEinh in component cAMP (fmol)');
    LEGEND_RATES(:,11) = strpad('d/dt q_five_AMP in component cAMP (fmol)');
    LEGEND_RATES(:,16) = strpad('d/dt q_aGi_GTP in component cAMP (fmol)');
    LEGEND_RATES(:,17) = strpad('d/dt q_ACinh in component cAMP (fmol)');
    LEGEND_RATES(:,18) = strpad('d/dt q_PPi in component cAMP (fmol)');
    LEGEND_RATES(:,19) = strpad('d/dt q_L_B1 in component LRGbinding_B1AR (fmol)');
    LEGEND_RATES(:,20) = strpad('d/dt q_R_B1 in component LRGbinding_B1AR (fmol)');
    LEGEND_RATES(:,21) = strpad('d/dt q_Gs in component LRGbinding_B1AR (fmol)');
    LEGEND_RATES(:,22) = strpad('d/dt q_LR_B1 in component LRGbinding_B1AR (fmol)');
    LEGEND_RATES(:,23) = strpad('d/dt q_R_B1Gs in component LRGbinding_B1AR (fmol)');
    LEGEND_RATES(:,24) = strpad('d/dt q_LR_B1Gs in component LRGbinding_B1AR (fmol)');
    LEGEND_RATES(:,25) = strpad('d/dt q_L_M2 in component LRGbinding_M2 (fmol)');
    LEGEND_RATES(:,26) = strpad('d/dt q_R_M2 in component LRGbinding_M2 (fmol)');
    LEGEND_RATES(:,27) = strpad('d/dt q_Gi in component LRGbinding_M2 (fmol)');
    LEGEND_RATES(:,28) = strpad('d/dt q_LR_M2 in component LRGbinding_M2 (fmol)');
    LEGEND_RATES(:,29) = strpad('d/dt q_R_M2Gi in component LRGbinding_M2 (fmol)');
    LEGEND_RATES(:,30) = strpad('d/dt q_LR_M2Gi in component LRGbinding_M2 (fmol)');
    LEGEND_RATES(:,31) = strpad('d/dt q_R_B1 in component GsProtein (fmol)');
    LEGEND_RATES(:,33) = strpad('d/dt q_R_B1Gs in component GsProtein (fmol)');
    LEGEND_RATES(:,34) = strpad('d/dt q_R_B1GsP in component GsProtein (fmol)');
    LEGEND_RATES(:,32) = strpad('d/dt q_Gs in component GsProtein (fmol)');
    LEGEND_RATES(:,35) = strpad('d/dt q_LR_B1 in component GsProtein (fmol)');
    LEGEND_RATES(:,36) = strpad('d/dt q_LR_B1Gs in component GsProtein (fmol)');
    LEGEND_RATES(:,37) = strpad('d/dt q_LR_B1GsP in component GsProtein (fmol)');
    LEGEND_RATES(:,38) = strpad('d/dt q_aGs_GTP in component GsProtein (fmol)');
    LEGEND_RATES(:,39) = strpad('d/dt q_beta_gamma_Gs in component GsProtein (fmol)');
    LEGEND_RATES(:,40) = strpad('d/dt q_aGs_GDP in component GsProtein (fmol)');
    LEGEND_RATES(:,41) = strpad('d/dt q_Pi in component GsProtein (fmol)');
    LEGEND_RATES(:,42) = strpad('d/dt q_R_M2 in component GiProtein (fmol)');
    LEGEND_RATES(:,44) = strpad('d/dt q_R_M2Gi in component GiProtein (fmol)');
    LEGEND_RATES(:,45) = strpad('d/dt q_R_M2GiP in component GiProtein (fmol)');
    LEGEND_RATES(:,43) = strpad('d/dt q_Gi in component GiProtein (fmol)');
    LEGEND_RATES(:,46) = strpad('d/dt q_LR_M2 in component GiProtein (fmol)');
    LEGEND_RATES(:,47) = strpad('d/dt q_LR_M2Gi in component GiProtein (fmol)');
    LEGEND_RATES(:,48) = strpad('d/dt q_LR_M2GiP in component GiProtein (fmol)');
    LEGEND_RATES(:,49) = strpad('d/dt q_aGi_GTP in component GiProtein (fmol)');
    LEGEND_RATES(:,50) = strpad('d/dt q_beta_gamma_Gi in component GiProtein (fmol)');
    LEGEND_RATES(:,51) = strpad('d/dt q_aGi_GDP in component GiProtein (fmol)');
    LEGEND_RATES(:,52) = strpad('d/dt q_Pi in component GiProtein (fmol)');
    LEGEND_STATES  = LEGEND_STATES';
    LEGEND_ALGEBRAIC = LEGEND_ALGEBRAIC';
    LEGEND_RATES = LEGEND_RATES';
    LEGEND_CONSTANTS = LEGEND_CONSTANTS';
end

function [STATES, CONSTANTS] = initConsts(Gmult,igs)
    VOI = 0; CONSTANTS = []; STATES = []; ALGEBRAIC = [];
    CONSTANTS(:,1) = 3.63265e+06;
    CONSTANTS(:,2) = 0.000758462;
    CONSTANTS(:,3) = 333398;
    CONSTANTS(:,4) = 0.0899646;
    CONSTANTS(:,5) = 2.40489e+08;
    CONSTANTS(:,6) = 2.79639e-17;
    CONSTANTS(:,7) = 30916.4;
    CONSTANTS(:,8) = 0.11891;
    CONSTANTS(:,9) = 824.604;
    CONSTANTS(:,10) = 6142.12;
    CONSTANTS(:,11) = 443048;
    CONSTANTS(:,12) = 1734.45;
    CONSTANTS(:,13) = 1320.77;
    CONSTANTS(:,14) = 24.8319;
    CONSTANTS(:,15) = 5.26566;
    CONSTANTS(:,16) = 4.19518e+06;
    CONSTANTS(:,17) = 2426.3;
    CONSTANTS(:,18) = 68.6013;
    CONSTANTS(:,19) = 14.5471;
    CONSTANTS(:,20) = 2.90239e+06;
    CONSTANTS(:,21) = 24.1902;
    CONSTANTS(:,22) = 7.80819;
    CONSTANTS(:,23) = 1.42953;
    CONSTANTS(:,24) = 0.0374674;
    CONSTANTS(:,25) = 0.287462; % kappa_hyd_Gs
    CONSTANTS(:,26) = 2.7312e+06;
    CONSTANTS(:,27) = 44.4383;
    CONSTANTS(:,28) = 21.5711;
    CONSTANTS(:,29) = 0.410326; 
    CONSTANTS(:,30) = 0.000323464;
    CONSTANTS(:,31) = 2.02938; % kappa_hyd_Gi
    CONSTANTS(:,32) = 1.70408e+06;
    CONSTANTS(:,33) = 5.35546e-05;
    CONSTANTS(:,34) = 0.0158165;
    CONSTANTS(:,35) = 4.03967;
    CONSTANTS(:,36) = 7.66545;
    CONSTANTS(:,37) = 4.73286;
    CONSTANTS(:,38) = 2.74656;
    CONSTANTS(:,39) = 0.0656131;
    CONSTANTS(:,40) = 0.103955;
    CONSTANTS(:,41) = 1.72816;
    CONSTANTS(:,42) = 1.22235;
    CONSTANTS(:,43) = 0.0158165;
    CONSTANTS(:,44) = 0.0197666;
    CONSTANTS(:,45) = 35.253;
    CONSTANTS(:,46) = 0.085145;
    CONSTANTS(:,47) = 1.07308e-05;
    CONSTANTS(:,48) = 0.0120608;
    CONSTANTS(:,49) = 16.7602;
    CONSTANTS(:,50) = 9.843e-05;
    CONSTANTS(:,51) = 0.0480673;
    CONSTANTS(:,52) = 0.00573574;
    CONSTANTS(:,53) = 156.63;
    CONSTANTS(:,54) = 0.767984;
    CONSTANTS(:,55) = 517.271;
    CONSTANTS(:,56) = 456.649;
    CONSTANTS(:,57) = 0.0319627;
    CONSTANTS(:,58) = 0.0124678;
    CONSTANTS(:,59) = 39.2246;
    CONSTANTS(:,60) = 1.11006;
    CONSTANTS(:,61) = 281.579;
    CONSTANTS(:,62) = 165.295;
    CONSTANTS(:,63) = 0.625296;
    CONSTANTS(:,64) = 6.79829;
    CONSTANTS(:,65) = 1.83091e-05;
    CONSTANTS(:,66) = 0.0215206;
    CONSTANTS(:,67) = 0.00012979;
    CONSTANTS(:,68) = 0.340383;
    CONSTANTS(:,69) = 2.4608;
    CONSTANTS(:,70) = 0.000207164;
    CONSTANTS(:,71) = 0.00304839;
    CONSTANTS(:,72) = 34.4;
    CONSTANTS(:,73) = 500;
    CONSTANTS(:,74) = 3.5e-4;
    CONSTANTS(:,75) = 3e-4;
    CONSTANTS(:,76) = 0.25e-4;
    CONSTANTS(:,77) = 1.8e-4;
    CONSTANTS(:,78) = 1e1;
    CONSTANTS(:,79) = 1e-5;
    CONSTANTS(:,80) = 190;
    CONSTANTS(:,81) = 1.889E-03;
    CONSTANTS(:,82) = 1e-18;
    CONSTANTS(:,83) = 1e-18;
    CONSTANTS(:,84) = 3.800E-05;
    CONSTANTS(:,85) = 1e-18;
    CONSTANTS(:,86) = 1e-18;
    CONSTANTS(:,87) = 1e-18;
    CONSTANTS(:,88) = 1e-18;
    CONSTANTS(:,89) = 1e-18;
    CONSTANTS(:,90) = 1.482E-03;
    CONSTANTS(:,91) = 1e-18;
    CONSTANTS(:,92) = 1e-18;
    CONSTANTS(:,93) = 3.80E-02;
    CONSTANTS(:,94) = 1e-18;
    CONSTANTS(:,95) = 1e-18;
    CONSTANTS(:,96) = 1e-18;
    CONSTANTS(:,97) = 1e-18;
    CONSTANTS(:,98) = 0.0004579000;
    CONSTANTS(:,99) = 0.1455400000;
    CONSTANTS(:,100) = 1e-18;
    CONSTANTS(:,101) = 8.888e-4; % q_R_B1Gs_init
    CONSTANTS(:,102) = 1e-18;
    CONSTANTS(:,103) = 0.00072;
    CONSTANTS(:,104) = 0.00836;
    CONSTANTS(:,105) = 1e-18;
    CONSTANTS(:,106) = 8.888e-4; % q_R_M2Gi_init
    CONSTANTS(:,107) = 1e-18;
    CONSTANTS(:,108) = 1e-18;
    CONSTANTS(:,109) = 1e-18;
    CONSTANTS(:,110) = 570;
    CONSTANTS(:,111) = 1e-18;
    CONSTANTS(:,112) = 1e-18;
    CONSTANTS(:,113) = 1e-18;
    CONSTANTS(:,114) = 1e-18;
    CONSTANTS(:,115) = 1e-18;
    CONSTANTS(:,116) = 1e-18;
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
    STATES(:,19) = 1e-18;
    STATES(:,20) = 1e-18;
    STATES(:,21) = 1e-18;
    STATES(:,22) = 1e-18;
    STATES(:,23) = 1e-18;
    STATES(:,24) = 1e-18;
    STATES(:,25) = 1e-16;
    STATES(:,26) = 1e-16;
    STATES(:,27) = 1e-16;
    STATES(:,28) = 1e-16;
    STATES(:,29) = 1e-16;
    STATES(:,30) = 1e-16;
    STATES(:,31) = 1e-16;
    STATES(:,32) = 1e-16;
    STATES(:,33) = 1e-16;
    STATES(:,34) = 1e-16;
    STATES(:,35) = 1e-16;
    STATES(:,36) = 1e-16;
    STATES(:,37) = 1e-16;
    STATES(:,38) = 1e-16;
    STATES(:,39) = 1e-16;
    STATES(:,40) = 1e-16;
    STATES(:,41) = 1e-16;
    STATES(:,42) = 1e-16;
    STATES(:,43) = 1e-16;
    STATES(:,44) = 1e-16;
    STATES(:,45) = 1e-16;
    STATES(:,46) = 1e-16;
    STATES(:,47) = 1e-16;
    STATES(:,48) = 1e-16;
    STATES(:,49) = 1e-16;
    STATES(:,50) = 1e-16;
    STATES(:,51) = 1e-16;
    STATES(:,52) = 1e-16;
    CONSTANTS(:,117) = 8.31;
    CONSTANTS(:,118) = 310;
    CONSTANTS(:,119) = 96485;
    CONSTANTS(:,120) = 38.0;
    CONSTANTS(:,121) = 34.4;
    CONSTANTS(:,122) = 34.4;
    CONSTANTS(:,123) = CONSTANTS(:,78)./CONSTANTS(:,77);
    if (isempty(STATES)), warning('Initial values for states not set');, end
    % multiply constant values by Gmult, with indices given in igs
    for j=1:length(igs)
        CONSTANTS(:,igs(j)) = CONSTANTS(:,igs(j))*Gmult;
    end                    
end

function [RATES, ALGEBRAIC] = computeRates(VOI, STATES, CONSTANTS,p)
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
    ALGEBRAIC(:,27) = CONSTANTS(:,98)+STATES(:,20)+STATES(:,31);
    ALGEBRAIC(:,47) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,52).*ALGEBRAIC(:,27));
    ALGEBRAIC(:,28) = CONSTANTS(:,99)+STATES(:,21)+STATES(:,32);
    ALGEBRAIC(:,50) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,53).*ALGEBRAIC(:,28));
    ALGEBRAIC(:,32) = CONSTANTS(:,101)+STATES(:,23)+STATES(:,33);
    ALGEBRAIC(:,56) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,55).*ALGEBRAIC(:,32));
    ALGEBRAIC(:,64) =  CONSTANTS(:,13).*exp((ALGEBRAIC(:,47)+ALGEBRAIC(:,50))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,56)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    m = p.stimmag(1)/p.trAMP(1);
    if VOI > p.stimstart
        j = 10;
    end
    ALGEBRAIC(:,1) = piecewise({VOI<p.stimstart(1)&VOI>p.stimstart(1) - p.trAMP(1), p.stimholding(1)+ m.*((VOI - p.stimstart(1))+p.trAMP(1)) , VOI>=p.stimstart(1)&VOI<p.stimstart(1)+p.stimdur(1), p.stimmag(1)+p.stimholding(1) , VOI<p.stimstart(1)+p.trAMP(1)+p.stimdur(1)&VOI>=p.stimstart(1)+p.stimdur(1), p.stimholding(1)+  - m.*(((VOI - p.stimstart(1)) - p.trAMP(1)) - p.stimdur(1)) }, p.stimholding(1));                        
    ALGEBRAIC(:,25) = ALGEBRAIC(:,1)+STATES(:,19);
    ALGEBRAIC(:,40) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,51).*ALGEBRAIC(:,25));
    ALGEBRAIC(:,34) = CONSTANTS(:,102)+STATES(:,24)+STATES(:,36);
    ALGEBRAIC(:,59) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,56).*ALGEBRAIC(:,34));
    ALGEBRAIC(:,72) =  CONSTANTS(:,14).*exp((ALGEBRAIC(:,56)+ALGEBRAIC(:,40))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,59)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    RATES(:,23) = ALGEBRAIC(:,64) - ALGEBRAIC(:,72);
    ALGEBRAIC(:,30) = CONSTANTS(:,100)+STATES(:,22)+STATES(:,35);
    ALGEBRAIC(:,53) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,54).*ALGEBRAIC(:,30));
    ALGEBRAIC(:,76) =  CONSTANTS(:,15).*exp((ALGEBRAIC(:,53)+ALGEBRAIC(:,50))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,59)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    RATES(:,21) =  - ALGEBRAIC(:,64) - ALGEBRAIC(:,76);
    RATES(:,24) = ALGEBRAIC(:,72)+ALGEBRAIC(:,76);
    ALGEBRAIC(:,80) =  CONSTANTS(:,16).*exp((ALGEBRAIC(:,47)+ALGEBRAIC(:,40))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,53)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    RATES(:,19) =  - ALGEBRAIC(:,72) - ALGEBRAIC(:,80);
    RATES(:,20) =  - ALGEBRAIC(:,64) - ALGEBRAIC(:,80);
    RATES(:,22) =  - ALGEBRAIC(:,76)+ALGEBRAIC(:,80);
    ALGEBRAIC(:,45) = CONSTANTS(:,103)+STATES(:,26)+STATES(:,42);
    ALGEBRAIC(:,73) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,58).*ALGEBRAIC(:,45));
    ALGEBRAIC(:,48) = CONSTANTS(:,104)+STATES(:,27)+STATES(:,43);
    ALGEBRAIC(:,77) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,59).*ALGEBRAIC(:,48));
    ALGEBRAIC(:,54) = CONSTANTS(:,106)+STATES(:,29)+STATES(:,44);
    ALGEBRAIC(:,85) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,61).*ALGEBRAIC(:,54));
    ALGEBRAIC(:,92) =  CONSTANTS(:,17).*exp((ALGEBRAIC(:,73)+ALGEBRAIC(:,77))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,85)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    m = p.stimmag(2)/p.trAMP(2);
    ALGEBRAIC(:,2) = piecewise({VOI<p.stimstart(2)&VOI>p.stimstart(2) - p.trAMP(2), p.stimholding(2)+ m.*((VOI - p.stimstart(2))+p.trAMP(2)) , VOI>=p.stimstart(2)&VOI<p.stimstart(2)+p.stimdur(2), p.stimmag(2)+p.stimholding(2) , VOI<p.stimstart(2)+p.trAMP(2)+p.stimdur(2)&VOI>=p.stimstart(2)+p.stimdur(2), p.stimholding(2)+  - m.*(((VOI - p.stimstart(2)) - p.trAMP(2)) - p.stimdur(2)) }, p.stimholding(2));
    ALGEBRAIC(:,38) = ALGEBRAIC(:,2)+STATES(:,25);
    ALGEBRAIC(:,65) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,57).*ALGEBRAIC(:,38));
    ALGEBRAIC(:,57) = CONSTANTS(:,107)+STATES(:,30)+STATES(:,47);
    ALGEBRAIC(:,89) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,62).*ALGEBRAIC(:,57));
    ALGEBRAIC(:,96) =  CONSTANTS(:,18).*exp((ALGEBRAIC(:,85)+ALGEBRAIC(:,65))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,89)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    RATES(:,29) = ALGEBRAIC(:,92) - ALGEBRAIC(:,96);
    ALGEBRAIC(:,51) = CONSTANTS(:,105)+STATES(:,28)+STATES(:,46);
    ALGEBRAIC(:,81) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,60).*ALGEBRAIC(:,51));
    ALGEBRAIC(:,100) =  CONSTANTS(:,19).*exp((ALGEBRAIC(:,81)+ALGEBRAIC(:,77))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,89)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    RATES(:,27) =  - ALGEBRAIC(:,92) - ALGEBRAIC(:,100);
    RATES(:,30) = ALGEBRAIC(:,96)+ALGEBRAIC(:,100);
    ALGEBRAIC(:,3) = CONSTANTS(:,80)+STATES(:,1);
    ALGEBRAIC(:,29) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,33).*ALGEBRAIC(:,3));
    ALGEBRAIC(:,5) = CONSTANTS(:,81)+STATES(:,3);
    ALGEBRAIC(:,33) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,35).*ALGEBRAIC(:,5));
    ALGEBRAIC(:,6) = CONSTANTS(:,83)+STATES(:,4);
    ALGEBRAIC(:,35) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,36).*ALGEBRAIC(:,6));
    ALGEBRAIC(:,99) =  CONSTANTS(:,1).*(exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,29))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,35)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,4) = CONSTANTS(:,82)+STATES(:,2);
    ALGEBRAIC(:,31) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,34).*ALGEBRAIC(:,4));
    ALGEBRAIC(:,26) = CONSTANTS(:,97)+STATES(:,18);
    ALGEBRAIC(:,95) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,50).*ALGEBRAIC(:,26));
    ALGEBRAIC(:,104) =  CONSTANTS(:,2).*(exp(ALGEBRAIC(:,35)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,31)+ALGEBRAIC(:,95))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,4) = ALGEBRAIC(:,99) - ALGEBRAIC(:,104);
    ALGEBRAIC(:,105) =  CONSTANTS(:,20).*exp((ALGEBRAIC(:,73)+ALGEBRAIC(:,65))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,81)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    RATES(:,25) =  - ALGEBRAIC(:,96) - ALGEBRAIC(:,105);
    RATES(:,26) =  - ALGEBRAIC(:,92) - ALGEBRAIC(:,105);
    RATES(:,28) =  - ALGEBRAIC(:,100)+ALGEBRAIC(:,105);
    ALGEBRAIC(:,7) = CONSTANTS(:,88)+STATES(:,5);
    ALGEBRAIC(:,39) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,37).*ALGEBRAIC(:,7));
    ALGEBRAIC(:,8) = CONSTANTS(:,89)+STATES(:,6);
    ALGEBRAIC(:,46) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,38).*ALGEBRAIC(:,8));
    ALGEBRAIC(:,109) =  CONSTANTS(:,3).*(exp((ALGEBRAIC(:,39)+ALGEBRAIC(:,29))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,46)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,112) =  CONSTANTS(:,4).*(exp(ALGEBRAIC(:,46)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,39)+ALGEBRAIC(:,31)+ALGEBRAIC(:,95))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,6) = ALGEBRAIC(:,109) - ALGEBRAIC(:,112);
    ALGEBRAIC(:,9) = CONSTANTS(:,85)+STATES(:,7);
    ALGEBRAIC(:,49) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,39).*ALGEBRAIC(:,9));
    ALGEBRAIC(:,10) = CONSTANTS(:,86)+STATES(:,8);
    ALGEBRAIC(:,52) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,40).*ALGEBRAIC(:,10));
    ALGEBRAIC(:,115) =  CONSTANTS(:,5).*(exp((ALGEBRAIC(:,49)+ALGEBRAIC(:,29))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,52)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,1) = ( - ALGEBRAIC(:,99) - ALGEBRAIC(:,115)) - ALGEBRAIC(:,109);
    ALGEBRAIC(:,118) =  CONSTANTS(:,6).*(exp(ALGEBRAIC(:,52)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,49)+ALGEBRAIC(:,31)+ALGEBRAIC(:,95))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,8) = ALGEBRAIC(:,115) - ALGEBRAIC(:,118);
    ALGEBRAIC(:,11) = CONSTANTS(:,90)+STATES(:,9);
    ALGEBRAIC(:,55) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,41).*ALGEBRAIC(:,11));
    ALGEBRAIC(:,14) = CONSTANTS(:,92)+STATES(:,10);
    ALGEBRAIC(:,58) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,42).*ALGEBRAIC(:,14));
    ALGEBRAIC(:,121) =  CONSTANTS(:,7).*(exp((ALGEBRAIC(:,55)+ALGEBRAIC(:,31))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,58)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,2) = (ALGEBRAIC(:,104)+ALGEBRAIC(:,118)+ALGEBRAIC(:,112)) - ALGEBRAIC(:,121);
    ALGEBRAIC(:,20) = CONSTANTS(:,87)+STATES(:,14)+STATES(:,38);
    ALGEBRAIC(:,79) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,46).*ALGEBRAIC(:,20));
    ALGEBRAIC(:,122) =  CONSTANTS(:,10).*(exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,79))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,39)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,14) =  - ALGEBRAIC(:,122);
    RATES(:,5) = (ALGEBRAIC(:,122) - ALGEBRAIC(:,109))+ALGEBRAIC(:,112);
    ALGEBRAIC(:,21) = CONSTANTS(:,84)+STATES(:,15);
    ALGEBRAIC(:,84) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,47).*ALGEBRAIC(:,21));
    ALGEBRAIC(:,126) =  CONSTANTS(:,11).*(exp((ALGEBRAIC(:,84)+ALGEBRAIC(:,33))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,49)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,15) =  - ALGEBRAIC(:,126);
    RATES(:,7) = (ALGEBRAIC(:,126)+ALGEBRAIC(:,118)) - ALGEBRAIC(:,115);
    ALGEBRAIC(:,15) = CONSTANTS(:,94)+STATES(:,11);
    ALGEBRAIC(:,63) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,43).*ALGEBRAIC(:,15));
    ALGEBRAIC(:,125) =  CONSTANTS(:,8).*(exp(ALGEBRAIC(:,58)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,55)+ALGEBRAIC(:,63))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,10) = ALGEBRAIC(:,121) - ALGEBRAIC(:,125);
    RATES(:,11) = ALGEBRAIC(:,125);
    ALGEBRAIC(:,23) = CONSTANTS(:,95)+STATES(:,16)+STATES(:,49);
    ALGEBRAIC(:,88) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,48).*ALGEBRAIC(:,23));
    ALGEBRAIC(:,24) = CONSTANTS(:,96)+STATES(:,17);
    ALGEBRAIC(:,91) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,49).*ALGEBRAIC(:,24));
    ALGEBRAIC(:,130) =  CONSTANTS(:,12).*(exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,88))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,91)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,3) = (((ALGEBRAIC(:,104) - ALGEBRAIC(:,99)) - ALGEBRAIC(:,122)) - ALGEBRAIC(:,126)) - ALGEBRAIC(:,130);
    ALGEBRAIC(:,19) = CONSTANTS(:,91)+STATES(:,13);
    ALGEBRAIC(:,75) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,45).*ALGEBRAIC(:,19));
    ALGEBRAIC(:,18) = CONSTANTS(:,93)+STATES(:,12);
    ALGEBRAIC(:,71) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,44).*ALGEBRAIC(:,18));
    ALGEBRAIC(:,129) =  CONSTANTS(:,9).*(exp((ALGEBRAIC(:,55)+ALGEBRAIC(:,71))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,75)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,9) = (ALGEBRAIC(:,125) - ALGEBRAIC(:,121)) - ALGEBRAIC(:,129);
    RATES(:,12) =  - ALGEBRAIC(:,129);
    RATES(:,13) = ALGEBRAIC(:,129);
    RATES(:,16) =  - ALGEBRAIC(:,130);
    RATES(:,17) = ALGEBRAIC(:,130);
    RATES(:,18) = ALGEBRAIC(:,130);
    ALGEBRAIC(:,97) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,55).*ALGEBRAIC(:,32));
    ALGEBRAIC(:,62) = CONSTANTS(:,113)+STATES(:,34);
    ALGEBRAIC(:,101) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,63).*ALGEBRAIC(:,62));
    ALGEBRAIC(:,83) = CONSTANTS(:,110)+STATES(:,41)+STATES(:,52);
    ALGEBRAIC(:,127) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,67).*ALGEBRAIC(:,83));
    ALGEBRAIC(:,131) =  CONSTANTS(:,21).*(exp((ALGEBRAIC(:,97)+ALGEBRAIC(:,127))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,101)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,33) =  - ALGEBRAIC(:,131);
    ALGEBRAIC(:,110) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,56).*ALGEBRAIC(:,34));
    ALGEBRAIC(:,70) = CONSTANTS(:,114)+STATES(:,37);
    ALGEBRAIC(:,113) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,64).*ALGEBRAIC(:,70));
    ALGEBRAIC(:,133) =  CONSTANTS(:,22).*(exp((ALGEBRAIC(:,110)+ALGEBRAIC(:,127))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,113)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,36) =  - ALGEBRAIC(:,133);
    ALGEBRAIC(:,90) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,52).*ALGEBRAIC(:,27));
    ALGEBRAIC(:,116) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,46).*ALGEBRAIC(:,20));
    ALGEBRAIC(:,74) = CONSTANTS(:,108)+STATES(:,39);
    ALGEBRAIC(:,119) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,65).*ALGEBRAIC(:,74));
    ALGEBRAIC(:,135) =  CONSTANTS(:,23).*(exp(ALGEBRAIC(:,101)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,116)+ALGEBRAIC(:,119)+ALGEBRAIC(:,90))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,31) = ALGEBRAIC(:,135);
    RATES(:,34) = ALGEBRAIC(:,131) - ALGEBRAIC(:,135);
    ALGEBRAIC(:,106) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,54).*ALGEBRAIC(:,30));
    ALGEBRAIC(:,137) =  CONSTANTS(:,24).*(exp(ALGEBRAIC(:,113)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,116)+ALGEBRAIC(:,119)+ALGEBRAIC(:,106))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,35) = ALGEBRAIC(:,137);
    RATES(:,37) = ALGEBRAIC(:,133) - ALGEBRAIC(:,137);
    ALGEBRAIC(:,78) = CONSTANTS(:,109)+STATES(:,40);
    ALGEBRAIC(:,123) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,66).*ALGEBRAIC(:,78));
    ALGEBRAIC(:,139) =  CONSTANTS(:,25).*(exp(ALGEBRAIC(:,116)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,123)+ALGEBRAIC(:,127))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,38) = (ALGEBRAIC(:,135)+ALGEBRAIC(:,137)) - ALGEBRAIC(:,139);
    RATES(:,41) = ( - ALGEBRAIC(:,131) - ALGEBRAIC(:,133))+ALGEBRAIC(:,139);
    ALGEBRAIC(:,114) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,61).*ALGEBRAIC(:,54));
    ALGEBRAIC(:,87) = CONSTANTS(:,115)+STATES(:,45);
    ALGEBRAIC(:,117) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,68).*ALGEBRAIC(:,87));
    ALGEBRAIC(:,138) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,67).*ALGEBRAIC(:,83));
    ALGEBRAIC(:,140) =  CONSTANTS(:,27).*(exp((ALGEBRAIC(:,114)+ALGEBRAIC(:,138))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,117)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,44) =  - ALGEBRAIC(:,140);
    ALGEBRAIC(:,93) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,53).*ALGEBRAIC(:,28));
    ALGEBRAIC(:,141) =  CONSTANTS(:,26).*(exp((ALGEBRAIC(:,123)+ALGEBRAIC(:,119))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,93)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,32) = ALGEBRAIC(:,141);
    RATES(:,39) = (ALGEBRAIC(:,135)+ALGEBRAIC(:,137)) - ALGEBRAIC(:,141);
    RATES(:,40) = ALGEBRAIC(:,139) - ALGEBRAIC(:,141);
    ALGEBRAIC(:,124) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,62).*ALGEBRAIC(:,57));
    ALGEBRAIC(:,94) = CONSTANTS(:,116)+STATES(:,48);
    ALGEBRAIC(:,128) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,69).*ALGEBRAIC(:,94));
    ALGEBRAIC(:,142) =  CONSTANTS(:,28).*(exp((ALGEBRAIC(:,124)+ALGEBRAIC(:,138))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,128)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,47) =  - ALGEBRAIC(:,142);
    ALGEBRAIC(:,107) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,58).*ALGEBRAIC(:,45));
    ALGEBRAIC(:,132) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,48).*ALGEBRAIC(:,23));
    ALGEBRAIC(:,98) = CONSTANTS(:,111)+STATES(:,50);
    ALGEBRAIC(:,134) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,70).*ALGEBRAIC(:,98));
    ALGEBRAIC(:,143) =  CONSTANTS(:,29).*(exp(ALGEBRAIC(:,117)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,132)+ALGEBRAIC(:,134)+ALGEBRAIC(:,107))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,42) = ALGEBRAIC(:,143);
    RATES(:,45) = ALGEBRAIC(:,140) - ALGEBRAIC(:,143);
    ALGEBRAIC(:,120) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,60).*ALGEBRAIC(:,51));
    ALGEBRAIC(:,144) =  CONSTANTS(:,30).*(exp(ALGEBRAIC(:,128)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,132)+ALGEBRAIC(:,134)+ALGEBRAIC(:,120))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,46) = ALGEBRAIC(:,144);
    RATES(:,48) = ALGEBRAIC(:,142) - ALGEBRAIC(:,144);
    ALGEBRAIC(:,102) = CONSTANTS(:,112)+STATES(:,51);
    ALGEBRAIC(:,136) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,71).*ALGEBRAIC(:,102));
    ALGEBRAIC(:,145) =  CONSTANTS(:,31).*(exp(ALGEBRAIC(:,132)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,136)+ALGEBRAIC(:,138))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,49) = (ALGEBRAIC(:,143)+ALGEBRAIC(:,144)) - ALGEBRAIC(:,145);
    RATES(:,52) = ( - ALGEBRAIC(:,140) - ALGEBRAIC(:,142))+ALGEBRAIC(:,145);
    ALGEBRAIC(:,111) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,59).*ALGEBRAIC(:,48));
    ALGEBRAIC(:,146) =  CONSTANTS(:,32).*(exp((ALGEBRAIC(:,136)+ALGEBRAIC(:,134))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,111)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    RATES(:,43) = ALGEBRAIC(:,146);
    RATES(:,50) = (ALGEBRAIC(:,143)+ALGEBRAIC(:,144)) - ALGEBRAIC(:,146);
    RATES(:,51) = ALGEBRAIC(:,145) - ALGEBRAIC(:,146);
   RATES = RATES';
end

% Calculate algebraic variables
function ALGEBRAIC = computeAlgebraic(ALGEBRAIC, CONSTANTS, STATES, VOI,p)
    statesSize = size(STATES);
    statesColumnCount = statesSize(2);
    if ( statesColumnCount == 1)
        STATES = STATES';
        utilOnes = 1;
    else
        statesRowCount = statesSize(1);
        utilOnes = ones(statesRowCount, 1);
    end
    ALGEBRAIC(:,27) = CONSTANTS(:,98)+STATES(:,20)+STATES(:,31);
    ALGEBRAIC(:,47) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,52).*ALGEBRAIC(:,27));
    ALGEBRAIC(:,28) = CONSTANTS(:,99)+STATES(:,21)+STATES(:,32);
    ALGEBRAIC(:,50) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,53).*ALGEBRAIC(:,28));
    ALGEBRAIC(:,32) = CONSTANTS(:,101)+STATES(:,23)+STATES(:,33);
    ALGEBRAIC(:,56) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,55).*ALGEBRAIC(:,32));
    ALGEBRAIC(:,64) =  CONSTANTS(:,13).*exp((ALGEBRAIC(:,47)+ALGEBRAIC(:,50))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,56)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    m = p.stimmag(1)/p.trAMP(1);
    ALGEBRAIC(:,1) = piecewise({VOI<p.stimstart(1)&VOI>p.stimstart(1) - p.trAMP(1), p.stimholding(1)+ m.*((VOI - p.stimstart(1))+p.trAMP(1)) , VOI>=p.stimstart(1)&VOI<p.stimstart(1)+p.stimdur(1), p.stimmag(1)+p.stimholding(1) , VOI<p.stimstart(1)+p.trAMP(1)+p.stimdur(1)&VOI>=p.stimstart(1)+p.stimdur(1), p.stimholding(1)+  - m.*(((VOI - p.stimstart(1)) - p.trAMP(1)) - p.stimdur(1)) }, p.stimholding(1));
    ALGEBRAIC(:,25) = ALGEBRAIC(:,1)+STATES(:,19);
    ALGEBRAIC(:,40) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,51).*ALGEBRAIC(:,25));
    ALGEBRAIC(:,34) = CONSTANTS(:,102)+STATES(:,24)+STATES(:,36);
    ALGEBRAIC(:,59) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,56).*ALGEBRAIC(:,34));
    ALGEBRAIC(:,72) =  CONSTANTS(:,14).*exp((ALGEBRAIC(:,56)+ALGEBRAIC(:,40))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,59)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    ALGEBRAIC(:,30) = CONSTANTS(:,100)+STATES(:,22)+STATES(:,35);
    ALGEBRAIC(:,53) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,54).*ALGEBRAIC(:,30));
    ALGEBRAIC(:,76) =  CONSTANTS(:,15).*exp((ALGEBRAIC(:,53)+ALGEBRAIC(:,50))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,59)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    ALGEBRAIC(:,80) =  CONSTANTS(:,16).*exp((ALGEBRAIC(:,47)+ALGEBRAIC(:,40))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,53)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    ALGEBRAIC(:,45) = CONSTANTS(:,103)+STATES(:,26)+STATES(:,42);
    ALGEBRAIC(:,73) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,58).*ALGEBRAIC(:,45));
    ALGEBRAIC(:,48) = CONSTANTS(:,104)+STATES(:,27)+STATES(:,43);
    ALGEBRAIC(:,77) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,59).*ALGEBRAIC(:,48));
    ALGEBRAIC(:,54) = CONSTANTS(:,106)+STATES(:,29)+STATES(:,44);
    ALGEBRAIC(:,85) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,61).*ALGEBRAIC(:,54));
    ALGEBRAIC(:,92) =  CONSTANTS(:,17).*exp((ALGEBRAIC(:,73)+ALGEBRAIC(:,77))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,85)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    m = p.stimmag(2)/p.trAMP(2);
    ALGEBRAIC(:,2) = piecewise({VOI<p.stimstart(2)&VOI>p.stimstart(2) - p.trAMP(2), p.stimholding(2)+ m.*((VOI - p.stimstart(2))+p.trAMP(2)) , VOI>=p.stimstart(2)&VOI<p.stimstart(2)+p.stimdur(2), p.stimmag(2)+p.stimholding(2) , VOI<p.stimstart(2)+p.trAMP(2)+p.stimdur(2)&VOI>=p.stimstart(2)+p.stimdur(2), p.stimholding(2)+  - m.*(((VOI - p.stimstart(2)) - p.trAMP(2)) - p.stimdur(2)) }, p.stimholding(2));
    ALGEBRAIC(:,38) = ALGEBRAIC(:,2)+STATES(:,25);
    ALGEBRAIC(:,65) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,57).*ALGEBRAIC(:,38));
    ALGEBRAIC(:,57) = CONSTANTS(:,107)+STATES(:,30)+STATES(:,47);
    ALGEBRAIC(:,89) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,62).*ALGEBRAIC(:,57));
    ALGEBRAIC(:,96) =  CONSTANTS(:,18).*exp((ALGEBRAIC(:,85)+ALGEBRAIC(:,65))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,89)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    ALGEBRAIC(:,51) = CONSTANTS(:,105)+STATES(:,28)+STATES(:,46);
    ALGEBRAIC(:,81) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,60).*ALGEBRAIC(:,51));
    ALGEBRAIC(:,100) =  CONSTANTS(:,19).*exp((ALGEBRAIC(:,81)+ALGEBRAIC(:,77))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,89)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    ALGEBRAIC(:,3) = CONSTANTS(:,80)+STATES(:,1);
    ALGEBRAIC(:,29) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,33).*ALGEBRAIC(:,3));
    ALGEBRAIC(:,5) = CONSTANTS(:,81)+STATES(:,3);
    ALGEBRAIC(:,33) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,35).*ALGEBRAIC(:,5));
    ALGEBRAIC(:,6) = CONSTANTS(:,83)+STATES(:,4);
    ALGEBRAIC(:,35) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,36).*ALGEBRAIC(:,6));
    ALGEBRAIC(:,99) =  CONSTANTS(:,1).*(exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,29))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,35)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,4) = CONSTANTS(:,82)+STATES(:,2);
    ALGEBRAIC(:,31) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,34).*ALGEBRAIC(:,4));
    ALGEBRAIC(:,26) = CONSTANTS(:,97)+STATES(:,18);
    ALGEBRAIC(:,95) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,50).*ALGEBRAIC(:,26));
    ALGEBRAIC(:,104) =  CONSTANTS(:,2).*(exp(ALGEBRAIC(:,35)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,31)+ALGEBRAIC(:,95))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,105) =  CONSTANTS(:,20).*exp((ALGEBRAIC(:,73)+ALGEBRAIC(:,65))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,81)./( CONSTANTS(:,117).*CONSTANTS(:,118)));
    ALGEBRAIC(:,7) = CONSTANTS(:,88)+STATES(:,5);
    ALGEBRAIC(:,39) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,37).*ALGEBRAIC(:,7));
    ALGEBRAIC(:,8) = CONSTANTS(:,89)+STATES(:,6);
    ALGEBRAIC(:,46) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,38).*ALGEBRAIC(:,8));
    ALGEBRAIC(:,109) =  CONSTANTS(:,3).*(exp((ALGEBRAIC(:,39)+ALGEBRAIC(:,29))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,46)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,112) =  CONSTANTS(:,4).*(exp(ALGEBRAIC(:,46)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,39)+ALGEBRAIC(:,31)+ALGEBRAIC(:,95))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,9) = CONSTANTS(:,85)+STATES(:,7);
    ALGEBRAIC(:,49) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,39).*ALGEBRAIC(:,9));
    ALGEBRAIC(:,10) = CONSTANTS(:,86)+STATES(:,8);
    ALGEBRAIC(:,52) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,40).*ALGEBRAIC(:,10));
    ALGEBRAIC(:,115) =  CONSTANTS(:,5).*(exp((ALGEBRAIC(:,49)+ALGEBRAIC(:,29))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,52)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,118) =  CONSTANTS(:,6).*(exp(ALGEBRAIC(:,52)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,49)+ALGEBRAIC(:,31)+ALGEBRAIC(:,95))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,11) = CONSTANTS(:,90)+STATES(:,9);
    ALGEBRAIC(:,55) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,41).*ALGEBRAIC(:,11));
    ALGEBRAIC(:,14) = CONSTANTS(:,92)+STATES(:,10);
    ALGEBRAIC(:,58) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,42).*ALGEBRAIC(:,14));
    ALGEBRAIC(:,121) =  CONSTANTS(:,7).*(exp((ALGEBRAIC(:,55)+ALGEBRAIC(:,31))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,58)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,20) = CONSTANTS(:,87)+STATES(:,14)+STATES(:,38);
    ALGEBRAIC(:,79) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,46).*ALGEBRAIC(:,20));
    ALGEBRAIC(:,122) =  CONSTANTS(:,10).*(exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,79))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,39)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,21) = CONSTANTS(:,84)+STATES(:,15);
    ALGEBRAIC(:,84) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,47).*ALGEBRAIC(:,21));
    ALGEBRAIC(:,126) =  CONSTANTS(:,11).*(exp((ALGEBRAIC(:,84)+ALGEBRAIC(:,33))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,49)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,15) = CONSTANTS(:,94)+STATES(:,11);
    ALGEBRAIC(:,63) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,43).*ALGEBRAIC(:,15));
    ALGEBRAIC(:,125) =  CONSTANTS(:,8).*(exp(ALGEBRAIC(:,58)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,55)+ALGEBRAIC(:,63))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,23) = CONSTANTS(:,95)+STATES(:,16)+STATES(:,49);
    ALGEBRAIC(:,88) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,48).*ALGEBRAIC(:,23));
    ALGEBRAIC(:,24) = CONSTANTS(:,96)+STATES(:,17);
    ALGEBRAIC(:,91) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,49).*ALGEBRAIC(:,24));
    ALGEBRAIC(:,130) =  CONSTANTS(:,12).*(exp((ALGEBRAIC(:,33)+ALGEBRAIC(:,88))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,91)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,19) = CONSTANTS(:,91)+STATES(:,13);
    ALGEBRAIC(:,75) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,45).*ALGEBRAIC(:,19));
    ALGEBRAIC(:,18) = CONSTANTS(:,93)+STATES(:,12);
    ALGEBRAIC(:,71) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,44).*ALGEBRAIC(:,18));
    ALGEBRAIC(:,129) =  CONSTANTS(:,9).*(exp((ALGEBRAIC(:,55)+ALGEBRAIC(:,71))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,75)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,97) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,55).*ALGEBRAIC(:,32));
    ALGEBRAIC(:,62) = CONSTANTS(:,113)+STATES(:,34);
    ALGEBRAIC(:,101) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,63).*ALGEBRAIC(:,62));
    ALGEBRAIC(:,83) = CONSTANTS(:,110)+STATES(:,41)+STATES(:,52);
    ALGEBRAIC(:,127) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,67).*ALGEBRAIC(:,83));
    ALGEBRAIC(:,131) =  CONSTANTS(:,21).*(exp((ALGEBRAIC(:,97)+ALGEBRAIC(:,127))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,101)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,110) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,56).*ALGEBRAIC(:,34));
    ALGEBRAIC(:,70) = CONSTANTS(:,114)+STATES(:,37);
    ALGEBRAIC(:,113) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,64).*ALGEBRAIC(:,70));
    ALGEBRAIC(:,133) =  CONSTANTS(:,22).*(exp((ALGEBRAIC(:,110)+ALGEBRAIC(:,127))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,113)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,90) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,52).*ALGEBRAIC(:,27));
    ALGEBRAIC(:,116) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,46).*ALGEBRAIC(:,20));
    ALGEBRAIC(:,74) = CONSTANTS(:,108)+STATES(:,39);
    ALGEBRAIC(:,119) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,65).*ALGEBRAIC(:,74));
    ALGEBRAIC(:,135) =  CONSTANTS(:,23).*(exp(ALGEBRAIC(:,101)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,116)+ALGEBRAIC(:,119)+ALGEBRAIC(:,90))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,106) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,54).*ALGEBRAIC(:,30));
    ALGEBRAIC(:,137) =  CONSTANTS(:,24).*(exp(ALGEBRAIC(:,113)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,116)+ALGEBRAIC(:,119)+ALGEBRAIC(:,106))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,78) = CONSTANTS(:,109)+STATES(:,40);
    ALGEBRAIC(:,123) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,66).*ALGEBRAIC(:,78));
    ALGEBRAIC(:,139) =  CONSTANTS(:,25).*(exp(ALGEBRAIC(:,116)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,123)+ALGEBRAIC(:,127))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,114) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,61).*ALGEBRAIC(:,54));
    ALGEBRAIC(:,87) = CONSTANTS(:,115)+STATES(:,45);
    ALGEBRAIC(:,117) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,68).*ALGEBRAIC(:,87));
    ALGEBRAIC(:,138) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,67).*ALGEBRAIC(:,83));
    ALGEBRAIC(:,140) =  CONSTANTS(:,27).*(exp((ALGEBRAIC(:,114)+ALGEBRAIC(:,138))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,117)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,93) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,53).*ALGEBRAIC(:,28));
    ALGEBRAIC(:,141) =  CONSTANTS(:,26).*(exp((ALGEBRAIC(:,123)+ALGEBRAIC(:,119))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,93)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,124) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,62).*ALGEBRAIC(:,57));
    ALGEBRAIC(:,94) = CONSTANTS(:,116)+STATES(:,48);
    ALGEBRAIC(:,128) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,69).*ALGEBRAIC(:,94));
    ALGEBRAIC(:,142) =  CONSTANTS(:,28).*(exp((ALGEBRAIC(:,124)+ALGEBRAIC(:,138))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,128)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,107) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,58).*ALGEBRAIC(:,45));
    ALGEBRAIC(:,132) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,48).*ALGEBRAIC(:,23));
    ALGEBRAIC(:,98) = CONSTANTS(:,111)+STATES(:,50);
    ALGEBRAIC(:,134) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,70).*ALGEBRAIC(:,98));
    ALGEBRAIC(:,143) =  CONSTANTS(:,29).*(exp(ALGEBRAIC(:,117)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,132)+ALGEBRAIC(:,134)+ALGEBRAIC(:,107))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,120) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,60).*ALGEBRAIC(:,51));
    ALGEBRAIC(:,144) =  CONSTANTS(:,30).*(exp(ALGEBRAIC(:,128)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,132)+ALGEBRAIC(:,134)+ALGEBRAIC(:,120))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,102) = CONSTANTS(:,112)+STATES(:,51);
    ALGEBRAIC(:,136) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,71).*ALGEBRAIC(:,102));
    ALGEBRAIC(:,145) =  CONSTANTS(:,31).*(exp(ALGEBRAIC(:,132)./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp((ALGEBRAIC(:,136)+ALGEBRAIC(:,138))./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,111) =  CONSTANTS(:,117).*CONSTANTS(:,118).*log( CONSTANTS(:,59).*ALGEBRAIC(:,48));
    ALGEBRAIC(:,146) =  CONSTANTS(:,32).*(exp((ALGEBRAIC(:,136)+ALGEBRAIC(:,134))./( CONSTANTS(:,117).*CONSTANTS(:,118))) - exp(ALGEBRAIC(:,111)./( CONSTANTS(:,117).*CONSTANTS(:,118))));
    ALGEBRAIC(:,12) = ALGEBRAIC(:,3)+ALGEBRAIC(:,6)+ALGEBRAIC(:,10)+ALGEBRAIC(:,8);
    ALGEBRAIC(:,13) = ALGEBRAIC(:,5)+ALGEBRAIC(:,6)+ALGEBRAIC(:,9)+ALGEBRAIC(:,10)+ALGEBRAIC(:,7)+ALGEBRAIC(:,8);
    ALGEBRAIC(:,16) = ALGEBRAIC(:,4)+ALGEBRAIC(:,14)+STATES(:,11);
    ALGEBRAIC(:,17) = ALGEBRAIC(:,4)+ALGEBRAIC(:,14)+ALGEBRAIC(:,15)+ALGEBRAIC(:,3)+ALGEBRAIC(:,6)+ALGEBRAIC(:,8)+ALGEBRAIC(:,10);
    ALGEBRAIC(:,22) = ALGEBRAIC(:,20)+ALGEBRAIC(:,7)+ALGEBRAIC(:,8);
    ALGEBRAIC(:,36) = ALGEBRAIC(:,25)+ALGEBRAIC(:,34)+ALGEBRAIC(:,30);
    ALGEBRAIC(:,37) = ALGEBRAIC(:,27)+ALGEBRAIC(:,32)+ALGEBRAIC(:,30)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,41) = ALGEBRAIC(:,25)+ALGEBRAIC(:,30)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,42) = ALGEBRAIC(:,27)+ALGEBRAIC(:,30)+ALGEBRAIC(:,32)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,43) = ALGEBRAIC(:,28)+ALGEBRAIC(:,32)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,44) = ALGEBRAIC(:,27)+ALGEBRAIC(:,32)+ALGEBRAIC(:,30)+ALGEBRAIC(:,34);
    ALGEBRAIC(:,60) = ALGEBRAIC(:,38)+ALGEBRAIC(:,57)+ALGEBRAIC(:,51);
    ALGEBRAIC(:,61) = ALGEBRAIC(:,45)+ALGEBRAIC(:,54)+ALGEBRAIC(:,51)+ALGEBRAIC(:,57);
    ALGEBRAIC(:,66) = ALGEBRAIC(:,38)+ALGEBRAIC(:,51)+ALGEBRAIC(:,57);
    ALGEBRAIC(:,67) = ALGEBRAIC(:,45)+ALGEBRAIC(:,51)+ALGEBRAIC(:,54)+ALGEBRAIC(:,57);
    ALGEBRAIC(:,68) = ALGEBRAIC(:,48)+ALGEBRAIC(:,54)+ALGEBRAIC(:,57);
    ALGEBRAIC(:,69) = ALGEBRAIC(:,45)+ALGEBRAIC(:,54)+ALGEBRAIC(:,51)+ALGEBRAIC(:,57);
    ALGEBRAIC(:,82) = ALGEBRAIC(:,28)+ALGEBRAIC(:,32)+ALGEBRAIC(:,34)+ALGEBRAIC(:,62)+ALGEBRAIC(:,70)+ALGEBRAIC(:,20)+ALGEBRAIC(:,78);
    ALGEBRAIC(:,86) = ALGEBRAIC(:,28)+ALGEBRAIC(:,32)+ALGEBRAIC(:,34)+ALGEBRAIC(:,20)+ALGEBRAIC(:,78);
    ALGEBRAIC(:,103) = ALGEBRAIC(:,48)+ALGEBRAIC(:,54)+ALGEBRAIC(:,57)+ALGEBRAIC(:,87)+ALGEBRAIC(:,94)+ALGEBRAIC(:,23)+ALGEBRAIC(:,102);
    ALGEBRAIC(:,108) = ALGEBRAIC(:,48)+ALGEBRAIC(:,54)+ALGEBRAIC(:,57)+ALGEBRAIC(:,23)+ALGEBRAIC(:,102);
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
    req_length = 60;
    insize = size(strin,2);
    if insize > req_length
        strout = strin(1:req_length);
    else
        strout = [strin, blanks(req_length - insize)];
    end
end

