/************************************************************************
Rabbit Purkinje cell model, developed by Rakan Sleiman & Oleg Aslanidi
Results are published in Aslanidi et al, Biophys J. 2010; 98(11): 2420-31
Created: 25-02-2009, Updated: 14-06-2012. Email: oleg.aslanidi@kcl.ac.uk
************************************************************************/

#include <cmath>
#include <cstdio>
#include <iostream>
#include <fstream>

using namespace std;

/***************Simulation constants**********************/
//#define bcl	350
double bcl;
#define beats	20
#define S2	bcl
#define HT	0.005         /* ms */

/*****************Basic physical constants****************/

#define RTF 26.7081
const float Faraday=96487;
#define zCa 2.0
#define zNa 1.0
#define zK 1.0

#define PNaK 0.01833    /* IKs - for determining EKs*/
#define fCaKd 7.0  	/* uM */
/***************Declarations**************************/

double INa,INal;
double IKs, IKr, IK1, IKp, ITO_slow, ITO_fast, ITO;
double ICa,ICaT,ICaL, ICl, IClB,ICaB;
double INaB,IKB, INaK, ISLCaP,INaCaX,IKp_Kp;
double Iion;
double Istim;

double EK, ECl,ENa, ECa, EKs;

double V, m, h, j,ml,hl, x,x_,y_,y2_, X2, d, f,f2,b,g,xr,a, i, xto_slow, yto_slow, r_slow, xto_fast, yto_fast,fCa;
double NaIono ,NaIoni,CaIono ,KIono ,KIoni,ClIono ,ClIoni;

double m_inf, h_inf, j_inf, alpha_m, beta_m, alpha_h, beta_h, alpha_j, beta_j, tau_m, tau_h, tau_j;
double alpha_ml,beta_ml,ml_inf,tau_ml,tau_hl,hl_inf;
double d_inf, f_inf, tau_d, tau_f;
double b_inf, g_inf, tau_b, tau_g, alpha_b, beta_b, alpha_g, beta_g;
double x_inf, tau_x;
double xr_inf, tau_xr, GKr, r_inf;
double alpha_k1, beta_k1, k1_inf;                                                      /* IK1 */
double a_inf, i_inf, tau_i;
double x__inf, tau__x, alpha__x, beta__x, alpha__y,alpha__y2,beta__y2, beta__y, y__inf,y2__inf, tau__y,tau__y2;

double SLGKs,pCa;
double GNa;
double GNal;
double GCaL,GCaT;
double GKr_factor;
double GK1;
double Gto;
double GCl;
double GClB;
double GCaB;
double GNaB;
double GKB;

double INaK_Kmr;
double INaK_Hill;
double sigma, fNaK, INaK_Vmf, INaK_Kmf;

//canine PF model INaCa paramters
const double frdy = 96485;		// Faraday's constant (C/mol)
const double R = 8314;			// Universal gas Constant (J/kmol*K)
const double temp = 310;		// temperature (K)
const double inacamax = 4.5;		// maximal inaca (uA/uF)
const double kmcaact = 0.000125;	// half-saturation concentration for cai activation (mM)
const double kmnai1 = 12.3;		// half-saturation concentration for nai (mM)
const double kmnao = 87.5;		// half-saturation concentration for NaIono  (mM)
const double kmcai = 0.0036;		// half-saturation concentration for cai (mM)
const double kmcao = 1.3;		// half-saturation concentration for cao (mM)
const double nu = 0.35;			// position of energy barrier for inaca
const double ksat = 0.27;		// saturation factor for inaca at negative potentials

double allo;				// Ca2+ dependent allosteric activation factor for inaca
double num;				// numerator (used to simplify inaca equation)
double denommult;			// denominator multiplier (used to simplify inaca equation)
double denomterm1;			// term 1 of denominator (used to simplify inaca equation)
double denomterm2;			// term 2 of denominator (used to simplify inaca equation)
double deltaE;				// electrochemical factor for inaca
// end of canine parameters

double ISLCaP_Hill;
double ISLCaP_Vmf,ISLCaP_Kmf;


/*****************************Ca Handling parameters******************************/

//------------------------------------------------------------------------------
// Constants
//------------------------------------------------------------------------------
int ii;

double Ca_buffer___Bmax_Calsequestrin;   // millimolar
double Ca_buffer___Bmax_SLB_SL;   // millimolar
double Ca_buffer___Bmax_SLB_jct;   // millimolar
double Ca_buffer___Bmax_SLHigh_SL;   // millimolar
double Ca_buffer___Bmax_SLHigh_jct;   // millimolar
double Ca_buffer___koff_Calsequestrin;   // per_millisecond
double Ca_buffer___koff_SLB;   // per_millisecond
double Ca_buffer___koff_SLHigh;   // per_millisecond
double Ca_buffer___kon_Calsequestrin;   // per_millimolar_per_millisecond
double Ca_buffer___kon_SL;   // per_millimolar_per_millisecond


double Jleak_SR___KSRleak;   // per_millisecond
double Jpump_SR___H;   // dimensionless
double Jpump_SR___Kmf;   // millimolar
double Jpump_SR___Kmr;   // millimolar
double Jpump_SR___Q10_SRCaP;   // dimensionless
double Jpump_SR___V_max;   // millimolar_per_millisecond
double Jrel_SR___EC50_SR;   // millimolar
double Jrel_SR___HSR;   // dimensionless
double Jrel_SR___Max_SR;   // dimensionless
double Jrel_SR___Min_SR;   // dimensionless
double Jrel_SR___kiCa;   // per_millimolar_per_millisecond
double Jrel_SR___kim;   // per_millisecond
double Jrel_SR___koCa;   // per_millimolar2_per_millisecond
double Jrel_SR___kom;   // per_millisecond
double Jrel_SR___ks;   // per_millisecond

