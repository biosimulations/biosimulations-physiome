% Simulating mechano-energetics of isometric and work-loops contractions
% This code reproduces the simulation Figures in the JPhysiol paper:
% Experimental and modelling evidence of shortening heat in cardiac muscle
% Kenneth Tran
% August 2017 

% Each set of workloops at a given preload takes approx 100s
% on a laptop (i7 6650U CPU @2.20 GHZ)

%%
clear;
tic 
% SL for isometric contractions
preload_SL_iso = [1.635 1.935 2.035 2.11 2.175 2.23 2.3];

Afterload = [1]; % Not used in isometric simulations - a dummy value
kxb = 72; % Scaling constant to scale normalised force to units of kPa
G_ATP = -58; % Free energy of ATP hydrolysis (kJ/mol)
passive = 1; % Passive present = 1; Passive absent = 0;

% Set the twitch protocol
protocol = 'Isometric';
    
% Creating matrices for storing variables from ISOMETRIC contractions
p = 800;
Force_iso_vec = nan*ones(p, length(preload_SL_iso));
T_iso_vec = nan*ones(p, length(preload_SL_iso));
ATP_iso_vec = nan*ones(p, length(preload_SL_iso));
SL_iso_vec = nan*ones(p, length(preload_SL_iso));

for i=1:length(preload_SL_iso)

    loop = 0; % No-loop simulation
    T_loop = [2000 2000]; % Not used in non-loop simulations - these are dummy values
    [T_iso Y_iso dy_iso F_total_iso ATPase_iso] = XBSolve(loop,T_loop,preload_SL_iso(i),Afterload(1),protocol,passive);
    SL_iso = Y_iso(:,9);

    % Storing the vectors
    T_iso_vec(1:length(T_iso),i) = T_iso;
    Force_iso_vec(1:length(F_total_iso),i) = kxb*F_total_iso;
    SL_iso_vec(1:length(SL_iso),i) = SL_iso;
    ATP_iso_vec(1:length(ATPase_iso),i) = ATPase_iso;

    % Finding the index for t<800ms to avoid numerical spike at end
    j = 0;
    find = 1;
    while(find)
        j = j+1;
        if (T_iso(j)>800)
            find = 0;
        end
    end

    % Integrating to compute total ATP consumed in a twitch
    ATPase_iso_per_beat(i) = trapz(T_iso(1:j), ATPase_iso(1:j));
    
    % Isometric twitch Peak Force
    % Maximum Peak Force (i.e. PF for SL = 2.3) is used to normalise afterloads and stresses
    PF(i) = max(F_total_iso);
    
end

% Total enthalpy 
enthalpy_IS = -ATPase_iso_per_beat*G_ATP;

% Max enthalpy - used to normalise energy outputs
ME = max(enthalpy_IS); 

disp('Isometric simulations completed.');

%% Workloop contractions

% String for naming the initial preloads for the workloop contractions
SL_string = {'SL1935','SL2035','SL211','SL2175','SL223','SL23'};

% Peak isometric force for each preload
% Used to scale the work-loop afterloads
SL_PF = [0.1624,0.2873,0.4131,0.5422,0.6640,0.8353];

% Initial preloads for the workloop contractions
preload_SL = [1.935 2.035 2.11 2.175 2.23 2.3];

% Normalised afterloads for work-loop contractions
% Note its multiplication by SL_PF when it is used in the code
Afterload = [0.2 0.35 0.5 0.65 0.8 1]; 

kxb = 72; % Scaling constant to scale normalised force to units of kPa
G_ATP = -58; % Free energy of ATP hydrolysis (kJ/mol)

% Creating vectors for storing variables for WORKLOOP contractions
p = 800;
T_vec = nan*ones(p, length(Afterload));
Force_vec = nan*ones(p, length(Afterload));
SL_vec = nan*ones(p, length(Afterload));
ATP_vec = nan*ones(p, length(Afterload));

% Set the contraction protocol
protocol = 'Workloop';

