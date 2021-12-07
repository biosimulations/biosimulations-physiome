function [Vsav,is,concs,APs,vars]=Varela_CanineAtrial_Model(BCL,nbeats,celltype,drug,remod,extrams)
% Copyright: Marta Varela, atrial dog electrophysiology model
% See Varela et al, PLoS Comp Bio, 2016 (http://dx.doi.org/10.1371/journal.pcbi.1005245)
% Email: marta.varela@kcl.ac.uk

% INPUTS:
% BCL is the basic cycle length
% nbeats is the number of stimuli to apply
% celltype is the type of cell
% 1: RA, 2: LA, 3: BB/CT, 4: PV
% drug is the index of the drug used (same as in C code)
% remod is the degree of remodelling (0: no remodelling, 1: (moderate) 7-day
% remodelling; 2: (severe) 21-day remodelling)
% extrams: is the number of extra ms for the code to run after the last
% stimulus (default: 0)

% OUTPUTS:
% Vsav is the transmembrane potential saved every ms
% is is a vector of ionic currents through time (every ms)
% concs is a vector of ionic concentrations through time (every ms)
% APs is a structure with action potential proprties (commented out)
% vars is the end-status of each state variable


 vcell=  20100.0 ;     % cell volume, um3 */
 vi = (vcell*0.68);      % intracellular volume, 13668 um3 */
 vup = (0.0552*vcell);   % volume of sarcoplasmic uptake compartment, 1109.52 um3 */
 vrel= (0.0048*vcell);  % volume of sarcoplasmic uptake compartment, 96.48 um3 */
 T= (310.0);              % (baseline) temperature, 37 deg Celsius = 310 K */
 Cm= 100.0  ;        % membrane capacitance, pF
 F= 96.4867  ;        % Faraday constant (charge per mol), coul/mmol */
 R= 8.3143    ;       % universal gas constant, J K-1 mol-1 */
 FRT= (F/(R*T));
 Fvi =(F*vi);


  nai=11.75;			%10.0 ? initial Na+ concentration, mM from table 2 of paper (denominator in Nernst)
  cai=1.024e-4;			% initial Ca2+ concentration, mM from table 2 of paper
  ki=138.4;				% initial K+ concentration, mM from table 2 of paper
  cli=29.26;			% initial Cl- concentration, mM from table 2 of paper
  caup=1.502;			% initial Ca2+ in uptake SR concentration, mM from table 2 of paper
  carel=1.502;			% initial Ca2+ in release SR, mM from table 2 of paper

  V=-85.53;				% resting potential, mV from table 2 of paper
  m=0.001972;			% INa activation variable
  hh=0.9791;				% INa fast inactivation variable
  jj=0.9869;				% INa slow inactivation variable
  d=4.757e-6;			% ICa activation variable
  f=0.9999;				% ICa V-dependent inactivation variable
  fca=0.7484;			% ICa Ca2+-dependent inactivation variable
  %qca=0.0;				% Ca2+flux-dependent activation gating variable for ICaCl
  xr=7.433e-7;			% IKr activation variable
  xs=0.01791;			% IKs activation variable
  xa=1e-5;              % IKAch activation variable
    
    
  oa=0.07164;			% Ito activation variable
  oi=0.9980;			% Ito inactivation variable
  ua=0.05869;			% IKurd activation variable
  ui=0.9987;			% Ikurd inactivation variable
  uu=0.0;				% activation gating variable for Irel
  vv=1.0;				% Ca2+ flux-dependent inactivation variable for Irel
  w=0.9993;				% V-dependent inactivation variable for Irel
  cmdn=1.856e-3;		% calmodulin concentration in myoplasm, mM
  trpn=7.022e-3;		% troponin concentration in myoplasm, mM
  csqn=6.432;			% sequestrin concentration in myoplasm, mM
 
  ndtperms = 200;		 	% determines V evaluation temporal evolution
  stiminten=-29.0;        % intensity of stimulus current
  stimdur=2;                % duration of stimulus (ms)
  dvdtmax=0;                % maximum dvdt
  
  if ~exist('extrams','var')
      extrams=0;
  end
  
  nms=BCL*nbeats+extrams;			% maximum number of miliseconds
  Vsav=zeros(1,nms);
  is=zeros(15,nms);
  concs=zeros(10,nms);
  dt = 1.0/ndtperms;		% time step for V=V+dt*dvdt; 

  trpnbar = 0.35;   
  cmdnbar = 0.045;			
  csqnbar = 10.0;  
  kmnai = 10.0;				% mM
  kmko = 1.5;				% mM         
  kmcap = 0.0005;			% mM */	
  kmnalr = 87.5;			% mM */               
  kmcalr = 1.38;			% mM */
  ksatlr = 0.1;
  gammalr = 0.35;
  kmup = 6e-4;
  iupbar = 0.0035;
  caupmax = 27.0;
  tautr = 180.0;
  grelbar = 8.0;			% ms-1, max release rate*/ 

  kc = 5.4;             % K+ baseline concentration ?, mM (numerator in Nernst)
  nac = 140.0;            % Na+ baseline concentration ?, mM 
  cac = 1.8;            % Ca2+ baseline concentration ?, mM ?? used 2 for( wilders ? 
  clc = 132;

  % non-cell-type-dependent currents
  gna = 7.8;
  gbna = 1.0e-5;
  gbca = 1.0e-5;
  gkur = 0.0115;

  icapbar = 0.275;
  knacalr = 1600.0;
  inakbar = 0.6;
  
  % LA currents 
  gcaL=0.34;
  gk1=0.1;
  gto=0.096;
  gbcl=8.0e-4;
  gkr=0.0145;
  gks=0.052;
  gkach=0.0045;
  
  % CARDIAC REGION
  switch (celltype) 
  case 1 % RA
      gkr=0.00899;
      disp('RA')
  case 3 % BB
	  gcaL=0.58;
	  gkr=0.00899;
      disp('BB-CT')
  case 4 %PV
	  gcaL=0.255;
	  gk1=0.036;
	  gto=0.07104;
	  gbcl=0.0055;
	  gkr=0.022475;
	  gks=0.0832;
	  gkach=0.0065;
      disp('PV')
  case 2 % LA
      disp('LA')
  otherwise
      error('Unknown cell type.');
  end

  % DEGREE OF REMODELLING
  switch remod
  case 1   % moderate remodelling
      disp('Moderate remodelling')
	  gna=gna*0.90; % new value
	  gcaL=gcaL*0.47;
	  gk1=gk1*1.80;
	  gto=gto*0.54;
	  knacalr=knacalr*1.64;
	  gkach=gkach*1.8;
 case 2   % severe remodelling
      disp('Severe remodelling')
	  gna=gna*0.80;  % new value
	  gcaL=gcaL*0.31;
	  gk1=gk1*2.57;
	  gto=gto*0.38;
	  knacalr=knacalr*2.34;
	  gkach=gkach*2.57;
  case 0
      disp('No remodelling.')
  otherwise
      error('Unknown remodelling.')  
  end

  %DRUG IN USE
  switch drug 
      case 1   % Vernakalant 10
          disp('Vernakalant 10')
          gkur=gkur*0.55;
          gto=gto*0.56;
          gkr=gkr*0.68;
          %gna=gna*0.90; %new
          gkach=gkach*0.54;
      case 2   % Vernakalant 30
          disp('Vernakalant 30')
          gkur=gkur*0.30;
          gto=gto*0.30;
          gkr=gkr*0.41;
          gna=gna*0.90; %gna=gna*0.70;
          gkach=gkach*0.22;
      case 7 %  Amiodarone 5
          disp('Amiodarone 5')
          gks=gks*0.80;
          gkr=gkr*0.50;
          gna=gna*0.90;
          %gna=gna*0.60;
          gkach=gkach*0.22;
          gcaL=gcaL*0.50;
          gk1=gk1*0.70;
      case 9 % Amiodarone 10
          disp('Amiodarone 10')
          gks=gks*0.80*0.7;
          gkr=gkr*0.50*0.7;
          gna=gna*0.90*0.9;
          gkach=gkach*0.22;
          gcaL=gcaL*0.50*0.7;
          gk1=gk1*0.70*0.7;
      case 12 % Amiodarone 10 with ICaL off
          disp('Amiodarone 10 - no ICaL')
          gks=gks*0.80*0.7;
          gkr=gkr*0.50*0.7;
          gna=gna*0.90*0.9;
          gkach=gkach*0.22;
          gk1=gk1*0.70*0.7;
      case 13 % Amiodarone 10 with IK1 off
          disp('Amiodarone 10 - no IK1')
          gks=gks*0.80*0.7;
          gkr=gkr*0.50*0.7;
          gna=gna*0.90*0.9;
          gkach=gkach*0.22;
          gcaL=gcaL*0.50*0.7;
      case 14 % Vernakalant 30 - with ICaL
          disp('Vernakalant 30 - with ICaL')
          gkur=gkur*0.30;
          gto=gto*0.30;
          gkr=gkr*0.41;
          gna=gna*0.70;
          gkach=gkach*0.22;
          gcaL=gcaL*0.60;
      case 15 % Vernakalant 30 - with IK1
          disp('Vernakalant 30 - with IK1')
          gkur=gkur*0.30;
          gto=gto*0.30;
          gkr=gkr*0.41;
          gna=gna*0.70;
          gkach=gkach*0.22;
          gk1=gk1*0.60;
      otherwise
          disp('No drug');
   end
    
    
    sigma = (exp(nac/67.3)-1.0)/7.0;   
    nac3=power(nac,3.0);
    CNaCa2=1/((power(kmnalr,3.0)+power(nac,3.0))*(kmcalr+cac));
   
       % apply stimulation every BCL period for stimdur iterations
  istimv=zeros(1,nms);
  istimv(logical(mod(0:(nbeats+1)*BCL-1,BCL)<stimdur))=stiminten;
  istimv=circshift(istimv,50);
  
  for ms=0:1:nms-1  
     istim=istimv(ms+1);
     for step=0:1:ndtperms-1   
     % compute equilibrium Vusing Nernst
		Ek = 26.71*log(kc/ki );
		Ena = 26.71*log(nac/nai );
		Eca = 13.35*log(cac/cai );    
        Ecl = 26.71*log(cli /clc);

        % compute currents 
		ina = gna*power(m ,3.0)*hh *jj *(V-Ena);   
		ito = gto*power(oa ,3.0)*oi *(V-Ek);   
        
        fkur = 1.0+3.0/(1.0+exp((V-14.0)/-6.0));
		ikur = gkur*fkur*power(ua ,3.0)*ui *(V-Ek);
        
        if (celltype ==2||celltype ==4)   % LA or PV
            rect = 0.6+1.0/(0.5+0.5*exp((V+8.0)/24.4)); 
        else   % RA or BB
            rect =  0.6+1.0/(0.5+exp((V-26.0)/20.4));
		end
            
		ikr = gkr*rect*xr *(V-Ek);         
		iks = gks*xs *xs *(V-Ek);
		icaL = gcaL*d *f *fca *(V-60.0);  
        
        if (celltype ==4)   % PV
            ik1 = gk1*(V-Ek)/(0.66+exp(0.078*(V-Ek-18.0)));
        else  
            ik1 = gk1*(V-Ek)/(1.0+exp(0.072*(V-Ek)));
		end
        
        recta=1.0/(0.1+exp(0.078*(V-Ek-65.0)));
        ikach= gkach*xa *(V-Ek)*recta;

        ibna = gbna*(V-Ena);
        ibca = gbca*(V-Eca); 

        fnak = 1.0/(1.0+0.1245*exp(-0.1*V*FRT)+0.0365*sigma*exp(-V*FRT));  
        inak = inakbar*fnak*kc/(kc+kmko)/(1+power((kmnai/nai ),1.5));     

        icap = icapbar*cai /(cai +kmcap); 

        expnaca=exp((gammalr-1)*V*FRT);
		inaca = knacalr*CNaCa2/(1+ksatlr*expnaca)*(nai *nai *nai *cac*...
            exp(V*gammalr*FRT)-nac3*cai *expnaca); 
        
        ibcl = gbcl*(V-Ecl);  
              
        % update concentrations of each ion
		naidot = Cm*(-3*inak-3*inaca-ibna-ina)/(Fvi);
        kidot = Cm*(2*inak-ik1-ito-ikur-ikr-iks-ikach)/(Fvi);
        clidot = Cm*ibcl/(Fvi);

		%dynamic buffers  
		cmdndot = 200.0*cai *(1.0-cmdn /cmdnbar) - 0.476*cmdn /cmdnbar;
		trpndot =  78.4*cai *(1.0-trpn /trpnbar) - 0.392*trpn /trpnbar;
		csqndot = 0.48*carel *(1.0-csqn /csqnbar) - 0.4*csqn /csqnbar;
		% above buffer derivatives in units: per milliseconds */

		cmdn  = cmdn  + dt*cmdndot*cmdnbar;      
		trpn  = trpn  + dt*trpndot*trpnbar;
		csqn  = csqn  + dt*csqndot*csqnbar;
		% above bound buffer units: mM */

		irel = grelbar*uu*uu *vv *w *(carel -cai );          

		iup = iupbar/(1.0+kmup/cai );
		iupleak = iupbar*caup /caupmax;     
		itr = (caup -carel )/tautr;      
          
		caidot = Cm*(2.0*inaca-icap-icaL-ibca)/(2.0*Fvi) + (iupleak-iup)*...
            vup/vi+irel*vrel/vi - trpnbar*trpndot - cmdnbar*cmdndot;
		caupdot = iup-itr*vrel/vup-iupleak;
		caup  = caup  + dt*caupdot;
		careldot = itr-irel-31.0*csqndot;
		carel  = carel  + dt*careldot;

        % update all concentrations */
        nai  = nai  + dt*naidot;
        ki  = ki  + dt*kidot;
        cai  = cai  + dt*caidot;
        cli  = cli  + dt*clidot;

        % update ina m gate */
        a = 0.32*(V+47.13)/(1-exp(-0.1*(V+47.13)));
        if (abs(V+47.13) < 1e-10)  
            a = 3.2;
        end
        b = 0.08*exp(-V/11);
        tau = 1.0/(a+b);
		inff = a*tau;
        m  = inff + (m -inff)*exp(-dt/tau);
          
        % update ina hh and jj gates */
        if (V >= -40.0)       
			a  = 0.0;
            b = 1.0/(0.13*(1.0+exp((V+10.66)/-11.1)));
        else   
			a = 0.135*exp((V+80.0)/-6.8);
            b = 3.56*exp(0.079*V)+3.1e5*exp(0.35*V);
		end
        tau = 1.0/(a+b);
		inff = a*tau;
        hh  = inff + (hh -inff)*exp(-dt/tau);
        if (V >= -40.0)   
            a  = 0.0;
            b = 0.3*exp(-2.535e-7*V)/(1.0+exp(-0.1*(V+32.0)));
        else   
            a = (-1.2714e5*exp(0.2444*V)-3.474e-5*exp(-0.04391*V))*(V+37.78)/(1.0+exp(0.311*(V+79.23)));
            b = 0.1212*exp(-0.01052*V)/(1+exp(-0.1378*(V+40.14)));
		end
        tau = 1.0/(a+b);
		inff = a*tau;
        jj  = inff + (jj -inff)*exp(-dt/tau);
          
        % update oa ito gate */
        inff = power((1.0+exp((V-12.0)/-11.5)),(-1.0/3.0));
        tau = 0.4/(exp((V-15.0)/20.0));
        oa  = inff + (oa -inff)*exp(-dt/tau);

        % update oi ito gate */
        inff = 1.0/(1.0+exp((V+31.0)/6.45));    
        a = 1.0/(1.2+exp((V +95.2)/5.85));      
        b = 1.0/(9.54+exp((V -48.0)/-20.0));  
        tau = 1.0/(a+b); 
        oi  = inff + (oi -inff)*exp(-dt/tau);

        % update ua ikur gate */
        a = 1.47/(exp((V +33.20)/-30.63)+exp((V -27.6)/-30.65));
        b = 0.42/(exp((V +26.64)/2.49)+exp((V +44.41)/20.36));
        tau = 1.0/(a+b); 
        inff = power((1+exp((V +2.81)/-9.49)),(-1.0/3.0));
        ua  = inff + (ua -inff)*exp(-dt/tau);

        % update ui ikur gate */
        a = 1.0/(21.0+exp((V -185.0)/-28.0));
        b = exp((V -158.0)/16.0);
        tau = 1.0/(a+b); 
        inff = 1.0/(1.0+exp((V -99.45)/27.48));
        ui  = inff + (ui -inff)*exp(-dt/tau);

        % update the xr ikr gate */
        a = 0.04*(V -248.0)/(1.0-exp((V -248.0)/-28.0));
        b = 0.028*(V +163.0)/(exp((V +163.0)/21.0)-1.0);
        tau = 1.0/(a+b);
        inff = 1.0/(1.0+exp((V +7.654)/-5.377));  
        xr  = inff + (xr -inff)*exp(-dt/tau);

        % update the xs iks gate */
        a = 0.00001*(V+28.5)/(1.0-exp((V+28.5)/-115.0));
        b = 0.00023*(V+28.5)/(exp((V+28.5)/3.3)-1.0);
        if (abs(V+28.5) < 1e-10)  
            a = 0.00115; 
            b = 0.000759;
		end
        tau = 1.0/(a+b);
        inff = sqrt(1.0/(1.0+exp((V-13.0)/-12.0)));
	    xs  = inff + (xs -inff)*exp(-dt/tau);

        % update icaL d gate */
        inff =  1.0/(1.0+exp((-V-2.0)/5.0));
        tau = (1.0/(1.0+exp((V+10.0)/-6.24)))*(1.0-exp((V+10.0)/-6.24))/(0.035*(V+10.0));
        if (abs(V-10)<1e-10)  
            tau = 0.763;
		end
        d  = inff + (d -inff)*exp(-dt/tau);

        % update icaL f gate */
        tau = 400.0/(1+4.5*exp(-0.0007*power(V-9,2.0)));
        inff = 1.0/(1.0+exp((-V-34.0)/-6.3));      
        f  = inff + (f -inff)*exp(-dt/tau);

        % update icaL fca gate 
        inff = 0.29+0.8/(1.0+exp((cai -1.2e-4)/0.00006));                           
        tau = 2.0;
        fca  = inff + (fca -inff)*exp(-dt/tau);   
        
        % update the SR gating variables */
        % caflux is expected in umoles/ms, hence the factor of 1000 */
        % 1e-15 is used to scale the volumes~ */ 
        
        % update irel uu gate
        caflux = 1e3*(1e-15*vrel*irel-1e-15*Cm*(0.5*icaL-0.2*inaca)/(2.0*F));
        inff = 1.0/(1.0+exp(-(caflux-3.4175e-13 )/13.67e-16));
        tau = 11.2;
        uu  = inff + (uu -inff)*exp(-dt/tau); 
        
        % update irel vv gate
        inff = 1.0-1.0/(1.0+exp(-(caflux-6.835e-14)/13.67e-16));
        tau = 1.91+2.09/(1.0+exp(-(caflux-3.4175e-13)/13.67e-16));  
        vv  = inff + (vv -inff)*exp(-dt/tau); 
        
        % update irel w gate
        inff = 1.0-1.0/(1.0+exp(-(V-40.0)/17.0));
        tau = 6.0*(1.0-exp(-(V-7.9)/5.0))/(1.0+0.3*exp(-(V-7.9)/5.0))/(V-7.9);
	    if (abs(V-7.9) < 1e-10)  
            tau = 0.9231;
		end
        w  = inff + (w -inff)*exp(-dt/tau);
         
        % update the ikach xa gate
        inff=1.0/(1.0+exp((-93.0-V)/-15.2));
        tau=360.0+130.0*(1.0-exp(-(V+130.0)/50.0));
        xa  = inff + (xa -inff)*exp(-dt/tau);
        
		% update membrane voltage                                 
		dvdt = -(ina+icaL+icap+ik1+ito+...
            ikur+ikr+iks+ibna+ibca+...
            inak+inaca+istim+ikach+ibcl);
        V = V + dt*dvdt;   
        if ms>BCL*(nbeats-1)
            if dvdt>dvdtmax
                dvdtmax=dvdt;
            end
        end
    end % end of step loop
        
     Vsav(ms+1)=V;
     is(1,ms+1)=ina;
     is(2,ms+1)=icaL;
     is(3,ms+1)=icap;
     is(4,ms+1)=ik1;
     is(5,ms+1)=ito;
     is(6,ms+1)=ikur;
     is(7,ms+1)=ibcl;
     is(8,ms+1)=ikr;
     is(9,ms+1)=iks;
     is(10,ms+1)=ibna;
     is(11,ms+1)=ibca;
     is(12,ms+1)=inaca;
     is(13,ms+1)=inak;
     is(14,ms+1)=0;
     is(15,ms+1)=ikach;
     
     concs(1,ms+1)=nai;
     concs(2,ms+1)=ki;
     concs(3,ms+1)=cai;
     concs(4,ms+1)=cli;
     concs(5,ms+1)=caup;
     concs(6,ms+1)=carel;
        
 end % end of ms loop
 
vars(1)=m;
vars(2)=hh;
vars(3)=jj;
vars(4)=d;
vars(5)=f;
vars(6)=fca;
vars(7)=xr;
vars(8)=xs;
vars(9)=oa;
vars(10)=oi;
vars(11)=ua;
vars(12)=ui;
vars(13)=uu;
vars(14)=vv;
vars(15)=w;
vars(16)=cmdn;
vars(17)=trpn;
vars(18)=csqn;
vars(19)=caup;
vars(20)=carel;
vars(21)=nai;
vars(22)=cai;
vars(23)=ki;
vars(24)=V;
vars(25)=xa;
vars(26)=cli;
vars=vars';

% disp(celltype)
APs=computeAPspecs(Vsav(BCL*(nbeats-1)+1:BCL*nbeats));
APs.Vmax=dvdtmax;
CaT=1e6*(max(concs(3,BCL*(nbeats-1)+1:BCL*nbeats))-concs(3,BCL*nbeats));
CaMax=1e6*(max(concs(3,BCL*(nbeats-1)+1:BCL*nbeats)));
APs.CaT=CaT;
disp(['APD90:' num2str(APs.APD90) ' ms'])
disp(['APD50:' num2str(APs.APD50) ' ms'])
disp(['RMP:' num2str(APs.RMP,'%2.1f') ' mV'])
disp(['Vmax:' num2str(APs.Vmax,'%2.0f') ' V/s'])
disp(['APA:' num2str(APs.APA,'%2.1f') ' mV'])
disp(['CaT:' num2str(CaT,'%2.0f') ' nM'])
disp(['Ca Max:' num2str(CaMax,'%2.0f') ' nM'])

% figure
% subplot(2,1,1)
showper=1;
hold all
plot(1:BCL*showper,Vsav(BCL*(nbeats-showper)+1-10:BCL*nbeats-10),'-','LineWidth',3)
axis([0 BCL*showper -100 50])
set(gca,'FontSize',14)
ylabel('V (mV)')
xlabel('Time (ms)')
grid on

% subplot(2,1,2)
% hold all
% plot(1:BCL,1e6*concs(3,BCL*(nbeats-1)+1:BCL*nbeats),'-','LineWidth',3) % cai
% plot(1:BCL,1e2*concs(5,BCL*(nbeats-1)+1:BCL*nbeats),':','LineWidth',3) % caup
% plot(1:BCL,1e2*concs(6,BCL*(nbeats-1)+1:BCL*nbeats),'-.','LineWidth',3) % carel
% ylabel('[Ca^{2+}]_i (nM)')
% axis([0 600 0 800])