double cytosolic_Ca_buffer___Bmax_Calmodulin;   // millimolar
double cytosolic_Ca_buffer___Bmax_Myosin_Ca;   // millimolar
double cytosolic_Ca_buffer___Bmax_Myosin_Mg;   // millimolar
double cytosolic_Ca_buffer___Bmax_SRB;   // millimolar
double cytosolic_Ca_buffer___Bmax_TroponinC;   // millimolar
double cytosolic_Ca_buffer___Bmax_TroponinC_Ca_Mg_Ca;   // millimolar
double cytosolic_Ca_buffer___Bmax_TroponinC_Ca_Mg_Mg;   // millimolar
double cytosolic_Ca_buffer___koff_Calmodulin;   // per_millisecond
double cytosolic_Ca_buffer___koff_Myosin_Ca;   // per_millisecond
double cytosolic_Ca_buffer___koff_Myosin_Mg;   // per_millisecond
double cytosolic_Ca_buffer___koff_SRB;   // per_millisecond
double cytosolic_Ca_buffer___koff_TroponinC;   // per_millisecond
double cytosolic_Ca_buffer___koff_TroponinC_Ca_Mg_Ca;   // per_millisecond
double cytosolic_Ca_buffer___koff_TroponinC_Ca_Mg_Mg;   // per_millisecond
double cytosolic_Ca_buffer___kon_Calmodulin;   // per_millimolar_per_millisecond
double cytosolic_Ca_buffer___kon_Myosin_Ca;   // per_millimolar_per_millisecond
double cytosolic_Ca_buffer___kon_Myosin_Mg;   // per_millimolar_per_millisecond
double cytosolic_Ca_buffer___kon_SRB;   // per_millimolar_per_millisecond
double cytosolic_Ca_buffer___kon_TroponinC;   // per_millimolar_per_millisecond
double cytosolic_Ca_buffer___kon_TroponinC_Ca_Mg_Ca;   // per_millimolar_per_millisecond
double cytosolic_Ca_buffer___kon_TroponinC_Ca_Mg_Mg;   // per_millimolar_per_millisecond
double ion_diffusion___A_SL_cytosol;   // cm2
double ion_diffusion___A_jct_SL;   // cm2
double ion_diffusion___D_Ca_SL_cytosol;   // dm2_per_second
double ion_diffusion___D_Ca_jct_SL;   // dm2_per_second
double ion_diffusion___D_Na_SL_cytosol;   // dm2_per_second
double ion_diffusion___D_Na_jct_SL;   // dm2_per_second
double ion_diffusion___x_SL_cytosol;   // micrometre
double ion_diffusion___x_jct_SL;   // micrometre
double model_parameters___Cao;   // millimolar
double model_parameters___Cli;   // millimolar
double model_parameters___Clo;   // millimolar
double model_parameters___Cm_per_area;   // farad_per_cm2
double model_parameters___F;   // coulomb_per_mole
double model_parameters___Ki;   // millimolar
double model_parameters___Ko;   // millimolar
double model_parameters___Mgi;   // millimolar
double model_parameters___Nao;   // millimolar
double model_parameters___R;   // joule_per_kilomole_kelvin
double model_parameters___T;   // kelvin
double model_parameters___cell_length;   // micrometre
double model_parameters___cell_radius;   // micrometre

//------------------------------------------------------------------------------
// Computed variables
//------------------------------------------------------------------------------

double Ca_buffer___dCa_SLB_SL;   // millimolar_per_millisecond
double Ca_buffer___dCa_SLB_jct;   // millimolar_per_millisecond
double Ca_buffer___dCa_SLHigh_SL;   // millimolar_per_millisecond
double Ca_buffer___dCa_SLHigh_jct;   // millimolar_per_millisecond
double Ca_buffer___dCa_SL_tot_bound;   // millimolar_per_millisecond
double Ca_buffer___dCa_jct_tot_bound;   // millimolar_per_millisecond
double Ca_buffer___dCalsequestrin;   // millimolar_per_millisecond
double Ca_buffer___i_Ca_SL_tot;   // microA_per_microF
double Ca_buffer___i_Ca_jct_tot;   // microA_per_microF

double Jleak_SR___j_leak_SR;   // millimolar_per_millisecond
double Jpump_SR___j_pump_SR;   // millimolar_per_millisecond
double Jrel_SR___RI;   // dimensionless
double Jrel_SR___j_rel_SR;   // millimolar_per_millisecond
double Jrel_SR___kCaSR;   // dimensionless
double Jrel_SR___kiSRCa;   // per_millimolar_per_millisecond
double Jrel_SR___koSRCa;   // per_millimolar2_per_millisecond
double cell___i_Stim;   // microA_per_microF
double cytosolic_Ca_buffer___dCa_Calmodulin;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dCa_Myosin;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dCa_SRB;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dCa_TroponinC;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dCa_TroponinC_Ca_Mg;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dCa_cytosol_tot_bound;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dMg_Myosin;   // millimolar_per_millisecond
double cytosolic_Ca_buffer___dMg_TroponinC_Ca_Mg;   // millimolar_per_millisecond
double ion_diffusion___J_Ca_SL_cytosol;   // millimole_per_millisecond
double ion_diffusion___J_Ca_SL_cytosol_old;   // millimole_per_millisecond
double ion_diffusion___J_Ca_jct_SL;   // millimole_per_millisecond
double ion_diffusion___J_Ca_jct_SL_old;   // millimole_per_millisecond
double ion_diffusion___J_Na_SL_cytosol;   // millimole_per_millisecond
double ion_diffusion___J_Na_SL_cytosol_old;   // millimole_per_millisecond
double ion_diffusion___J_Na_jct_SL;   // millimole_per_millisecond
double ion_diffusion___J_Na_jct_SL_old;   // millimole_per_millisecond
double model_parameters___Cm;   // farad
double model_parameters___Vol_Cell;   // litre
double model_parameters___Vol_SL;   // litre
double model_parameters___Vol_SR;   // litre
double model_parameters___Vol_cytosol;   // litre
double model_parameters___Vol_jct;   // litre
double model_parameters___Vol_mito;   // litre

