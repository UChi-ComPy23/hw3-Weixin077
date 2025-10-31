"""
Defintions for problem 0
"""

import numpy as np
import scipy.integrate
from scipy.integrate import DenseOutput
from scipy.interpolate import interp1d
from warnings import warn
from scipy.integrate import solve_ivp


class ForwardEuler(scipy.integrate.OdeSolver):
    def __init__(self, fun, t0, y0, t_bound, vectorized,
                 h = False, # Add a parameter that allows users to set h
                 support_complex=False,
                 **extraneous # A variable handling extraneous variables.
                 ):
        super(ForwardEuler, self).__init__(fun, t0, y0, t_bound, vectorized, support_complex)
        if not h: # The case that users don't set h.
            self.h = (t_bound - t0) / 100
        else:
            self.h = h
        if extraneous:
            # Warn users when they enter extraneous parameters.
            # 'common.warn_extraneous'?
            warn('There are extraneous pamameters!!', UserWarning)
        self.direction = 1 # Ensure that direction = +1
    
    def _step_impl(self):
        if self.h == 0:
            return (False, 'The stepsize must be non-zero!')
        elif self.t >= self.t_bound:
            return (False, 'Reach the Time Bound!')
        else: # push a step forward
            outcome = self.y + self.h*self.fun(self.t, self.y)
            self.t += self.h
            self.y = outcome.copy() # Use .copy to avoiding storing reference
            # We only need the value!!!!
            return (True, None)
    
    def _dense_output_impl(self):   
        return ForwardEulerOutput(self.t_old, self.t, self.fun, self.y)

class ForwardEulerOutput(DenseOutput):
    def __init__(self, t_old, t, fun, y): # overwrite the class initiation
        # Add necessary parameters: fun and y
        super().__init__(t_old, t)
        self.fun = fun # The function of Euler Method
        self.y = y # The current state y
    def _call_impl(self, t):
        if t <= self.t_min or t >= self.t_max:
            raise ValueError()
        # There should use try/except to diaplay error message,
        # but I guess this object occur after checking t whether in the time range
        # So just writw the simple one.
        else:
            print(self.t_min)
            return self.y + (t-self.t_min)*self.fun(t, self.y) 
  

if __name__ == '__main__':
    pass
    
