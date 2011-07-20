% space...and beyond
newtonian n

% the bicycle frame
frames b

% handlebar
bodies h

% the handlebar is symmetric about the 1-3 plane
inertia h, I11, I22, I33, 0, 0, I31
mass h=mh

% s is a point on the steer axis of which we want the angular momentum about
points s

% v is the vectornav center (location of the accelerometer)
points v

% d is the perpendicular distance from the steer axis to ho (handlebar com)
constants d

% ds are the measure numbers for the location of v with respect to s
constants ds{3}

% we want to know the steer torque
variables Tdelta

% we know the measured torque, the damping and the columb friction
specified Tm, Tf
constants c % damping

% we know the body fixed angular rates and angular acclereations of the frame
specified wb{3}'

% we know the body fixed velocity and acceleration of v
specified vv{3}'

% we know the body fixed component of angular rate of the fork about one axis
specified wh3'

% we know the steer angle, delta, and the steer rate
specified delta'

% the angular rate of the bicycle frame in space expressed in body fixed
% coordinates
w_b_n> = wb1 * b1> + wb2 * b2> + wb3 * b3>

% handlebars, h, rotate relative to the bicycle frame, b, about the 3 axis through
% delta
simprot(b, h, 3, delta)

% this is the angular rate of the handlebar in space as a function of what we
% measured
w_h_n> = (wb1 * cos(delta) + wb2 * sin(delta))  * h1> + (-wb1 * sin(delta) + &
    wb2 * cos(delta)) * h2> + wh3 * h3>

% locate v relative to s
p_v_s> = ds1 * b1> + ds2 * b3>

% locate ho relative to s
p_ho_s> = d * h1>

% we know the velocity of point v (we integrate the accelerometer signals)
v_v_n> = vv1 * b1> + vv2 * b2> + vv3 * b3>

% find the velocity of s in n, knowing the velocity of v in n, both points
% being in frame b
v2pts(n, b, v, s)

% find the velocity of ho in n, knowing the velocity of s in n, both points
% beign in body h
v2pts(n, h, s, ho)

% now find the angular momentum of the handlebar in n about s
H_h_s_n> = momentum(angular, s, h)

% take the derivative
hdot> = dt(H_h_s_n>, n)

% form the Newton/Eular equation
Tdelta = dot(hdot>, h3>) + Tm + c * delta' + Tf

% we don't actually measure delta', use delta' = wh3 - wb3 instead
Tdelta = replace(Tdelta, delta'=wh3 - wb3)

output Tdelta
code algebraic() SteerTorqueEquations.c

save SteerTorqueEquations.all