/*************State Variables*****************/

double Y[39];
double dY[39];

//------------------------------------------------------------------------------
// Initialisation
//------------------------------------------------------------------------------

void init()
{
   //---------------------------------------------------------------------------
   // State variables
   //---------------------------------------------------------------------------
//fCa=0.329616;

Y[0] = 1.28293;// Ca_buffer___Ca_Calsequestrin (millimolar)
Y[1] = 0.000131111;// Ca_buffer___Ca_SL (millimolar)
Y[2] = 0.0121366;// Ca_buffer___Ca_SLB_SL (millimolar)
Y[3] = 0.0116031;// Ca_buffer___Ca_SLB_jct (millimolar)
Y[4] = 0.132481; // Ca_buffer___Ca_SLHigh_SL (millimolar)
Y[5] = 0.0981466;// Ca_buffer___Ca_SLHigh_jct (millimolar)
Y[6] = 0.633156;// Ca_buffer___Ca_SR (millimolar)
Y[7] = 0.00026248;// Ca_buffer___Ca_jct (millimolar )
Y[8] = 9.93905e-05;// Ca_buffer___Cai (millimolar)
Y[11] = 0.04;
Y[23] = 2.67486e-07; // Jrel_SR___I (dimensionless)
Y[24] = 1.94911e-06;// Jrel_SR___O (dimensionless)
Y[25] = 0.879232;// Jrel_SR___R (dimensionless)
Y[26] = 8.87408;// Na_buffer___Na_SL (millimolar)
Y[27] = 0.776121;// Na_buffer___Na_SL_buf (millimolar)
Y[28] = 8.87282;// Na_buffer___Na_jct (millimolar)
Y[29] = 3.55706;// Na_buffer___Na_jct_buf (millimolar)
Y[30] = 8.87446;// Na_buffer___Nai (millimolar)
Y[31] = -85.7197; // cell___V (millivolt)
Y[32] = 0.000336009;// cytosolic_Ca_buffer___Ca_Calmodulin (millimolar)
Y[33] = 0.00244706;// cytosolic_Ca_buffer___Ca_Myosin (millimolar)
Y[34] = 0.00243042;// cytosolic_Ca_buffer___Ca_SRB (millimolar)
Y[35] = 0.00996049;// cytosolic_Ca_buffer___Ca_TroponinC (millimolar)
Y[36] = 0.12297;// cytosolic_Ca_buffer___Ca_TroponinC_Ca_Mg (millimolar)
Y[37] = 0.136961;// cytosolic_Ca_buffer___Mg_Myosin (millimolar)
Y[38] = 0.0079682; // cytosolic_Ca_buffer___Mg_TroponinC_Ca_Mg (millimolar)

NaIono = 140.0;
CaIono = 1.8;
KIono = 5.4;
KIoni = 135.0;            /* K, mM */
ClIono = 150.0;
ClIoni = 30.0;            /* Cl, mM */
NaIoni = 8.8;

V=-85.49190000;
m=0.00142380;
h=0.98646900;
j=0.99907100;
x=0.03065770;
d=1.71221e-06;
f=0.99764600;
xr=0.00195127;
a=0.00031926;
i=0.999;
ml=0.00142380;
hl=0.93722800;
x_=0.00036627;
y_=0.99816200;
y2_=0.99816200;
b=8.06835e-05;
g=0.97941500;


   //---------------------------------------------------------------------------
   // Constants
   //---------------------------------------------------------------------------
GNa=20.0;
GNal=0.0162;//1.62e-2;
GCaL=0.27;
GCaT=0.2;
GKr_factor=1.1*0.85;
Gto=0.7*0.16;
GCl=0.3;
GClB=0.0009;
GCaB=0.7*2*0.0002513;
GNaB=0.1*0.297e-3;
GKB=0.1*0.0005;

INaK_Kmr= 1.5;
INaK_Hill=4.0;
INaK_Vmf=1.90719;
INaK_Kmf=11.0;

ISLCaP_Hill = 1.6;
ISLCaP_Vmf=0.0538*1.25;
ISLCaP_Kmf=0.5;

Ca_buffer___Bmax_Calsequestrin = 0.14;   // millimolar
Ca_buffer___Bmax_SLB_SL = 0.0374;   // millimolar
Ca_buffer___Bmax_SLB_jct = 0.0046;   // millimolar
Ca_buffer___Bmax_SLHigh_SL = 0.0134;   // millimolar
Ca_buffer___Bmax_SLHigh_jct = 0.00165;   // millimolar
Ca_buffer___koff_Calsequestrin = 65.0;   // per_millisecond
Ca_buffer___koff_SLB = 1.3;   // per_millisecond
Ca_buffer___koff_SLHigh = 30.0e-3;   // per_millisecond
Ca_buffer___kon_Calsequestrin = 100.0;   // per_millimolar_per_millisecond
Ca_buffer___kon_SL = 100.0;   // per_millimolar_per_millisecond



Jleak_SR___KSRleak = 5.348e-6;   // per_millisecond
Jpump_SR___H = 1.787;   // dimensionless
Jpump_SR___Kmf = 0.000246;   // millimolar
Jpump_SR___Kmr = 1.7;   // millimolar
Jpump_SR___Q10_SRCaP = 2.6;   // dimensionless
Jpump_SR___V_max = 286.0e-6;   // millimolar_per_millisecond
Jrel_SR___EC50_SR = 0.45;   // millimolar
Jrel_SR___HSR = 2.5;   // dimensionless
Jrel_SR___Max_SR = 15.0;   // dimensionless
Jrel_SR___Min_SR = 1.0;   // dimensionless
Jrel_SR___kiCa = 0.5;   // per_millimolar_per_millisecond
Jrel_SR___kim = 0.005;   // per_millisecond
Jrel_SR___koCa = 10.0;   // per_millimolar2_per_millisecond
Jrel_SR___kom = 0.06;   // per_millisecond
Jrel_SR___ks = 25.0;   // per_millisecond

cytosolic_Ca_buffer___Bmax_Calmodulin = 0.024;   // millimolar
cytosolic_Ca_buffer___Bmax_Myosin_Ca = 0.14;   // millimolar
cytosolic_Ca_buffer___Bmax_Myosin_Mg = 0.14;   // millimolar
cytosolic_Ca_buffer___Bmax_SRB = 0.0171;   // millimolar
cytosolic_Ca_buffer___Bmax_TroponinC = 0.07;   // millimolar
cytosolic_Ca_buffer___Bmax_TroponinC_Ca_Mg_Ca = 0.14;   // millimolar
cytosolic_Ca_buffer___Bmax_TroponinC_Ca_Mg_Mg = 0.14;   // millimolar
cytosolic_Ca_buffer___koff_Calmodulin = 238.0e-3;   // per_millisecond
cytosolic_Ca_buffer___koff_Myosin_Ca = 0.46e-3;   // per_millisecond
cytosolic_Ca_buffer___koff_Myosin_Mg = 0.057e-3;   // per_millisecond
cytosolic_Ca_buffer___koff_SRB = 60.0e-3;   // per_millisecond
cytosolic_Ca_buffer___koff_TroponinC = 19.6e-3;   // per_millisecond
cytosolic_Ca_buffer___koff_TroponinC_Ca_Mg_Ca = 0.032e-3;   // per_millisecond
cytosolic_Ca_buffer___koff_TroponinC_Ca_Mg_Mg = 3.33e-3;   // per_millisecond
cytosolic_Ca_buffer___kon_Calmodulin = 34.0;   // per_millimolar_per_millisecond
cytosolic_Ca_buffer___kon_Myosin_Ca = 13.8;   // per_millimolar_per_millisecond
cytosolic_Ca_buffer___kon_Myosin_Mg = 15.7e-3;   // per_millimolar_per_millisecond
cytosolic_Ca_buffer___kon_SRB = 100.0;   // per_millimolar_per_millisecond
cytosolic_Ca_buffer___kon_TroponinC = 32.7;   // per_millimolar_per_millisecond
cytosolic_Ca_buffer___kon_TroponinC_Ca_Mg_Ca = 2.37;   // per_millimolar_per_millisecond
cytosolic_Ca_buffer___kon_TroponinC_Ca_Mg_Mg = 3.0e-3;   // per_millimolar_per_millisecond
ion_diffusion___A_SL_cytosol = 1.3e-4;   // cm2
ion_diffusion___A_jct_SL = 3.01e-6;   // cm2
ion_diffusion___D_Ca_SL_cytosol = 1.22e-6;   // dm2_per_second
ion_diffusion___D_Ca_jct_SL = 1.64e-6;   // dm2_per_second
ion_diffusion___D_Na_SL_cytosol = 1.79e-5;   // dm2_per_second
ion_diffusion___D_Na_jct_SL = 1.09e-5;   // dm2_per_second
ion_diffusion___x_SL_cytosol = 0.45;   // micrometre
ion_diffusion___x_jct_SL = 0.5;   // micrometre
model_parameters___Cao = 1.8;   // millimolar
model_parameters___Cli = 15.0;   // millimolar
model_parameters___Clo = 150.0;   // millimolar
model_parameters___Cm_per_area = 2.0e-6;   // farad_per_cm2
model_parameters___F = 96486.7;   // coulomb_per_mole
model_parameters___Ki = 135.0;   // millimolar
model_parameters___Ko = 5.4;   // millimolar
model_parameters___Mgi = 1.0;   // millimolar
model_parameters___Nao = 140.0;   // millimolar
model_parameters___R = 8314.3;   // joule_per_kilomole_kelvin
model_parameters___T = 310.0;   // kelvin
model_parameters___cell_length = 100.0;   // micrometre
model_parameters___cell_radius = 10.25;   // micrometre

//---------------------------------------------------------------------------
// Computed variables
//---------------------------------------------------------------------------

model_parameters___Vol_Cell = 3.141592654*pow(model_parameters___cell_radius/1000.0, 2.0)*model_parameters___cell_length/pow(1000.0, 3.0);
model_parameters___Vol_cytosol = 0.65*model_parameters___Vol_Cell;
model_parameters___Vol_SR = 0.035*model_parameters___Vol_Cell;
model_parameters___Vol_SL = 0.02*model_parameters___Vol_Cell;
model_parameters___Vol_jct = 0.00051*model_parameters___Vol_Cell;
model_parameters___Cm = model_parameters___Cm_per_area*2.0*model_parameters___cell_radius/10000.0*3.14159265358979*model_parameters___cell_length/10000.0;
   

}

