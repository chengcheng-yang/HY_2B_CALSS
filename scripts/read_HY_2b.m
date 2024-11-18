%% read and plot HY-2B data
clear;clc;

%% load HY-2B data
data_dir = '../data/';  % base folder save HY_2B data
files = dir(fullfile(data_dir, '*.h5')); % filenames of the HY-2b data
step = 2;  %original data is too large, here we set "2" to load data every 2 points 

% Initialize variables to save the scatter data
lon_all = [];
lat_all = [];
speed_all = [];
direction_all = [];

% Loop through each file to read data and process
for i = 1:length(files)
    file = fullfile(data_dir, files(i).name); % path of the HY-2B data
    
    % Read data from HDF5 file
    lon = double(h5read(file, '/wvc_lon'));
    lat = double(h5read(file, '/wvc_lat'));
    speed = double(h5read(file, '/wind_speed_selection'));
    direction = double(h5read(file, '/wind_dir_selection'));
    
    % Subsample and reshape data
    lon = lon(1:step:end, 1:step:end);
    lat = lat(1:step:end, 1:step:end);
    speed = speed(1:step:end, 1:step:end) / 100;  % Scale wind speed to m/s
    direction = direction(1:step:end, 1:step:end) / 10 * pi / 180; % Convert to radians
    
    % Reshape to 1D
    lon_1d = reshape(lon, [], 1);
    lat_1d = reshape(lat, [], 1);
    speed_1d = reshape(speed, [], 1);
    direction_1d = reshape(direction, [], 1);
    
    % Remove invalid data where speed < 0
    valid_idx = speed_1d >= 0;
    lon_1d = lon_1d(valid_idx);
    lat_1d = lat_1d(valid_idx);
    speed_1d = speed_1d(valid_idx);
    direction_1d = direction_1d(valid_idx);
    
    % Concatenate data
    lon_all = [lon_all; lon_1d];
    lat_all = [lat_all; lat_1d];
    speed_all = [speed_all; speed_1d];
    direction_all = [direction_all; direction_1d];
end

%% Figure to show the HY-2B data
figure('unit','centimeters','position',[1,1,18,10],'color','w'); % figure size
left = 1.5/18; 
bottom = 1/10;
width = 15/18;
height = 8/10;
axes('position',[left bottom width height]); % axe location
% using m_map to plot the fgure
m_proj('Equidistant cylindrical','long',[0 360],'lat',[-90 90]);
m_scatter(lon_all,lat_all,2,speed_all, 'filled');hold on; 
colormap('jet'); % set 'jet' type of the colormap
caxis([3 15]); % min and max limitaton of the figure
m_coast('patch',[.86 .86 .86]); hold on; % land patch
% vector of the wind direction
x_comp = sin(direction_all);
y_comp = cos(direction_all);
m_quiver(lon_all(1:40:end), lat_all(1:40:end), x_comp(1:40:end), y_comp(1:40:end), 3, ...
        'k', 'MaxHeadSize', 5, 'AutoScale', 'off');
% tick and ticklabels of the x and y coordinate
m_grid('linestyle','none','tickdir','out','xtick',0:60:360,'ytick',-90:30:90,'fontsize',12,...
    'fontname','Times New Roman','linewidth',1.5);
hc = colorbar;
set(hc,'tickdir','out','position',[0.93 0.15 0.012 0.7],...
   'ytick',3:3:15,'fontsize',12,'fontname','Times New Roman');
% export_fig(sprintf('%s%d.png','../figures/HY_2B_matlab'),'-r300','-zbuffer');
