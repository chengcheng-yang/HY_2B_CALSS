# %% import libraries
import os
import numpy as np
import xarray as xr
import h5py
import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import glob
from netCDF4 import Dataset

"""
Python codes for data analysis of the windsat data. 
"""
# %% path of the data
base_folder = "../data/"
# file name of wind speed and wind direction
fname_speed = glob.glob(os.path.join(base_folder, "*speed*.nc"))
fname_direction = glob.glob(os.path.join(base_folder, "*direction*.nc"))

# %% base info of the data
file_path = fname_speed[1]
# open NetCDF
with Dataset(file_path, "r") as nc:
    # dimensions
    print("dimensions:")
    for dim in nc.dimensions:
        print(f"    {dim} = {len(nc.dimensions[dim])} ;")

    # variables
    print("\nvariables:")
    for var in nc.variables:
        var_obj = nc.variables[var]
        print(f"    {var_obj.dtype} {var}({', '.join(var_obj.dimensions)}) ;")

        # attributes
        for attr in var_obj.ncattrs():
            print(f'            {var}:{attr} = "{getattr(var_obj, attr)}" ;')

    # global attributes
    print("\nGlobal Attributes:")
    for attr in nc.ncattrs():
        print(f'    {attr} = "{getattr(nc, attr)}" ;')
# %%  read windsat data
# load lon and lat
lon = xr.open_dataset(fname_speed[0])["LONN719_720"].values
lat = xr.open_dataset(fname_speed[0])["LAT"].values
# load wind speed and wind direction
wind = np.zeros((720, 1440, 2))  # Assuming the shape of the data is (1440, 720, 2)
wind[:, :, 0] = np.squeeze(xr.open_dataset(fname_speed[0])["WINDAW_A"].values)
wind[:, :, 1] = np.squeeze(xr.open_dataset(fname_speed[1])["WINDAW_D"].values)
wind = np.squeeze(np.nanmean(wind, axis=2))
wind = np.where(wind > 0, wind, np.nan)
wind_dir = np.zeros((720, 1440, 2))  # Assuming the shape of the data is (1440, 720, 2)
wind_dir[:, :, 0] = np.squeeze(xr.open_dataset(fname_direction[0])["WDIR_A"].values)
wind_dir[:, :, 1] = np.squeeze(xr.open_dataset(fname_direction[1])["WDIR_D"].values)
wind_dir = np.squeeze(np.nanmean(wind_dir, axis=2))

# %% post processing (shift the map center from 0E to 180E )
lon_new = np.concatenate((lon[len(lon) // 2 :], lon[: len(lon) // 2] + 360))
wind_new = np.concatenate((wind[:, len(lon) // 2 :], wind[:, : len(lon) // 2]), axis=1)
wind_dir = np.concatenate(
    (wind_dir[:, len(lon) // 2 :], wind_dir[:, : len(lon) // 2]), axis=1
)

# %% plot the wind speed
fig = plt.figure(figsize=(18, 10), dpi=300)  # set the figure size
ax = plt.axes(
    projection=ccrs.PlateCarree(central_longitude=180)
)  # set the map projection
ax.coastlines()  # add coastlines
# set the extent
ax.set_extent([0, 359.9, -90, 90], crs=ccrs.PlateCarree())  # set the extent
# plot the wind speed
contourf = ax.contourf(
    lon_new,
    lat,
    wind_new,
    vmin=3,
    vmax=15,
    levels=np.linspace(3, 15, 31),
    cmap="coolwarm",
    transform=ccrs.PlateCarree(),
    extend="both",
)
# plot the wind direction
quiver = ax.quiver(
    lon_new[::20],
    lat[::20],
    np.cos(wind_dir[::20, ::20] / 180 * np.pi),
    np.sin(wind_dir[::20, ::20] / 180 * np.pi),
    scale=80,
    width=0.001,
    headlength=8,
    headwidth=8,
    transform=ccrs.PlateCarree(),
)
# add the colorbar
cbar = plt.colorbar(
    contourf,
    ax=ax,
    orientation="vertical",
    extend="both",
    pad=0.01,
    shrink=0.6,
    label="Wind Speed (m/s)",
    ticks=np.linspace(3, 15, 4),
)
# set the labels
cbar.ax.tick_params(labelsize=15)
ax.set_xticks(np.arange(0, 360, 30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
lon_labels = [str(int(lon)) for lon in np.arange(0, 360, 30)]
ax.set_xticklabels(lon_labels, fontsize=15)
ax.tick_params(axis="both", labelsize=15)
# save the figure
plt.savefig("../figures/windsat_wind_python.png", dpi=300, bbox_inches="tight")
plt.show()
