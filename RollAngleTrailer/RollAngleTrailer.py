'''
This code makes a couple of plots for the trailer design. The first shows the
potentiometer angle as a function of the bicycle roll angle. Each line is a
differnet height of the potentiometer pivot off of the ground. The second plot
shows the trailer pitch angle as a function of bicycle frame roll.
'''
import matplotlib.pyplot as plt
from numpy import sin, cos, tan, arcsin, arccos, arctan, linspace, pi, rad2deg
from numpy import sqrt

# define some bicycle roll angles
roll = linspace(-pi/2, pi/2, num=500)

# d1 is the height of the pivot off the ground
d1 = linspace(0, 10, num=11)
# d2 is the length of the trailer fork
d2 = 25.

for num in d1:
    plt.figure(1)
    # calculate the potentiometer angle
    #pot = arctan(-tan(roll)/sqrt(1-(num/d2*(1/cos(roll)-1))**2))
    pot = arctan(-tan(roll)/cos(arcsin(num/d2*(1/cos(roll)-1))))
    #pot = arctan(tan(roll)/(1-cos(arcsin(num/d2*(1./cos(roll))))))
    plt.plot(rad2deg(roll), -rad2deg(pot))
    plt.figure(2)
    # calculate the trailer fork pitch
    pitch = arccos(-tan(roll)/tan(pot))
    plt.plot(rad2deg(roll), -rad2deg(pitch))

plt.figure(1)
plt.legend(d1, loc=2)
plt.xlabel('Bicycle roll angle')
plt.ylabel('Potentiometer angle')

plt.figure(2)
plt.legend(d1)
plt.xlabel('Bicycle roll angle')
plt.ylabel('Trailer pitch angle')
plt.ylim((-90, 10))

plt.show()
