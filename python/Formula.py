
## constants ##

def absoluteZeroDeg ():
    """
    () -> c:float
    c: [deg C]
    """
    return -273.15

def normalAtmosPressure ():
    """
    () -> p:float
    p: normal atmospheric pressure [hPa]
    """
    return 1013.25

def gasConst ():
    """
    () -> R:float
    R: gas constant [J/kg*K]
    """
    return 287.04

def lapseRate ():
    """
    () -> gamma:float
    gamma: [deg C/m]
    Note: only in troposhere. 
    """
    return 6.5e-3

def gravityAcceleration ():
    """
    () -> g:float
    g: gravity acceleration [m/s^2]
    """
    return 9.80665

def StdAtmosTemp ():
    """
    () -> t:float
    t: standard atmospheric temperature [deg C]
    """
    return 15.0

## utilities ##

def densOfDryAir (t, P):
    """
    (t:float, P:float) -> rho:float
    t  : temperature [deg C]
    P  : atmospheric pressure [kg/m^3]
    rho: [kg/m^3] 
    """
    # 1.293: density of dry air
    #  in 0 deg C and normal atmospheric pressure
    Pn = normalAtmosPressure ()
    zero = absoluteZeroDeg ()
    rho = (-zero * 1.293 * P) / ((t - zero) * Pn)
    return rho

def innerTempToStop (We, V, P, To):
    """
    (We:float, V:float, P:float, To:float) -> Tb:float
    We: weight of envelope [kg-weight]
    V : volume of balloon [m^3]
    P : atmos pressure [hPa]
    To: outer temperature [deg C]
    Tb: inner temperature [deg C]
    """
    Pn = normalAtmosPressure ()
    zero = absoluteZeroDeg ()
    a  = 1.293 * P / Pn * (-zero)
    b  = 1 / (To - zero) - We / (V * a)
    Tb = 1 / b + zero
    return Tb
    
def outerTempToStop (We, V, P, Tb):
    """
    (We:float, V:float, P:float, Tb:float) -> To:float
    We: weight of envelope [kg-weight]
    V : volume of balloon [m^3]
    P : atmos pressure [hPa]
    Tb: inner temperature [deg C]
    To: outer temperature [deg C]
    """
    Pn = normalAtmosPressure ()
    zero = absoluteZeroDeg ()
    a  = 1.293 * P / Pn * (-zero)
    b  = 1 / (Tb - zero) + We / (V * a)
    To = 1 / b + zero
    return To

def temperature (t0, h):
    """
    (t0:float, h:float) -> t:float
    t0: temperature at 0m [deg C]
    h : height [m]
    t : temperature at hm [deg C]
    """
    gm = lapseRate ()
    return t0 - gm * h

def atmosPressure (P0, t, h):
    """
    (t:float, h:float) -> P:float
    P0: atmosphere pressure at 0m [hPa]
    t : temperature at 0m [deg C]
    h : height [m]
    P : air pressure [hPa]
    """
    z = absoluteZeroDeg ()
    R = gasConst ()
    gm = lapseRate ()
    g = gravityAcceleration ()

    a = (t - z - gm * h) / (t - z)
    a = a ** (g / R / gm)
    p = P0 * a
    return p

## unit conversion ##
def mToFt (m):
    return m / 0.3048
def ftToM (ft):
    return ft * 0.3048
def nmToM (nm):
    return nm * 1852.0
def mToNM (m):
    return m / 1852.0
