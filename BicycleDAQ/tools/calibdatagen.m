clear all; close all; clc;

% Path to calibration files
path = '../../BicycleDAQ/data/CalibData/';


%% Roll Angle sensor
filename = '00001.mat';
load([path filename]);

N = 1;
calibdata(N).filename = filename;
calibdata(N).name  = data.calibration;
calibdata(N).slope = data.slope;
calibdata(N).offset = data.offset;
calibdata(N).timestamp = data.timestamp;
clear data;

%% Steer angle
filename = '00000.mat';
load([path filename]);

N = 2;
calibdata(N).filename = filename;
calibdata(N).name  = data.calibration;
calibdata(N).slope = data.slope;
calibdata(N).offset = data.offset;
calibdata(N).timestamp = data.timestamp;
clear data;

%% Pull force
filename = '00002.mat';
load([path filename]);

N = 3;
calibdata(N).filename = filename;
calibdata(N).name  = data.calibration;
calibdata(N).slope = data.slope;
calibdata(N).offset = data.offset;
calibdata(N).timestamp = [];
clear data;

%% Torque sensor calibration

%% Torque sensor calibration data
% Coverting prehistoric units to SI units
in2m = 0.0254;
lb2kg = 0.45359237;
rawdata = [
     0      0.002
   -30      1.998
   -60      3.993
   -90      5.997
  -120      7.994
  -150      9.997
    30     -1.995
    60     -3.994
    90     -5.989
   120     -7.986
   150     -9.986
   ];

y = in2m*lb2kg*rawdata(:,1); % Torque [Nm]
x = rawdata(:,2); % Voltage [V]

% sort the data in case it is not in order
[y, indice] = sort(y);
x = x(indice);

% basic regression fit for the mean voltage and the applied weight
coef    = polyfit(x, y, 1);
f       = polyval(coef, x);
sst     = sum((y-mean(y)).^2);
sse     = sum((y-f).^2);
rsq     = 1-sse/sst;

plot(x,y,'.'); hold on;
plot(x,f);

data = struct('calibration', 'Steertorque sensor', ...
              'calibID', 'Steertorque', ...
              'timestamp', [2010,9,8,00,00,00;], ...
              'accuracy', [], ...
              'y', y, ...
              'x', x, ...
              'slope', coef(1), ...
              'offset', coef(2), ...
              'rsq', rsq);

% Substituting calibdata:
N = 4;
calibdata(N).name  = 'Steertorque Sensor';
calibdata(N).slope = coef(1);
calibdata(N).offset = coef(2);
calibdata(N).timestamp =  [2010,9,8,00,00,00;];


%% Steerrate gyro


% rad/s = f(voltage)

% rad/s = (Vout-2.5)/(573/1000) +- 0.10472 rad/s uncertainty
% Substituting calibdata

Vin = 5;
slope = 573/1000; %[V/{rad/s)]

N = 5;
calibdata(N).name  = 'Steerrate Gyro';
calibdata(N).Vin = 5;
calibdata(N).slope = slope; % [V/{rad/s)]
calibdata(N).offset = -Vin/2*slope;
calibdata(N).timestamp =  clock;

%% Forward velocity

r_cont = 13.000*0.0254; % Contact point radius
r_rear = 13.329*0.0254; % Rear wheel radius
r_disc = 2.2696/2*0.0254; % Disc radius
slope = 12*60*r_disc/(5200*2*pi)*r_cont/r_rear;
offset = 0;

% Substituting calibdata:
N = 6;
calibdata(N).name  = 'Forward Velocity';
calibdata(N).Vin = [];
calibdata(N).slope = slope; % [V/{m/s)]
calibdata(N).offset = offset; % [V/{m/s)]
calibdata(N).timestamp =  clock;

%% Saving the calibdata structure
addpath('hdf5matlab')

% Load matfile
% load(['..' filesep '..' filesep 'BicycleDAQ' filesep 'data' filesep '00170.mat'])
calibdata = calibdata(1);
% Save to h5 format
todata = ['..' filesep '..' filesep 'BicycleDAQ' filesep 'data'];
hdf5save(['..' filesep '..' filesep 'BicycleDAQ' filesep 'data' ...
     filesep 'calibdata.h5'],'calibdata','calibdata');
    

% save(['..' filesep '..' filesep 'BicycleDAQ' filesep 'data' ...
%     filesep 'calibdata.mat'],'calibdata');
% hdf5write(['..' filesep '..' filesep 'BicycleDAQ' filesep 'data' ...
%     filesep 'calibdata.h5'],'/calibdata',calibdata)
