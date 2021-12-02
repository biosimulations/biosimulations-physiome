function gate_plot(alpha,beta,g_ss,tau,params_vec,V,T,g,fval)
t=tiledlayout(2,2);
g_ss_fit = p2gss(params_vec,V,T);
ax = nexttile;
plot(ax,V,g_ss,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,g_ss_fit,'k','LineWidth',2);
xlabel('Voltage (mV)');
ylabel([g '_{ss}']);
xlim([-120 60]);
set(gca,'XTick',-120:30:60);
set(gca,'YTick',0:0.2:1);
xticklabels({-120,'',-60,'',0,'',60});
yticklabels({0,'','','','',1});
set(gca,'LineWidth',2);
grid on;
legend('HH','BG','Location','best')

tau_fit = p2tau(params_vec,V,T);
ax = nexttile;
plot(ax,V,tau,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,tau_fit,'k','LineWidth',2);
% legend('Luo and Rudy','Fitted');
xlabel('Voltage (mV)');
ylabel(['\tau_' g '(ms)']);
xlim([-120 60]);
set(gca,'XTick',-120:30:60);
% set(gca,'YTick',0:0.2:1);
xticklabels({-120,'',-60,'',0,'',60});
% yticklabels({0,'','','','',1});
set(gca,'LineWidth',2);
grid on;

alpha_fit = calc_alpha(params_vec,V/1000,T);
ax = nexttile;
plot(ax,V,alpha,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,alpha_fit,'k','LineWidth',2);
% legend('Luo and Rudy','Fitted');
xlabel('Voltage (mV)');
ylabel(['\alpha_' g '(ms)']);
xlim([-120 60]);
set(gca,'XTick',-120:30:60);
% set(gca,'YTick',0:0.2:1);
xticklabels({-120,'',-60,'',0,'',60});
% yticklabels({0,'','','','',1});
set(gca,'LineWidth',2);
grid on;

beta_fit = calc_beta(params_vec,V/1000,T);
ax = nexttile;
plot(ax,V,beta,'k--','LineWidth',2);
hold (ax,'on');
plot(ax,V,beta_fit,'k','LineWidth',2);
% legend('Luo and Rudy','Fitted');
xlabel('Voltage (mV)');
ylabel(['\beta_' g ' (ms)']);
xlim([-120 60]);
set(gca,'XTick',-120:30:60);
% set(gca,'YTick',0:0.2:1);
xticklabels({-120,'',-60,'',0,'',60});
% yticklabels({0,'','','','',1});
set(gca,'LineWidth',2);
grid on;
title(t,[g ' gate fitting results'], sprintf('fval=%.1f',fval))