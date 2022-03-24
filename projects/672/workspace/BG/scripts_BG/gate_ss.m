clear;
clc;
close all;
addpath(genpath('../../cellLib/BG_fit/'))
T = 279.45; % K
phi = 3^((T - 6.3-273.15) / 10);
%% n4 bg
opts = detectImportOptions('gate_n4_BG_ss.csv');
opts.SelectedVariableNames = ['outputs_q_S4_norm']; 
n4_ss = readmatrix('gate_n4_BG_ss.csv',opts);
opts.SelectedVariableNames = ['boundary_conditions_V_m']; 
V_m_n4 = readmatrix('gate_n4_BG_ss.csv',opts)*1000; %V->mV
opts.SelectedVariableNames = [2:(length(opts.VariableNames)-1)];
qn4_name=opts.SelectedVariableNames';
qn4_init_name=strrep(qn4_name,'outputs_','');
wline=find(V_m_n4==-65)+1;
opts.DataLines = [wline wline];
qn4_inits = readmatrix('gate_n4_BG_ss.csv',opts);

%% m3h bg
opts = detectImportOptions('gate_m3h_BG_ss.csv');
opts.SelectedVariableNames = ['outputs_q_S31_norm']; 
m3h_ss = readmatrix('gate_m3h_BG_ss.csv',opts);
opts.SelectedVariableNames = ['boundary_conditions_V_m']; 
V_m_m3h = readmatrix('gate_m3h_BG_ss.csv',opts)*1000; %V->mV
opts.SelectedVariableNames = [2:(length(opts.VariableNames)-1)];
qm3h_name=opts.SelectedVariableNames';
qm3h_init_name=strrep(qm3h_name,'outputs_','');
wline=find(V_m_m3h==-65)+1;
opts.DataLines = [wline wline];
qm3h_inits = readmatrix('gate_m3h_BG_ss.csv',opts);

%% Write for CellML
opts = detectImportOptions('paraCell.csv');
opts.SelectedVariableNames = [3:length(opts.VariableNames)];
extr_name={'C_m','g_leak','q_m_init','q_i_Na_init','q_e_Na_init','q_i_K_init','q_e_K_init'};
extr_unit={'fF','fS','fmol','fmol','fmol','fmol','fmol'};
extr=readmatrix('paraCell.csv',opts);
data_extr=[extr_name;extr_unit;num2cell(extr)];
blanks=strcat('',cell(1,length(extr_name)));
data_all=[blanks;data_extr];
fileID = fopen('Init_paras_CellML.txt','w');
fprintf(fileID,'%7s var %s: %s {init: %g, pub: out};\n',data_all{:});

q_name=strcat([qm3h_init_name;qn4_init_name],'_init');
q_init=num2cell([qm3h_inits,qn4_inits]);
q_unit=strcat('fmol',cell(1,length(q_name)));
blanks=strcat('',cell(1,(length(qm3h_init_name)+length(qn4_init_name))));
data_all=[blanks;q_name';q_unit;q_init;];
fprintf(fileID,'%7s var %s: %s {init: %g, pub: out};\n',data_all{:});
fclose(fileID);
%% Plot for comparison
load(['Na_m_parameters.mat']);
V_m_bg = V;
m_ss_bg = g_ss_bg;
m_ss_HH = g_ss;

load(['Na_h_parameters.mat']);
h_ss_bg = g_ss_bg;
h_ss_HH = g_ss;

load(['K_n_parameters.mat']);
V_n_bg = V;
n_ss_bg = g_ss_bg;
n_ss_HH = g_ss;

m3h_ss_bg = m_ss_bg.^3.*h_ss_bg;
n4_ss_bg = n_ss_bg.^4;
m3h_ss_HH = m_ss_HH.^3.*h_ss_HH;
n4_ss_HH = n_ss_HH.^4;

h=figure;
width=400*2;
height=350;
x0=100;
y0=50;
set(gcf,'position',[x0,y0,width,height])
t=tiledlayout(1,2);
ax = nexttile;
plot(ax,V,n4_ss_HH,'k--','LineWidth',2);
hold ('on');
plot(ax,V_m_n4,n4_ss,'k','LineWidth',2);
hold ('on');
plot(ax,V_n_bg,n4_ss_bg,'b--','LineWidth',2);
xlabel('Voltage (mV)');
ylabel(['n^4_{ss}']);
Vmin=min(V_n_bg);
Vmax=max(V_n_bg);
xlim([Vmin Vmax]);
set(gca,'XTick',Vmin:30:Vmax);
set(gca,'LineWidth',2);
grid on;
legend('HH','BG','Location','best')
ax = nexttile;
plot(ax,V,m3h_ss_HH,'k--','LineWidth',2);
hold ('on');
plot(ax,V_m_m3h,m3h_ss,'k','LineWidth',2);
hold ('on');
plot(ax,V_m_bg,m3h_ss_bg,'b--','LineWidth',2);
xlabel('Voltage (mV)');
ylabel(['m^3h_{ss}']);
Vmin=min(V_m_bg);
Vmax=max(V_m_bg);
xlim([Vmin Vmax]);
set(gca,'XTick',Vmin:30:Vmax);
set(gca,'LineWidth',2);
grid on;
title(t,'Steady state')
filename='gate_ss';
savefig(h,sprintf('%s.fig',filename))
exportgraphics(h,sprintf('%s.eps',filename));