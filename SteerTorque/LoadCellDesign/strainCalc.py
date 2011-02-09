import numpy as np
import matplotlib.pyplot as plt

in2met = 25.4/1000 # inch to meter conversion

d1 = 3*in2met # outer diameter in meters
d2 = 0.25*in2met # core diameter in meters
t1 = 0.0325*in2met # web thickness in meters
t2 = 0.0625*in2met # outer wall thickness in meters
T = 2 # applied torque in newton-meters
n = 4 # number of webs
h = 3*in2met # height of cylinder in meters
#E = 200*10**9 # modulus of elasticity of Tool Steel L2 in Pa
E = 73.1*10**9 # modulus of elasticity of AL 2014-T6 in Pa
#sigmaY = 703*10**6 # yield strength of Tool Steel L2 in Pa
sigmaY = 414*10**6 # yield strength of AL 2014-T6 in Pa


L = d1 - 2*t2 - d2 # length of beam element in meters
F = 2*T/n/(d1-2*t2) # force applied to beam in newtons
I = h*t1**3/12 # moment of inertia of the cross section in inches^4

x = np.arange(0, L, 0.001)

# shear force along the beam
V = F*np.ones_like(x)
# moment along the beam
M = F*x - 4*F*L/5
# slope of the beam
theta = (-F*x**2/2 + 4*F*L*x/5)/E/I
# deflection of the beam
y = (-F*x**3/6 + 4*F*L*x**2/10)/E/I
# maximum stress along the beam
maxStress = M*t1/2/I
# maximum strain along the beam
maxStrain = M*t1/2/I/E
# safety factor to yield
SF = sigmaY/np.max(np.abs(maxStress))

print SF
test = 'Max Stress = {0:.2f} MPa'.format(np.max(np.abs(maxStress)))
print test
#print 'Safety Factor =', SF
print 'Max Strain =', np.max(np.abs(maxStrain)), 'm/m'

plt.subplot(4, 1, 1)
plt.plot(x, V)
plt.subplot(4, 1, 2)
plt.plot(x, M)
plt.subplot(4, 1, 3)
plt.plot(x, theta)
plt.subplot(4, 1, 4)
plt.plot(x, y)
plt.show()
