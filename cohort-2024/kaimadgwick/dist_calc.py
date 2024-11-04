import numpy as np

def num_int(function,upperbound,lowerbound=0,steps=101):
    '''Numerically integrates a function from 0 to an upper bound using Simpson's Rule.
    '''
    xs = np.linspace(lowerbound,upperbound,steps*2)
    stepsize = np.abs(upperbound-lowerbound)/(steps-1) 
    totalvalue = 0 
    for i in range(steps-2):
        y1 = function(xs[2*i])
        y2 = function(xs[2*i + 1])*4
        y3 = function(xs[2*(i+1)])
        totalvalue += stepsize/6 * (y1+y2+y3) 
    return totalvalue

def D_M(D_C,omega_k,D_H):
    '''Defines the formula used to calculate transverse comoving distance, based on the value of Omega_k.
    '''
    if omega_k > 0:
        return D_H/np.sqrt(omega_k) * np.sinh(D_C/D_H * np.sqrt(omega_k))
    elif omega_k == 0:
        return D_C
    else:
        omega_k = np.abs(omega_k)
        return D_H/np.sqrt(omega_k) * np.sin(D_C/D_H * np.sqrt(omega_k))
        

def distcalc(z,omega_m=0.28,omega_lambda=0.72,omega_k=0,H0 = 75e3):
    '''Calculates the transverse comoving distance based on the formula defined in D_M. 
    As an intermediary step, calculates comoving distance, D_C, by numerically integrating over the function E(z)
    and multiplying by the Hubble distance, D_H. 
    All formulas implemented in this function are taken from Hogg (2000), Distance Measures in Cosmology.
    '''
    def E_z(z,omega_m=omega_m,omega_lambda=omega_lambda,omega_k=omega_k):
        term = np.sqrt((1+z)**3 * omega_m + (1+z)**2 * omega_k + omega_lambda)
        if term == 0:
            raise ValueError("E(z) cannot be zero. Try again with z and omega_lambda not equal to zero.")
        else:
            return 1/term

    D_H = 3e8/H0
    D_C = D_H*num_int(E_z,z)

    DM = D_M(D_C, omega_k, D_H)

    return DM

zinput = 2.5
zdist = distcalc(zinput)

print(f"The distance to an object of redshift {zinput:.2f} is {zdist:.2f} Megaparsecs.")
