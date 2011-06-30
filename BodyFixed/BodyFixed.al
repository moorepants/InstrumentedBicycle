% this code calculates the equations for the yaw, roll and pitch rates of the
% bicycle frame as functions of the body fixed rates measured by the VN-100

newtonian n

% y : yaw frame
% r : roll frame
% p : pitch frame
% v : vn-100 frame
frames y, r, p, v

motionvariables yaw', roll', pitch'

simprot(n, y, 3, yaw)
simprot(y, r, 1, roll)
simprot(r, p, 2, pitch)

% steer axis tilt
constants lam

simprot(p, v, 2, lam)

% get the body fixed angular velocity of the VN-100
angvel(n, v)
express(w_v_n>, v)

% name the body fixed angular rates of the VN-100
constants wx,wy,wz

% solve for the rates of the bicycle generalized coordinates
A = [wx - dot(w_v_n>, v1>); wy - dot(w_v_n>, v2>); wz - dot(w_v_n>, v3>)]
B = [yaw'; pitch'; roll']
solve(A,B)

% assuming pitch is zero, the equations reduce to this
yawrate = evaluate(yaw', pitch=0)
pitchrate = evaluate(pitch', pitch=0)
rollrate = evaluate(roll', pitch=0)

% assuming pitch is zero and roll is small, the equations reduce to this
yawrate = evaluate(yaw', pitch=0, roll=0)
pitchrate = evaluate(pitch', pitch=0, roll=0)
rollrate = evaluate(roll', pitch=0, roll=0)

% save the output
save BodyFixed.all
