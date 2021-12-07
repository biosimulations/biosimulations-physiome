

% This file extracts the derivative vector from ExtendedModel

function dy = getDeriv(t,y,Phase,Params)

    % Calls the model function to get the derivatives
    [dy F_total ATPase F_net] = XBModel(t,y,Phase,Params);