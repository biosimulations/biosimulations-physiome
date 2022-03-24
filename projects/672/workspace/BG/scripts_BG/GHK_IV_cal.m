function GHK_IV_cal(T,R,F,dNa,W_i,W_e,A_cap,V_m)
V_Na=-115;% HH mV
V_K=12;% HH mV
V_leak=-10.613;
E_Na=(-V_Na-65)/1000;% unit V
E_K=(-V_K-65)/1000;% unit V
E_leak=(-V_leak-65)/1000;% unit V
cNao_st = 484; % unit mM
cNai_st=cNao_st/exp(E_Na*F/(R*T));
%cNai_st = 60.7; % unit mM
cKo_st = 20;
cKi_st=cKo_st/exp(E_K*F/(R*T));
%cKi_st = 489.5;
gK_max=36.0; % mS_per_cmsq
gNa_max=120.0;% mS_per_cmsq
G_Na = gNa_max*A_cap; % mS
G_K = gK_max*A_cap; % mS
zNa=1;
zK=1;
dK=dNa/gNa_max*gK_max; % K channel density /cm^2
nNa=dNa*A_cap;%the number of Na channel
nK=dK*A_cap; %the number of K channel
%% calculate and save data
formatSpec={'%g','%.2f','%g','%g','%.3e','%.3e'};
M(1,:)={'Ion','\#Channels','Channels($fmol$)','$\bar G^X(mS)$','$P(pL/s)$','$k^+(s^{-1}fmol^{-1})$','$k^-(s^{-1}fmol^{-1})$'};

[P,kf_GHK,kr_GHK,X]=GHK_cal(T,R,F,zNa,cNai_st,cNao_st,nNa,W_i,W_e,G_Na);
save(['Na_GHK_paras.mat'],'P','kf_GHK','kr_GHK','X');
M(2,:)=['Na' compose(formatSpec,[nNa,X,G_Na,P,kf_GHK,kr_GHK])];

[P,kf_GHK,kr_GHK,X]=GHK_cal(T,R,F,zK,cKi_st,cKo_st,nK,W_i,W_e,G_K);
save(['K_GHK_paras.mat'],'P','kf_GHK','kr_GHK','X');
M(3,:)=['K' compose(formatSpec,[nK,X,G_K,P,kf_GHK,kr_GHK])];

writecell(M,'kineticGHK.csv','Delimiter',',')

formatSpec={'%g','%g','%g','%g','%g','%g','%g','%g','%g',};
M2(1,:)={'$A_{cap}$','$V_m$','$C_m$','$\bar G^leak$','$q_m$','$q_i^{Na}$','$q_e^{Na}$','$q_i^{K}$','$q_e^{K}$'};
M2(2,:)={'$cm^2$','$mV$','$fF$','$fS$','$fmol$','$fmol$','$fmol$','$fmol$','$fmol$'};

Cm_HH=1; %uF/cmsq
C_m=Cm_HH*10^9; %fF
gleak=0.3;% mS_per_cmsq
G_leak=gleak*A_cap*10^12; %fS
q_i_Na=cNai_st*W_i;%fmol
q_e_Na=cNao_st*W_e;%fmol
q_i_K=cKi_st*W_i;%fmol
q_e_K=cKo_st*W_e;%fmol
q_m=V_m/1000*C_m;%fC

M2(3,:)=[compose(formatSpec,[A_cap,V_m,C_m,G_leak,q_m,q_i_Na,q_e_Na,q_i_K,q_e_K])];

writecell(M2,'paraCell.csv','Delimiter',',')

formatSpec={'%g','%g','%g','%.1f','%d'};
M3(1,:)={'Ion channel','$g^{X}_{max}(mS/cm^2)$','$V^{X}(mV)$','$E^{X}(V)$','$[X_i](mM)$','$[X_o](mM)$'};
M3(2,:)=['Na' compose(formatSpec,[gNa_max,V_Na,E_Na,cNai_st,cNao_st,])];
M3(3,:)=['K' compose(formatSpec,[gK_max,V_K,E_K,cKi_st,cKo_st,])];
formatSpec={'%g','%g','%g'};
M3(4,:)=['Leak' compose(formatSpec,[gleak,V_leak,E_leak,]) 'NA' 'NA'];

writecell(M3,'paraHH.csv','Delimiter',',')

