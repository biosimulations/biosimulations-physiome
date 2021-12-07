
% Function that executes the isometric and work-loop protocols

function [T Y dy F_total ATPase] = XBSolve(loop,T_loop,preload_SL,Afterload,protocol,passive)

Params = [Afterload,loop,preload_SL,T_loop,passive];

if strcmp(protocol,'Isometric')
    Phase = 'isometric';
    run IC_XBModel;
    init(9) = preload_SL; % Set the initial SL
    options = odeset('RelTol',1e-6,'AbsTol',1e-6); 
    tspan = [0 1000]; %ms

    % Solve ODE
    [T_isom,Y_isom] = ode15s(@getDeriv,tspan,init,options,Phase,Params);
    
    T = [T_isom];
    Y = [Y_isom];
    
    %Retrieve Force and ATPase information
    for i=1:length(T)

         Phase = 'isometric';

        [dy F_total(i) ATPase(i) F_net(i)] = XBModel(T(i),Y(i,:),Phase,Params);
        dSL(i) = dy(9);
    end
    
else % Work loop contraction
    
    % Isometric phase ******************************************
    Phase = 'isometric';
    run IC_XBModel;
    init(9) = preload_SL; % Set the preloaded length
    options = odeset('RelTol',1e-6,'AbsTol',1e-6,'Events',@Fevents); % Set event for finding the start of isotonic contraction
    tspan = [0 2000]; %ms

    % Solve the ODE to find the contraction point (point of shortening)
    [T_isom,Y_isom,te1,ye,ie] = ode15s(@getDeriv,tspan,init,options,Phase,Params);

    % Isotonic phase *******************************************
    Phase = 'isotonic';
    options = odeset('Events',[]); %Remove the stop condition
    tspan = [te1 900]; % Use the time when isotonic contraction starts
    init = ye; % Use the state variables from the end of isometric
    init(8) = 0;  % Reset the force integral
    init(9) = preload_SL; % Set the preload
    
    % Solve through the contraction to find the relaxation point
    [T_isoton,Y_isoton] = ode15s(@getDeriv,tspan,init,options,Phase,Params);

    T = [T_isom; T_isoton;];
    Y = [Y_isom; Y_isoton];

    %Retrieve force information
    for i=1:length(T)

        if i<=length(T_isom)
            Phase = 'isometric';
        else
            Phase = 'isotonic';
        end

        [dy F_total(i) ATPase(i) F_net(i)] = XBModel(T(i),Y(i,:),Phase,Params);
        dSL(i) = dy(9);
    end

end




