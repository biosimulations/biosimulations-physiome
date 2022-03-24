function [kappa,K,kappa_name,Kname,diff]=BG_paras_conv(chn,kf,kr,K_c,N_c,Ws)
%chn: reaction network; kf/kr: vectors of the forward and reverse kinetic
%rate constants; K_c: vector of known constraints between the species
%defined in N_c; Ws: vector of the volumes of species
%% Read stoichiometric matrices
fmaxtrixf=[chn '_forward_matrix.csv'];
opts = detectImportOptions(fmaxtrixf);
opts.SelectedVariableNames = [2:length(opts.VariableNames)]; 
N_f = readmatrix(fmaxtrixf,opts);
kappa_name=opts.SelectedVariableNames';
opts.SelectedVariableNames = [1];
Kname=readmatrix(fmaxtrixf,opts);
fmaxtrixr=[chn '_reverse_matrix.csv'];
opts = detectImportOptions(fmaxtrixr);
opts.SelectedVariableNames = [2:length(opts.VariableNames)]; 
N_r = readmatrix(fmaxtrixr,opts);
%% Construct M
N_fT = transpose(N_f);
N_rT = transpose(N_r);
N = N_r - N_f;
num_cols = size(N,2);
I = eye(num_cols);
zerofill = zeros(1,num_cols);
N_c_T=transpose(N_c);
M = [I N_fT; I N_rT;zerofill N_c_T;];
%% Construct W
W = [ones(size(N,2),1);Ws;];
%% Contruct vector of kinetic paras
k = [kf;kr;K_c];
%% Convert kinetic paras to BG paras
lambdaW = exp(pinv(M)*log(k));
lambda = lambdaW./W;
kappa = lambda(1:size(N,2));
K = lambda(size(N,2)+1:end);
%% Checks
N_rref = rref(N);
R_mat = null(N,'r');
K_eq = kf./kr;
zero_est = R_mat'*K_eq;
k_est = exp(M*log(lambdaW));
diff = sum(abs((k-k_est)./k));
