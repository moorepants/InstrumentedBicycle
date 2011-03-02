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

def pitch_roll_constraint(x, roll, rr, rt, d1, d4):
    '''
    x : trailer pitch
    '''
    return rt-np.cos(roll)*(rr-d1-d4*np.sin(x)-(rr-d1-rt)*np.cos(x))

def dcondpitch(x, roll, rr, rt, d1, d4):
    '''
    The derivative of the pitch_roll_constraint.
    '''
    return np.cos(roll)*(d4*np.cos(x)-(rr-d1-rt)*np.sin(x))

def compute_pitch(pitchguess, roll, rr, rt, d1, d4):
    return newton(pitch_roll_constraint, pitchguess, args=(roll, rr, rt, d1, d4))

def compute_pot(roll, pitch):
    return np.arctan(-np.tan(roll)/np.cos(pitch))

def draw_trailer(rr, rt, d1, d2, d3, d4, d5):

    layout = svg.canvas()
    layout.attr['width'] = '40in'
    layout.attr['height'] = '60in'
    layout.attr['viewBox'] = '0 0 40 60'
    # draw the wheels
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
    j1 = svg.SVG('circle', cx=d2, cy=rr-d1, r=0.2)
    j2 = svg.SVG('circle', cx=d2+d4, cy=rt, r=0.2)
    j = svg.SVG('g', j1, j2, stroke='blue', fill='blue')
    # draw a rectangle for the pot joint
    potrev = svg.SVG('rect', x=(d2+d4)/2, y=rr-d1-d3, width="2", height="1",)
    # draw some coordinate axes
    start = svg.make_marker('start', 'arrow_start')
    end = svg.make_marker('end', 'arrow_end')
    newtonian = svg.SVG('path',
                        d='M -10,0 0,0 0,-10',
                        marker_start='url(#start)',
                        marker_end='url(#end)')

    group = svg.SVG("g", rwheel, twheel, hitch, trailer, j, potrev, newtonian,
                    start, end, transform="translate(15, 15)")# rotate(180)")

    layout.append(group)
    layout.save()

    layout.inkview()

    return layout

# define some bicycle roll angles
roll = np.linspace(-pi/2, pi/2, num=500)

# the geometry
rr = 13.
rt = 38./25.4
d1 = 0.
d2 = 0.
d3 = 12.
d4 = 16.
d5 = 6.

pitch = np.zeros_like(roll)
pot = np.zeros_like(roll)

for i, ang in enumerate(roll):
    if i == 0:
        pitchguess = 0.
    else:
        pitchguess = pitch[i-1]
    x = compute_pitch(pitchguess, ang, rr, rt, d1, d4)
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

#plt.show()

layout = draw_trailer(rr, rt, d1, d2, d3, d4, d5)
