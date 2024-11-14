# %% import libraries
import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

"""
Python codes for data analysis of the CMEMS satellite data.
"""
# %% read filename
file_names = [f for f in os.listdir("../data/") if f.endswith(".nc")]

# %% read the netcdf file
ds = xr.open_dataset(f"../data/{file_names[0]}")
ds

# %% read ssh data
ssh = ds["adt"].squeeze()

# %% plot the ssh data
fig = plt.figure(figsize=(18, 10), dpi=300)
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
ax.coastlines()
contourf = ax.contourf(
    ssh.longitude,
    ssh.latitude,
    ssh,
    vmin=-1.5,
    vmax=1.5,
    levels=np.arange(-1.5, 1.6, 0.05),
    cmap="RdBu_r",
    transform=ccrs.PlateCarree(),
    extend="both",
)
cbar = plt.colorbar(
    contourf,
    ax=ax,
    orientation="vertical",
    extend="both",
    pad=0.008,
    shrink=0.6,
    label="ADT (m)",
    ticks=np.arange(-1.5, 1.6, 0.5),
)
cbar.set_label("ADT (m)", fontsize=15)
cbar.ax.tick_params(labelsize=15)
ax.set_xticks(np.arange(0, 360, 30), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-90, 91, 30), crs=ccrs.PlateCarree())
lon_labels = [str(int(lon)) for lon in np.arange(0, 360, 30)]
ax.set_xticklabels(lon_labels, fontsize=15)
ax.tick_params(axis="both", labelsize=15)

plt.savefig("../figures/cmems_adt_python.png", dpi=300, bbox_inches="tight")
plt.show()
