function gate_plot(alpha,beta,g_ss,tau,alpha_bg,beta_bg,g_ss_bg,tau_bg,V,g,fval)
Vmin=min(V);
Vmax=max(V);
t=tiledlayout(2,2);
ax = nexttile;
plot(ax,V,g_ss,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,g_ss_bg,'k','LineWidth',2);
xlabel('Voltage (mV)');
ylabel([g '_{ss}']);
xlim([Vmin Vmax]);
set(gca,'XTick',Vmin:30:Vmax);
set(gca,'YTick',0:0.2:1);
set(gca,'LineWidth',2);
grid on;
legend('HH','BG','Location','best')

ax = nexttile;
plot(ax,V,tau,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,tau_bg,'k','LineWidth',2);
% legend('Luo and Rudy','Fitted');
xlabel('Voltage (mV)');
ylabel(['\tau_' g '(ms)']);
xlim([Vmin Vmax]);
set(gca,'XTick',Vmin:30:Vmax);
set(gca,'LineWidth',2);
grid on;

ax = nexttile;
plot(ax,V,alpha,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,alpha_bg,'k','LineWidth',2);
% legend('Luo and Rudy','Fitted');
xlabel('Voltage (mV)');
ylabel(['\alpha_' g '(ms)']);
xlim([Vmin Vmax]);
set(gca,'XTick',Vmin:30:Vmax);
set(gca,'LineWidth',2);
grid on;

ax = nexttile;
plot(ax,V,beta,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,beta_bg,'k','LineWidth',2);
% legend('Luo and Rudy','Fitted');
xlabel('Voltage (mV)');
ylabel(['\beta_' g ' (ms)']);
xlim([Vmin Vmax]);
set(gca,'XTick',Vmin:30:Vmax);
set(gca,'LineWidth',2);
grid on;
title(t,[g ' gate fitting results'], sprintf('MSE=%.2f',fval))