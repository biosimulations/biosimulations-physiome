% find bond-graph parameters whole whole cell with multiple modules
% present:
%  {'cAMP','LRGbinding_B1AR','LRGbinding_M2','GsProtein','GiProtein'}

% based on Pan cardiac AP 2018 code

% find kf and kr through a single file that accounts for potential closed
% loops in the new composite model

clear;
clc;
close all;

%% Set directories
current_dir = cd;
Idx_backslash = find(current_dir == filesep);
parent_dir = current_dir(1:Idx_backslash(end-1));
main_dir = current_dir(1:Idx_backslash(end));
output_dir = [current_dir filesep 'output' filesep];

%% Define constants
R = 8.314; % unit J/mol/K
T = 310;
F = 96485;

N_A = 6.022e23;

combined_kinetic_parameters = false; % all listed modules must be present
noLRG = false;


%% Define volumes (unit pL)
V_myo = 34.4;
V_e = 5.182;     % external volume
V_SR = V_myo*0.035; % SR volume
V_di = V_myo*0.0539; % diadic volume
V = struct();
V.V_myo = V_myo;
V.V_SR = V_SR;
V.V_di = V_di;
V.V_e = V_e;

%% Load stoichiometric matrices and kinetic rate constants
if false
    % order of modules is not guaranteed
    d = dir(main_dir);
    isub = [d(:).isdir]; %# returns logical vector
    array_names = {d(isub).name}';
    array_names(ismember(array_names,{'.','..','.git','MATLAB','units_and_constants'})) = [];
    disp('Modules are:');
    disp(array_names);
else
    array_names = {'cAMP',...
        'LRGbinding_B1AR','LRGbinding_M2',...
        'GsProtein','GiProtein'}; % excluding B1AR module (which only contains BARK and PKA action)
    if noLRG
        array_names = {'cAMP',...
        'GsProtein','GiProtein'};
    end
    if false % Gs and LRG_B1 only
        array_names = {'LRGbinding_B1AR','GsProtein'}; 
    end
    if false % Gi and LRG_M2 only
        array_names = {'LRGbinding_B1AR','LRGbinding_M2','GsProtein','GiProtein'}; 
        array_names = {'LRGbinding_M2','GiProtein'}; 
    end
end

