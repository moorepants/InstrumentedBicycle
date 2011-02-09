'''
This code makes a couple of plots for the trailer design. The first shows the
potentiometer angle as a function of the bicycle roll angle. Each line is a
differnet height of the potentiometer pivot off of the ground. The second plot
shows the trailer pitch angle as a function of bicycle frame roll.
'''
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from scipy.optimize import fsolve, newton
import svgfig as svg

def pitch_roll_constraint(x, roll, rr, rt, d1, d4): '''
    x : trailer pitch
    '''
    return rt - np.cos(roll)*(rr-d1-d4*np.sin(x)-(rr-d1-rt)*np.cos(x))

def compute_pitch(pitchguess, roll, rr, rt, d1, d4):
    return newton(pitch_roll_constraint, pitchguess, args=(roll, rr, rt, d1, d4))

def compute_pot(roll, pitch):
    return np.arctan(-np.tan(roll)/np.cos(pitch))

###def draw_trailer(roll, rr, rt, d1, d2, d3, d4, d5):
    #### calculate the pitch and pot
    ###pitch = compute_pitch(0., roll, rr, rt, d1, d4)
    ###pot = compute_pot(roll, pitch)
###
    #### some common expressions
    ###sr = np.sin(roll)
    ###cr = np.cos(roll)
    ###sp = np.sin(pitch)
    ###cp = np.cos(pitch)
    ###spo = np.sin(pot)
    ###cpo = np.cos(pot)
###
    #### draw the bicycle wheel
    ###bwcen = [0., rr*cr]
    ###bwrad = [rr, rr*cr]
    ###bwheel = svg.SVG('ellipse', cx=bwcen[0], cy=bwcen[1], rx=bwrad[0],
            ###ry=bwrad[1])
###
    #### draw the right trailer wheel
    ###rwcen = 
    ###(0.5*d5*sp*spo+(rr-d1-rt)*sp-d2-d4*cp)*n1> + (d4*sp*cr+(d1-rr)*cr+(rr-d1-rt)*cp*cr+0.5*d5*(sr*cpo+spo*cp*cr))*n3>
    ###rwheel = svg.SVG('circle', cx=rwcen[0], cy=rwcen[1], r=rt)
###
    ###scene = svg.SVG('g', bwheel, rwheel)
    ###scene.save('scene.svg')
    ###scene.inkview()

# define some bicycle roll angles
roll = np.linspace(-pi/2, pi/2, num=500)

# the geometry
rr = 13.
d1 = 0.
rt = 1.5
d2 = 0.
d3 = 12.
d3 = 0.  d5 = 6.

pitch = np.zeros_like(roll)
pot = np.zeros_like(roll)

for i, ang in enumerate(roll):
    if i == 0:
        pitchguess = 0.
    else:
        pitchguess = pitch[i-1]
    x = compute_pitch(pitchguess, ang, rr, rt, d1, d4)
    print x
    pitch[i] = x
    pot[i] = compute_pot(ang, pitch[i])

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

plt.figure(3)
p = np.linspace(-pi, pi, num=100)
plt.plot(p, pitch_roll_constraint(p, 0., rr, rt, d1, d4))

plt.show()

rwheel = svg.SVG("circle", cx=0., cy=rr, r=rr)
twheel = svg.SVG("circle", cx=d2+d4, cy=rt, r=rt)
# draw the trailer hitch
hitch1 = svg.SVG('line', x1=0., y1=rr, x2=0., y2=rr-d1)
hitch2 = svg.SVG('line', x1=0., y1=rr-d1, x2=d2, y2=rr-d1)
hitch = svg.SVG('g', hitch1, hitch2)
# draw the trailer
tr = []
tr.append(svg.SVG("line", x1=d2, y1=rr-d1, x2=d2, y2=rr-d1-d3))
tr.append(svg.SVG("line", x1=d2, y1=rr-d1-d3, x2=d2+d4, y2=rr-d1-d3))
tr.append(svg.SVG('line', x1=d2+d4, y1=rr-d1-d3, x2=d2+d4, y2=rt))
trailer = svg.SVG('g', tr[0], tr[1], tr[2])
# add some dots for the joints
j1 = svg.SVG('circle', cx=d2, cy=rr-d1, r=0.5)
j2 = svg.SVG('circle', cx=d2+d4, cy=rt, r=0.5)
j = svg.SVG('g', j1, j2, stroke='blue', fill='blue')

group = svg.SVG("g", rwheel, twheel, hitch, trailer, j,
                transform="translate(20, 50)")
group.save()

group.inkview()

#draw_trailer(pi/3, rr, rt, d1, d2, d3, d4, d5)
