% This script calculates the bond graph parameters for all reactions of the
% a given module. Specify the directory.
% based on SERCA model of Pan et al, which is based on Tran et al. (2009). 
% Parameters calculated in module's directory, by using the kinetic
% parameters and stoichiometric matrix.

% 19 Jul INITIAL CONDITIONS
% given dq/dt = A.q + c where A is a square matrix, use null(A) to find ICs
% of q. 
% A is constructed from linearising equations through lm, and
% contains BG parameters 
% K kappa are contained in c, but disregarding this
% as this is not dependent on q.

% return W from kinetic_parameters

clear;
clc;
close all;

%% booleans
write_parameters_file = true;
include_constraints = true;
include_type2_reactions = true;

%% Set directories
current_dir = pwd;
Idx_backslash = find(current_dir == filesep);
data_dir =  [current_dir filesep 'data' filesep];
output_dir = [current_dir filesep 'output' filesep];
modname = current_dir(Idx_backslash(end-1):Idx_backslash(end));
modname = modname(5:end-1);

if contains(current_dir, 'beta1') && false
    matstr = '_withR_LR_scheme4';
else
    matstr = '';
end

%% Define volumes
V_myo = 34.4; % pL
V = struct();
V.V_myo = V_myo;

%% Load forward matrix
if include_type2_reactions
    stoich_path = [data_dir sprintf('all_forward_matrix%s.txt',matstr)];
else
    stoich_path = [data_dir 'all_noType2_forward_matrix.txt'];
end
stoich_file_id = fopen(stoich_path,'r');

stoich_file_data = textscan(stoich_file_id,'%s','delimiter','\n');
fclose(stoich_file_id);

num_rows = length(stoich_file_data{1});
num_cols = sum(stoich_file_data{1}{1} == ',')+1;
dims = struct();
dims.num_cols = num_cols;
dims.num_rows = num_rows;

N_f = zeros(num_rows,num_cols);

for i_row = 1:num_rows
    line_str = stoich_file_data{1}{i_row};
    line_split = regexp(line_str,',','split');
    
    for i_col = 1:num_cols
        N_f(i_row,i_col) = str2double(line_split{i_col});
    end
end


%% Load reverse matrix
if include_type2_reactions
    stoich_path = [data_dir sprintf('all_reverse_matrix%s.txt',matstr)];
else
    stoich_path = [data_dir 'all_noType2_reverse_matrix.txt'];
end
stoich_file_id = fopen(stoich_path,'r');

stoich_file_data = textscan(stoich_file_id,'%s','delimiter','\n');
fclose(stoich_file_id);

num_rows = length(stoich_file_data{1}); % num of kappa + K
num_cols = sum(stoich_file_data{1}{1} == ',')+1; % num of reactions

N_r = zeros(num_rows,num_cols);

for i_row = 1:num_rows
    line_str = stoich_file_data{1}{i_row};
    line_split = regexp(line_str,',','split');
    
    for i_col = 1:num_cols
        N_r(i_row,i_col) = str2double(line_split{i_col});
    end
end

N_fT = transpose(N_f);
N_rT = transpose(N_r);

%% Calculate stoichiometric matrix
% I matrix to align with placement of kappa down the column.
% x-axis of stoich matrix (R1a, R1b etc) coincides with the kp km of that
% kinetic reaction
N = N_r - N_f;
N_T = N_rT - N_fT;

I = eye(num_cols);

M = [I N_fT; I N_rT];  

addpath(current_dir);
addpath(data_dir);
[k_kinetic, N_cT, K_C, W] = kinetic_parameters(M, include_type2_reactions, dims, V); %%%%%%%%%%%%%%%%
if ~include_constraints
    N_cT = [];
end

M = [M; N_cT];

