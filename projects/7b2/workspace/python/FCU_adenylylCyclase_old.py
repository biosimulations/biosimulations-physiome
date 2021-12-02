# ----------------------------------------------------------------
# This python script is the export of FCU_adenylyl_cyclase.cellml made on 22 Oct 2021
# ----------------------------------------------------------------
# Size of variable arrays:
sizeAlgebraic = 141
sizeStates = 50
sizeConstants = 120
from math import *
from numpy import *
import matplotlib.pyplot as plt
import time

def createLegends():
    legend_states = [""] * sizeStates
    legend_rates = [""] * sizeStates
    legend_algebraic = [""] * sizeAlgebraic
    legend_voi = ""
    legend_constants = [""] * sizeConstants
    legend_constants[0] = "kappa_1a in component BG_parameters (fmol_per_sec)"
    legend_constants[1] = "kappa_1b in component BG_parameters (fmol_per_sec)"
    legend_constants[2] = "kappa_2a in component BG_parameters (fmol_per_sec)"
    legend_constants[3] = "kappa_2b in component BG_parameters (fmol_per_sec)"
    legend_constants[4] = "kappa_3a in component BG_parameters (fmol_per_sec)"
    legend_constants[5] = "kappa_3b in component BG_parameters (fmol_per_sec)"
    legend_constants[6] = "kappa_4a in component BG_parameters (fmol_per_sec)"
    legend_constants[7] = "kappa_4b in component BG_parameters (fmol_per_sec)"
    legend_constants[8] = "kappa_5 in component BG_parameters (fmol_per_sec)"
    legend_constants[9] = "kappa_6 in component BG_parameters (fmol_per_sec)"
    legend_constants[10] = "kappa_7 in component BG_parameters (fmol_per_sec)"
    legend_constants[11] = "kappa_GiAC in component BG_parameters (fmol_per_sec)"
    legend_constants[12] = "kappa_sig1_B1 in component BG_parameters (fmol_per_sec)"
    legend_constants[13] = "kappa_sig2_B1 in component BG_parameters (fmol_per_sec)"
    legend_constants[14] = "kappa_sig3_B1 in component BG_parameters (fmol_per_sec)"
    legend_constants[15] = "kappa_sig4_B1 in component BG_parameters (fmol_per_sec)"
    legend_constants[16] = "kappa_sig1_M2 in component BG_parameters (fmol_per_sec)"
    legend_constants[17] = "kappa_sig2_M2 in component BG_parameters (fmol_per_sec)"
    legend_constants[18] = "kappa_sig3_M2 in component BG_parameters (fmol_per_sec)"
    legend_constants[19] = "kappa_sig4_M2 in component BG_parameters (fmol_per_sec)"
    legend_constants[20] = "kappa_act1_Gs in component BG_parameters (fmol_per_sec)"
    legend_constants[21] = "kappa_act2_Gs in component BG_parameters (fmol_per_sec)"
    legend_constants[22] = "kappa_hyd_Gs in component BG_parameters (fmol_per_sec)"
    legend_constants[23] = "kappa_reassoc_Gs in component BG_parameters (fmol_per_sec)"
    legend_constants[24] = "kappa_PiPhos in component BG_parameters (fmol_per_sec)"
    legend_constants[25] = "kappa_act1_Gi in component BG_parameters (fmol_per_sec)"
    legend_constants[26] = "kappa_act2_Gi in component BG_parameters (fmol_per_sec)"
    legend_constants[27] = "kappa_hyd_Gi in component BG_parameters (fmol_per_sec)"
    legend_constants[28] = "kappa_reassoc_Gi in component BG_parameters (fmol_per_sec)"
    legend_constants[29] = "K_ATP in component BG_parameters (per_fmol)"
    legend_constants[30] = "K_cAMP in component BG_parameters (per_fmol)"
    legend_constants[31] = "K_AC in component BG_parameters (per_fmol)"
    legend_constants[32] = "K_AC_ATP in component BG_parameters (per_fmol)"
    legend_constants[33] = "K_aGs_GTP_AC in component BG_parameters (per_fmol)"
    legend_constants[34] = "K_aGs_GTP_AC_ATP in component BG_parameters (per_fmol)"
    legend_constants[35] = "K_FSK_AC in component BG_parameters (per_fmol)"
    legend_constants[36] = "K_FSK_AC_ATP in component BG_parameters (per_fmol)"
    legend_constants[37] = "K_PDE in component BG_parameters (per_fmol)"
    legend_constants[38] = "K_PDE_cAMP in component BG_parameters (per_fmol)"
    legend_constants[39] = "K_five_AMP in component BG_parameters (per_fmol)"
    legend_constants[40] = "K_IBMX in component BG_parameters (per_fmol)"
    legend_constants[41] = "K_PDEinh in component BG_parameters (per_fmol)"
    legend_constants[42] = "K_aGs_GTP in component BG_parameters (per_fmol)"
    legend_constants[43] = "K_FSK in component BG_parameters (per_fmol)"
    legend_constants[44] = "K_aGi_GTP in component BG_parameters (per_fmol)"
    legend_constants[45] = "K_ACinh in component BG_parameters (per_fmol)"
    legend_constants[46] = "K_PPi in component BG_parameters (per_fmol)"
    legend_constants[47] = "K_L_B1 in component BG_parameters (per_fmol)"
    legend_constants[48] = "K_R_B1 in component BG_parameters (per_fmol)"
    legend_constants[49] = "K_Gs in component BG_parameters (per_fmol)"
    legend_constants[50] = "K_LR_B1 in component BG_parameters (per_fmol)"
    legend_constants[51] = "K_R_B1Gs in component BG_parameters (per_fmol)"
    legend_constants[52] = "K_LR_B1Gs in component BG_parameters (per_fmol)"
    legend_constants[53] = "K_L_M2 in component BG_parameters (per_fmol)"
    legend_constants[54] = "K_R_M2 in component BG_parameters (per_fmol)"
    legend_constants[55] = "K_Gi in component BG_parameters (per_fmol)"
    legend_constants[56] = "K_LR_M2 in component BG_parameters (per_fmol)"
    legend_constants[57] = "K_R_M2Gi in component BG_parameters (per_fmol)"
    legend_constants[58] = "K_LR_M2Gi in component BG_parameters (per_fmol)"
    legend_constants[59] = "K_beta_gamma_Gs in component BG_parameters (per_fmol)"
    legend_constants[60] = "K_aGs_GDP in component BG_parameters (per_fmol)"
    legend_constants[61] = "K_Pi in component BG_parameters (per_fmol)"
    legend_constants[62] = "K_GTP in component BG_parameters (per_fmol)"
    legend_constants[63] = "K_GDP in component BG_parameters (per_fmol)"
    legend_constants[64] = "K_beta_gamma_Gi in component BG_parameters (per_fmol)"
    legend_constants[65] = "K_aGi_GDP in component BG_parameters (per_fmol)"
    legend_voi = "time in component environment (second)"
    legend_constants[66] = "vol_myo in component environment (pL)"
    legend_constants[67] = "freq in component environment (dimensionless)"
    legend_constants[68] = "stimSt in component environment (second)"
    legend_constants[69] = "stimSt2 in component environment (second)"
    legend_constants[70] = "stimDur in component environment (second)"
    legend_constants[71] = "tRamp in component environment (second)"
    legend_constants[72] = "stimMag in component environment (fmol)"
    legend_constants[73] = "stimHolding in component environment (fmol)"
    legend_constants[119] = "m in component environment (fmol_per_sec)"
    legend_constants[74] = "q_ATP_init in component environment (fmol)"
    legend_constants[75] = "q_AC_init in component environment (fmol)"
    legend_constants[76] = "q_cAMP_init in component environment (fmol)"
    legend_constants[77] = "q_AC_ATP_init in component environment (fmol)"
    legend_constants[78] = "q_FSK_init in component environment (fmol)"
    legend_constants[79] = "q_FSK_AC_init in component environment (fmol)"
    legend_constants[80] = "q_FSK_AC_ATP_init in component environment (fmol)"
    legend_constants[81] = "q_aGs_GTP_init in component environment (fmol)"
    legend_constants[82] = "q_aGs_GTP_AC_init in component environment (fmol)"
    legend_constants[83] = "q_aGs_GTP_AC_ATP_init in component environment (fmol)"
    legend_constants[84] = "q_PDE_init in component environment (fmol)"
    legend_constants[85] = "q_PDEinh_init in component environment (fmol)"
    legend_constants[86] = "q_PDE_cAMP_init in component environment (fmol)"
    legend_constants[87] = "q_IBMX_init in component environment (fmol)"
    legend_constants[88] = "q_five_AMP_init in component environment (fmol)"
    legend_constants[89] = "q_aGi_GTP_init in component environment (fmol)"
    legend_constants[90] = "q_ACinh_init in component environment (fmol)"
    legend_constants[91] = "q_PPi_init in component environment (fmol)"
    legend_constants[92] = "q_R_B1_init in component environment (fmol)"
    legend_constants[93] = "q_Gs_init in component environment (fmol)"
    legend_algebraic[0] = "q_L_B1_init in component environment (fmol)"
    legend_constants[94] = "q_LR_B1_init in component environment (fmol)"
    legend_constants[95] = "q_R_B1Gs_init in component environment (fmol)"
    legend_constants[96] = "q_LR_B1Gs_init in component environment (fmol)"
    legend_algebraic[1] = "q_L_M2_init in component environment (fmol)"
    legend_constants[97] = "q_R_M2_init in component environment (fmol)"
    legend_constants[98] = "q_Gi_init in component environment (fmol)"
    legend_constants[99] = "q_LR_M2_init in component environment (fmol)"
    legend_constants[100] = "q_R_M2Gi_init in component environment (fmol)"
    legend_constants[101] = "q_LR_M2Gi_init in component environment (fmol)"
    legend_constants[102] = "q_beta_gamma_Gs_init in component environment (fmol)"
    legend_constants[103] = "q_aGs_GDP_init in component environment (fmol)"
    legend_constants[104] = "q_Pi_init in component environment (fmol)"
    legend_constants[105] = "q_beta_gamma_Gi_init in component environment (fmol)"
    legend_constants[106] = "q_aGi_GDP_init in component environment (fmol)"
    legend_constants[107] = "q_R_B1GsP_init in component environment (fmol)"
    legend_constants[108] = "q_LR_B1GsP_init in component environment (fmol)"
    legend_constants[109] = "q_GTP_init in component environment (fmol)"
    legend_constants[110] = "q_GDP_init in component environment (fmol)"
    legend_algebraic[35] = "L_B1_T in component environment (fmol)"
    legend_algebraic[59] = "L_M2_T in component environment (fmol)"
    legend_algebraic[36] = "R_B1_T in component environment (fmol)"
    legend_algebraic[60] = "R_M2_T in component environment (fmol)"
    legend_algebraic[73] = "Gs_T in component environment (fmol)"
    legend_algebraic[94] = "Gi_T in component environment (fmol)"
    legend_algebraic[16] = "adenosine_T in component environment (fmol)"
    legend_algebraic[2] = "q_ATP in component environment (fmol)"
    legend_algebraic[3] = "q_cAMP in component environment (fmol)"
    legend_algebraic[4] = "q_AC in component environment (fmol)"
    legend_algebraic[5] = "q_AC_ATP in component environment (fmol)"
    legend_algebraic[6] = "q_aGs_GTP_AC in component environment (fmol)"
    legend_algebraic[7] = "q_aGs_GTP_AC_ATP in component environment (fmol)"
    legend_algebraic[8] = "q_FSK_AC in component environment (fmol)"
    legend_algebraic[9] = "q_FSK_AC_ATP in component environment (fmol)"
    legend_algebraic[10] = "q_PDE in component environment (fmol)"
    legend_algebraic[13] = "q_PDE_cAMP in component environment (fmol)"
    legend_algebraic[14] = "q_five_AMP in component environment (fmol)"
    legend_algebraic[17] = "q_IBMX in component environment (fmol)"
    legend_algebraic[18] = "q_PDEinh in component environment (fmol)"
    legend_algebraic[19] = "q_aGs_GTP in component environment (fmol)"
    legend_algebraic[20] = "q_FSK in component environment (fmol)"
    legend_algebraic[22] = "q_aGi_GTP in component environment (fmol)"
    legend_algebraic[23] = "q_ACinh in component environment (fmol)"
    legend_algebraic[25] = "q_PPi in component environment (fmol)"
    legend_algebraic[24] = "q_L_B1 in component environment (fmol)"
    legend_algebraic[26] = "q_R_B1 in component environment (fmol)"
    legend_algebraic[27] = "q_Gs in component environment (fmol)"
    legend_algebraic[29] = "q_LR_B1 in component environment (fmol)"
    legend_algebraic[31] = "q_R_B1Gs in component environment (fmol)"
    legend_algebraic[33] = "q_LR_B1Gs in component environment (fmol)"
    legend_algebraic[37] = "q_L_M2 in component environment (fmol)"
    legend_algebraic[44] = "q_R_M2 in component environment (fmol)"
    legend_algebraic[47] = "q_Gi in component environment (fmol)"
    legend_algebraic[50] = "q_LR_M2 in component environment (fmol)"
    legend_algebraic[53] = "q_R_M2Gi in component environment (fmol)"
    legend_algebraic[56] = "q_LR_M2Gi in component environment (fmol)"
    legend_algebraic[61] = "q_beta_gamma_Gs in component environment (fmol)"
    legend_algebraic[69] = "q_aGs_GDP in component environment (fmol)"
    legend_algebraic[74] = "q_Pi in component environment (fmol)"
    legend_algebraic[79] = "q_GTP in component environment (fmol)"
    legend_algebraic[83] = "q_GDP in component environment (fmol)"
    legend_algebraic[86] = "q_beta_gamma_Gi in component environment (fmol)"
    legend_algebraic[93] = "q_aGi_GDP in component environment (fmol)"
    legend_states[0] = "q_ATP in component cAMP (fmol)"
    legend_states[1] = "q_cAMP in component cAMP (fmol)"
    legend_states[2] = "q_AC in component cAMP (fmol)"
    legend_states[3] = "q_AC_ATP in component cAMP (fmol)"
    legend_states[4] = "q_aGs_GTP_AC in component cAMP (fmol)"
    legend_states[5] = "q_aGs_GTP_AC_ATP in component cAMP (fmol)"
    legend_states[6] = "q_FSK_AC in component cAMP (fmol)"
    legend_states[7] = "q_FSK_AC_ATP in component cAMP (fmol)"
    legend_states[8] = "q_PDE in component cAMP (fmol)"
    legend_states[9] = "q_PDE_cAMP in component cAMP (fmol)"
    legend_states[10] = "q_five_AMP in component cAMP (fmol)"
    legend_states[11] = "q_IBMX in component cAMP (fmol)"
    legend_states[12] = "q_PDEinh in component cAMP (fmol)"
    legend_states[13] = "q_aGs_GTP in component cAMP (fmol)"
    legend_states[14] = "q_FSK in component cAMP (fmol)"
    legend_states[15] = "q_aGi_GTP in component cAMP (fmol)"
    legend_states[16] = "q_ACinh in component cAMP (fmol)"
    legend_states[17] = "q_PPi in component cAMP (fmol)"
    legend_states[18] = "q_L_B1 in component LRGbinding_B1AR (fmol)"
    legend_states[19] = "q_R_B1 in component LRGbinding_B1AR (fmol)"
    legend_states[20] = "q_Gs in component LRGbinding_B1AR (fmol)"
    legend_states[21] = "q_LR_B1 in component LRGbinding_B1AR (fmol)"
    legend_states[22] = "q_R_B1Gs in component LRGbinding_B1AR (fmol)"
    legend_states[23] = "q_LR_B1Gs in component LRGbinding_B1AR (fmol)"
    legend_states[24] = "q_L_M2 in component LRGbinding_M2 (fmol)"
    legend_states[25] = "q_R_M2 in component LRGbinding_M2 (fmol)"
    legend_states[26] = "q_Gi in component LRGbinding_M2 (fmol)"
    legend_states[27] = "q_LR_M2 in component LRGbinding_M2 (fmol)"
    legend_states[28] = "q_R_M2Gi in component LRGbinding_M2 (fmol)"
    legend_states[29] = "q_LR_M2Gi in component LRGbinding_M2 (fmol)"
    legend_states[30] = "q_R_B1 in component GsProtein (fmol)"
    legend_states[31] = "q_Gs in component GsProtein (fmol)"
    legend_states[32] = "q_R_B1Gs in component GsProtein (fmol)"
    legend_states[33] = "q_LR_B1 in component GsProtein (fmol)"
    legend_states[34] = "q_LR_B1Gs in component GsProtein (fmol)"
    legend_states[35] = "q_aGs_GTP in component GsProtein (fmol)"
    legend_states[36] = "q_beta_gamma_Gs in component GsProtein (fmol)"
    legend_states[37] = "q_aGs_GDP in component GsProtein (fmol)"
    legend_states[38] = "q_Pi in component GsProtein (fmol)"
    legend_states[39] = "q_GTP in component GsProtein (fmol)"
    legend_states[40] = "q_GDP in component GsProtein (fmol)"
    legend_states[41] = "q_R_M2 in component GiProtein (fmol)"
    legend_states[42] = "q_Gi in component GiProtein (fmol)"
    legend_states[43] = "q_R_M2Gi in component GiProtein (fmol)"
    legend_states[44] = "q_LR_M2 in component GiProtein (fmol)"
    legend_states[45] = "q_LR_M2Gi in component GiProtein (fmol)"
    legend_states[46] = "q_aGi_GTP in component GiProtein (fmol)"
    legend_states[47] = "q_beta_gamma_Gi in component GiProtein (fmol)"
    legend_states[48] = "q_aGi_GDP in component GiProtein (fmol)"
    legend_states[49] = "q_Pi in component GiProtein (fmol)"
    legend_constants[111] = "q_GTP in component GiProtein (fmol)"
    legend_constants[112] = "q_GDP in component GiProtein (fmol)"
    legend_constants[113] = "R in component constants (J_per_K_per_mol)"
    legend_constants[114] = "T in component constants (kelvin)"
    legend_constants[115] = "F in component constants (C_per_mol)"
    legend_algebraic[100] = "v1a in component cAMP (fmol_per_sec)"
    legend_algebraic[104] = "v1b in component cAMP (fmol_per_sec)"
    legend_algebraic[108] = "v2a in component cAMP (fmol_per_sec)"
    legend_algebraic[111] = "v2b in component cAMP (fmol_per_sec)"
    legend_algebraic[114] = "v3a in component cAMP (fmol_per_sec)"
    legend_algebraic[117] = "v3b in component cAMP (fmol_per_sec)"
    legend_algebraic[120] = "v4a in component cAMP (fmol_per_sec)"
    legend_algebraic[124] = "v4b in component cAMP (fmol_per_sec)"
    legend_algebraic[128] = "v5 in component cAMP (fmol_per_sec)"
    legend_algebraic[121] = "v6 in component cAMP (fmol_per_sec)"
    legend_algebraic[125] = "v7 in component cAMP (fmol_per_sec)"
    legend_algebraic[129] = "vGiAC in component cAMP (fmol_per_sec)"
    legend_algebraic[28] = "mu_ATP in component cAMP (J_per_mol)"
    legend_algebraic[32] = "mu_AC in component cAMP (J_per_mol)"
    legend_algebraic[30] = "mu_cAMP in component cAMP (J_per_mol)"
    legend_algebraic[34] = "mu_AC_ATP in component cAMP (J_per_mol)"
    legend_algebraic[84] = "mu_FSK in component cAMP (J_per_mol)"
    legend_algebraic[48] = "mu_FSK_AC in component cAMP (J_per_mol)"
    legend_algebraic[51] = "mu_FSK_AC_ATP in component cAMP (J_per_mol)"
    legend_algebraic[80] = "mu_aGs_GTP in component cAMP (J_per_mol)"
    legend_algebraic[38] = "mu_aGs_GTP_AC in component cAMP (J_per_mol)"
    legend_algebraic[45] = "mu_aGs_GTP_AC_ATP in component cAMP (J_per_mol)"
    legend_algebraic[54] = "mu_PDE in component cAMP (J_per_mol)"
    legend_algebraic[75] = "mu_PDEinh in component cAMP (J_per_mol)"
    legend_algebraic[57] = "mu_PDE_cAMP in component cAMP (J_per_mol)"
    legend_algebraic[70] = "mu_IBMX in component cAMP (J_per_mol)"
    legend_algebraic[62] = "mu_five_AMP in component cAMP (J_per_mol)"
    legend_algebraic[87] = "mu_aGi_GTP in component cAMP (J_per_mol)"
    legend_algebraic[90] = "mu_ACinh in component cAMP (J_per_mol)"
    legend_algebraic[95] = "mu_PPi in component cAMP (J_per_mol)"
    legend_constants[116] = "vol in component cAMP (pL)"
    legend_algebraic[11] = "ATP_T in component cAMP (fmol)"
    legend_algebraic[12] = "AC_T in component cAMP (fmol)"
    legend_algebraic[21] = "Gs_T in component cAMP (fmol)"
    legend_algebraic[15] = "cAMP_T in component cAMP (fmol)"
    legend_algebraic[39] = "mu_L_B1 in component LRGbinding_B1AR (J_per_mol)"
    legend_algebraic[46] = "mu_R_B1 in component LRGbinding_B1AR (J_per_mol)"
    legend_algebraic[49] = "mu_Gs in component LRGbinding_B1AR (J_per_mol)"
    legend_algebraic[52] = "mu_LR_B1 in component LRGbinding_B1AR (J_per_mol)"
    legend_algebraic[55] = "mu_R_B1Gs in component LRGbinding_B1AR (J_per_mol)"
    legend_algebraic[58] = "mu_LR_B1Gs in component LRGbinding_B1AR (J_per_mol)"
    legend_algebraic[63] = "vsig1_B1 in component LRGbinding_B1AR (fmol_per_sec)"
    legend_algebraic[71] = "vsig2_B1 in component LRGbinding_B1AR (fmol_per_sec)"
    legend_algebraic[76] = "vsig3_B1 in component LRGbinding_B1AR (fmol_per_sec)"
    legend_algebraic[81] = "vsig4_B1 in component LRGbinding_B1AR (fmol_per_sec)"
    legend_constants[117] = "vol in component LRGbinding_B1AR (pL)"
    legend_algebraic[40] = "L_T in component LRGbinding_B1AR (fmol)"
    legend_algebraic[41] = "R_T in component LRGbinding_B1AR (fmol)"
    legend_algebraic[42] = "Gs_T in component LRGbinding_B1AR (fmol)"
    legend_algebraic[64] = "mu_L_M2 in component LRGbinding_M2 (J_per_mol)"
    legend_algebraic[72] = "mu_R_M2 in component LRGbinding_M2 (J_per_mol)"
    legend_algebraic[77] = "mu_Gi in component LRGbinding_M2 (J_per_mol)"
    legend_algebraic[82] = "mu_LR_M2 in component LRGbinding_M2 (J_per_mol)"
    legend_algebraic[85] = "mu_R_M2Gi in component LRGbinding_M2 (J_per_mol)"
    legend_algebraic[88] = "mu_LR_M2Gi in component LRGbinding_M2 (J_per_mol)"
    legend_algebraic[91] = "vsig1_M2 in component LRGbinding_M2 (fmol_per_sec)"
    legend_algebraic[96] = "vsig2_M2 in component LRGbinding_M2 (fmol_per_sec)"
    legend_algebraic[101] = "vsig3_M2 in component LRGbinding_M2 (fmol_per_sec)"
    legend_algebraic[105] = "vsig4_M2 in component LRGbinding_M2 (fmol_per_sec)"
    legend_constants[118] = "vol in component LRGbinding_M2 (pL)"
    legend_algebraic[65] = "L_T in component LRGbinding_M2 (fmol)"
    legend_algebraic[66] = "R_T in component LRGbinding_M2 (fmol)"
    legend_algebraic[67] = "Gi_T in component LRGbinding_M2 (fmol)"
    legend_algebraic[130] = "vact1_Gs in component GsProtein (fmol_per_sec)"
    legend_algebraic[132] = "vact2_Gs in component GsProtein (fmol_per_sec)"
    legend_algebraic[134] = "vhyd_Gs in component GsProtein (fmol_per_sec)"
    legend_algebraic[136] = "vreassoc_Gs in component GsProtein (fmol_per_sec)"
    legend_algebraic[137] = "vPiPhos in component GsProtein (fmol_per_sec)"
    legend_algebraic[89] = "mu_R_B1 in component GsProtein (J_per_mol)"
    legend_algebraic[92] = "mu_Gs in component GsProtein (J_per_mol)"
    legend_algebraic[97] = "mu_R_B1Gs in component GsProtein (J_per_mol)"
    legend_algebraic[102] = "mu_LR_B1 in component GsProtein (J_per_mol)"
    legend_algebraic[106] = "mu_LR_B1Gs in component GsProtein (J_per_mol)"
    legend_algebraic[109] = "mu_aGs_GTP in component GsProtein (J_per_mol)"
    legend_algebraic[112] = "mu_beta_gamma_Gs in component GsProtein (J_per_mol)"
    legend_algebraic[115] = "mu_aGs_GDP in component GsProtein (J_per_mol)"
    legend_algebraic[118] = "mu_Pi in component GsProtein (J_per_mol)"
    legend_algebraic[122] = "mu_GTP in component GsProtein (J_per_mol)"
    legend_algebraic[126] = "mu_GDP in component GsProtein (J_per_mol)"
    legend_algebraic[43] = "R_T in component GsProtein (fmol)"
    legend_algebraic[78] = "Gs_T in component GsProtein (fmol)"
    legend_algebraic[135] = "vact1_Gi in component GiProtein (fmol_per_sec)"
    legend_algebraic[138] = "vact2_Gi in component GiProtein (fmol_per_sec)"
    legend_algebraic[139] = "vhyd_Gi in component GiProtein (fmol_per_sec)"
    legend_algebraic[140] = "vreassoc_Gi in component GiProtein (fmol_per_sec)"
    legend_algebraic[98] = "mu_R_M2 in component GiProtein (J_per_mol)"
    legend_algebraic[103] = "mu_Gi in component GiProtein (J_per_mol)"
    legend_algebraic[107] = "mu_R_M2Gi in component GiProtein (J_per_mol)"
    legend_algebraic[110] = "mu_LR_M2 in component GiProtein (J_per_mol)"
    legend_algebraic[113] = "mu_LR_M2Gi in component GiProtein (J_per_mol)"
    legend_algebraic[116] = "mu_aGi_GTP in component GiProtein (J_per_mol)"
    legend_algebraic[119] = "mu_beta_gamma_Gi in component GiProtein (J_per_mol)"
    legend_algebraic[123] = "mu_aGi_GDP in component GiProtein (J_per_mol)"
    legend_algebraic[127] = "mu_Pi in component GiProtein (J_per_mol)"
    legend_algebraic[131] = "mu_GTP in component GiProtein (J_per_mol)"
    legend_algebraic[133] = "mu_GDP in component GiProtein (J_per_mol)"
    legend_algebraic[68] = "R_T in component GiProtein (fmol)"
    legend_algebraic[99] = "Gi_T in component GiProtein (fmol)"
    legend_rates[0] = "d/dt q_ATP in component cAMP (fmol)"
    legend_rates[2] = "d/dt q_AC in component cAMP (fmol)"
    legend_rates[3] = "d/dt q_AC_ATP in component cAMP (fmol)"
    legend_rates[1] = "d/dt q_cAMP in component cAMP (fmol)"
    legend_rates[14] = "d/dt q_FSK in component cAMP (fmol)"
    legend_rates[6] = "d/dt q_FSK_AC in component cAMP (fmol)"
    legend_rates[7] = "d/dt q_FSK_AC_ATP in component cAMP (fmol)"
    legend_rates[13] = "d/dt q_aGs_GTP in component cAMP (fmol)"
    legend_rates[4] = "d/dt q_aGs_GTP_AC in component cAMP (fmol)"
    legend_rates[5] = "d/dt q_aGs_GTP_AC_ATP in component cAMP (fmol)"
    legend_rates[9] = "d/dt q_PDE_cAMP in component cAMP (fmol)"
    legend_rates[8] = "d/dt q_PDE in component cAMP (fmol)"
    legend_rates[11] = "d/dt q_IBMX in component cAMP (fmol)"
    legend_rates[12] = "d/dt q_PDEinh in component cAMP (fmol)"
    legend_rates[10] = "d/dt q_five_AMP in component cAMP (fmol)"
    legend_rates[15] = "d/dt q_aGi_GTP in component cAMP (fmol)"
    legend_rates[16] = "d/dt q_ACinh in component cAMP (fmol)"
    legend_rates[17] = "d/dt q_PPi in component cAMP (fmol)"
    legend_rates[18] = "d/dt q_L_B1 in component LRGbinding_B1AR (fmol)"
    legend_rates[19] = "d/dt q_R_B1 in component LRGbinding_B1AR (fmol)"
    legend_rates[20] = "d/dt q_Gs in component LRGbinding_B1AR (fmol)"
    legend_rates[21] = "d/dt q_LR_B1 in component LRGbinding_B1AR (fmol)"
    legend_rates[22] = "d/dt q_R_B1Gs in component LRGbinding_B1AR (fmol)"
    legend_rates[23] = "d/dt q_LR_B1Gs in component LRGbinding_B1AR (fmol)"
    legend_rates[24] = "d/dt q_L_M2 in component LRGbinding_M2 (fmol)"
    legend_rates[25] = "d/dt q_R_M2 in component LRGbinding_M2 (fmol)"
    legend_rates[26] = "d/dt q_Gi in component LRGbinding_M2 (fmol)"
    legend_rates[27] = "d/dt q_LR_M2 in component LRGbinding_M2 (fmol)"
    legend_rates[28] = "d/dt q_R_M2Gi in component LRGbinding_M2 (fmol)"
    legend_rates[29] = "d/dt q_LR_M2Gi in component LRGbinding_M2 (fmol)"
    legend_rates[30] = "d/dt q_R_B1 in component GsProtein (fmol)"
    legend_rates[32] = "d/dt q_R_B1Gs in component GsProtein (fmol)"
    legend_rates[31] = "d/dt q_Gs in component GsProtein (fmol)"
    legend_rates[33] = "d/dt q_LR_B1 in component GsProtein (fmol)"
    legend_rates[34] = "d/dt q_LR_B1Gs in component GsProtein (fmol)"
    legend_rates[35] = "d/dt q_aGs_GTP in component GsProtein (fmol)"
    legend_rates[36] = "d/dt q_beta_gamma_Gs in component GsProtein (fmol)"
    legend_rates[37] = "d/dt q_aGs_GDP in component GsProtein (fmol)"
    legend_rates[38] = "d/dt q_Pi in component GsProtein (fmol)"
    legend_rates[39] = "d/dt q_GTP in component GsProtein (fmol)"
    legend_rates[40] = "d/dt q_GDP in component GsProtein (fmol)"
    legend_rates[41] = "d/dt q_R_M2 in component GiProtein (fmol)"
    legend_rates[43] = "d/dt q_R_M2Gi in component GiProtein (fmol)"
    legend_rates[42] = "d/dt q_Gi in component GiProtein (fmol)"
    legend_rates[44] = "d/dt q_LR_M2 in component GiProtein (fmol)"
    legend_rates[45] = "d/dt q_LR_M2Gi in component GiProtein (fmol)"
    legend_rates[46] = "d/dt q_aGi_GTP in component GiProtein (fmol)"
    legend_rates[47] = "d/dt q_beta_gamma_Gi in component GiProtein (fmol)"
    legend_rates[48] = "d/dt q_aGi_GDP in component GiProtein (fmol)"
    legend_rates[49] = "d/dt q_Pi in component GiProtein (fmol)"
    return (legend_states, legend_algebraic, legend_voi, legend_constants)