/*****************Current calculatations********************/

void comp_ina(){
//labheart
alpha_m = 0.32 * (V+47.13)/(1- exp (-0.1* (V+47.13)));
beta_m = 0.08 * exp (-V/11);
if ( V >= -40 ){
alpha_h = 0;
beta_h = 1/(0.13 * (1+exp ((V+10.66)/-11.1)));
alpha_j = 0;
beta_j = 0.3 * exp (-2.535 * 10e-7 * V)/(1+ exp (-0.1* (V+32)));
}
else if ( V < -40){
alpha_h = 0.135 * exp ((80+V)/-6.8);
beta_h = 3.56 * exp (0.079 * V) + 3.1* 10e5 * exp (0.35*V);
alpha_j = ((-1.2714 * 10e5 * exp (0.2444* V) - (3.474 * 10e-5 * exp (-0.0439 * V)) * (V+37.78)))/(1+exp (0.311 * (V+79.23)));
beta_j = 0.1212 * exp (-0.01052* V)/(1+exp (-0.1378 * (V+40.14)));
}
tau_m	= 1.0/(alpha_m+beta_m);
tau_h	= 1.0/(alpha_h+beta_h);
tau_j	= 1.0/(alpha_j+beta_j);
m_inf	= alpha_m*tau_m;
h_inf	= alpha_h*tau_h;
j_inf	= alpha_j*tau_j;

m += HT*(m_inf - m)/tau_m;
h += HT*(h_inf - h)/tau_h;
j += HT*(j_inf - j)/tau_j;

INa =GNa * pow(m, 3.0) *h*j* (V-ENa);

//Slow component

alpha_ml	= 0.32*(V+47.13)/(1-exp(-0.1*(V+47.13)));
beta_ml	= 0.08*exp(-V/11);
tau_ml	= 1/(alpha_ml + beta_ml);
ml_inf	= alpha_ml/(alpha_ml+beta_ml);
tau_hl=132.4+ 112.8*exp(0.02325*V);
hl_inf	= 1/(1+exp((V-22.0+91.0)/6.1));
ml += HT*(ml_inf - ml)/tau_ml;
hl += HT*(hl_inf - hl)/tau_hl;

INal=GNal*ml*hl*(V-ENa);

}

