

function [dy F_total ATPase F_net] = XBModel(t,y,Phase,Params)

    % Get parameters
    run Parameters_XBModel;
    
    % Assign the state variables
    Nxb = y(1);  % Non-permissive fraction in overlap region
    XBpreR = y(2);   % Fraction of XBs in pre-rotated state (Stiffness generation)
    XBpostR = y(3);  % Fraction of XBS in post-rotated state (force generation)
    x_XBpreR = y(4);    % Strain of XBs in the pre-rotated state
    x_XBpostR = y(5);  % Strain of XBs in the post-rotated state
    TropCaL = y(6); % Ca bound to the low affinity troponin site
    TropCaH = y(7); % Ca bound to the high affinity troponin site
    IntegF = y(8); % Integral of force
    SL = y(9); % Sarcomere length
 
    Afterload = Params(1); % Afterload for work-loop contraction
    loop = Params(2); % Boolean to indicate if it is a work-loop contraction
    preload_SL = Params(3); % Initial SL for work-loop contractions
    T_loop(1) = Params(4); % Time for start of relaxation phasea (end of isotonic)
    T_loop(2) = Params(5); % Tme for end of relaxation phase 
    passive = Params(6); % % Boolean for presence of passive force

    % *****************************************************
    % Specifying the three phases in the simulation
    switch Phase
        case 'isometric'
            F_after = Afterload;
            dSL = 0;
            F_passive = passiveForces(SL,passive);
        case 'isotonic'
            F_after = Afterload;
            dSL = (IntegF + viscosity*(SL_rest - SL))/mass;
            F_passive = passiveForces(SL,passive);
    end
   
    % Prevent over extension
    if SL > preload_SL
        dSL = 0;
    end

    %% *****************************************************    
    % Ca binding to troponin
    
    % Call function to get Ca
    Cai = getCai(t); %uM
    
    % convert pH to mM
    H = 10^(-pH)*1e3; % H concentration in mM
    
    % Ca binding to troponin C
    konT = kon*1*Q_kon^((TmpC-37)/10);
    konT_app = konT*(kdHCa^m + Href^m)/(kdHCa^m + H^m);
    
    koffLT = koffL*1*1*Q_koff^((TmpC-37)/10); % Intact as opposed to skinned
    koffHT = koffH*1*1*Q_koff^((TmpC-37)/10);
    
    d_TropCaL = konT_app*Cai*(1-TropCaL) - koffLT*TropCaL;
    d_TropCaH = konT_app*Cai*(1-TropCaH) - koffHT*TropCaH;  
    
    
    %% *****************************************************
    % Thin filament activation rates
    
    % Sarcomere geometry
    sovr_ze = min(L_thick/2, SL/2);
    sovr_cle = max(SL/2 - (SL-L_thin),L_hbare/2);
    L_sovr = sovr_ze - sovr_cle; % Length of single overlap region
    
    % Overlap fraction for thick filament
    sov_thick = L_sovr*2/(L_thick - L_hbare);
    % Overlap fraction for thin filament
    sov_thin = L_sovr/L_thin;
    
    TropReg = (1-sov_thin)*TropCaL + sov_thin*TropCaH;
    permtot = (1/(1+(perm50/TropReg)^n_perm))^0.5;
    permtot_p_n = min(100,1/permtot);
    
    % Rate constants governing the transition btw Permissive and Non
    kn_pT = kn_p*permtot*Q_kn_p^((TmpC-37)/10);
    kp_nT = kp_n*permtot_p_n*Q_kp_n^((TmpC-37)/10);

    
    %% *****************************************************
    % Cross-bridge cycling rates
    
    % Pxb to XBpreR
    fappT = fapp*Xsp*Q_fapp^((TmpC-37)/10);

    % Pi-dependent transition XBpreR to Pxb
    gappslmd = 1 + (1-sov_thick)*gslmod;
    gappT = gapp*gappslmd*Xsp*Q_gapp^((TmpC-37)/10);
    gappT_true = gappT/Pi_ref;  % True first order rate constant
    
    % XBpreR to XBpostR
    hfmd = exp(-sign(x_XBpreR)*hfmdc*(x_XBpreR/x0)^2);
    hfT = hf*hfmd*Xsp*Q_hf^((TmpC-37)/10);
    
    % H-dependent transition XBpostR to XBpreR
    hbT = hb*Xsp*Q_hb^((TmpC-37)/10);
    hbT_true = hbT/Href;
    hbT_app = ((kdADP+MgADP_ref)/MgADP_ref)*(MgADP/(kdADP+MgADP))*hbT_true;  

    % MgATP-dependent transition from XBpostR to Pxb
    if (x_XBpostR < x0)
        gxbmd = exp(sigma_p*((x0-x_XBpostR)/x0)^2);
    else
        gxbmd = exp(sigma_n*((x0-x_XBpostR)/x0)^2);
    end
    
    gxbT = gxb*max(gxbmd,1)*Xsp*Q_gxb^((TmpC-37)/10);
    gxbT_true = gxbT/MgATP_ref;
    gxbT_app = ((kdADP+MgADP_ref)/(kdADP+MgADP))*gxbT_true;

    % Pxb to XBpostR - Introduced for thermodynamic efficiency
    G0 = -29600 + log(10)*R*(TmpC+273)*(-log10(1e-7));
    K_MgATP = exp(-G0./(R.*(TmpC+273)))*1e6;  % 1e6 to convert from M2 to mM2
    fxbT = (kdADP*fappT*hfT*gxbT_true)/(gappT_true*hbT_true*K_MgATP);
    fxb = (kdADP*fapp*hf*(gxb/MgATP_ref))/((gapp/Pi_ref)*(hb/Href)*K_MgATP); % Used for calculating max
    
    ap1 = fappT;
    ap2 = hfT;
    ap3 = MgATP*gxbT_app;
    am1 = Pi*gappT_true;
    am2 = H*hbT_app;
    am3 = fxbT;
    
    %% *****************************************************
    %  Cross_bridge transitions
    
    % Update all RUs   
    Pxb = 1 - Nxb - XBpreR - XBpostR;
    d_Nxb = -kn_pT*Nxb + kp_nT*Pxb;
    
    d_XBpreR = ap1*Pxb - am1*XBpreR - ap2*XBpreR + am2*XBpostR;
    d_XBpostR = ap2*XBpreR + am3*Pxb - am2*XBpostR - ap3*XBpostR;
    
    ATPase = rho*phi*sov_thick*(ap3*XBpostR - am3*Pxb);
    
    %% *****************************************************
    % Mean strain of strongly-bound states
           
    % Steady State occupancies of the bound states - Duty fractions
    Sum_duty = am3*am2 + ap3*ap1 + am2*ap1 + ap1*ap2 + am3*am1 + am3*ap2...
        + ap2*ap3 + am3*am1 + ap3*am1;

    dutyPreR = (am3*am2 + ap3*ap1 + am2*ap1)/Sum_duty;
    dutyPostR = (ap1*ap2 + am3*am1 + am3*ap2)/Sum_duty;
    
    % No shortening during isotonic period
    % This is to hold the SL at max contraction to get a loop
    if (t>T_loop(1)) & (t<T_loop(2)) & loop
        dSL = 0;
    end
    
    % Rate of change of the average distortions
    d_x_XBpreR = dSL/2 + (Psi/dutyPreR)*(-ap1*x_XBpreR) + am2*(x_XBpostR-x0-x_XBpreR);
    d_x_XBpostR = dSL/2 + (Psi/dutyPostR)*(ap2*(x_XBpreR + x0 - x_XBpostR));

    % Compute the active force
    F_active = sov_thick*(x_XBpreR*XBpreR + x_XBpostR*XBpostR);

    % Maximal state occupancies under optimal conditions
    max_XBpreR = (fapp*(hb+gxb)+fxb*fapp)/(gxb*hf + fapp*hf + gapp*hb + ...
        gapp*gxb + fapp*hb + fapp*gxb + fxb*(hb+gapp+hb));

    max_XBpostR = (fapp*hf+fxb*(gapp+hb))/(gxb*hf + fapp*hf + gapp*hb + ...
        gapp*gxb + fapp*hb + fapp*gxb + fxb*(hb+gapp+hb));

    % Factor to normalise force
    FnormD = x0*max_XBpostR;
    
    % Normalised Active force
    Fnorm = F_active/FnormD;
    
    % Normalised Passive force
    F_passive = passiveForces(SL,passive);
    
    % No shortening during isotonic period
    % This is to hold the SL at max contraction to get a loop
    if (t>T_loop(1)) & (t<T_loop(2)) & loop
        dSL = 0;
    end
    
    % Difference in force
    d_Force =  F_after -  Fnorm - F_passive;
    
    % Total normalised force
    F_total = Fnorm + F_passive;
    
    % Used in Fevents script 
    F_net = F_total - F_after;
     
    %% *****************************************************
    % Assembling the derivative vector
 
    dy = [d_Nxb; d_XBpreR; d_XBpostR; d_x_XBpreR;...
        d_x_XBpostR; d_TropCaL; d_TropCaH; d_Force; dSL];
    
    