def initConsts(Gmult,igs):
    hackMultiplier = 1e0;
    constants = [0.0] * sizeConstants; states = [0.0] * sizeStates;
    constants[0] = 1.19049e+06
    constants[1] = 0.00248563
    constants[2] = 49840.4
    constants[3] = 0.13449
    constants[4] = 5.81948e+07
    constants[5] = 6.76684e-17
    constants[6] = 6013.05
    constants[7] = 0.23128
    constants[8] = 220.24
    constants[9] = 1173.07
    constants[10] = 136970
    constants[11] = 351.702
    constants[12] = 1949.85
    constants[13] = 14.6972
    constants[14] = 4.76612
    constants[15] = 48932.3
    constants[16] = 3468.13
    constants[17] = 20.1802
    constants[18] = 82.6965
    constants[19] = 23570
    constants[20] = 0.363553
    constants[21] = 0.472994
    constants[22] = 0.0560685
    constants[23] = 1563.43
    constants[24] = 428.713
    constants[25] = 0.10939
    constants[26] = 0.00358651
    constants[27] = 0.413631
    constants[28] = 3802.06
    constants[29] = 6.842e-05
    constants[30] = 0.0154937
    constants[31] = 0.964843
    constants[32] = 2.33903
    constants[33] = 2.4781
    constants[34] = 1.83726
    constants[35] = 0.0212235
    constants[36] = 0.0429592
    constants[37] = 0.907054
    constants[38] = 0.628454
    constants[39] = 0.0154937
    constants[40] = 0.0141004
    constants[41] = 13.1991
    constants[42] = 0.186657
    constants[43] = 1.45328e-05
    constants[44] = 0.024903
    constants[45] = 8.26545
    constants[46] = 0.000128372
    constants[47] = 0.0783988
    constants[48] = 0.0220282
    constants[49] = 1.31984
    constants[50] = 9.01184
    constants[51] = 73.3398
    constants[52] = 56.3705
    constants[53] = 0.11083
    constants[54] = 0.0323495
    constants[55] = 0.501288
    constants[56] = 1.35667
    constants[57] = 37.7835
    constants[58] = 23.0482
    constants[59] = 0.0048057
    constants[60] = 0.0612439
    constants[61] = 0.546852
    constants[62] = 0.000340182
    constants[63] = 0.0718472
    constants[64] = 0.0141226
    constants[65] = 0.00843467
    constants[66] = 34.4
    constants[67] = 500
    constants[68] = 3.5e-4
    constants[69] = 3e-4
    constants[70] = 0.25e-4
    constants[71] = 1.8e-4
    constants[72] = 1e1
    constants[73] = 1e-5
    constants[74] = 190
    constants[75] = 1.889E-03
    constants[76] = 1e-18
    constants[77] = 1e-18
    constants[78] = 3.800E-05
    constants[79] = 1e-18
    constants[80] = 1e-18
    constants[81] = 1e-18
    constants[82] = 1e-18
    constants[83] = 1e-18
    constants[84] = 1.482E-03
    constants[85] = 1e-18
    constants[86] = 1e-18
    constants[87] = 3.80E-02
    constants[88] = 1e-18
    constants[89] = 1e-18
    constants[90] = 1e-18
    constants[91] = 1e-18
    constants[92] = 0.0004579000
    constants[93] = 0.1455400000
    constants[94] = 1e-18
    constants[95] = 1e-18
    constants[96] = 1e-18
    constants[97] = 0.00072
    constants[98] = 0.00836
    constants[99] = 1e-18
    constants[100] = 1e-18
    constants[101] = 1e-18
    constants[102] = 1e-18
    constants[103] = 1e-18
    constants[104] = 570
    constants[105] = 1e-18
    constants[106] = 1e-18
    constants[107] = 1e-18
    constants[108] = 1e-18
    constants[109] = 2.2
    constants[110] = 1.1
    states[0] = 1e-16
    states[1] = 1e-16
    states[2] = 1e-16
    states[3] = 1e-16
    states[4] = 1e-16
    states[5] = 1e-16
    states[6] = 1e-16
    states[7] = 1e-16
    states[8] = 1e-16
    states[9] = 1e-16
    states[10] = 1e-16
    states[11] = 1e-16
    states[12] = 1e-16
    states[13] = 1e-16
    states[14] = 1e-16
    states[15] = 1e-16
    states[16] = 1e-16
    states[17] = 1e-16
    states[18] = 1e-18
    states[19] = 1e-18
    states[20] = 1e-18
    states[21] = 1e-18
    states[22] = 1e-18
    states[23] = 1e-18
    states[24] = 1e-16
    states[25] = 1e-16
    states[26] = 1e-16
    states[27] = 1e-16
    states[28] = 1e-16
    states[29] = 1e-16
    states[30] = 1e-16
    states[31] = 1e-16
    states[32] = 1e-16
    states[33] = 1e-16
    states[34] = 1e-16
    states[35] = 1e-16
    states[36] = 1e-16
    states[37] = 1e-16
    states[38] = 1e-16
    states[39] = 1e-16
    states[40] = 1e-16
    states[41] = 1e-16
    states[42] = 1e-16
    states[43] = 1e-16
    states[44] = 1e-16
    states[45] = 1e-16
    states[46] = 1e-16
    states[47] = 1e-16
    states[48] = 1e-16
    states[49] = 1e-16
    constants[111] = 1e-16
    constants[112] = 1e-16
    constants[113] = 8.31
    constants[114] = 310
    constants[115] = 96485
    constants[116] = 38.0
    constants[117] = 34.4
    constants[118] = 34.4
    constants[119] = constants[72]/constants[71]
    
    constants = [c*Gmult if i in igs else c for i, c in enumerate(constants)]
    states = [s*hackMultiplier for s in states]
    return (states, constants)

