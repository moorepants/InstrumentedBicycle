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
% p3 : hitch point
% p4 : fork pivot point
% p5 : trailer point
% p6 : trailer point
% p7 : trailer axle center
% p8 : right trailer wheel center
% p9 : left trailer wheel center
% p10 : right trailer wheel to ground contact
% p11 : left trailer wheel to ground contact
points p{11}

% the wheel contact point is located at the newtonian origin
p_no_p1> = 0*n1> + 0*n2> + 0*n3>

p_p1_p2> = -rr*wheel3>

p_p2_p3> = d1*wheel3>

p_p3_p4> = -d2*wheel1>

p_p4_p5> = d3*fork3>

p_p5_p6> = -d4*fork1>

p_p6_p7> = -(rt-rr+d1+d3)*fork3>

p_p7_p8> = d5/2*trailer2>

p_p8_p9> = -d5*trailer2>

% the following are actually rt*n3> because the axle is always horizontal relative to
% the ground plane, but for completeness they should be specified as so at
% first allowing the possibility of the trailer roll
p_p8_p10> = rt*unitvec(n3>-dot(n3>,trailer2>)*trailer2>)

p_p9_p11> = rt*unitvec(n3>-dot(n3>,trailer2>)*trailer2>)

% force the trailer axle center to be rt above the ground
zero1 = dot(n3>, p_p1_p7>) + rt
dzdp = d(zero1, pitch)

% force the trailer axle to be horizontal
zero2 = dot(trailer2>, n3>)

% the previous two constraints should be equivalent to the next two

% force p7 and p8 to touch the ground
zero3 = dot(n3>, p_p1_p10>)
zero4 = dot(n3>, p_p1_p11>)

% info for svg plotting, subtract the n2 component from the vectors
prj_d1> = express(p_p2_p3> - dot(p_p2_p3>, n2>)*n2>, n)
prj_d2> = express(p_p3_p4> - dot(p_p3_p4>, n2>)*n2>, n)
prj_d3> = express(p_p4_p5> - dot(p_p4_p5>, n2>)*n2>, n)
prj_d4> = express(p_p5_p6> - dot(p_p5_p6>, n2>)*n2>, n)
prj_x>  = express(p_p6_p7> - dot(p_p6_p7>, n2>)*n2>, n)
prj_d5> = express(p_p8_p9> - dot(p_p8_p9>, n2>)*n2>, n)

% wheel centers
prj_bw> = express(p_p1_p2> - dot(p_p1_p2>, n2>)*n2>, n)
prj_rw> = express(p_p1_p8> - dot(p_p1_p8>, n2>)*n2>, n)
prj_lw> = express(p_p1_p9> - dot(p_p1_p9>, n2>)*n2>, n)

% four points for each wheel, used to map the ellipse in svg
points bwe{4}, rwe{4}, lwe{4}

p_p2_bwe1> = rr*wheel1>
p_p2_bwe2> = -rr*wheel3>
p_p2_bwe3> = -rr*wheel1>
p_p2_bwe4> = rr*wheel3>

prj_bwe1> = express(p_p2_bwe1> - dot(p_p2_bwe1>, n2>)*n2>, n)
prj_bwe2> = express(p_p2_bwe2> - dot(p_p2_bwe2>, n2>)*n2>, n)
prj_bwe3> = express(p_p2_bwe3> - dot(p_p2_bwe3>, n2>)*n2>, n)
prj_bwe4> = express(p_p2_bwe4> - dot(p_p2_bwe4>, n2>)*n2>, n)

p_p8_rwe1> = rt*trailer1>
p_p8_rwe2> = -rt*trailer3>
p_p8_rwe3> = -rt*trailer1>
p_p8_rwe4> = rt*trailer3>

prj_rwe1> = express(p_p8_rwe1> - dot(p_p8_rwe1>, n2>)*n2>, n)
prj_rwe2> = express(p_p8_rwe2> - dot(p_p8_rwe2>, n2>)*n2>, n)
prj_rwe3> = express(p_p8_rwe3> - dot(p_p8_rwe3>, n2>)*n2>, n)
prj_rwe4> = express(p_p8_rwe4> - dot(p_p8_rwe4>, n2>)*n2>, n)

p_p9_lwe1> = rt*trailer1>
p_p9_lwe2> = -rt*trailer3>
p_p9_lwe3> = -rt*trailer1>
p_p9_lwe4> = rt*trailer3>

prj_lwe1> = express(p_p9_lwe1> - dot(p_p9_lwe1>, n2>)*n2>, n)
prj_lwe2> = express(p_p9_lwe2> - dot(p_p9_lwe2>, n2>)*n2>, n)
prj_lwe3> = express(p_p9_lwe3> - dot(p_p9_lwe3>, n2>)*n2>, n)
prj_lwe4> = express(p_p9_lwe4> - dot(p_p9_lwe4>, n2>)*n2>, n)

save RollAngleTrailer.all