for k=1:length(SL_string)
    for i=1:length(Afterload)

        loop = 0; % No-loop simulation
        T_loop = [2000 2000]; % Not used in non-loop simulations - these are dummy values
        [T_noL Y_noL dy_noL F_total_noL ATPase_noL] = XBSolve(loop,T_loop,preload_SL(k),SL_PF(k)*Afterload(i),protocol,passive);
        SL_noL = Y_noL(:,9);

        % Find the minimum SL (SL_min) from the above simulation
        % This is used to hold the SL fixed at SL_min until T = 900
        [Y I] = min(SL_noL);
        T_start = T_noL(I);
        T_stop = 900;
        T_loop = [T_start T_stop]; %Used to set start and end time for relaxation phase

        loop = 1; % Simulation with loop
        [T_L Y_L dy_L F_total_L ATPase_L] = XBSolve(loop,T_loop,preload_SL(k),SL_PF(k)*Afterload(i),protocol,passive);
        SL_L = Y_L(:,9);

        % Restretch phase
        SL_WL(i) = SL_L(end); % SL at end of workloop
        n = 20;
        T_stretch = linspace(901,1000,n);
        SL_stretch = linspace(SL_WL(i),preload_SL(k),n);
        for j=1:length(SL_stretch)
            Force_stretch(j) = passiveForces(SL_stretch(j),passive);
        end

        % Storing the vectors
        T_vec(1:length(T_L),i) = T_L;
        T_vec(length(T_L)+1:length(T_L)+20,i)= T_stretch;
        Force_vec(1:length(F_total_L),i) = kxb*F_total_L;
        Force_vec(length(F_total_L)+1:length(F_total_L)+20,i) = kxb*Force_stretch;
        SL_vec(1:length(SL_L),i) = SL_L;
        SL_vec(length(SL_L)+1:length(SL_L)+20,i) = SL_stretch;
        ATP_vec(1:length(ATPase_L),i) = ATPase_L;

        % Finding the index for t<800ms to avoid numerical spike at end
        j = 0;
        find = 1;
        while(find)
            j = j+1;
            if (T_L(j)>800)
                find = 0;
            end
        end

        % Integrating to calculate total ATP consumption and work done
        ATPase_per_beat(i) = trapz(T_L(1:j), ATPase_L(1:j));
        Work(i) = trapz([SL_L;SL_stretch']/max(preload_SL(k)),kxb*[F_total_L Force_stretch]);

    end

    enthalpy_WL = -ATPase_per_beat*G_ATP;
    work = -Work;  % Work is negative for contraction
    heat_WL = enthalpy_WL - work;  
    
    % Interpolate the isometric enthalpy-stress curve at equivalent 
    % afterloads in the work-loop curve
    enthalpy_IS_interp = interp1(PF/max(PF),enthalpy_IS,SL_PF(k)*Afterload/max(PF));
    SH = heat_WL - enthalpy_IS_interp;
    SH(end) = 0;

    % Outputting the data
    eval([SL_string{k},'_T_vec = T_vec;']);
    eval([SL_string{k},'_SL_vec = SL_vec;']);
    eval([SL_string{k},'_Force_vec = Force_vec;']);
    eval([SL_string{k},'_AF = SL_PF(k)*Afterload;']);
    eval([SL_string{k},'_enthalpy_IS = enthalpy_IS;']);
    eval([SL_string{k},'_enthalpy_WL = enthalpy_WL;']);
    eval([SL_string{k},'_work = work;']);
    eval([SL_string{k},'_ATP_vec = ATP_vec;']);
    eval([SL_string{k},'_heat_WL = heat_WL;']);
    eval([SL_string{k},'_enthalpy_IS_interp = enthalpy_IS_interp;']);
    eval([SL_string{k},'_SH = SH;']);

    disp([SL_string{k},' work-loops completed.']);
end

% Run the PlotFigures.m script to generate figures from this simulation
toc