def computeRates(voi, states, constants):
    print(voi)
    rates = [0.0] * sizeStates; algebraic = [0.0] * sizeAlgebraic
    algebraic[26] = constants[92]+states[19]+states[30]
    algebraic[46] = constants[113]*constants[114]*log(constants[48]*algebraic[26])
    algebraic[27] = constants[93]+states[20]+states[31]
    algebraic[49] = constants[113]*constants[114]*log(constants[49]*algebraic[27])
    algebraic[31] = constants[95]+states[22]+states[32]
    algebraic[55] = constants[113]*constants[114]*log(constants[51]*algebraic[31])
    algebraic[63] = constants[12]*exp((algebraic[46]+algebraic[49])/(constants[113]*constants[114]))-exp(algebraic[55]/(constants[113]*constants[114]))
    algebraic[0] = custom_piecewise([less(voi , constants[68]) & greater(voi , constants[68]-constants[71]), constants[73]+constants[119]*((voi-constants[68])+constants[71]) , greater_equal(voi , constants[68]) & less(voi , constants[68]+constants[70]), constants[72]+constants[73] , less(voi , constants[68]+constants[71]+constants[70]) & greater_equal(voi , constants[68]+constants[70]), constants[73]+-constants[119]*(((voi-constants[68])-constants[71])-constants[70]) , True, constants[73]])
    algebraic[24] = algebraic[0]+states[18]
    algebraic[39] = constants[113]*constants[114]*log(constants[47]*algebraic[24])
    algebraic[33] = constants[96]+states[23]+states[34]
    algebraic[58] = constants[113]*constants[114]*log(constants[52]*algebraic[33])
    algebraic[71] = constants[13]*exp((algebraic[55]+algebraic[39])/(constants[113]*constants[114]))-exp(algebraic[58]/(constants[113]*constants[114]))
    rates[22] = algebraic[63]-algebraic[71]
    algebraic[29] = constants[94]+states[21]+states[33]
    algebraic[52] = constants[113]*constants[114]*log(constants[50]*algebraic[29])
    algebraic[76] = constants[14]*exp((algebraic[52]+algebraic[49])/(constants[113]*constants[114]))-exp(algebraic[58]/(constants[113]*constants[114]))
    rates[20] = -algebraic[63]-algebraic[76]
    rates[23] = algebraic[71]+algebraic[76]
    algebraic[81] = constants[15]*exp((algebraic[46]+algebraic[39])/(constants[113]*constants[114]))-exp(algebraic[52]/(constants[113]*constants[114]))
    rates[18] = -algebraic[71]-algebraic[81]
    rates[19] = -algebraic[63]-algebraic[81]
    rates[21] = -algebraic[76]+algebraic[81]
    algebraic[44] = constants[97]+states[25]+states[41]
    algebraic[72] = constants[113]*constants[114]*log(constants[54]*algebraic[44])
    algebraic[47] = constants[98]+states[26]+states[42]
    algebraic[77] = constants[113]*constants[114]*log(constants[55]*algebraic[47])
    algebraic[53] = constants[100]+states[28]+states[43]
    algebraic[85] = constants[113]*constants[114]*log(constants[57]*algebraic[53])
    algebraic[91] = constants[16]*exp((algebraic[72]+algebraic[77])/(constants[113]*constants[114]))-exp(algebraic[85]/(constants[113]*constants[114]))
    algebraic[1] = custom_piecewise([less(voi , constants[69]) & greater(voi , constants[69]-constants[71]), constants[73]+constants[119]*((voi-constants[69])+constants[71]) , greater_equal(voi , constants[69]) & less(voi , constants[69]+constants[70]), constants[72]+constants[73] , less(voi , constants[69]+constants[71]+constants[70]) & greater_equal(voi , constants[69]+constants[70]), constants[73]+-constants[119]*(((voi-constants[69])-constants[71])-constants[70]) , True, constants[73]])
    algebraic[37] = algebraic[1]+states[24]
    algebraic[64] = constants[113]*constants[114]*log(constants[53]*algebraic[37])
    algebraic[56] = constants[101]+states[29]+states[45]
    algebraic[88] = constants[113]*constants[114]*log(constants[58]*algebraic[56])
    algebraic[96] = constants[17]*exp((algebraic[85]+algebraic[64])/(constants[113]*constants[114]))-exp(algebraic[88]/(constants[113]*constants[114]))
    rates[28] = algebraic[91]-algebraic[96]
    algebraic[50] = constants[99]+states[27]+states[44]
    algebraic[82] = constants[113]*constants[114]*log(constants[56]*algebraic[50])
    algebraic[101] = constants[18]*exp((algebraic[82]+algebraic[77])/(constants[113]*constants[114]))-exp(algebraic[88]/(constants[113]*constants[114]))
    rates[26] = -algebraic[91]-algebraic[101]
    rates[29] = algebraic[96]+algebraic[101]
    algebraic[2] = constants[74]+states[0]
    algebraic[28] = constants[113]*constants[114]*log(constants[29]*algebraic[2])
    algebraic[4] = constants[75]+states[2]
    algebraic[32] = constants[113]*constants[114]*log(constants[31]*algebraic[4])
    algebraic[5] = constants[77]+states[3]
    algebraic[34] = constants[113]*constants[114]*log(constants[32]*algebraic[5])
    algebraic[100] = constants[0]*(exp((algebraic[32]+algebraic[28])/(constants[113]*constants[114]))-exp(algebraic[34]/(constants[113]*constants[114])))
    algebraic[3] = constants[76]+states[1]
    algebraic[30] = constants[113]*constants[114]*log(constants[30]*algebraic[3])
    algebraic[25] = constants[91]+states[17]
    algebraic[95] = constants[113]*constants[114]*log(constants[46]*algebraic[25])
    algebraic[104] = constants[1]*(exp(algebraic[34]/(constants[113]*constants[114]))-exp((algebraic[32]+algebraic[30]+algebraic[95])/(constants[113]*constants[114])))
    rates[3] = algebraic[100]-algebraic[104]
    algebraic[105] = constants[19]*exp((algebraic[72]+algebraic[64])/(constants[113]*constants[114]))-exp(algebraic[82]/(constants[113]*constants[114]))
    rates[24] = -algebraic[96]-algebraic[105]
    rates[25] = -algebraic[91]-algebraic[105]
    rates[27] = -algebraic[101]+algebraic[105]
    algebraic[6] = constants[82]+states[4]
    algebraic[38] = constants[113]*constants[114]*log(constants[33]*algebraic[6])
    algebraic[7] = constants[83]+states[5]
    algebraic[45] = constants[113]*constants[114]*log(constants[34]*algebraic[7])
    algebraic[108] = constants[2]*(exp((algebraic[38]+algebraic[28])/(constants[113]*constants[114]))-exp(algebraic[45]/(constants[113]*constants[114])))
    algebraic[111] = constants[3]*(exp(algebraic[45]/(constants[113]*constants[114]))-exp((algebraic[38]+algebraic[30]+algebraic[95])/(constants[113]*constants[114])))
    rates[5] = algebraic[108]-algebraic[111]
    algebraic[8] = constants[79]+states[6]
    algebraic[48] = constants[113]*constants[114]*log(constants[35]*algebraic[8])
    algebraic[9] = constants[80]+states[7]
    algebraic[51] = constants[113]*constants[114]*log(constants[36]*algebraic[9])
    algebraic[114] = constants[4]*(exp((algebraic[48]+algebraic[28])/(constants[113]*constants[114]))-exp(algebraic[51]/(constants[113]*constants[114])))
    rates[0] = (-algebraic[100]-algebraic[114])-algebraic[108]
    algebraic[117] = constants[5]*(exp(algebraic[51]/(constants[113]*constants[114]))-exp((algebraic[48]+algebraic[30]+algebraic[95])/(constants[113]*constants[114])))
    rates[7] = algebraic[114]-algebraic[117]
    algebraic[10] = constants[84]+states[8]
    algebraic[54] = constants[113]*constants[114]*log(constants[37]*algebraic[10])
    algebraic[13] = constants[86]+states[9]
    algebraic[57] = constants[113]*constants[114]*log(constants[38]*algebraic[13])
    algebraic[120] = constants[6]*(exp((algebraic[54]+algebraic[30])/(constants[113]*constants[114]))-exp(algebraic[57]/(constants[113]*constants[114])))
    rates[1] = (algebraic[104]+algebraic[117]+algebraic[111])-algebraic[120]
    algebraic[19] = constants[81]+states[13]+states[35]
    algebraic[80] = constants[113]*constants[114]*log(constants[42]*algebraic[19])
    algebraic[121] = constants[9]*(exp((algebraic[32]+algebraic[80])/(constants[113]*constants[114]))-exp(algebraic[38]/(constants[113]*constants[114])))
    rates[13] = -algebraic[121]
    rates[4] = (algebraic[121]-algebraic[108])+algebraic[111]
    algebraic[20] = constants[78]+states[14]
    algebraic[84] = constants[113]*constants[114]*log(constants[43]*algebraic[20])
    algebraic[125] = constants[10]*(exp((algebraic[84]+algebraic[32])/(constants[113]*constants[114]))-exp(algebraic[48]/(constants[113]*constants[114])))
    rates[14] = -algebraic[125]
    rates[6] = (algebraic[125]+algebraic[117])-algebraic[114]
    algebraic[14] = constants[88]+states[10]
    algebraic[62] = constants[113]*constants[114]*log(constants[39]*algebraic[14])
    algebraic[124] = constants[7]*(exp(algebraic[57]/(constants[113]*constants[114]))-exp((algebraic[54]+algebraic[62])/(constants[113]*constants[114])))
    rates[9] = algebraic[120]-algebraic[124]
    rates[10] = algebraic[124]
    algebraic[22] = constants[89]+states[15]+states[46]
    algebraic[87] = constants[113]*constants[114]*log(constants[44]*algebraic[22])
    algebraic[23] = constants[90]+states[16]
    algebraic[90] = constants[113]*constants[114]*log(constants[45]*algebraic[23])
    algebraic[129] = constants[11]*(exp((algebraic[32]+algebraic[87])/(constants[113]*constants[114]))-exp(algebraic[90]/(constants[113]*constants[114])))
    rates[2] = (((algebraic[104]-algebraic[100])-algebraic[121])-algebraic[125])-algebraic[129]
    algebraic[18] = constants[85]+states[12]
    algebraic[75] = constants[113]*constants[114]*log(constants[41]*algebraic[18])
    algebraic[17] = constants[87]+states[11]
    algebraic[70] = constants[113]*constants[114]*log(constants[40]*algebraic[17])
    algebraic[128] = constants[8]*(exp((algebraic[54]+algebraic[70])/(constants[113]*constants[114]))-exp(algebraic[75]/(constants[113]*constants[114])))
    rates[8] = (algebraic[124]-algebraic[120])-algebraic[128]
    rates[11] = -algebraic[128]
    rates[12] = algebraic[128]
    rates[15] = -algebraic[129]
    rates[16] = algebraic[129]
    rates[17] = algebraic[129]
    algebraic[89] = constants[113]*constants[114]*log(constants[48]*algebraic[26])
    algebraic[97] = constants[113]*constants[114]*log(constants[51]*algebraic[31])
    algebraic[109] = constants[113]*constants[114]*log(constants[42]*algebraic[19])
    algebraic[61] = constants[102]+states[36]
    algebraic[112] = constants[113]*constants[114]*log(constants[59]*algebraic[61])
    algebraic[79] = constants[109]+states[39]+constants[111]
    algebraic[122] = constants[113]*constants[114]*log(constants[62]*algebraic[79])
    algebraic[83] = constants[110]+states[40]+constants[112]
    algebraic[126] = constants[113]*constants[114]*log(constants[63]*algebraic[83])
    algebraic[130] = constants[20]*(exp((algebraic[97]+algebraic[122])/(constants[113]*constants[114]))-exp((algebraic[109]+algebraic[112]+algebraic[89]+algebraic[126])/(constants[113]*constants[114])))
    rates[30] = algebraic[130]
    rates[32] = -algebraic[130]
    algebraic[102] = constants[113]*constants[114]*log(constants[50]*algebraic[29])
    algebraic[106] = constants[113]*constants[114]*log(constants[52]*algebraic[33])
    algebraic[132] = constants[21]*(exp((algebraic[106]+algebraic[122])/(constants[113]*constants[114]))-exp((algebraic[109]+algebraic[112]+algebraic[102]+algebraic[126])/(constants[113]*constants[114])))
    rates[33] = algebraic[132]
    rates[34] = -algebraic[132]
    algebraic[69] = constants[103]+states[37]
    algebraic[115] = constants[113]*constants[114]*log(constants[60]*algebraic[69])
    algebraic[74] = constants[104]+states[38]+states[49]
    algebraic[118] = constants[113]*constants[114]*log(constants[61]*algebraic[74])
    algebraic[134] = constants[22]*(exp(algebraic[109]/(constants[113]*constants[114]))-exp((algebraic[115]+algebraic[118])/(constants[113]*constants[114])))
    rates[35] = (algebraic[130]+algebraic[132])-algebraic[134]
    algebraic[98] = constants[113]*constants[114]*log(constants[54]*algebraic[44])
    algebraic[107] = constants[113]*constants[114]*log(constants[57]*algebraic[53])
    algebraic[116] = constants[113]*constants[114]*log(constants[44]*algebraic[22])
    algebraic[86] = constants[105]+states[47]
    algebraic[119] = constants[113]*constants[114]*log(constants[64]*algebraic[86])
    algebraic[131] = constants[113]*constants[114]*log(constants[62]*algebraic[79])
    algebraic[133] = constants[113]*constants[114]*log(constants[63]*algebraic[83])
    algebraic[135] = constants[25]*(exp((algebraic[107]+algebraic[131])/(constants[113]*constants[114]))-exp((algebraic[116]+algebraic[119]+algebraic[98]+algebraic[133])/(constants[113]*constants[114])))
    rates[41] = algebraic[135]
    rates[43] = -algebraic[135]
    algebraic[92] = constants[113]*constants[114]*log(constants[49]*algebraic[27])
    algebraic[136] = constants[23]*(exp((algebraic[115]+algebraic[112])/(constants[113]*constants[114]))-exp(algebraic[92]/(constants[113]*constants[114])))
    rates[31] = algebraic[136]
    rates[36] = (algebraic[130]+algebraic[132])-algebraic[136]
    rates[37] = algebraic[134]-algebraic[136]
    algebraic[137] = constants[24]*(exp((algebraic[126]+algebraic[118])/(constants[113]*constants[114]))-exp(algebraic[122]/(constants[113]*constants[114])))
    rates[38] = -algebraic[137]+algebraic[134]
    rates[39] = algebraic[137]
    rates[40] = -algebraic[137]
    algebraic[110] = constants[113]*constants[114]*log(constants[56]*algebraic[50])
    algebraic[113] = constants[113]*constants[114]*log(constants[58]*algebraic[56])
    algebraic[138] = constants[26]*(exp((algebraic[113]+algebraic[131])/(constants[113]*constants[114]))-exp((algebraic[116]+algebraic[119]+algebraic[110]+algebraic[133])/(constants[113]*constants[114])))
    rates[44] = algebraic[138]
    rates[45] = -algebraic[138]
    algebraic[93] = constants[106]+states[48]
    algebraic[123] = constants[113]*constants[114]*log(constants[65]*algebraic[93])
    algebraic[127] = constants[113]*constants[114]*log(constants[61]*algebraic[74])
    algebraic[139] = constants[27]*(exp(algebraic[116]/(constants[113]*constants[114]))-exp((algebraic[123]+algebraic[127])/(constants[113]*constants[114])))
    rates[46] = (algebraic[135]+algebraic[138])-algebraic[139]
    rates[49] = algebraic[139]
    algebraic[103] = constants[113]*constants[114]*log(constants[55]*algebraic[47])
    algebraic[140] = constants[28]*(exp((algebraic[123]+algebraic[119])/(constants[113]*constants[114]))-exp(algebraic[103]/(constants[113]*constants[114])))
    rates[42] = algebraic[140]
    rates[47] = (algebraic[135]+algebraic[138])-algebraic[140]
    rates[48] = algebraic[139]-algebraic[140]
    return(rates)

