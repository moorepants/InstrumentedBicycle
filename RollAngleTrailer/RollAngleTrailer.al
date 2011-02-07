newtonian n

frames wheel, fork, trailer

variables roll, pitch, pot

% the wheel rolls relative to the ground
simprot(n, wheel, 1, roll)

% the trailer fork can pitch relative to the wheel
simprot(wheel, fork, 2, pitch)

% the trailer can roll relative to the fork
simprot(fork, trailer, 1, pot)

% d1 : height of fork from ground
% d2 : length of fork
% d3 : wheel track
constants d{3}

% p1 : wheel to ground contact point
% p2 : fork pivot point on the wheel
% p3 : trailer axle center
% p4 : right trailer wheel center
% p5 : left trailer wheel center
% p6 : right trailer wheel to ground contact
% p7 : left trailer wheel to ground contact
points p{7}

% the wheel contact point is located at the newtonian origin
p_no_p1> = 0*n1> + 0*n2> + 0*n3>

p_p1_p2> = -d1*wheel3>

p_p2_p3> = -d2*fork1>

p_p3_p4> = d3/2*trailer2>

p_p4_p5> = -d3*trailer2>

% the following are actually d1*n3> because the axle is always horizontal relative to
% the ground plane, but for completeness they should be specified as so at
% first allowing the possibility of the trailer roll
p_p4_p6> = d1*unitvec(n3>-dot(n3>,trailer2>)*trailer2>)

p_p5_p7> = d1*unitvec(n3>-dot(n3>,trailer2>)*trailer2>)

% force the trailer axle center to be d1 above the ground
zero1 = dot(n3>, p_p1_p3>) + d1

% force the trailer axle to be horizontal
zero2 = dot(trailer2>, n3>)

% the previous two constraints should be equivalent to the next two

% force p6 and p7 to touch the ground
zero3 = dot(n3>, p_p1_p6>)
zero4 = dot(n3>, p_p1_p7>)
