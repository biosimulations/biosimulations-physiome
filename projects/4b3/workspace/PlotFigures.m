
%% This script plots Figures 3, 4, 7 and 8 from 
% the JPhysiol publication

% RUN THE Main.m SCRIPT FIRST TO GENERATE 
% THE OUTPUT FOR PLOTTING

%% Figure 3 - Mechanics - isometric vs isotonic
% Work-loops at initial SL = 2.3

lw = 1.75;

fig3 = figure(3);
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
plot(SL23_T_vec, SL23_Force_vec,'k-','LineWidth',lw);
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
plot(SL23_SL_vec/max(preload_SL_iso), SL23_Force_vec, 'k-','LineWidth',lw); 
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
plot(SL23_T_vec, SL23_ATP_vec,'k-','LineWidth',lw);
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',10);
box off;

set(fig3,'Position',[480   40  660  740])

%% Figure 4 - Energetics - isometric vs isotonic
% % Work-loops at initial SL = 2.3

lw = 1.5;

fig4 = figure(4);
subplot(4,1,1)
plot(SL23_AF/max(PF),SL23_enthalpy_WL/ME,'ko-','LineWidth',lw); hold on;
plot([PF(1) SL23_AF/max(PF)],[SL23_enthalpy_IS(1) SL23_enthalpy_IS_interp]/ME,'o-','Color', [0.5 0.5 0.5],'LineWidth',lw); 
L = legend('Work-loop','Isometric', 'location', 'NW');
set(L,'FontSize',8);
xlabel('Relative Afterload/Stress')
ylabel('Relative Enthalpy')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',10);
box off;

subplot(4,1,2)
plot(SL23_AF/max(PF),SL23_work/ME,'ko-','LineWidth',lw); hold on;
xlabel('Relative Afterload')
ylabel('Relatve Work')
axis([0 1.05 0 0.6])
set(gca,'fontsize',10);
box off;

subplot(4,1,3)
plot([PF(1) SL23_AF/max(PF)],[SL23_enthalpy_IS(1) SL23_enthalpy_IS_interp]/ME,'o-','Color', [0.5 0.5 0.5],'LineWidth',lw); hold on;
plot(SL23_AF/max(PF),SL23_heat_WL/ME,'ko-','LineWidth',lw);
ylabel('Relative Heat')
xlabel('Relative Afterload/Stress')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',10);
box off;

subplot(4,1,4)
plot(SL23_AF/max(PF),SL23_SH/ME,'ko-','LineWidth',lw); hold on;
ylabel('Shortening Heat (kJ/m^3)')
ylabel('Relative Shortening Heat')
xlabel('Relative Afterload')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',10);
box off;

set(fig4,'Position',[449.8000 -147.0000  332.0000  911.2000])


%% Figure 7 - Isometric vs Work-loop mechanics at different preloads
% Work-loops at preload SL 2.3, 2.11, 1.935 and isometric
 
MI = max(Force_iso_vec(:,end));
lw = 1.75;

fig7 = figure(7);
subplot(3,4,2)
plot(SL223_T_vec, SL223_Force_vec/MI,'k-','LineWidth',lw); hold off;
axis([0 1000 -2/MI 65/MI])
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('Relative Afterload')
xlabel('Time (ms)')
set(gca,'fontsize',12);
title('\rmWork-loop; \it{SL_i} \rm= 2.23 \mum','fontsize',12);
box off;

subplot(3,4,6)
plot(SL223_SL_vec/max(preload_SL_iso), SL223_Force_vec/MI, 'k-','LineWidth',lw); hold off;
axis([0.45 1.01 -2/MI 65/MI ])
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
ylabel('Relative Afterload')
xlabel('Relative SL');
set(gca,'fontsize',12);
box off;

subplot(3,4,10)
plot(SL223_T_vec, SL223_ATP_vec,'k-','LineWidth',lw);
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',12);
box off;

subplot(3,4,1)
plot(T_iso_vec,Force_iso_vec/MI,'k-','LineWidth',lw); hold off;
axis([0 1000 -2/MI 65/MI])
set(gca, 'xtick', [0 250 500 750 1000]);
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
ylabel('Relative Stress')
xlabel('Time (ms)')
set(gca,'fontsize',12);
box off;

subplot(3,4,5)
plot(SL_iso_vec/max(preload_SL_iso), Force_iso_vec/MI,'k-','LineWidth', lw); hold off;
axis([0.45 1.01 -2/MI 65/MI ])
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
xlabel('Relative SL');
ylabel('Relative Stress')
set(gca,'fontsize',12);
box off;

subplot(3,4,9)
plot(T_iso_vec, ATP_iso_vec,'k-','LineWidth',lw); 
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',12);
box off;

subplot(3,4,3)
plot(SL211_T_vec, SL211_Force_vec/MI,'k-','LineWidth',lw); hold off;
axis([0 1000 -2/MI 65/MI])
set(gca, 'xtick', [0 250 500 750 1000]);
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
ylabel('Relative Afterload')
xlabel('Time (ms)')
set(gca,'fontsize',12);
title('\rmWork-loop; \it{SL_i} \rm= 2.11 \mum','fontsize',12);
box off;

subplot(3,4,7)
plot(SL211_SL_vec/max(preload_SL_iso), SL211_Force_vec/MI, 'k-','LineWidth',lw); hold off;
axis([0.45 1.01 -2/MI 65/MI ])
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
xlabel('Relative SL');
ylabel('Relative Afterload')
set(gca,'fontsize',12);
box off;

subplot(3,4,11)
plot(SL211_T_vec, SL211_ATP_vec,'k-','LineWidth',lw);
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
%text(300,7.5e-4,'Work-loop','fontsize',12)
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',12);
box off;

