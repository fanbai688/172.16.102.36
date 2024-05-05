import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap
from matplotlib import rcParams
import cmaps
import subprocess

# 设置默认字体
plt.rcParams['font.family'] = 'Times New Roman'

# 设置绘图参数
params = {
    'backend': 'ps',
    'axes.labelsize': 12,
    'grid.linewidth': 0.2,
    'font.size': 15,
    'legend.fontsize': 40,
    'legend.frameon': False,
    'xtick.labelsize': 20,
    'xtick.direction': 'out',
    'ytick.labelsize': 20,
    'ytick.direction': 'out',
    'savefig.bbox': 'tight',
    'axes.unicode_minus': False,
    'text.usetex': False
}
rcParams.update(params)

titles = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)", "(j)", "(k)", "(l)", "(m)", "(n)", "(o)", "(p)"]
# titles = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]

variables = ["le", "sh", "rns", "mrro"]

fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(50, 30), subplot_kw={'projection': ccrs.PlateCarree()})

for i, ax in enumerate(axs.flat):
    
    if i in [0+0, 1+0, 2+0, 3+0]:
        j = [0+0, 1+0, 2+0, 3+0].index(i)
        datanc = xr.open_dataset('/stu01/baif/test/test9/le/coef.nc')
        data = np.flipud(datanc['variable'][j, :, :])
        data = np.where(np.isclose(data, -1e+36), np.nan, data)
        
    if i in [0+4, 1+4, 2+4, 3+4]:
        j = [0+4, 1+4, 2+4, 3+4].index(i)
        datanc = xr.open_dataset('/stu01/baif/test/test9/sh/coef.nc')
        data = np.flipud(datanc['variable'][j, :, :])
        data = np.where(np.isclose(data, -1e+36), np.nan, data)
        
    if i in [0+8, 1+8, 2+8, 3+8]:
        j = [0+8, 1+8, 2+8, 3+8].index(i)
        datanc = xr.open_dataset('/stu01/baif/test/test9/rns/coef.nc')
        data = np.flipud(datanc['variable'][j, :, :])
        data = np.where(np.isclose(data, -1e+36), np.nan, data)
        
    if i in [0+12, 1+12, 2+12, 3+12]:
        j = [0+12, 1+12, 2+12, 3+12].index(i)
        datanc = xr.open_dataset('/stu01/baif/test/test9/mrro/coef.nc')
        data = np.flipud(datanc['variable'][j, :, :])
        data = np.where(np.isclose(data, -1e+36), np.nan, data)
    
    im = ax.imshow(data, cmap=cmaps.BlueWhiteOrangeRed, vmin=-1.5, vmax=1.5, extent=[-180, 180, -60, 90])
    
    ax.coastlines(linewidth=2)
    ax.set_facecolor('grey')

    ax.text(0.08, 0.1, f"{titles[i]}", fontsize=65, transform=ax.transAxes, ha="center", )

    for spine in ax.spines.values():
        spine.set_linewidth(3)

plt.text(0.22, 0.81, "LW", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.415, 0.81, "SW", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.61, 0.81, "P", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.805, 0.81, "VPD", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.1, 0.72, "LH", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.1, 0.57, "SH", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.1, 0.42, "Rn", fontsize=80, transform=fig.transFigure, ha="center")
plt.text(0.1, 0.27, "Tro", fontsize=80, transform=fig.transFigure, ha="center")

cbar_ax = fig.add_axes([0.263, 0.15, 0.5, 0.02])  
cbar = plt.colorbar(im, ticks=np.arange(-1.5, 1.8, 0.3), boundaries=np.arange(-1.5, 1.51, 0.01),  orientation='horizontal',  pad=0.01, shrink=0.35,  cax=cbar_ax)
cbar.ax.tick_params(labelsize=50, width=3, length=8)

plt.subplots_adjust(wspace=0.03, hspace=-0.5)

plt.savefig('/stu01/baif/job/test/5.jpg', format='jpg', dpi=300, bbox_inches='tight')
input_file  = '/stu01/baif/job/test/5.jpg'
output_file = '/stu01/baif/job/test/5.jpg'
subprocess.run(['convert', input_file, '-trim', output_file])

# plt.savefig('/stu01/baif/job/test/9.pdf', format='pdf', dpi=300, bbox_inches='tight')
# plt.savefig('/stu01/baif/job/test/9.eps', format='eps', dpi=300, bbox_inches='tight')