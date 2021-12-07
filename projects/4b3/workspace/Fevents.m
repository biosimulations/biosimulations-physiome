

function [value,isterminal,direction] = Fevents(t,y,Phase,Params)
% Locate the time when the active force equals the afterload at  
% which point, the integration should stop.

    [dy F_total ATPase F_net] = XBModel(t,y,Phase,Params);

    value = F_net;     % Detect height = 0
    isterminal = 1;   % Stop the integration
    direction = 0;   % Negative direction only
end
