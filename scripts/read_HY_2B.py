# %% import libraries
import os
import numpy as np
import xarray as xr
import h5py
import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

"""
Python codes for data analysis of the HY-2B satellite data. 
"""
# %% read filename
file_names = [f for f in os.listdir("../data/") if f.endswith(".h5")]

# %% read attributes about the h5 file
ds = h5py.File(f"../data/{file_names[0]}", "r")
# check the attributes of the h5 file
for k in ds.attrs.keys():
    print("{}=>{}".format(k, ds.attrs[k]))
# check the keys of the h5 file
for key in ds.keys():
    print("\n")
    print(ds[key], key, ds[key].name)
# check the attributes of the keys
for k in ds[key].attrs.keys():
    print(k, ds[key].attrs[k])

# %%
# read all data and concatenate them
lon_all = []
lat_all = []
speed_all = []
direction_all = []

step = 2  # subtract the data every 3 steps

for file in file_names:
    ds = h5py.File(f"../data/{file}", "r")
    lon = ds["wvc_lon"][:][::step, ::step]  # lon
    lat = ds["wvc_lat"][:][::step, ::step]  # lat
    speed = ds["wind_speed_selection"][:][::step, ::step]  # wind speed
    direction = ds["wind_dir_selection"][:][::step, ::step]  # wind direction
    lon_1d = lon.reshape(lon.shape[0] * lon.shape[1], order="F")
    lat_1d = lat.reshape(lat.shape[0] * lat.shape[1], order="F")
    speed_1d = (
        speed.reshape(speed.shape[0] * speed.shape[1], order="F") / 100
    )  # rescale the speed to the actual m/s
    direction_1d = (
        direction.reshape(direction.shape[0] * direction.shape[1], order="F") / 10
    )  # rescale the direction to the actual degree
    direction_1d = (
        np.array(direction_1d) / 360 * 2 * np.pi
    )  # convert the degree to radian
    del_ind = np.where(speed_1d < 0)  # delete the none data
    lon_1d = np.delete(lon_1d, del_ind)
    lat_1d = np.delete(lat_1d, del_ind)
    speed_1d = np.delete(speed_1d, del_ind)
    direction_1d = np.delete(direction_1d, del_ind)
    # concatenate the data
    lon_all = np.concatenate((lon_all, lon_1d))
    lat_all = np.concatenate((lat_all, lat_1d))
    speed_all = np.concatenate((speed_all, speed_1d))
    direction_all = np.concatenate((direction_all, direction_1d))

# %% plot the data
fig = plt.figure(figsize=(18, 10), dpi=300)
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
ax.coastlines()
scatter = ax.scatter(
    lon_all,
    lat_all,
    s=0.5,
    c=speed_all,
    vmin=3,
    vmax=15,
    cmap="coolwarm",
    transform=ccrs.PlateCarree(),
)
# plot the wind direction
x_comp = np.sin(direction_all)
y_comp = np.cos(direction_all)
ax.quiver(
    lon_all[::40],
    lat_all[::40],
    x_comp[::40],
    y_comp[::40],
    scale=80,
    width=0.001,
    headlength=8,
    headwidth=8,
    transform=ccrs.PlateCarree(),
)
cbar = plt.colorbar(
    scatter,
    ax=ax,
    orientation="vertical",
    extend="both",
    pad=0.01,
    shrink=0.6,
    label="Wind Speed (m/s)",
    ticks=np.arange(3, 16, 3),
)
cbar.ax.tick_params(labelsize=15)
ax.set_xticks(np.arange(0, 360, 30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
lon_labels = [str(int(lon)) for lon in np.arange(0, 360, 30)]
ax.set_xticklabels(lon_labels, fontsize=15)
ax.tick_params(axis="both", labelsize=15)

plt.savefig("../figures/HY_2B_python.png", dpi=300, bbox_inches="tight")
plt.show()