def computeAlgebraic(constants, states, voi):
    algebraic = array([[0.0] * len(voi)] * sizeAlgebraic)
    states = array(states)
    voi = array(voi)
    if False: #len(voi)>1:
        # HACK: make any neative values positive
        print('******************')
        print('HARDCODING NUMBERS FOR Q_L_B1 AND Q_GS TO BE NON NEGATIVE')
        print('******************')
        algebraic[24] = [max(a,finfo(float).eps) for a in algebraic[24]] # q_L_B1
        algebraic[27] = [max(a,finfo(float).eps) for a in algebraic[27]] # q_Gs
    algebraic[26] = constants[92]+states[19]+states[30]
    algebraic[46] = constants[113]*constants[114]*log(constants[48]*algebraic[26])
    algebraic[27] = constants[93]+states[20]+states[31]
    algebraic[49] = constants[113]*constants[114]*log(constants[49]*algebraic[27])
    algebraic[31] = constants[95]+states[22]+states[32]
    algebraic[55] = constants[113]*constants[114]*log(constants[51]*algebraic[31])
    algebraic[63] = constants[12]*exp((algebraic[46]+algebraic[49])/(constants[113]*constants[114]))-exp(algebraic[55]/(constants[113]*constants[114]))
    algebraic[0] = custom_piecewise([less(voi , constants[68]) & greater(voi , constants[68]-constants[71]), constants[73]+constants[119]*((voi-constants[68])+constants[71]) , greater_equal(voi , constants[68]) & less(voi , constants[68]+constants[70]), constants[72]+constants[73] , less(voi , constants[68]+constants[71]+constants[70]) & greater_equal(voi , constants[68]+constants[70]), constants[73]+-constants[119]*(((voi-constants[68])-constants[71])-constants[70]) , True, constants[73]])
    algebraic[24] = algebraic[0]+states[18]
    algebraic[39] = constants[113]*constants[114]*log(constants[47]*algebraic[24])
    algebraic[33] = constants[96]+states[23]+states[34]
    algebraic[58] = constants[113]*constants[114]*log(constants[52]*algebraic[33])
    algebraic[71] = constants[13]*exp((algebraic[55]+algebraic[39])/(constants[113]*constants[114]))-exp(algebraic[58]/(constants[113]*constants[114]))
    algebraic[29] = constants[94]+states[21]+states[33]
    algebraic[52] = constants[113]*constants[114]*log(constants[50]*algebraic[29])
    algebraic[76] = constants[14]*exp((algebraic[52]+algebraic[49])/(constants[113]*constants[114]))-exp(algebraic[58]/(constants[113]*constants[114]))
    algebraic[81] = constants[15]*exp((algebraic[46]+algebraic[39])/(constants[113]*constants[114]))-exp(algebraic[52]/(constants[113]*constants[114]))
    algebraic[44] = constants[97]+states[25]+states[41]
    algebraic[72] = constants[113]*constants[114]*log(constants[54]*algebraic[44])
    algebraic[47] = constants[98]+states[26]+states[42]
    algebraic[77] = constants[113]*constants[114]*log(constants[55]*algebraic[47])
    algebraic[53] = constants[100]+states[28]+states[43]
    algebraic[85] = constants[113]*constants[114]*log(constants[57]*algebraic[53])
    algebraic[91] = constants[16]*exp((algebraic[72]+algebraic[77])/(constants[113]*constants[114]))-exp(algebraic[85]/(constants[113]*constants[114]))
    algebraic[1] = custom_piecewise([less(voi , constants[69]) & greater(voi , constants[69]-constants[71]), constants[73]+constants[119]*((voi-constants[69])+constants[71]) , greater_equal(voi , constants[69]) & less(voi , constants[69]+constants[70]), constants[72]+constants[73] , less(voi , constants[69]+constants[71]+constants[70]) & greater_equal(voi , constants[69]+constants[70]), constants[73]+-constants[119]*(((voi-constants[69])-constants[71])-constants[70]) , True, constants[73]])
    algebraic[37] = algebraic[1]+states[24]
    algebraic[64] = constants[113]*constants[114]*log(constants[53]*algebraic[37])
    algebraic[56] = constants[101]+states[29]+states[45]
    algebraic[88] = constants[113]*constants[114]*log(constants[58]*algebraic[56])
    algebraic[96] = constants[17]*exp((algebraic[85]+algebraic[64])/(constants[113]*constants[114]))-exp(algebraic[88]/(constants[113]*constants[114]))
    algebraic[50] = constants[99]+states[27]+states[44]
    algebraic[82] = constants[113]*constants[114]*log(constants[56]*algebraic[50])
    algebraic[101] = constants[18]*exp((algebraic[82]+algebraic[77])/(constants[113]*constants[114]))-exp(algebraic[88]/(constants[113]*constants[114]))
    algebraic[2] = constants[74]+states[0]
    algebraic[28] = constants[113]*constants[114]*log(constants[29]*algebraic[2])
    algebraic[4] = constants[75]+states[2]
    algebraic[32] = constants[113]*constants[114]*log(constants[31]*algebraic[4])
    algebraic[5] = constants[77]+states[3]
    algebraic[34] = constants[113]*constants[114]*log(constants[32]*algebraic[5])
    algebraic[100] = constants[0]*(exp((algebraic[32]+algebraic[28])/(constants[113]*constants[114]))-exp(algebraic[34]/(constants[113]*constants[114])))
    algebraic[3] = constants[76]+states[1]
    algebraic[30] = constants[113]*constants[114]*log(constants[30]*algebraic[3])
    algebraic[25] = constants[91]+states[17]
    algebraic[95] = constants[113]*constants[114]*log(constants[46]*algebraic[25])
    algebraic[104] = constants[1]*(exp(algebraic[34]/(constants[113]*constants[114]))-exp((algebraic[32]+algebraic[30]+algebraic[95])/(constants[113]*constants[114])))
    algebraic[105] = constants[19]*exp((algebraic[72]+algebraic[64])/(constants[113]*constants[114]))-exp(algebraic[82]/(constants[113]*constants[114]))
    algebraic[6] = constants[82]+states[4]
    algebraic[38] = constants[113]*constants[114]*log(constants[33]*algebraic[6])
    algebraic[7] = constants[83]+states[5]
    algebraic[45] = constants[113]*constants[114]*log(constants[34]*algebraic[7])
    algebraic[108] = constants[2]*(exp((algebraic[38]+algebraic[28])/(constants[113]*constants[114]))-exp(algebraic[45]/(constants[113]*constants[114])))
    algebraic[111] = constants[3]*(exp(algebraic[45]/(constants[113]*constants[114]))-exp((algebraic[38]+algebraic[30]+algebraic[95])/(constants[113]*constants[114])))
    algebraic[8] = constants[79]+states[6]
    algebraic[48] = constants[113]*constants[114]*log(constants[35]*algebraic[8])
    algebraic[9] = constants[80]+states[7]
    algebraic[51] = constants[113]*constants[114]*log(constants[36]*algebraic[9])
    algebraic[114] = constants[4]*(exp((algebraic[48]+algebraic[28])/(constants[113]*constants[114]))-exp(algebraic[51]/(constants[113]*constants[114])))
    algebraic[117] = constants[5]*(exp(algebraic[51]/(constants[113]*constants[114]))-exp((algebraic[48]+algebraic[30]+algebraic[95])/(constants[113]*constants[114])))
    algebraic[10] = constants[84]+states[8]
    algebraic[54] = constants[113]*constants[114]*log(constants[37]*algebraic[10])
    algebraic[13] = constants[86]+states[9]
    algebraic[57] = constants[113]*constants[114]*log(constants[38]*algebraic[13])
    algebraic[120] = constants[6]*(exp((algebraic[54]+algebraic[30])/(constants[113]*constants[114]))-exp(algebraic[57]/(constants[113]*constants[114])))
    algebraic[19] = constants[81]+states[13]+states[35]
    algebraic[80] = constants[113]*constants[114]*log(constants[42]*algebraic[19])
    algebraic[121] = constants[9]*(exp((algebraic[32]+algebraic[80])/(constants[113]*constants[114]))-exp(algebraic[38]/(constants[113]*constants[114])))
    algebraic[20] = constants[78]+states[14]
    algebraic[84] = constants[113]*constants[114]*log(constants[43]*algebraic[20])
    algebraic[125] = constants[10]*(exp((algebraic[84]+algebraic[32])/(constants[113]*constants[114]))-exp(algebraic[48]/(constants[113]*constants[114])))
    algebraic[14] = constants[88]+states[10]
    algebraic[62] = constants[113]*constants[114]*log(constants[39]*algebraic[14])
    algebraic[124] = constants[7]*(exp(algebraic[57]/(constants[113]*constants[114]))-exp((algebraic[54]+algebraic[62])/(constants[113]*constants[114])))
    algebraic[22] = constants[89]+states[15]+states[46]
    algebraic[87] = constants[113]*constants[114]*log(constants[44]*algebraic[22])
    algebraic[23] = constants[90]+states[16]
    algebraic[90] = constants[113]*constants[114]*log(constants[45]*algebraic[23])
    algebraic[129] = constants[11]*(exp((algebraic[32]+algebraic[87])/(constants[113]*constants[114]))-exp(algebraic[90]/(constants[113]*constants[114])))
    algebraic[18] = constants[85]+states[12]
    algebraic[75] = constants[113]*constants[114]*log(constants[41]*algebraic[18])
    algebraic[17] = constants[87]+states[11]
    algebraic[70] = constants[113]*constants[114]*log(constants[40]*algebraic[17])
    algebraic[128] = constants[8]*(exp((algebraic[54]+algebraic[70])/(constants[113]*constants[114]))-exp(algebraic[75]/(constants[113]*constants[114])))
    algebraic[89] = constants[113]*constants[114]*log(constants[48]*algebraic[26])
    algebraic[97] = constants[113]*constants[114]*log(constants[51]*algebraic[31])
    algebraic[109] = constants[113]*constants[114]*log(constants[42]*algebraic[19])
    algebraic[61] = constants[102]+states[36]
    algebraic[112] = constants[113]*constants[114]*log(constants[59]*algebraic[61])
    algebraic[79] = constants[109]+states[39]+constants[111]
    algebraic[122] = constants[113]*constants[114]*log(constants[62]*algebraic[79])
    algebraic[83] = constants[110]+states[40]+constants[112]
    algebraic[126] = constants[113]*constants[114]*log(constants[63]*algebraic[83])
    algebraic[130] = constants[20]*(exp((algebraic[97]+algebraic[122])/(constants[113]*constants[114]))-exp((algebraic[109]+algebraic[112]+algebraic[89]+algebraic[126])/(constants[113]*constants[114])))
    algebraic[102] = constants[113]*constants[114]*log(constants[50]*algebraic[29])
    algebraic[106] = constants[113]*constants[114]*log(constants[52]*algebraic[33])
    algebraic[132] = constants[21]*(exp((algebraic[106]+algebraic[122])/(constants[113]*constants[114]))-exp((algebraic[109]+algebraic[112]+algebraic[102]+algebraic[126])/(constants[113]*constants[114])))
    algebraic[69] = constants[103]+states[37]
    algebraic[115] = constants[113]*constants[114]*log(constants[60]*algebraic[69])
    algebraic[74] = constants[104]+states[38]+states[49]
    algebraic[118] = constants[113]*constants[114]*log(constants[61]*algebraic[74])
    algebraic[134] = constants[22]*(exp(algebraic[109]/(constants[113]*constants[114]))-exp((algebraic[115]+algebraic[118])/(constants[113]*constants[114])))
    algebraic[98] = constants[113]*constants[114]*log(constants[54]*algebraic[44])
    algebraic[107] = constants[113]*constants[114]*log(constants[57]*algebraic[53])
    algebraic[116] = constants[113]*constants[114]*log(constants[44]*algebraic[22])
    algebraic[86] = constants[105]+states[47]
    algebraic[119] = constants[113]*constants[114]*log(constants[64]*algebraic[86])
    algebraic[131] = constants[113]*constants[114]*log(constants[62]*algebraic[79])
    algebraic[133] = constants[113]*constants[114]*log(constants[63]*algebraic[83])
    algebraic[135] = constants[25]*(exp((algebraic[107]+algebraic[131])/(constants[113]*constants[114]))-exp((algebraic[116]+algebraic[119]+algebraic[98]+algebraic[133])/(constants[113]*constants[114])))
    algebraic[92] = constants[113]*constants[114]*log(constants[49]*algebraic[27])
    algebraic[136] = constants[23]*(exp((algebraic[115]+algebraic[112])/(constants[113]*constants[114]))-exp(algebraic[92]/(constants[113]*constants[114])))
    algebraic[137] = constants[24]*(exp((algebraic[126]+algebraic[118])/(constants[113]*constants[114]))-exp(algebraic[122]/(constants[113]*constants[114])))
    algebraic[110] = constants[113]*constants[114]*log(constants[56]*algebraic[50])
    algebraic[113] = constants[113]*constants[114]*log(constants[58]*algebraic[56])
    algebraic[138] = constants[26]*(exp((algebraic[113]+algebraic[131])/(constants[113]*constants[114]))-exp((algebraic[116]+algebraic[119]+algebraic[110]+algebraic[133])/(constants[113]*constants[114])))
    algebraic[93] = constants[106]+states[48]
    algebraic[123] = constants[113]*constants[114]*log(constants[65]*algebraic[93])
    algebraic[127] = constants[113]*constants[114]*log(constants[61]*algebraic[74])
    algebraic[139] = constants[27]*(exp(algebraic[116]/(constants[113]*constants[114]))-exp((algebraic[123]+algebraic[127])/(constants[113]*constants[114])))
    algebraic[103] = constants[113]*constants[114]*log(constants[55]*algebraic[47])
    algebraic[140] = constants[28]*(exp((algebraic[123]+algebraic[119])/(constants[113]*constants[114]))-exp(algebraic[103]/(constants[113]*constants[114])))
    algebraic[11] = algebraic[2]+algebraic[5]+algebraic[9]+algebraic[7]
    algebraic[12] = algebraic[4]+algebraic[5]+algebraic[8]+algebraic[9]+algebraic[6]+algebraic[7]
    algebraic[15] = algebraic[3]+algebraic[13]+states[10]
    algebraic[16] = algebraic[3]+algebraic[13]+algebraic[14]+algebraic[2]+algebraic[5]+algebraic[7]+algebraic[9]
    algebraic[21] = algebraic[19]+algebraic[6]+algebraic[7]
    algebraic[35] = algebraic[24]+algebraic[33]+algebraic[29]
    algebraic[36] = algebraic[26]+algebraic[31]+algebraic[29]+algebraic[33]
    algebraic[40] = algebraic[24]+algebraic[29]+algebraic[33]
    algebraic[41] = algebraic[26]+algebraic[29]+algebraic[31]+algebraic[33]
    algebraic[42] = algebraic[27]+algebraic[31]+algebraic[33]
    algebraic[43] = algebraic[26]+algebraic[31]+algebraic[29]+algebraic[33]
    algebraic[59] = algebraic[37]+algebraic[56]+algebraic[50]
    algebraic[60] = algebraic[44]+algebraic[53]+algebraic[50]+algebraic[56]
    algebraic[65] = algebraic[37]+algebraic[50]+algebraic[56]
    algebraic[66] = algebraic[44]+algebraic[50]+algebraic[53]+algebraic[56]
    algebraic[67] = algebraic[47]+algebraic[53]+algebraic[56]
    algebraic[68] = algebraic[44]+algebraic[53]+algebraic[50]+algebraic[56]
    algebraic[73] = algebraic[27]+algebraic[31]+algebraic[33]+algebraic[19]+algebraic[69]
    algebraic[78] = algebraic[27]+algebraic[31]+algebraic[33]+algebraic[19]+algebraic[69]
    algebraic[94] = algebraic[47]+algebraic[53]+algebraic[56]+algebraic[22]+algebraic[93]
    algebraic[99] = algebraic[47]+algebraic[53]+algebraic[56]+algebraic[22]+algebraic[93]
    return algebraic