void comp_ica_ipca(){
ECa = (RTF)/2.0 * log(CaIono/(Y[8]));
//L-type
d_inf	= (1/(1.0+exp(-(V-4.0)/6.74)));
tau_d	= (0.59+0.8*exp(0.052*(V+13))/(1+exp(0.132*(V+13))));
f_inf	= 1./(1.0 + exp((V+25.)/10.));
tau_f 	= 0.005*pow((V-2.5),2)+4.0;

d += HT*(d_inf - d)/tau_d;
f += HT*(f_inf - f)/tau_f;

ICaL = GCaL*d*f*(1-Y[11])*(V-60.0);

//T-type

b_inf = 1/(1+ exp (-(V+28)/6.1));
alpha_b = 1.068*exp((V+16.3)/30.0);
beta_b  = 1.068*exp(-(V+16.3)/30.0);
tau_b = 1.0/(alpha_b+beta_b);

g_inf = 1/(1+exp((V+60)/6.6));
alpha_g = 0.015*exp(-(V+71.7)/83.3);
beta_g  = 0.015*exp((V+71.7)/15.4);
tau_g = 1.0/(alpha_g+beta_g);

b += HT*(b_inf - b)/tau_b;
g += HT*(g_inf - g)/tau_g;

ICaT = GCaT * b * g * (V - 50);

//TOTAL

ICa=ICaL+ICaT;
}

void comp_iks(){
pCa = -1.0*log10(0.0001)+3.0;
SLGKs = (0.14/2)*(0.057+0.19/(1.0+exp((-7.2+pCa)/0.6)));  

x_inf = 1.1/(1.0+exp(-1.0*(V-1.5)/20));
tau_x = (600.0/(1.0+exp((V-20)/15.0)) + 250.0);
x += HT*(x_inf - x)/tau_x;
IKs = 1.0*SLGKs  * x * (V-EKs);

}

void comp_ikr(){

xr_inf = 1.0/(1.0 + exp(-1.0 * (V + 20.0)/10.5));
tau_xr = 1.0/(0.00138 * (V + 7.0)/(1.0 - exp(-0.123 * (V + 7.0))) + 0.00061 * (V + 10.0)/(exp(0.145 * (V + 10.0)) - 1.0));
r_inf = 1.0/(1.0 + exp(V/50));
GKr = (0.03 / 1.8) * sqrt(KIono/5.4);

xr += HT*(xr_inf - xr)/tau_xr;
IKr =  GKr_factor*GKr * xr * r_inf * (V - EK);

}

void comp_ik1(){

alpha_k1 = 0.3/(1.0 + exp(0.2385 * (V - EK - 59.215)));
beta_k1 = (0.49124 * exp(0.08032 * (V - EK + 5.476)) + exp(0.06175 * (V - EK - 594.31)))/(1.0 + exp(-0.5143 * (V - EK + 4.753)));
k1_inf = alpha_k1/(alpha_k1 + beta_k1);
GK1 = 0.5 * sqrt(KIono/5.4);

IK1 = GK1 * (k1_inf + 0.008) * (V - EK);   

}
void comp_ikp(){

IKp_Kp = 1.0/(1.0 + exp((7.488 - V)/5.98));      
IKp = 0.001 * IKp_Kp * (V - EK);
}

void comp_ito(){

alpha__x = (0.0451 * exp (0.85*0.03577 * V));
beta__x = (0.0989 * exp (-0.85*0.0623 * V));
x__inf= alpha__x/(alpha__x+beta__x);
tau__x=0.2/(alpha__x+beta__x);

alpha__y = (0.05415 * exp (-(V+12.5)/15)/(1+0.051335 * exp(-(V+12.5)/15)));
beta__y = (0.05415 * exp ((V+33.5)/15)/(1+0.051335 * exp((V+33.5)/15)));
y__inf= alpha__y/(alpha__y+beta__y);
tau__y=0.7*(15+20.0/(alpha__y+beta__y));
tau__y2=4.0/(alpha__y+beta__y);

x_ += HT*(x__inf - x_)/tau__x;
y_ += HT*(y__inf - y_)/tau__y;
y2_ += HT*(y__inf - y2_)/tau__y2;

ITO = (Gto  * x_ * (y_*0.75 + y2_*0.25)+0.00) * (V - EK);

}

void comp_icl(){

a_inf = 1.0/(1.0 + exp(-(V + 5.0)/10.0));
i_inf = 1.0/(1.0 + exp((V + 75.0)/10.0));
tau_i = (10.0 / (1.0 + exp((V + 33.5)/10.0)) + 10.0)*2;

a += HT*(a_inf - a)/1.0;
i += HT*(i_inf - i)/tau_i;

ICl = GCl * a_inf * i / (1.0 + 0.1/(Y[8]*1000)) * (V - ECl);
}

void comp_ib(){

IClB = GClB * (V - ECl);
ICaB = GCaB * (V - ECa);
INaB = GNaB * (V - ENa);
IKB  = GKB * (V - EK);
}

