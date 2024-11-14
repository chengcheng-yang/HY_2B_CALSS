%% read name of the nc file

fname = dir('../data/*.nc');
fpath = strcat('../data/',fname.name);
ncdisp(fpath);
clear fname;
%% read ssh data
ssh = ncread(fpath,'adt');
ssh_lon = ncread(fpath,'longitude');
ssh_lat = ncread(fpath,'latitude');
clear fpath;
ssh_lon(ssh_lon<0) = ssh_lon(ssh_lon<0)+360;
ssh_lon = [ssh_lon(length(ssh_lon)/2+1:end);ssh_lon(1:length(ssh_lon)/2)];
ssh = [ssh(length(ssh_lon)/2+1:end,:);ssh(1:length(ssh_lon)/2,:)];

%% Figure
figure('unit','centimeters','position',[1,1,18,10],'color','w');
left = 1.5/18; 
bottom = 1/10;
width = 15/18;
height = 8/10;
axes('position',[left bottom width height]);
m_proj('Equidistant cylindrical','long',[0 360],'lat',[-90 90]);
m_contourf(ssh_lon,ssh_lat,ssh',80,'linestyle','none');hold on; 
colormap('jet');
caxis([-1.5 1.5]);
m_coast('patch',[.86 .86 .86]); hold on;
m_grid('linestyle','none','tickdir','out','xtick',0:60:360,'ytick',-90:30:90,'fontsize',12,...
    'fontname','Times New Roman','linewidth',1.5);
hc = colorbar;
set(hc,'tickdir','out','position',[0.93 0.15 0.012 0.7],...
   'ytick',-1.5:0.5:1.5,'fontsize',12,'fontname','Times New Roman');
% export_fig(sprintf('%s%d.png','../figures/cmems_adt_matlab'),'-r300','-zbuffer');