% Calculate bond graph constants from kinetic parameters
% Note: units of kappa are fmol/s, units of K are fmol^-1
k = transpose([k_kinetic' K_C]);
lambdaW = exp(pinv(M) * log(k));

% Check that kinetic parameters are reproduced by bond graph parameters
k_sub = exp(M*log(lambdaW));
diff = (k - k_sub)./k;
error = sum(abs(diff));

% Check that there is a detailed balance constraint
Z = transpose(null(transpose(M),'r'));

N_rref = rref(N);
R_mat = null(N,'r');
kf = k_kinetic(1:num_cols);
kr = k_kinetic(num_cols+1:end);
K_eq = kf'./kr';
zero_est = R_mat'*(K_eq');
zero_est_log = R_mat'*log(K_eq');

if isempty(R_mat)
    warning('R_mat is empty: matrix is full rank');
end
%% Save bond graph parameters
lambda = lambdaW./W;
kappa = lambda(1:num_cols);
K = lambda(num_cols+1:end);

fID = fopen([data_dir 'rxnID.txt'], 'r');
rxnID = textscan(fID,'%s', 'delimiter','\n');
fclose(fID);
fID = fopen([data_dir 'Kname.txt'], 'r');
Kname = textscan(fID,'%s');
fclose(fID);

Knamed = struct();
for k = 1:length(Kname{1})
    % assign name to K values. store as struct for output in .mat.
    sname = Kname{1}{k};
    Knamed.(sname) = K(k);
end
kappa_named = struct();
for k = 1:length(rxnID{1})
    % assign name to K values. store as struct for output in .mat.
    sname = rxnID{1}{k};
    kappa_named.(['r' sname]) = kappa(k);
end



if write_parameters_file
    save([output_dir 'all_params.mat'],'kappa','K','k_kinetic', 'Knamed','kappa_named'); %
end

for j = 1:length(kappa)
    fprintf('var kappa_%s: fmol_per_sec {init: %g, pub: out};\n',rxnID{1}{j},kappa(j));
end
for j = 1:length(K)
    fprintf('var K_%s: per_fmol {init: %g, pub: out};\n',Kname{1}{j},K(j));
end

if true 
    if false
        for j=1:length(K)
            fprintf('var q_%s: fmol {init: 1e-13};\n',Kname{1}{j});
        end

        for j=1:length(kappa)
            fprintf('var v%s: fmol_per_sec;\n',rxnID{1}{j})
        end
        for j=1:length(K)
            fprintf('var mu_%s: J_per_mol;\n',Kname{1}{j});
        end
        for j=1:length(kappa)
            fprintf('v%s = kappa_%s*exp(mu_a/(R*T));\n',rxnID{1}{j}, rxnID{1}{j})
        end
        for j=1:length(K)
            fprintf('ode(q_%s, time) = p;\n',Kname{1}{j});
        end
    end
    disp(newline)
    disp('// Global value');
    for j=1:length(K)
        fprintf('var q_%s: fmol {pub: out};\n',Kname{1}{j});
    end
    disp('// From submodule');
    for j=1:length(K)
        fprintf('var q_%s_m%s: fmol {pub: in};\n',Kname{1}{j}, modname);
    end

    for j=1:length(K)
        fprintf('q_%s = q_%s_m%s + q_%s_init;\n',Kname{1}{j}, Kname{1}{j},...
            modname,Kname{1}{j});
    end
    
    disp(newline)
    disp('// Input from global environment');
    for j=1:length(K)
        fprintf('var q_%s_global: fmol {pub: in};\n',Kname{1}{j});
    end
    disp('// Output to global environment');
    for j=1:length(K)
        fprintf('var q_%s: fmol {init: 1e-16, pub: out};\n',Kname{1}{j});
    end
    
    for j=1:length(K)
        fprintf('mu_%s = R*T*ln(K_%s*q_%s_global);\n',Kname{1}{j},Kname{1}{j},Kname{1}{j});
    end
    
    disp(newline)
    fprintf('def map between environment and %s for\n',modname);
    fprintf('vars time and time;\n');
    for j=1:length(K)
        fprintf('vars q_%s_m%s and q_%s;\n',Kname{1}{j}, modname,Kname{1}{j});
        fprintf('vars q_%s and q_%s_global;\n',Kname{1}{j}, Kname{1}{j});
    end
    disp('enddef;');
end

disp(newline)