void comp_inak(){

sigma = (exp(NaIono/67.3) - 1.0)/7.0;
fNaK = 1.0/(1.0 + 0.1245 * exp(-0.1 * V/(RTF)) + 0.0365 * sigma * exp(-1.0*V/(RTF)));
INaK = 0.61875*fNaK*1/(1+pow(10/NaIoni,2))*(KIono/(KIono+1.5));
}

void comp_inaca(){

	allo		= 1/(1+pow((kmcaact/(1.5*Y[8])),2));
	num		= 0.4*inacamax*(pow(NaIoni,3)*CaIono*exp(nu*V*frdy/(R*temp))-pow(NaIono,3)*1.5*Y[8]*exp((nu-1)*V*frdy/(R*temp)));
	denommult	= 1+ksat*exp((nu-1)*V*frdy/(R*temp));
	denomterm1	= kmcao*pow(NaIoni,3)+pow(kmnao,3)*1.5*Y[8]+pow(kmnai1,3)*CaIono*(1+1.5*Y[8]/kmcai);
	denomterm2	= kmcai*pow(NaIono,3)*(1+pow(NaIoni/kmnai1,3))+pow(NaIoni,3)*CaIono+pow(NaIono,3)*1.5*Y[8];
	deltaE		= num/(denommult*(denomterm1+denomterm2));

	INaCaX = allo*deltaE;

}

void comp_ip(){
ISLCaP = 0.5*ISLCaP_Vmf/(1.0 + pow((ISLCaP_Kmf/(Y[8]*1000)), ISLCaP_Hill));

}

void comp_itot()
{
Iion = (-(IKs+IKr+IKp+IK1+ITO+ICl+IClB+INa+INal+ICa+ICaB+INaB+IKB+INaK+INaCaX+ISLCaP));
}

