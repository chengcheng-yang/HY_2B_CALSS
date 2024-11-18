%% obtain  wind speed and wind vector from windsat observations
clear;clc;
%% read windsat observations
fname_speed = dir('../data/*speed*.nc'); % file name of wind speed
fname_direction = dir('../data/*direction*.nc'); % file name of wind direction
base_folder = '../data/'; % folder name of the observation data
% obtain lon, lat, wind speed and wind direction
fpath = strcat(base_folder,fname_speed(1).name);
ncdisp(fpath); 
lon = ncread(fpath,'LONN719_720');
lat = ncread(fpath,'LAT');
% wind speed of ascend map
wind(:,:,1) = squeeze(ncread(strcat(base_folder,fname_speed(1).name),'WINDAW_A'));
% wind speed of descend map
wind(:,:,2) = squeeze(ncread(strcat(base_folder,fname_speed(2).name),'WINDAW_D'));
% calculate the mean wind speed
wind = squeeze(nanmean(wind,3));

% wind direction of ascend map
wind_dir(:,:,1) = squeeze(ncread(strcat(base_folder,fname_direction(1).name),'WDIR_A'));
wind_dir(:,:,2) = squeeze(ncread(strcat(base_folder,fname_direction(2).name),'WDIR_D'));
wind_dir = squeeze(nanmean(wind_dir,3));

%% post processing (shift the map center from 0E to 180E )
lon = [lon(length(lon)/2+1:end);lon(1:length(lon)/2)+360];
wind = [wind(length(lon)/2+1:end,:);wind(1:length(lon)/2,:)];
wind(wind<0) = nan;
wind_dir = [wind_dir(length(lon)/2+1:end,:);wind_dir(1:length(lon)/2,:)];

%% Figure 
figure('unit','centimeters','position',[1,1,18,10],'color','w'); % figure size
left = 1.5/18; 
bottom = 1/10;
width = 15/18;
height = 8/10;
axes('position',[left bottom width height]); % axe location
m_proj('Equidistant cylindrical','long',[0 360],'lat',[-90 90]);
m_contourf(lon,lat,wind', 80,'linestyle','none');hold on; 
colormap('jet');
caxis([3 15]); % min and max limitation of colorbar
m_coast('patch',[.86 .86 .86]); hold on; % land patch
% tick and ticklabels of x and y coordinate 
m_grid('linestyle','none','tickdir','out','xtick',0:60:360,'ytick',-90:30:90,'fontsize',12,...
    'fontname','Times New Roman','linewidth',1.5);
% vectors imply the direction of the wind
x_comp = sind(wind_dir);
y_comp = cosd(wind_dir);
[lat2d,lon2d] = meshgrid(lat,lon);
m_quiver(lon2d(1:10:end,1:10:end)', lat2d(1:10:end,1:10:end)', x_comp(1:10:end,1:10:end)', y_comp(1:10:end,1:10:end)', 2, ...
        'k', 'MaxHeadSize', 5, 'AutoScale', 'off');
% set colorbar in the figure 
hc = colorbar;
set(hc,'tickdir','out','position',[0.93 0.15 0.012 0.7],...
   'ytick',3:3:15,'fontsize',12,'fontname','Times New Roman');
% export_fig(sprintf('%s%d.png','../figures/windsat_wind_matlab'),'-r300','-zbuffer');
