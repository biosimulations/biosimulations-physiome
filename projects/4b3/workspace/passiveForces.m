
% Function to calculate the passive force
% Passive force function is fitted to passive data presented in Fig 2D

function PF = passiveForces(SL, passive)

    if passive

        x = SL/2.3;
        SHAM = [-1212.77 4497.99 -5565.60 2298.68]/110;
        PF = SHAM(1) + SHAM(2).*x + SHAM(3).*x.^2 + SHAM(4).*x.^3;

    else
        
        PF = 0;
end