void comp_cai ()
{

Ca_buffer___dCalsequestrin = Ca_buffer___kon_Calsequestrin*Y[6]*(Ca_buffer___Bmax_Calsequestrin*model_parameters___Vol_cytosol/model_parameters___Vol_SR-Y[0])-	Ca_buffer___koff_Calsequestrin*Y[0];

dY[0] = Ca_buffer___dCalsequestrin;

Ca_buffer___dCa_SLB_SL = Ca_buffer___kon_SL*Y[1]*(Ca_buffer___Bmax_SLB_SL*model_parameters___Vol_cytosol/model_parameters___Vol_SL-Y[2])-Ca_buffer___koff_SLB*Y[2];
Ca_buffer___dCa_SLB_jct = Ca_buffer___kon_SL*Y[7]*(Ca_buffer___Bmax_SLB_jct*0.1*model_parameters___Vol_cytosol/model_parameters___Vol_jct-Y[3])-Ca_buffer___koff_SLB*Y[3];
Ca_buffer___dCa_SLHigh_SL = Ca_buffer___kon_SL*Y[1]*(Ca_buffer___Bmax_SLHigh_SL*model_parameters___Vol_cytosol/model_parameters___Vol_SL-Y[4])-Ca_buffer___koff_SLHigh*Y[4];
Ca_buffer___dCa_SLHigh_jct = Ca_buffer___kon_SL*Y[7]*(Ca_buffer___Bmax_SLHigh_jct*0.1*model_parameters___Vol_cytosol/model_parameters___Vol_jct-Y[5])-Ca_buffer___koff_SLHigh*Y[5];

dY[2] = Ca_buffer___dCa_SLB_SL;
dY[3] = Ca_buffer___dCa_SLB_jct;
dY[4] = Ca_buffer___dCa_SLHigh_SL;
dY[5] = Ca_buffer___dCa_SLHigh_jct;

Ca_buffer___dCa_jct_tot_bound = Ca_buffer___dCa_SLB_jct+Ca_buffer___dCa_SLHigh_jct;
Ca_buffer___dCa_SL_tot_bound = Ca_buffer___dCa_SLB_SL+Ca_buffer___dCa_SLHigh_SL;


Ca_buffer___i_Ca_jct_tot = ICa;
Ca_buffer___i_Ca_SL_tot = -2.0*INaCaX+1.0*ICaB+1.0*ISLCaP;

Jpump_SR___j_pump_SR =2.0*Jpump_SR___V_max*model_parameters___Vol_cytosol/model_parameters___Vol_SR*(pow(Y[8]/Jpump_SR___Kmf, Jpump_SR___H)-pow(Y[6]/Jpump_SR___Kmr, Jpump_SR___H))/(1.0+pow(Y[8]/Jpump_SR___Kmf, Jpump_SR___H)+pow(Y[6]/Jpump_SR___Kmr, Jpump_SR___H));    //*2 works at low bcl//increases --> increases transient amp & shortens time // 0.6
Jleak_SR___j_leak_SR = 0.5*Jleak_SR___KSRleak*(Y[6]-Y[7]);
Jrel_SR___j_rel_SR =2.0*Jrel_SR___ks*Y[24]*(Y[6]-Y[7]);

dY[6] = Jpump_SR___j_pump_SR-(Jleak_SR___j_leak_SR*model_parameters___Vol_cytosol/model_parameters___Vol_SR+Jrel_SR___j_rel_SR)-Ca_buffer___dCalsequestrin;
ion_diffusion___J_Ca_jct_SL = (Y[7]-Y[1])*8.2413e-13;

dY[7] = -0.5*Ca_buffer___i_Ca_jct_tot*model_parameters___Cm/(model_parameters___Vol_jct*2.0*model_parameters___F)-ion_diffusion___J_Ca_jct_SL/model_parameters___Vol_jct+Jrel_SR___j_rel_SR*model_parameters___Vol_SR/model_parameters___Vol_jct+Jleak_SR___j_leak_SR*model_parameters___Vol_cytosol/model_parameters___Vol_jct-1.0*Ca_buffer___dCa_jct_tot_bound;

dY[11] = 0.7*Y[7]*(1.0-Y[11])-11.9e-3*Y[11];

ion_diffusion___J_Ca_SL_cytosol = (Y[1]-Y[8])*3.7243e-12;
dY[1] = -0.5*Ca_buffer___i_Ca_SL_tot*model_parameters___Cm/(model_parameters___Vol_SL*2.0*model_parameters___F)+(ion_diffusion___J_Ca_jct_SL-ion_diffusion___J_Ca_SL_cytosol)/model_parameters___Vol_SL-1.0*Ca_buffer___dCa_SL_tot_bound;

cytosolic_Ca_buffer___dCa_TroponinC = cytosolic_Ca_buffer___kon_TroponinC*Y[8]*(cytosolic_Ca_buffer___Bmax_TroponinC-Y[35])-cytosolic_Ca_buffer___koff_TroponinC*Y[35];
cytosolic_Ca_buffer___dCa_TroponinC_Ca_Mg = cytosolic_Ca_buffer___kon_TroponinC_Ca_Mg_Ca*Y[8]*(cytosolic_Ca_buffer___Bmax_TroponinC_Ca_Mg_Ca-(Y[36]+Y[38]))-cytosolic_Ca_buffer___koff_TroponinC_Ca_Mg_Ca*Y[36];
cytosolic_Ca_buffer___dMg_TroponinC_Ca_Mg = cytosolic_Ca_buffer___kon_TroponinC_Ca_Mg_Mg*model_parameters___Mgi*(cytosolic_Ca_buffer___Bmax_TroponinC_Ca_Mg_Mg-(Y[36]+Y[38]))-cytosolic_Ca_buffer___koff_TroponinC_Ca_Mg_Mg*Y[38];
cytosolic_Ca_buffer___dCa_Calmodulin = cytosolic_Ca_buffer___kon_Calmodulin*Y[8]*(cytosolic_Ca_buffer___Bmax_Calmodulin-Y[32])-cytosolic_Ca_buffer___koff_Calmodulin*Y[32];
cytosolic_Ca_buffer___dCa_Myosin = cytosolic_Ca_buffer___kon_Myosin_Ca*Y[8]*(cytosolic_Ca_buffer___Bmax_Myosin_Ca-(Y[33]+Y[37]))-cytosolic_Ca_buffer___koff_Myosin_Ca*Y[33];
cytosolic_Ca_buffer___dMg_Myosin = cytosolic_Ca_buffer___kon_Myosin_Mg*model_parameters___Mgi*(cytosolic_Ca_buffer___Bmax_Myosin_Mg-(Y[33]+Y[37]))-cytosolic_Ca_buffer___koff_Myosin_Mg*Y[37];
cytosolic_Ca_buffer___dCa_SRB = cytosolic_Ca_buffer___kon_SRB*Y[8]*(cytosolic_Ca_buffer___Bmax_SRB-Y[34])-cytosolic_Ca_buffer___koff_SRB*Y[34];
cytosolic_Ca_buffer___dCa_cytosol_tot_bound = cytosolic_Ca_buffer___dCa_TroponinC+cytosolic_Ca_buffer___dCa_TroponinC_Ca_Mg+cytosolic_Ca_buffer___dMg_TroponinC_Ca_Mg+cytosolic_Ca_buffer___dCa_Calmodulin+cytosolic_Ca_buffer___dCa_Myosin+cytosolic_Ca_buffer___dMg_Myosin+cytosolic_Ca_buffer___dCa_SRB;

dY[8] = -Jpump_SR___j_pump_SR*model_parameters___Vol_SR/model_parameters___Vol_cytosol+ion_diffusion___J_Ca_SL_cytosol/model_parameters___Vol_cytosol-1.0*cytosolic_Ca_buffer___dCa_cytosol_tot_bound;


Jrel_SR___kCaSR = Jrel_SR___Max_SR-(Jrel_SR___Max_SR-Jrel_SR___Min_SR)/(1.0+pow(Jrel_SR___EC50_SR/Y[6], Jrel_SR___HSR));

Jrel_SR___koSRCa = Jrel_SR___koCa/Jrel_SR___kCaSR;
Jrel_SR___kiSRCa = Jrel_SR___kiCa*Jrel_SR___kCaSR;
Jrel_SR___RI = 1.0-Y[25]-Y[24]-Y[23];

dY[25] = Jrel_SR___kim*Jrel_SR___RI-Jrel_SR___kiSRCa*Y[7]*Y[25]-(Jrel_SR___koSRCa*Y[7]*Y[7]*Y[25]-Jrel_SR___kom*Y[24]);
dY[24] = Jrel_SR___koSRCa*Y[7]*Y[7]*Y[25]-Jrel_SR___kom*Y[24]-(Jrel_SR___kiSRCa*Y[7]*Y[24]-Jrel_SR___kim*Y[23]);
dY[23] = Jrel_SR___kiSRCa*Y[7]*Y[24]-Jrel_SR___kim*Y[23]-(Jrel_SR___kom*Y[23]-Jrel_SR___koSRCa*Y[7]*Y[7]*Jrel_SR___RI);


dY[35] = cytosolic_Ca_buffer___dCa_TroponinC;
dY[36] = cytosolic_Ca_buffer___dCa_TroponinC_Ca_Mg;
dY[38] = cytosolic_Ca_buffer___dMg_TroponinC_Ca_Mg;
dY[32] = cytosolic_Ca_buffer___dCa_Calmodulin;
dY[33] = cytosolic_Ca_buffer___dCa_Myosin;
dY[37] = cytosolic_Ca_buffer___dMg_Myosin;
dY[34] = cytosolic_Ca_buffer___dCa_SRB;

for (ii = 0; ii <= 38; ii++)
 Y[ii] += HT*dY[ii];
}


int main()