subplot(3,4,4)
plot(SL1935_T_vec, SL1935_Force_vec/MI,'k-','LineWidth',lw); hold off;
axis([0 1000 -2/MI 65/MI]);
set(gca, 'xtick', [0 250 500 750 1000]);
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
ylabel('Relative Afterload');
xlabel('Time (ms)');
set(gca,'fontsize',12);
title('\rmWork-loop; \it{SL_i} \rm= 1.94 \mum','fontsize',12);
box off;

subplot(3,4,8)
plot(SL1935_SL_vec/max(preload_SL_iso), SL1935_Force_vec/MI, 'k-','LineWidth',lw); hold off;
axis([0.45 1.01 -2/MI 65/MI ])
set(gca, 'ytick', [0 0.2 0.4 0.6 0.8 1]);
xlabel('Relative SL');
ylabel('Relative Afterload')
set(gca,'fontsize',12);
box off;

subplot(3,4,12)
plot(SL1935_T_vec, SL1935_ATP_vec,'k-','LineWidth',lw);
axis([0 1000 0 0.8e-3])
set(gca, 'xtick', [0 250 500 750 1000]);
ylabel('ATPase rate (mM/ms)')
xlabel('Time (ms)')
set(gca,'fontsize',12);
box off;

set(fig7,'Position',[108 45 1340 720])


%% Figure 8 - Energetics for work-loops at different initial lengths

lw = 1.5;
lw2 = 1;

fig8 = figure(8);
subplot(4,1,1)
plot(SL23_AF/max(PF),SL23_enthalpy_WL/ME,'ko-','LineWidth',lw); hold on;
plot(SL223_AF/max(PF),SL223_enthalpy_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL2175_AF/max(PF),SL2175_enthalpy_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL211_AF/max(PF),SL211_enthalpy_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL2035_AF/max(PF),SL2035_enthalpy_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL1935_AF/max(PF),SL1935_enthalpy_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot([PF(1) SL23_AF/max(PF)],[SL23_enthalpy_IS(1) SL23_enthalpy_IS_interp]/ME,'o-','Color', [0.5 0.5 0.5],'LineWidth',lw); hold off;
xlabel('Relative Afterload/Stress')
ylabel('Relative Enthalpy')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',11);
text(01-0.1, 1.1, '\it{SL_i} \rm= 2.3 \mum','fontsize', 8)
text(0.85, 0.77, '\it{SL_i} \rm= 2.23 \mum','fontsize', 8)
text(0.7, 0.61, '\it{SL_i} \rm= 2.18 \mum','fontsize', 8)
text(0.55, 0.45, '\it{SL_i} \rm= 2.11 \mum','fontsize', 8)
text(0.4, 0.31, '\it{SL_i} \rm= 2.04 \mum','fontsize', 8)
text(0.25, 0.16, '\it{SL_i} \rm= 1.94 \mum','fontsize', 8)
box off;

subplot(4,1,2)
plot(SL23_AF/max(PF),SL23_work/ME,'ko-','LineWidth',lw); hold on;
plot(SL223_AF/max(PF),SL223_work/ME,'ko-','LineWidth',lw2,'markersize',2); 
plot(SL2175_AF/max(PF),SL2175_work/ME,'ko-','LineWidth',lw2,'markersize',2); 
plot(SL211_AF/max(PF),SL211_work/ME,'ko-','LineWidth',lw2,'markersize',2); 
plot(SL2035_AF/max(PF),SL2035_work/ME,'ko-','LineWidth',lw2,'markersize',2); 
plot(SL1935_AF/max(PF),SL1935_work/ME,'ko-','LineWidth',lw2,'markersize',2);
xlabel('Relative Afterload')
ylabel('Relative Work')
axis([0 1.05 0 0.6])
set(gca,'fontsize',11);
box off;

subplot(4,1,3)
plot([PF(1) SL23_AF/max(PF)],[SL23_enthalpy_IS(1) SL23_enthalpy_IS_interp]/ME,'o-','Color', [0.5 0.5 0.5],'LineWidth',lw); hold on;
plot(SL23_AF/max(PF),SL23_heat_WL/ME,'ko-','LineWidth',lw);
plot(SL223_AF/max(PF),SL223_heat_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL2175_AF/max(PF),SL2175_heat_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL211_AF/max(PF),SL211_heat_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL2035_AF/max(PF),SL2035_heat_WL/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL1935_AF/max(PF),SL1935_heat_WL/ME,'ko-','LineWidth',lw2,'markersize',2);hold off;
ylabel('Relative Heat')
xlabel('Relative Afterload/Stress')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',11);
box off;

subplot(4,1,4)
plot(SL23_AF/max(PF),SL23_SH/ME,'ko-','LineWidth',lw); hold on;
plot(SL223_AF/max(PF),SL223_SH/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL2175_AF/max(PF),SL2175_SH/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL211_AF/max(PF),SL211_SH/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL2035_AF/max(PF),SL2035_SH/ME,'ko-','LineWidth',lw2,'markersize',2);
plot(SL1935_AF/max(PF),SL1935_SH/ME,'ko-','LineWidth',lw2,'markersize',2);
ylabel('Shortening Heat (kJ/m^3)')
ylabel('Relative Shortening Heat')
xlabel('Relative Afterload')
axis([0 1.05 0 1.1])
set(gca, 'ytick', [0.2 0.4 0.6 0.8 1]);
set(gca,'fontsize',11);
box off;

set(fig8,'Position',[449.8000 -147.0000  332.0000  911.2000])
