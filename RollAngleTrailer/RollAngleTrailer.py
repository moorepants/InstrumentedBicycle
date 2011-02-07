'''
This code makes a couple of plots for the trailer design. The first shows the
potentiometer angle as a function of the bicycle roll angle. Each line is a
differnet height of the potentiometer pivot off of the ground. The second plot
shows the trailer pitch angle as a function of bicycle frame roll.
'''
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from scipy.optimize import fsolve

# define some bicycle roll angles
roll = np.linspace(-pi/3, pi/3, num=500)

# the geometry
rr = 13.
rt = 2.
d1 = 13.
d2 = 0.
d3 = 0.
d4 = 15.
d5 = 6.

def find_pitch_pot(x, roll, rr, rt, d1, d2, d3, d4, d5):
    '''
    x[0] : pitch
    x[1] : pot
    '''
    eq = np.zeros(2)
    eq[0] = rt - np.cos(roll)*(rr-d1-d4*np.sin(x[0])-(rr-d1-rt)*np.cos(x[0]))
    eq[1] = np.sin(roll)*np.cos(x[1]) + np.sin(x[1])*np.cos(x[0])*np.cos(roll)
    return eq

pitch = np.zeros_like(roll)
pot = np.zeros_like(roll)

for i, ang in enumerate(roll):
    if i == 0:
        pitchguess = 0.
        potguess = 0.
    else:
        pitchguess = pitch[i-1]
        potguess = pot[i-1]
    sol = fsolve(find_pitch_pot,
                 [pitchguess, potguess],
                 args=(ang, rr, rt, d1, d2, d3, d4, d5))
    pitch[i] = sol[0];
    pot[i] = -np.tan(roll)/np.cos(pitch)
    pot[i] = sol[1];

plt.figure(1)
# calculate the potentiometer angle
plt.plot(np.rad2deg(roll), np.rad2deg(pot))
plt.figure(2)
# calculate the trailer fork pitch
plt.plot(np.rad2deg(roll), np.rad2deg(pitch))

plt.figure(1)
plt.xlabel('Bicycle roll angle')
plt.ylabel('Potentiometer angle')

plt.figure(2)
plt.xlabel('Bicycle roll angle')
plt.ylabel('Trailer pitch angle')

plt.show()
