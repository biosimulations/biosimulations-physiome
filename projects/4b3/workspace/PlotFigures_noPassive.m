
%% This script plots Figures 5 and 6 (no passive simulations) 
% from the JPhysiol publication

% RUN THE Main_noPassive.m SCRIPT FIRST TO GENERATE 
% THE OUTPUT FOR PLOTTING

%% Figure 5 - Mechanics with no passive - isometric vs isotonic
% Work-loops at initial SL = 2.3

lw = 1.75;
fig6 = figure(5);
subplot(3,2,1)
plot(T_iso_vec,Force_iso_vec,'k-','LineWidth',lw);
axis([0 1000 -2 65])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('Stress (kPa)')
xlabel('Time (ms)')
title('Isometric contractions');
set(gca,'fontsize',10);
box off;

subplot(3,2,2)
plot(NoPassive_SL23_T_vec, NoPassive_SL23_Force_vec,'k-','LineWidth',lw);
axis([0 1000 -2 65])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('Stress (kPa)')
xlabel('Time (ms)')
title('Work-loop contractions');
set(gca,'fontsize',10);
box off;

subplot(3,2,3)
plot(SL_iso_vec/max(preload_SL_iso), Force_iso_vec,'k-','LineWidth', lw); 
axis([0.45 1.01 -2 65 ])
xlabel('Relative SL');
ylabel('Stress (kPa)')
set(gca,'fontsize',10);
box off;

subplot(3,2,4)
plot(NoPassive_SL23_SL_vec/max(preload_SL_iso), NoPassive_SL23_Force_vec, 'k-','LineWidth',lw); 
axis([0.45 1.01 -2 65 ])
xlabel('Relative SL');
ylabel('Stress (kPa)')
set(gca,'fontsize',10);
box off;

subplot(3,2,5)
plot(T_iso_vec, ATP_iso_vec,'k-','LineWidth',lw); 
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',10);
box off;

subplot(3,2,6)
plot(NoPassive_SL23_T_vec, NoPassive_SL23_ATP_vec,'k-','LineWidth',lw);
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',10);
box off;

set(fig6,'Position',[480   40  660  740])

%% Figure 6 - Energetics with no Passive - isometric vs isotonic
% % Work-loops at initial SL = 2.3

lw = 1.5;
fig6 = figure(6);
subplot(4,1,1)
plot(NoPassive_SL23_AF/max(PF),NoPassive_SL23_enthalpy_WL/ME,'ko-','LineWidth',lw); hold on;
plot([PF(1) NoPassive_SL23_AF/max(PF)],[NoPassive_SL23_enthalpy_IS(1) NoPassive_SL23_enthalpy_IS_interp]/ME,'o-','Color', [0.5 0.5 0.5],'LineWidth',lw); 
L = legend('Work-loop','Isometric', 'location', 'NW');
set(L,'FontSize',8);
xlabel('Relative Afterload/Stress')
ylabel('Relative Enthalpy')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',10);
box off;

subplot(4,1,2)
plot(NoPassive_SL23_AF/max(PF),NoPassive_SL23_work/ME,'ko-','LineWidth',lw); hold on;
xlabel('Relative Afterload')
ylabel('Relatve Work')
axis([0 1.05 0 0.6])
set(gca,'fontsize',10);
box off;

subplot(4,1,3)
plot([PF(1) NoPassive_SL23_AF/max(PF)],[NoPassive_SL23_enthalpy_IS(1) NoPassive_SL23_enthalpy_IS_interp]/ME,'o-','Color', [0.5 0.5 0.5],'LineWidth',lw); hold on;
plot(NoPassive_SL23_AF/max(PF),NoPassive_SL23_heat_WL/ME,'ko-','LineWidth',lw);
ylabel('Relative Heat')
xlabel('Relative Afterload/Stress')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',10);
box off;

subplot(4,1,4)
plot(NoPassive_SL23_AF/max(PF),NoPassive_SL23_SH/ME,'ko-','LineWidth',lw); hold on;
ylabel('Shortening Heat (kJ/m^3)')
ylabel('Relative Shortening Heat')
xlabel('Relative Afterload')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',10);
box off;

set(fig6,'Position',[449.8000 -147.0000  332.0000  911.2000])


