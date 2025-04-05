"""
Functions used for symmetric regular solution fit
"""

import numpy as np

kb = 8.617333E-5 #eV/K
kb_j = 1.380649E-23 #J/K

def line(x1,x2,y1,y2):
    m = (y2 - y1) / (x2 - x1)
    return m 

def line_b(x,y,m):
    b = y - (m*x)
    return b

def deltaX(x,wx):
    """
    Wx of mixing function

    where x = entropy (S), enthalpy (H), or volume (V)

    dX = Wx*x(1-x)
    """
    
    dX = wx*x*(1-x)
    return dX

def deltaG(x,wh,ws):
    """
    Gibbs free energy of mixing
    w = wh - temp*ws
    dG = w*x*(1-x)
    """
    w = wh - (temp*ws)
    dG = w*x*(1-x)
    return dG

def xfunc(temp,wh,ws,wv,press,x):
    """
    This function sets chemical potential A and chemical potential B equal to
    each other. The function is then set equal to zero in order to incorporate
    a root finding algorithm, which solves for the solvus temperature.
    P in this function equals the pressure difference between high- and low-P

    The reference pressure is 60 GPa. This value will depend on the system and pressure
    set in each NPT simulation.
    
    w = wh - (temp*ws) + (P*wv)
    xfunc = np.exp( -1*w/RT * (1-2x) ) - x/(1-x)

    Example calculation:
    -------------------
    import scipy 

    xlin = np.linspace(0.0001, 0.999999, 500)
    solvus = np.zeros(500)

    for i,x in enumerate(xlin):
        solvus[i] += scipy.optimize.brentq(xfunc,minimum_temp,maximum_temp,args=(wh,ws,wv_sp,press,x))


    input parameters:
    ----------------
        temp: temperature in K
        wh: enthalpy of mixing in J/mol
        ws: enthalpy of mixing in J/K/mol
        wv: volume of mixing in m^3/mol
        press: pressure in Pa
        x: mol % or wt % (depending on phase space of interest). Typically ranges between 0 and 1

    output:
    ------
        solvus temperature when put into root finding routine

    """
    R = 8.3143 # ideal gas constant
    p_ref = 60E9 # reference pressure
    w = wh - (temp*ws) + ( (press-p_ref) *wv)
    xfunc = np.exp( (-1*w/(R*temp)) * (1 - (2*x)) ) - x/(1 - x)
    
    return xfunc

def mult_div_error(z,x,dx,y,dy):
    """
    Multiplication or Division Error Propagation
    
    dz/z = dx/x + dy/y + ...
    """
    dz = np.sqrt( ((dx/x)**2.) + ((dy/y)**2.) ) * z
    return np.abs(dz)