{
double cl;
char option1,option2;
double max_bcl_restitution;

ofstream out("ap.txt");
ofstream out1("restitution.txt");
ofstream out2("initials_gates.txt");
ofstream out3("initials_cai.txt");
ofstream out4("ap_char.txt");
ofstream out10("ap_ina.txt");

int flag = 1;

while ( flag==1){

        cout << "would you like to run restitution simulation? (Y/N) " ;
        cin >> option1;
        cout << endl << endl;
        if (option1== 'Y' || option1 == 'y'){
        max_bcl_restitution=2000;
        flag = 0;
        }

        else if (option1== 'n' || option1 == 'N'){
        max_bcl_restitution=0;
        flag =0;
        }
        else {flag=1;}
        }

cout << "insert cycle length to start (ms): ";
cin >> cl;
cout << endl << endl;
for (int loop=0;loop<=max_bcl_restitution;loop=loop+100){

cout << "Simulation @ bcl: " << loop + cl << endl << endl;
bcl=cl+loop;

//if (bcl > 600){
//loop=loop+75;
//}


double STOPTIME=1000;
double tstim=10.0;
double tend=11.0;
double stimtime=0.0;
double time=0;
double dvdt;
int step;
int i=-1;

double vmax[beats+1];
double dvdtmax[beats+1];
double apd[beats+1];
double toneapd[beats+1];
double ttwoapd[beats+1];
double trep[beats+1];
double di[beats+1];
double rmbp[beats+1];

init();


ENa =(RTF)*log(NaIono/NaIoni);
EKs = (RTF)*log((KIono + PNaK * NaIono)/(KIoni + PNaK * NaIoni));
ECa = (RTF)/2.0 * log(CaIono/(Y[8]));
EK = (RTF)*log(KIono/KIoni);
ECl = (RTF)*log(ClIoni/ClIono);

for (i = 0; i <= beats; i++) {
  dvdtmax[i] = -10000;
  vmax[i] = -10000;
} i = -1;


  STOPTIME=S2+bcl*beats+5000;
  for(step=0;time<=STOPTIME;step++)
    {
      time+=HT;

      if (time>=tstim && time<(tstim+HT) && time <= (S2 + bcl*(beats-1))) {
       stimtime = 0;
       i = i+1;

       if (i < beats-2)
         tstim = tstim+bcl;
       else if (i == beats-2)
         tstim = tstim+S2;
       else tstim = tstim+10000;
       cout << "Stimulus " << i+1 <<" applied, Time = " << time << endl;

       rmbp[i]=V;
     }

comp_iks();
comp_ikr();
comp_ik1();
comp_ikp();
comp_ito();
comp_icl();
comp_ib();
comp_ina();
comp_ica_ipca();
comp_inak();
comp_inaca();
comp_ip();
comp_itot();
comp_cai();

if(stimtime>=0 && stimtime<1)
Istim=-40;
else Istim=0.0;

stimtime = stimtime+HT;

dvdt = Iion-Istim;
V += HT*dvdt;

if (V>vmax[i])
vmax[i] = V;
if (dvdt>dvdtmax[i])
{dvdtmax[i] = dvdt;
toneapd[i] = time;}
if (V>=(vmax[i]-0.9*(vmax[i]-rmbp[i])))
ttwoapd[i] = time;

//if (step%200 == 0)
//out<<time-10 << "\t"<< V<< "\t" << Y[8] << endl;

    } //end of time loop


out2<< "V = " << V << "\n"<< "m = " << m << "\n"<< "h = " << h << "\n"<< "j = " << j << "\n"<< "x = " << x << "\n"<< "d = " << d << "\n"
	<< "f = " << f << "\n"<< "xr = " << xr << "\n"<< "a = " << a<< "\n"<< "i = " << i<< "\n"<< "ml = " <<ml<< "\n"<< "hl = " << hl << "\n"<< "x_ = " << x_<< "\n"
	<< "y_ = " << y_ << "\n"<< "y2_ = " << y2_<< "\n"<< "b = " << b << "\n"<< "g = " << g<<endl;

out3<< "Y[0] = " << Y[0] << "\n"<< "Y[1] = " << Y[1] << "\n"<< "Y[2] = " << Y[2] << "\n"<< "Y[3] = " << Y[3] << "\n"<< "Y[4] = " << Y[4] << "\n"<< "Y[5] = " << Y[5] << "\n"
	<< "Y[6] = " << Y[6] << "\n"<< "Y[7] = " << Y[7] << "\n"<< "Y[8] = " << Y[8]<< "\n"<< "Y[23] = " << Y[23]<< "\n"<< "Y[24] = " <<Y[24] << "\n"<< "Y[25] = " << Y[25] << "\n"<< "Y[26] = " << Y[26]<< "\n"
	<< "Y[27] = " << Y[27] << "\n"<< "Y[28] = " << Y[28] << "\n"<< "Y[29] = " << Y[29] << "\n"<< "Y[30] = " << Y[30] << "\n"<< "Y[31] = " << Y[31] << "\n"<< "Y[32] = " << Y[32] << "\n"<< "Y[33] = " << Y[33] << "\n"<< "Y[34] = " << Y[34] << "\n"<< "Y[35] = " << Y[35] << "\n"<< "Y[36] = " << Y[36] << "\n"<< "Y[37] = " << Y[37] << "\n"<< "Y[38] = " << Y[38] <<"\t"<<Y[11]<< endl;

apd[beats-1] = ttwoapd[beats-1]-toneapd[beats-1];
apd[beats-2] = ttwoapd[beats-2]-toneapd[beats-2];
di[beats-1] = toneapd[beats-1]-ttwoapd[beats-2];

cout << "DI = " << di[beats-1] << "\t" << "APD90 = " << apd[beats -1]<< "\t" << apd[beats-2]<< endl;
out1 << bcl << "\t" << apd[beats -1]<< "\t" << apd[beats-2]<<endl;
out4 << bcl << "\t" << apd[beats -1]<< "\t" << dvdtmax[beats-1]<< "\t" << rmbp[beats -1]<< "\t" << vmax[beats-1]-rmbp[beats-1]<<endl;

}return 0;

}