def custom_piecewise(cases):
    """Compute result of a piecewise function"""
    return select(cases[0::2],cases[1::2])

def solve_model():
    (legend_states, legend_algebraic, legend_voi, legend_constants) = createLegends()
    """Solve model with ODE solver"""
    from scipy.integrate import ode
    # Initialise constants and state variables. Multiply vertain enzyme concentrations with Gmult factor
    glabels = [
        # 'q_AC_init in component environment (fmol)',
        # 'q_cAMP_init in component environment (fmol)',
        # 'q_R_B1_init in component environment (fmol)',
        'q_Gs_init in component environment (fmol)',
        # 'q_R_M2_init in component environment (fmol)',
        # 'q_Gi_init in component environment (fmol)'
        ]
    [igs,_,_] = find_indices(glabels, legend_constants, legend_states, legend_algebraic);
    Gmult = 5e1; #1e3;
    (init_states, constants) = initConsts(Gmult,igs)

    # Set timespan to solve over
    voi = linspace(0, 12e-5, 150000)

    # options for stimulus protocol
    stimLabels = ["stimSt in component environment (second)",
"stimSt2 in component environment (second)",
"stimDur in component environment (second)",
"tRamp in component environment (second)",
"stimMag in component environment (fmol)",
"stimHolding in component environment (fmol)",
"freq in component environment (dimensionless)",
"m in component environment (fmol_per_sec)"]
    sd = find_indices_from_labels(stimLabels, legend_constants)
    constants[sd['freq']] = 1 #[0.25,0.25]; # per second # UNUSED
    constants[sd['stimSt']] = 5e-5
    constants[sd['stimSt2']] = 4e-5
    constants[sd['stimHolding']] = 1e-9
    constants[sd['stimMag']] = 1.888e1 #[1e6,1e6];
    constants[sd['tRamp']] = 5e-5 # seconds for rAMP start
    constants[sd['stimDur']] = 1e-5
    if False:
        constants[sd['stimMag']] = 0
    # recalculate m
    constants[sd['m']] = constants[sd['stimMag']]/constants[sd['tRamp']]

    # Construct ODE object to solve
    r = ode(computeRates)
    r.set_integrator('vode', method='bdf', atol=1e-07, rtol=1e-07, max_step=1e-9)
    r.set_initial_value(init_states, voi[0])
    r.set_f_params(constants)

    # Solve model
    states = array([[0.0] * len(voi)] * sizeStates)
    states[:,0] = init_states
    for (i,t) in enumerate(voi[1:]):
        if r.successful():
            r.integrate(t)
            states[:,i+1] = r.y
        else:
            break

    # Compute algebraic variables
    algebraic = computeAlgebraic(constants, states, voi)

    for glab in glabels:
        print('Gmult applied for ' + glab)
    return (voi, constants,states, algebraic, Gmult)

