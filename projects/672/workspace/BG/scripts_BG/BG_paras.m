%% Define volumes (unit pL)
W_i = 4.24e6;
W_e = 6.06e5;
%% Import gate transition parameters
% Na channel
chn='Na';
load(['Na_GHK_paras.mat']);
load(['Na_m_parameters.mat']);
alpha_m0_bg = params_vec(1)*1e3; % unit s^-1
beta_m0_bg = params_vec(3)*1e3; % unit s^-1
z_m_f = params_vec(2);
z_m_r = params_vec(4);
load(['Na_h_parameters.mat']);
alpha_h0_bg = params_vec(1)*1e3; % unit s^-1
beta_h0_bg = params_vec(3)*1e3; % unit s^-1
z_h_f = params_vec(2);
z_h_r = params_vec(4);
kf = [kf_GHK; ... % R_GHK
    3*alpha_m0_bg; ... % Rm10
    2*alpha_m0_bg; ... % Rm20
    alpha_m0_bg; ... % Rm30
    3*alpha_m0_bg; ... % Rm11
    2*alpha_m0_bg; ... % Rm21
    alpha_m0_bg; ... % Rm31    
    alpha_h0_bg; ... % Rh0
    alpha_h0_bg; ... % Rh1
    alpha_h0_bg; ... % Rh2
    alpha_h0_bg; ... % Rh3
    ];     
kr = [kr_GHK; ... % R_GHK
    1*beta_m0_bg; ... % Rm10
    2*beta_m0_bg; ... % Rm20
    3*beta_m0_bg; ... % Rm30
    1*beta_m0_bg; ... % Rm11
    2*beta_m0_bg; ... % Rm21
    3*beta_m0_bg; ... % Rm31    
    beta_h0_bg; ... % Rh0
    beta_h0_bg; ... % Rh1
    beta_h0_bg; ... % Rh2
    beta_h0_bg; ... % Rh3
    ];
Ws=[ones(10,1);];
N_c=[1; -1; 0;0;0;0;0;0;0;0;];
K_c=[W_e/W_i;];
[kappa,K,kappa_name,Kname,diff]=BG_paras_conv(chn,kf,kr,K_c,N_c,Ws);
%% Save the data
sfile=['BG_paras_' chn '.mat'];
save(sfile,'kappa','K','Kname','kappa_name','diff'); %
%% Write for CellML
extr_name={'z_m_f','z_m_r','z_h_f','z_h_r','z_Na'};
extr_unit=strcat('dimensionless',cell(1,length(extr_name)));
extr=[z_m_f,z_m_r,z_h_f,z_h_r,1];
data_extr=[extr_name;extr_unit;num2cell(extr)];
kappa_unit=strcat('fmol_per_sec',cell(length(kappa_name),1));
data_kappa=[strcat('kappa_',kappa_name),kappa_unit,num2cell(kappa)]';
K_unit=strcat('per_fmol',cell(length(Kname),1));
data_K=[strcat('K_',Kname),K_unit,num2cell(K)]';
blanks=strcat('',cell(1,(length(extr_name)+length(kappa_unit)+length(K_unit))));
data_all=[blanks;data_K,data_kappa,data_extr];
fileID = fopen('BG_paras_CellML.txt','w');
fprintf(fileID,'%7s var %s: %s {init: %g, pub: out};\n',data_all{:});
%% Import gate transition parameters
% K channel
chn='K';
load(['K_GHK_paras.mat']);
load(['K_n_parameters.mat']);
alpha_n0_bg = params_vec(1)*1e3; % unit s^-1
beta_n0_bg = params_vec(3)*1e3; % unit s^-1
z_n_f = params_vec(2);
z_n_r = params_vec(4);

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
Ws=[ones(7,1);];
N_c=[1; -1; 0;0;0;0;0;];
K_c=[W_e/W_i;];
[kappa,K,kappa_name,Kname,diff]=BG_paras_conv(chn,kf,kr,K_c,N_c,Ws);
%% Save the data
sfile=['BG_paras_' chn '.mat'];
save(sfile,'kappa','K','Kname','kappa_name','diff'); %
%% Write for CellML
extr_name={'z_n_f','z_n_r','z_K'};
extr_unit=strcat('dimensionless',cell(1,length(extr_name)));
extr=[z_n_f,z_n_r,1];
data_extr=[extr_name;extr_unit;num2cell(extr)];
kappa_unit=strcat('fmol_per_sec',cell(length(kappa_name),1));
data_kappa=[strcat('kappa_',kappa_name),kappa_unit,num2cell(kappa)]';
K_unit=strcat('per_fmol',cell(length(Kname),1));
data_K=[strcat('K_',Kname),K_unit,num2cell(K)]';
blanks=strcat('',cell(1,(length(extr_name)+length(kappa_unit)+length(K_unit))));
data_all=[blanks;data_K,data_kappa,data_extr];
fprintf(fileID,'%7s var %s: %s {init: %g, pub: out};\n',data_all{:});
fclose(fileID);
%% For open channels
% Na channel
chn='sa_Na';
load(['Na_GHK_paras.mat']);
kf = [kf_GHK; ... % R_GHK
    ];     
