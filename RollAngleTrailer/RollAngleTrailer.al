% this neglects bicycle frame pitch
newtonian n

frames wheel, fork, trailer

variables roll, pitch, pot

% the wheel rolls (leans) relative to the ground
simprot(n, wheel, 1, roll)

% the trailer fork can pitch relative to the wheel
simprot(wheel, fork, 2, pitch)

% the trailer can roll relative to the fork
simprot(fork, trailer, 1, pot)

% rr : bicycle rear wheel radius
% rt : trailer wheel radius
% d1 : location of the trailer pitch pivot 3>
% d2 : location of the trailer pitch pivot 1>
% d3 : fork drop from pivot
% d4 : length of fork
% d5 : wheel track
constants rr, rt, d{5}

% p1 : bicycle wheel to ground contact point
% p2 : bicycle wheel center
% p3 : fork pivot point
% p4 : trailer axle center
% p5 : right trailer wheel center
% p6 : left trailer wheel center
% p7 : right trailer wheel to ground contact
% p8 : left trailer wheel to ground contact
points p{8}

% the wheel contact point is located at the newtonian origin
p_no_p1> = 0*n1> + 0*n2> + 0*n3>

p_p1_p2> = -rr*wheel3>

p_p2_p3> = d1*wheel3> - d2*wheel1>

p_p3_p4> = d3*fork3> - d4*fork1> - (rt-rr+d1+d3)*fork3>

p_p4_p5> = d5/2*trailer2>

p_p5_p6> = -d5*trailer2>

% the following are actually rt*n3> because the axle is always horizontal relative to
% the ground plane, but for completeness they should be specified as so at
% first allowing the possibility of the trailer roll
p_p5_p7> = rt*unitvec(n3>-dot(n3>,trailer2>)*trailer2>)

p_p6_p8> = rt*unitvec(n3>-dot(n3>,trailer2>)*trailer2>)

% force the trailer axle center to be rt above the ground
zero1 = dot(n3>, p_p1_p4>) + rt

% force the trailer axle to be horizontal
zero2 = dot(trailer2>, n3>)

% the previous two constraints should be equivalent to the next two

% force p7 and p8 to touch the ground
zero3 = dot(n3>, p_p1_p7>)
zero4 = dot(n3>, p_p1_p8>)

save RollAngleTrailer.all