def plot_model(voi, constants,states, algebraic, Gmult):
    """Plot variables against variable of integration"""
                
    (legend_states, legend_algebraic, legend_voi, legend_constants) = createLegends()
    
    labels = ['q_L_B1_init in component environment (fmol)',
                'q_L_M2_init in component environment (fmol)', 
                'q_LR_B1Gs in component environment (fmol)', 
                'q_LR_M2Gi in component environment (fmol)', 
                'q_aGs_GTP in component environment (fmol)', 
                'q_aGi_GTP in component environment (fmol)', 
                'q_aGs_GTP_AC in component cAMP (fmol)', 
                'q_AC in component environment (fmol)',
                'q_ACinh in component environment (fmol)',
                'q_cAMP in component environment (fmol)', 
                'q_ATP in component environment (fmol)']
        
    if True:
        [_, i_st, i_alg] = find_indices(labels, legend_constants, legend_states, legend_algebraic)
        plot_selected(i_st,voi,states,legend_voi,legend_states,('LR_B1\nGmult=%g' %(Gmult)),int(ceil(sqrt(len(i_st)))))
        plot_selected(i_alg,voi,algebraic,legend_voi,legend_algebraic,('LR_B1\nGmult=%g' %(Gmult)),int(ceil(sqrt(len(i_alg)))))

        # plot chemostat concentrations: they should be constant, or machine
    # error order
    labels = [
        'L_B1_T in component environment (fmol)',
        'L_M2_T in component environment (fmol)',
        'R_B1_T in component environment (fmol)',
        'Gs_T in component environment (fmol)',
        'R_M2_T in component environment (fmol)',
        'Gi_T in component environment (fmol)',
        'adenosine_T in component environment (fmol)'
        ]
    labels_init = [
        'q_L_B1_init in component environment (fmol)',
        'q_L_M2_init in component environment (fmol)',
        'q_R_B1_init in component environment (fmol)',
        'q_Gs_init in component environment (fmol)',
        'q_R_M2_init in component environment (fmol)',
        'q_Gi_init in component environment (fmol)',
        'q_ATP_init in component environment (fmol)'
        ]
    [_, _, i_alg] = find_indices(labels, legend_constants, legend_states, legend_algebraic)
    [i_con, _, i_algstim] = find_indices(labels, legend_constants, legend_states, legend_algebraic)
    plot_2per(i_algstim,i_con, i_alg,voi,constants,algebraic,legend_algebraic,legend_constants,('chemostats\nGmult=%g' %(Gmult)),3)
    
    # debug R_B1_t
    if False:
        labels = ['q_R_B1 in component LRGbinding_B1AR (fmol)','q_R_B1 in component GsProtein (fmol)']
        [_, i_st, _] = find_indices(labels, legend_constants, legend_states, legend_algebraic)
        plot_selected(i_st,VOI,states,legend_VOI,LEGEND_STATES,('R_B1\nGmult=%g' %(Gmult)),int(ceil(sqrt(len(i_st)))))

    
    # debug aGs_GTP and aGiGTP
    if False:
        labels = [
            'q_R_B1GsP in component environment (fmol)',
            'q_R_M2GiP in component environment (fmol)',
            'q_aGs_GTP in component environment (fmol)',
            'q_aGi_GTP in component environment (fmol)',
            'vphos_R_B1Gs in component GsProtein (fmol_per_sec)',
            'vphos_LR_B1Gs in component GsProtein (fmol_per_sec)',
            'vphos_R_M2Gi in component GiProtein (fmol_per_sec)',
            'vphos_LR_M2Gi in component GiProtein (fmol_per_sec)',
            'vact1_Gs in component GsProtein (fmol_per_sec)',
            'vact2_Gs in component GsProtein (fmol_per_sec)',
            'vact1_Gi in component GiProtein (fmol_per_sec)',
            'vact2_Gi in component GiProtein (fmol_per_sec)',
            'vhyd_Gs in component GsProtein (fmol_per_sec)',
            'vhyd_Gi in component GiProtein (fmol_per_sec)',
            'q_aGs_GTP in component GsProtein (fmol)',
            'q_aGi_GTP in component GiProtein (fmol)',
            ]
        [_, i_st, i_alg] = find_indices(labels, legend_constants, legend_states, legend_algebraic)
        plot_selected(i_alg,voi,algebraic,legend_voi,legend_algebraic,('ag_gtp\ngmult=%g' %(Gmult)),int(ceil(sqrt(len(i_alg)))))
        plot_selected(i_st,voi,states,legend_voi,legend_states,('ag_GTP\nGmult=%g' %(Gmult)),int(ceil(sqrt(len(i_st)))))

        
    # plot all q variables to confirm if we are SS
    if False:
        plt.figure()
        n = ceil(sqrt(size(states,2)))
        for i in range(1,size(states,2)):
            plt.subplot(n,n,i+1)
            plt.plot(voi, states[:,i])
            xlabel(legend_voi)
            title(legend_states[i])

    if False:
        plt.figure(1)
        plt.plot(voi,vstack((states,algebraic)).T)
        plt.xlabel(legend_voi)
        plt.legend(legend_states + legend_algebraic, loc='best')

    plt.show()


