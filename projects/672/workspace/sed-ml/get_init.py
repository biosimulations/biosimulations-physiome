def init_gate(T, V):

    import math

    phi = 3**((T - 6.3) / 10)
    alpha_m = 0.1 * (V + 25) * phi / (math.exp( (V + 25) / 10) -1 )
    beta_m = 4 * math.exp( V / 18 ) * phi
    alpha_h = 0.07 * math.exp( V / 20 ) * phi
    beta_h = phi / (math.exp( (V + 30) /10 ) + 1)
    alpha_n = 0.01 * (V + 10) * phi / (math.exp( (V + 10) / 10) -1 )
    beta_n = 0.125 * math.exp( V / 80 ) * phi
    m_init = alpha_m / (alpha_m + beta_m)
    n_init = alpha_n / (alpha_n + beta_n)
    h_init = alpha_h / (alpha_h + beta_h) 

    return  m_init, n_init, h_init