kr = [kr_GHK; ... % R_GHK   
    ];
Ws=[ones(3,1);];
N_c=[1; -1; 0;];
K_c=[W_e/W_i;];
[kappa,K,kappa_name,Kname,diff]=BG_paras_conv(chn,kf,kr,K_c,N_c,Ws);
%% Save the data
sfile=['BG_paras_' chn '.mat'];
save(sfile,'kappa','K','Kname','kappa_name','diff'); %
%% Write for CellML
extr_name={'q_sa_Na',};
extr_unit=strcat('fmol',cell(1,length(extr_name)));
extr=[X];
data_extr=[extr_name;extr_unit;num2cell(extr)];
kappa_unit=strcat('fmol_per_sec',cell(length(kappa_name),1));
data_kappa=[strcat('kappa_',kappa_name),kappa_unit,num2cell(kappa)]';
K_unit=strcat('per_fmol',cell(length(Kname),1));
data_K=[strcat('K_',Kname),K_unit,num2cell(K)]';
blanks=strcat('',cell(1,(length(extr_name)+length(kappa_unit)+length(K_unit))));
data_all=[blanks;data_K,data_kappa,data_extr];
fileID = fopen('BG_paras_openCH_CellML.txt','w');
fprintf(fileID,'%7s var %s: %s {init: %g, pub: out};\n',data_all{:});
% K channel
chn='sa_K';
load(['K_GHK_paras.mat']);
kf = [kf_GHK; ... % R_GHK
    ];     
kr = [kr_GHK; ... % R_GHK   
    ];
Ws=[ones(3,1);];
N_c=[1; -1; 0;];
K_c=[W_e/W_i;];
[kappa,K,kappa_name,Kname,diff]=BG_paras_conv(chn,kf,kr,K_c,N_c,Ws);
%% Save the data
sfile=['BG_paras_' chn '.mat'];
save(sfile,'kappa','K','Kname','kappa_name','diff'); %
%% Write for CellML
extr_name={'q_sa_K',};
extr_unit=strcat('fmol',cell(1,length(extr_name)));
extr=[X];
data_extr=[extr_name;extr_unit;num2cell(extr)];
kappa_unit=strcat('fmol_per_sec',cell(length(kappa_name),1));
data_kappa=[strcat('kappa_',kappa_name),kappa_unit,num2cell(kappa)]';
K_unit=strcat('per_fmol',cell(length(Kname),1));
data_K=[strcat('K_',Kname),K_unit,num2cell(K)]';
blanks=strcat('',cell(1,(length(extr_name)+length(kappa_unit)+length(K_unit))));
data_all=[blanks;data_K,data_kappa,data_extr];
fprintf(fileID,'%7s var %s: %s {init: %g, pub: out};\n',data_all{:});
fclose(fileID);