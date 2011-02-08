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
import svgfig as svg

# define some bicycle roll angles
roll = np.linspace(-pi/3, pi/3, num=500)

# the geometry
rr = 13.
d1 = 12
rt = rr-d1
d2 = 0.
d3 = 0.
d4 = 16.
d5 = 6.

# draw the wheels
rwheel = svg.SVG("circle", cx=0., cy=-rr, r=rr)
twheel = svg.SVG("circle", cx=d2+d4, cy=-rt, r=rt)
# draw the trailer hitch
hitch1 = svg.SVG('line', x1=0., y1=-rr, x2=0., y2=-(rr-d1))
hitch2 = svg.SVG('line', x1=0., y1=-(rr-d1), x2=d2, y2=-(rr-d1))
hitch = svg.SVG('g', hitch1, hitch2)
# draw the trailer
tr = []
tr.append(svg.SVG("line", x1=d2, y1=-(rr-d1), x2=d2, y2=-(rr-d1-d3)))
tr.append(svg.SVG("line", x1=d2, y1=-(rr-d1-d3), x2=d2+d4, y2=-(rr-d1-d3)))
tr.append(svg.SVG('line', x1=d2+d4, y1=-(rr-d1-d3), x2=d2+d4, y2=-(rt)))
trailer = svg.SVG('g', tr[0], tr[1], tr[2])
# add some dots for the joints
j1 = svg.SVG('circle', cx=d2, cy=-(rr-d1), r=0.5)
j2 = svg.SVG('circle', cx=d2+d4, cy=-rt, r=0.5)
j = svg.SVG('g', j1, j2, stroke='blue', fill='blue')

group = svg.SVG("g", rwheel, twheel, hitch, trailer, j,
                transform="translate(20, 50)")
group.save()
group.inkview()

def find_pitch(x, roll, rr, rt, d1, d2, d3, d4, d5):
    '''
    x : pitch
    '''
    return rt - np.cos(roll)*(rr-d1-d4*np.sin(x)-(rr-d1-rt)*np.cos(x))

pitch = np.zeros_like(roll)
pot = np.zeros_like(roll)

for i, ang in enumerate(roll):
    if i == 0:
        pitchguess = 0.
    else:
        pitchguess = pitch[i-1]
    pitch[i] = fsolve(find_pitch, pitchguess,
                 args=(ang, rr, rt, d1, d2, d3, d4, d5))
    pot[i] = np.arctan(-np.tan(ang)/np.cos(pitch[i]))

# plot the potentiometer angle
plt.figure(1)
plt.plot(np.rad2deg(roll), np.rad2deg(pot))
plt.xlabel('Bicycle roll angle')
plt.ylabel('Potentiometer angle')

# plot the trailer fork pitch
plt.figure(2)
plt.plot(np.rad2deg(roll), np.rad2deg(pitch))
plt.xlabel('Bicycle roll angle')
plt.ylabel('Trailer pitch angle')

plt.show()
