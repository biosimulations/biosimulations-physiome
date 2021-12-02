clear;
%% Define volumes (unit pL)
W_i = 38;
W_e = 5.182;

opts = detectImportOptions('K_forward_matrix.xlsx');
opts.SelectedVariableNames = [2:6]; 
opts.DataRange = '2:8';
N_f = readmatrix('K_forward_matrix.xlsx',opts);
opts.SelectedVariableNames = 'species';
opts.DataRange = '2:8';
Kname=readmatrix('Na_forward_matrix.xlsx',opts);
opts.SelectedVariableNames = [2:6]; 
kappa_name=opts.SelectedVariableNames';

opts = detectImportOptions('Na_reverse_matrix.xlsx');
opts.SelectedVariableNames = [2:6]; 
opts.DataRange = '2:8';
N_r = readmatrix('K_reverse_matrix.xlsx',opts);

N_fT = transpose(N_f);
N_rT = transpose(N_r);

N = N_r - N_f;
N_T = N_rT - N_fT;

num_cols = size(N,2);
I = eye(num_cols);
zerofill = zeros(1,num_cols);

N_c=[1; -1; 0;0;0;0;0;];
K_c=[W_e/W_i;];
N_c_T=transpose(N_c);

M = [I N_fT; I N_rT;zerofill N_c_T;];

%% Import gate transition parameters
% K channel
load(['K_GHK_paras.mat']);
load(['K_n_parameters.mat']);
alpha_n0_bg = params_vec(1)*1e3; % unit s^-1
beta_n0_bg = params_vec(3)*1e3; % unit s^-1

kf = [kf_GHK; ... % R_GHK
    4*alpha_n0_bg; ... % Rn1
    3*alpha_n0_bg; ... % Rn2
    2*alpha_n0_bg; ... % Rn3
    1*alpha_n0_bg; ... % Rn4    
    ]; 
    
kr = [kr_GHK; ... % R_GHK
    1*beta_n0_bg; ... % Rn1
    2*beta_n0_bg; ... % Rn2
    3*beta_n0_bg; ... % Rn3
    4*beta_n0_bg; ... % Rn4    
    ];

k = [kf;kr;K_c];
W = [ones(size(N,2),1);W_i;W_e;ones(5,1);];

lambdaW = exp(pinv(M)*log(k));
lambda = lambdaW./W;
kappa = lambda(1:size(N,2));
K = lambda(size(N,2)+1:end);

save(['BG_paras_K.mat'],'kappa','K','Kname','kappa_name'); %

fileID = fopen('BG_paras_K_CellML.txt','w');
var_kappa=num2cell(kappa);
data_kappa=[kappa_name,var_kappa]';
var_K=num2cell(K);
data_K=[Kname,var_K]';
fprintf(fileID,'var kappa_%s: fmol_per_sec {init: %g};\n',data_kappa{:});
fprintf(fileID,'var K_%s: per_fmol {init: %g};\n',data_K{:});
fclose(fileID);

%% Checks
N_rref = rref(N);
R_mat = null(N,'r');

K_eq = kf./kr;
zero_est = R_mat'*K_eq;

k_est = exp(M*log(lambdaW));
diff = sum(abs((k-k_est)./k));
 