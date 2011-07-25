from sympy import *
from sympy.physics.mechanics import *

"""
This script calculates the actual steer torque applied to the handlebars as a
function of the measurements taken on the bicycle.
"""

# the unknown steer torque
Tdelta = dynamicsymbols('Tdelta')

# constants we measure on the bicycle
#
# d : distance from the handlebar center of mass to the point s on the the
#   steer axis
# ds1, ds3 : measure numbers for the location of the vectornav to the point on
#   the steer axis, s
d, ds1, ds3 = symbols('d ds1 ds2')
# damping coefficient for the upper bearing viscous friction
c = symbols('c')

# time varying signals we measure on the bicycle
#
# measured steer column torque and columb friction force
Tm, Tf = dynamicsymbols('Tm Tf')
# steer angle and body fixed handlebar rate about steer axis
delta, wh3 = dynamicsymbols('delta wh3')
# body fixed angular rates of the bicycle frame
wb1, wb2, wb3  = dynamicsymbols('wb1 wb2 wb3')
# body fixed acceleration of the vectornav point
av1, av2, av3  = dynamicsymbols('av1 av2 av3')

# time varying signals we calculate
#
# steer
deltad, wh3d = dynamicsymbols('delta wh3', 1)
# body fixed angular acceleration
wb1d, wb2d, wb3d  = dynamicsymbols('wb1 wb2 wb3', 1)

# newtonian frame
N = ReferenceFrame('N')
# bicycle frame
B = ReferenceFrame('B')
# handlebar frame
H = B.orientnew('H', 'Simple', delta, 3)

# handlebar inertia and mass
IH11, IH22, IH33, IH31 = symbols('IH11 IH22 IH33 IH31')
IH = inertia(H, I11, I22, I33, 0, 0, I31)
mH = symbols('mH')

# set the angular velocities of B and H
B.set_ang_vel(N, wb1 * B.x + wb2 * B.y + wb3 * B.z)
H.set_ang_vel(N, (wb1 * cos(delta) + wb2 * sin(delta))  * H.x + (-wb1 *
    sin(delta) + wb2 * cos(delta)) * H.y + wh3 * H.z)

# vectornav center
v = Point('v')
v.set_acc(N, av1 * B.x + av2 * B.y + av3 * B.z)

# point on the steer axis
s = Point('s')
s.set_pos(v, ds1 * B.x + ds3 * B.z)
s.a2pt(v, N, B)

# handlebar center of mass
ho = Point('ho')
ho.set_pos(s, d * H.x)
ho.a2pt(s, N, H)

# calculate the angular momentum of the handlebar in N about the center of mass
# of the handlebar
H_H_N_ho = IH.dot(H.ang_vel_in(N))

Hdot = H_H_N_ho.dt(N)

# euler's equation about an arbitrary point, s
sumT = Hdot + ho.pos_from(s).cross(mH * ho.acc(N))

# turn off the simplification cause it takes forever to compute (sumT).dot(H.z)
Vector.simp = False

# calculate the steer torque
Tdelta = (sumT).dot(H.z) + Tm + c * deltad + Tf

# let's make use of the steer rate gyro and frame rate gyro measurement instead
# of differentiating delta
Tdelta = Tdelta.subs(deltad, wh3 - wb3)

print "Tdelta as a function of the measured data:\nTdelta =", Tdelta
