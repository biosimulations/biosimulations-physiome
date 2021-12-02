T = 279.45;
%% Define volumes (unit pL)
W_i = 38;
W_e = 5.182;
A_cap = 0.123; % Unit cm^2

%Keener, J.P., Sneyd, J.: ‘Mathematical physiology: I: cellular physiology'
%E_Na=56mV, E_K=-77mV
cNao_st = 437; % unit mM
cNai_st = 50; % unit mM
cKo_st = 20;
cKi_st = 397;
gK_max=36.0; % mS_per_cmsq
gNa_max=120.0;% mS_per_cmsq
zNa=1;
zK=1;
nNa=122720;
nK=5369;

G_Na = gNa_max*A_cap; % mS
G_K = gK_max*A_cap; % mS

[P,kf_GHK,kr_GHK]=GHK_cal(T,zNa,cNai_st,cNao_st,nNa,W_i,W_e,G_Na);
save(['Na_GHK_paras.mat'],'P','kf_GHK','kr_GHK');
[P,kf_GHK,kr_GHK]=GHK_cal(T,zK,cKi_st,cKo_st,nK,W_i,W_e,G_K);
save(['K_GHK_paras.mat'],'P','kf_GHK','kr_GHK');