num_subsystems = length(array_names);
sys_struct = cell(num_subsystems,1);
rxnIDs = {};
Knames = {};
Kname_modules = struct();
for i_system = 1:num_subsystems
    sys_name = array_names{i_system};
    sys_struct{i_system}.name = sys_name;
    sys_dir = [main_dir sys_name '\parameter_finder\'];
    cd(sys_dir)
    forward_mat_path = ['data\all_forward_matrix.txt'];
    reverse_mat_path = ['data\all_reverse_matrix.txt'];
    N_f = load_matrix(forward_mat_path);
    N_r = load_matrix(reverse_mat_path);
    sys_struct{i_system}.N_f = N_f;
    sys_struct{i_system}.N_r = N_r;
    
%     disp(array_names{i_system});
    dims = struct();
    dims.num_rows = size(N_f,1);
    dims.num_cols = size(N_f,2);
    I = eye(dims.num_cols);
    M = [I transpose(N_f); I transpose(N_r)];
    if ~combined_kinetic_parameters
        [k_kinetic, N_cT, K_C, W] = kinetic_parameters(M, true, dims, V);
        sys_struct{i_system}.kfkr = k_kinetic;
        sys_struct{i_system}.Kc = K_C;
        sys_struct{i_system}.N_cT = N_cT;
    end
%         sys_struct{i_system}.W = W(dims.num_cols+1:end);
    fID = fopen('data\rxnID.txt', 'r');
    rxnID = textscan(fID,'%s', 'delimiter','\n');
    fclose(fID);
    rxnIDs = [rxnIDs; rxnID{1}];
    sys_struct{i_system}.rxnID = rxnID{1};

    fID = fopen('data\Kname.txt', 'r');
    Kname = textscan(fID,'%s', 'delimiter','\n');
    fclose(fID);
    Knames = [Knames; Kname{1}]; 
    sys_struct{i_system}.Kname = Kname{1};
end

Kunique = {};
for ik=1:length(Knames)
    if ~any(strcmp(Kunique,Knames{ik}))
        Kunique = [Kunique; Knames{ik}];
    end
end

cd(current_dir)

% relations between submodule to whole module
% {{'cAMP','LRGbinding_B1AR','LRGbinding_M2','GsProtein','GiProtein'}}
for j = 1:length(array_names)
    ids = [];
    for id = 1:length(sys_struct{j}.Kname)
        ids = [ids, find(strcmp(Kunique, sys_struct{j}.Kname{id}))];
    end
    sys_struct{j}.I_vec = ids;
end
% sys_struct{1}.I_vec = 1:18;           % cAMP
% sys_struct{2}.I_vec = 19:24;          % LRGbinding_B1AR
% sys_struct{3}.I_vec = 25:30;          % LRGbinding_M2
% sys_struct{4}.I_vec = [20 21 23 22 24 14 31:33];     % GsProtein
% sys_struct{5}.I_vec = [26 27 29 28 30 16 34 35 33];  % GiProtein  

num_rows = max(sys_struct{size(sys_struct,1)}.I_vec);

N_f = [];
N_r = [];

for i_system = 1:num_subsystems
    disp(array_names{i_system});
    T = calcT(sys_struct{i_system}.I_vec,num_rows);

    sys_struct{i_system}.T = T;
    
    N_f = [N_f T*sys_struct{i_system}.N_f];
    N_r = [N_r T*sys_struct{i_system}.N_r];
end

N_fT = transpose(N_f);
N_rT = transpose(N_r);

N = N_r - N_f;
N_T = N_rT - N_fT;

num_cols = size(N,2);
I = eye(num_cols);

M = [I N_fT; I N_rT];
M_rref = rref(M);

%% Set up the vectors for kinetic rate constants
%  {'cAMP','LRGbinding_B1AR','LRGbinding_M2','B1AR','GsProtein','GiProtein'}

kf = [];
kr = [];
W = ones(size(N,2),1);
if combined_kinetic_parameters
    [k_kinetic, N_cT, K_C, W] = grand_kinetic_parameters(M, true, dims, V, noLRG);
    sys_struct{i_system}.kfkr = k_kinetic;
    sys_struct{i_system}.Kc = K_C;
    sys_struct{i_system}.N_cT = N_cT;
    kf = k_kinetic(1:num_cols);
    kr = k_kinetic(num_cols+1:end);
else
    for i_system=1:num_subsystems
        nrx = length(sys_struct{i_system}.kfkr)/2;
        kf = [kf, sys_struct{i_system}.kfkr(1:nrx)'];
        kr = [kr, sys_struct{i_system}.kfkr(nrx+1:end)'];
    end
    k_kinetic = [kf, kr]';
end
W = [ones(size(N,2),1);V_myo*ones(num_rows,1)];

lambdaW = exp(pinv(M)*log(k_kinetic));
lambda = lambdaW./W;
kappa = lambda(1:size(N,2));
K = lambda(size(N,2)+1:end);

save([output_dir 'FCU_adenylylCyclase_BG_parameters.mat'],'kappa','K','k_kinetic');

%% Checks
N_rref = rref(N);
R_mat = null(N,'r');

k_est = exp(M*log(lambdaW));
diff = (k_kinetic - k_est)./k_kinetic;
error = sum(abs(diff));

K_eq = kf./kr;
if ~combined_kinetic_parameters
    K_eq = K_eq';
end
zero_est = R_mat'*(K_eq);
zero_est_log = R_mat'*log(K_eq);


%% print outputs
for ik=1:length(kappa)
    fprintf('var kappa_%s: fmol_per_sec {init: %g, pub: out};\n',rxnIDs{ik},kappa(ik));
end
for ik = 1:length(Kunique)
    fprintf('var K_%s: per_fmol {init: %g, pub: out};\n',Kunique{ik},K(ik));
end

% initialise struct for storing modules contributing to a given K
for ik=1:length(Kunique)
    Kname_modules.(Kunique{ik}) = {};
end
for i_system = 1:num_subsystems
    sys_name = array_names{i_system};
    modKname = sys_struct{i_system}.Kname;
    for ik=1:length(modKname)
        Kname_modules.(modKname{ik}) = [Kname_modules.(modKname{ik}), sys_name];
    end
end
%% write out CellML code
if true 
    cpath = main_dir(Idx_backslash(end-1):Idx_backslash(end));
    cellmlfilepath = [cpath(2:end-1) 'TEMP.cellml.txt'];
    cid = fopen(cellmlfilepath,'w');
    fwrite(cid, [sprintf('def model FCU_composite as\n def import using "units_and_constants/units_BG.cellml" for\n') ...
        ,sprintf('unit mM using unit mM;\nunit fmol using unit fmol;\nunit per_fmol using unit per_fmol;\n') ...
        ,sprintf('unit J_per_mol using unit J_per_mol;\nunit fmol_per_sec using unit fmol_per_sec;\n')...
        ,sprintf('unit C_per_mol using unit C_per_mol;\n  unit J_per_C using unit J_per_C;\n')...
        ,sprintf('unit microm3 using unit microm3;\n  unit fF using unit fF;\n')...
        ,sprintf('unit fC using unit fC;\n  unit fA using unit fA;\n')...
        ,sprintf('unit per_second using unit per_second;\n  unit millivolt using unit millivolt;\n')...
        ,sprintf('unit per_sec using unit per_sec;\n  unit J_per_K_per_mol using unit J_per_K_per_mol;\n')...
        ,sprintf('unit fmol_per_L using unit fmol_per_L;\n  unit fmol_per_L_per_sec using unit fmol_per_L_per_sec;\n')...
        ,sprintf('unit per_sec_per_fmol_per_L using unit per_sec_per_fmol_per_L;\n  unit uM using unit uM;\n')...
        ,sprintf('unit mM_per_sec using unit mM_per_sec;\n  unit uM_per_sec using unit uM_per_sec;\n')...
        ,sprintf('unit pL using unit pL;\n  unit m_to_u using unit m_to_u;\n enddef;\n')]);
    fwrite(cid,[sprintf('def import using "units_and_constants/constants_BG.cellml" for\n')...
        ,sprintf('comp constants using comp constants;\nenddef;\n\n')]);
    for im = 1:length(array_names)
        module = array_names{im};
        fwrite(cid,sprintf('def import using "%s/BG_%s.cellml" for\ncomp %s using comp %s;\nenddef;\n',module,module,module,module));
    end
    fwrite(cid,sprintf('\ndef comp BG_parameters as\n'));
    for ik=1:length(kappa)
        fwrite(cid,sprintf('var kappa_%s: fmol_per_sec {init: %g, pub: out};\n',rxnIDs{ik},kappa(ik)));
    end
    for ik = 1:length(Kunique)
        fwrite(cid,sprintf('var K_%s: per_fmol {init: %g, pub: out};\n',Kunique{ik},K(ik)));
    end
    fwrite(cid,sprintf('enddef;\n'));
    fwrite(cid,[sprintf('    def comp environment as\n')...
        ,sprintf('var time: second {pub: out};\n')...
        ,sprintf('var vol_myo: pL {init: 34.4, pub: out};\n')...
        ,sprintf('var freq: dimensionless {init: 500};\n')...
        ,sprintf('// stimulus\n')...
        ,sprintf('// ramp UP and ramp DOWN\n')...
        ,sprintf('var stimSt: second {init: 3.5e-4};\n')...
        ,sprintf('var stimSt2: second {init: 3e-4}; \n')...
        ,sprintf('var stimDur: second {init: 0.25e-4};  \n')...
        ,sprintf('var tR: second {init: 1.8e-4};\n')...
        ,sprintf('var stimMag: fmol {init: 1e1};\n')...
        ,sprintf('var stimHolding: fmol {init: 1e-5};   \n')...
        ,sprintf('var m: fmol_per_sec;  \n')...
        ,sprintf('m = stimMag/tR;   \n')...
        ,sprintf('q_L_B1_init = sel          \n')...
        ,sprintf('    case (time < stimSt) and (time > stimSt-tR):   \n')...
        ,sprintf('        stimHolding+m*(time-stimSt+tR);\n')...
        ,sprintf('    case (time >= stimSt) and (time < stimSt+stimDur): \n')...
        ,sprintf('        stimMag+stimHolding;   \n')...
        ,sprintf('    case (time < stimSt+tR+stimDur) and (time >= stimSt+stimDur):  \n')...
        ,sprintf('        stimHolding+-m*(time-stimSt-tR-stimDur);   \n')...
        ,sprintf('    otherwise:             \n')...
        ,sprintf('        stimHolding;       \n')...
        ,sprintf('endsel;                    \n')...
        ,sprintf('q_L_M2_init = sel          \n')...
        ,sprintf('    case (time < stimSt2) and (time > stimSt2-tR): \n')...
        ,sprintf('        stimHolding+m*(time-stimSt2+tR);   \n')...
        ,sprintf('    case (time >= stimSt2) and (time < stimSt2+stimDur):   \n')...
        ,sprintf('        stimMag+stimHolding;   \n')...
        ,sprintf('    case (time < stimSt2+tR+stimDur) and (time >= stimSt2+stimDur):\n')...
        ,sprintf('        stimHolding+-m*(time-stimSt2-tR-stimDur);  \n')...
        ,sprintf('    otherwise:             \n')...
        ,sprintf('        stimHolding;       \n')...
        ,sprintf('endsel;\n')]);
    for j=1:length(K)
        fwrite(cid,sprintf('var q_%s_init: fmol {init: 1e-888};\n',Kunique{j}));
    end
    fwrite(cid,sprintf('\n// Global value\n'));
    for j=1:length(K)
        fwrite(cid,sprintf('var q_%s: fmol {pub: out};\n',Kunique{j}));
    end
    for im = 1:length(array_names)
        module = array_names{im};
        modKname = sys_struct{im}.Kname;
        fwrite(cid,sprintf('\n// %s imports\n',module));
        for j=1:length(modKname)
            fwrite(cid,sprintf('var q_%s_m%s: fmol {pub: in};\n',modKname{j}, module));
        end
        fwrite(cid,newline);
    end
    fwrite(cid,newline);
    for j=1:length(Kunique)
        fwrite(cid,sprintf('q_%s = q_%s_init',Kunique{j},Kunique{j}));
        for imod=1:length(Kname_modules.(Kunique{j}))
            fwrite(cid,sprintf(' + q_%s_m%s ',Kunique{j},Kname_modules.(Kunique{j}){imod}));
        end
        fwrite(cid,sprintf(';\n'));
    end
    fwrite(cid,sprintf('enddef;\n'));

    if false % the below is for an individual module
        disp(newline)
        disp('// Input from global environment');
        for j=1:length(K)
            fprintf('var q_%s_global: fmol {pub: in};\n',Kunique{j});
        end
        disp('// Output to global environment');
        for j=1:length(K)
            fprintf('var q_%s: fmol {init: 1e-16, pub: out};\n',Kunique{j});
        end

        for j=1:length(K)
            fprintf('mu_%s = R*T*ln(K_%s*q_%s_global);\n',Kunique{j},Kunique{j},Kunique{j});
        end
    end
    fwrite(cid,newline);
    for im = 1:length(array_names)
        module = array_names{im};
        modKname = sys_struct{im}.Kname;

        fwrite(cid,sprintf('def map between environment and %s for\n',module));
        fwrite(cid,sprintf('vars time and time;\n'));
        for j=1:length(modKname)
            fwrite(cid,sprintf('vars q_%s_m%s and q_%s;\n',modKname{j}, module,modKname{j}));
            fwrite(cid,sprintf('vars q_%s and q_%s_global;\n',modKname{j}, modKname{j}));
        end
        fwrite(cid,sprintf('enddef;\n\n'));
    end
    
    for im = 1:length(array_names)
        module = array_names{im};
        modKname = sys_struct{im}.Kname;
        modrxnID = sys_struct{im}.rxnID;
        fwrite(cid,sprintf('def map between BG_parameters and %s for\n',module));
        for ik=1:length(modrxnID)
            fwrite(cid,sprintf('vars kappa_%s and kappa_%s;\n',modrxnID{ik},modrxnID{ik}));
        end
        for j=1:length(modKname)
            fwrite(cid,sprintf('vars K_%s and K_%s;\n',modKname{j}, modKname{j}));
        end
        fwrite(cid,sprintf('enddef;\n'));
    end
    fwrite(cid,newline);
    for im = 1:length(array_names)
        module = array_names{im};
        fwrite(cid,sprintf('def map between constants and %s for\n', module));
        fwrite(cid,sprintf('\tvars R and R;\n\tvars T and T;\nenddef;\n'));
    end
    
    fwrite(cid,sprintf('\nenddef;\n'));
    fclose(cid);
end

%% FUNCTION SCRIPTS
function matrix = load_matrix(stoich_path)
    stoich_file_id = fopen(stoich_path,'r');
    stoich_file_data = textscan(stoich_file_id,'%s','delimiter','\n');
    fclose(stoich_file_id);
    num_rows = length(stoich_file_data{1});
    num_cols = sum(stoich_file_data{1}{1} == ',')+1;
    matrix = zeros(num_rows,num_cols);
    for i_row = 1:num_rows
        line_str = stoich_file_data{1}{i_row};
        line_split = regexp(line_str,',','split');

        for i_col = 1:num_cols
            matrix(i_row,i_col) = str2double(line_split{i_col});
        end
    end
end


function T = calcT(I_vec,num_rows)
    num_cols = length(I_vec);
    T = zeros(num_rows,num_cols);
    for i = 1:num_cols
        T(I_vec(i),i) = 1;
    end
end