def find_indices(labels, legend_constants, legend_states, legend_algebraic):
    i_con = []
    i_st = []
    i_alg = []
    for lab in labels:
        try:
            i_con.append(legend_constants.index(lab))
        except:
            try:
                i_alg.append(legend_algebraic.index(lab))
            except:
                i_st.append(legend_states.index(lab))

    return (i_con, i_st, i_alg)


def find_indices_from_labels(labels, legend_list):
    # return indices for a name in a dict, with the key being the name of the label, andits value as the index
    sd = dict()
    i_found = [legend_list.index(lab) for lab in labels]
    sd = {labels[i].split(' ')[0]: i_found[i] for i in range(len(labels))}
    return sd
    
def plot_selected(ids,x,y,legend_x,legend_y,titlestr,ns):
    istart = 30;
    plt.figure();
    for i,id in enumerate(ids):
        plt.subplot(ns,ns,i+1)
        plt.plot(x[istart:-1], y[id, istart:-1])
        plt.xlabel('time (s)')
        plt.legend([legend_y[id].split(' ')[0]])
    # plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    plt.suptitle(titlestr)    

def plot_2per(i_alg0,id0,ids,x,y0,y,legend_y,legend_y_con,titlestr,ns):
    istart = 30;
    plt.figure()
    if i_alg0:
        idoffset = len(i_alg0)
        for i in range(idoffset):
            plt.subplot(ns,ns,i+1)
            plt.plot(x[istart:-1], y[i_alg0[i],istart:-1],'x-')
            plt.plot(x[istart:-1], y[ids[i],istart:-1])
            plt.xlabel('time (s)')
            diff = mean(abs(y[i_alg0[i],istart:-1] - y[ids[i],istart:-1]))
            plt.title(legend_y[i_alg0[i]].split(' in')[0] +' avg abs error = ' + str(diff))
            str1 = legend_y[i_alg0[i]].split(' ')[0]
            str2 = legend_y[ids[i]].split(' ')[0]
            plt.legend([str1,str2])
    else:
        idoffset = 0
    
    for i, id in enumerate(ids[idoffset+1:-1]):
        plt.subplot(ns,ns,i+1)
        plt.plot(x[istart:-1], (len(x)-istart+1)*[y0[id0[i-idoffset]]],'x-')
        plt.plot(x[istart:-1], y[ids,istart:-1])
        diff = abs(mean(y[ids, istart:-1]) - y0[id0[i-idoffset]])
        plt.xlabel('time (s)')
        str1 = legend_y[ids].split(' ')[0]
        plt.title(str1 + ' avg abs error = ' + str(diff))
        plt.legend([legend_y_con[id0[i-idoffset]],legend_y[ids]])
    # plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    plt.suptitle(titlestr +' eps = ' +str(finfo(float).eps))

if __name__ == "__main__":
                                            

    t = time.time()
    (voi, constants,states, algebraic,Gmult) = solve_model()
    print('elapsed = ', round(time.time() - t,3), ' s')
    plot_model(voi, constants,states, algebraic, Gmult)
