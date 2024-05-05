import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap
from matplotlib import rcParams
import subprocess
import cmaps

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

titles = ["(a) LH", "(b) SH", "(c) Rn", "(d) Tro"]
titles_line = ["LH", "SH", "Rn", "Tro"]
names =["le","sh","rns","mrro"]
units =["W/m²","W/m²","W/m²","mm/year"]
vmax=[2.5,2.5,2.5,250]
vmin=[0,0,0,0]
ticks = [
    np.arange(vmin[0]+0.5, vmax[0], 0.5),
    np.arange(vmin[1]+0.5, vmax[1], 0.5),
    np.arange(vmin[2]+0.5, vmax[2], 0.5),
    np.arange(vmin[3]+50, vmax[3], 50)
]
boundaries = [
    np.arange(vmin[0], vmax[0]+0.025, 0.025),
    np.arange(vmin[1], vmax[1]+0.025, 0.025),
    np.arange(vmin[2], vmax[2]+0.025, 0.025),
    np.arange(vmin[3], vmax[3]+2.5, 2.5)
]


fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(50, 30), subplot_kw={'projection': ccrs.PlateCarree()})

for i, ax in enumerate(axs.flat):
    if i == 4:
        break  
    # 读取数据
    datanc = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/PLSR/variable/process/inter/std_mean/{names[i]}.nc')
    data = np.flipud(datanc['std_mean'][:, :])
    data = np.where(np.isclose(data, -1e+36), np.nan, data)

    if i == 3:
        data = data*86400*365
        
    im = ax.imshow(data, cmap=cmaps.WhiteYellowOrangeRed, vmin=vmin[i], vmax=vmax[i], extent=[-180, 180, -60, 90])
    
    cbar = plt.colorbar(im, ticks=ticks[i], boundaries=boundaries[i], orientation='vertical', pad=0.01, shrink=0.8, extend="both", ax=ax)
    cbar.ax.tick_params(labelsize=65, width=2, length=7)

    ax.coastlines(linewidth=2)
    ax.set_facecolor('grey')

    ax.text(0.03, 0.1, f"{titles[i]}", fontsize=80, transform=ax.transAxes, ha="left") 
    ax.text(1.037, 0.92, f'{units[i]}', fontsize=50, transform=ax.transAxes, ha="left")
       
    # ax.text(0.5, 1.08, f"{titles[i]}", fontsize=80, transform=ax.transAxes, ha="center")
    # ax.text(1, 1.05, f'{units[i]}', fontsize=65, transform=ax.transAxes, ha="right")

    for spine in ax.spines.values():
        spine.set_linewidth(3)

plt.delaxes(axs[2, 0])
plt.delaxes(axs[2, 1])


ax = fig.add_axes([0.125, 0.15, 0.71, 0.17])
# ax = plt.subplot2grid((3, 3), (2, 1), colspan=2, rowspan=1)

# ax.set_ylim(-5, 7)
ax.tick_params(axis='y', labelsize=65)

x_values = range(1, 26) 
labels = [str(year) if year % 2 == 1 else '' for year in range(1995, 2020)]  
ax.set_xticks(x_values)
ax.set_xticklabels(labels, fontsize=65, rotation=30)

ax.tick_params(axis='x', which='both', direction='out', length=10, width=2)
ax.tick_params(axis='y', which='both', direction='out', length=10, width=2)
ax.yaxis.tick_right()

for spine in ax.spines.values():
    spine.set_linewidth(2.5)

ax.grid(True, linestyle='--', alpha=0.5)

for i in range(1, 5):
    # 读取 NetCDF 文件
    file_path = f'/tera11/zhwei/students/Baifan/hard/PLSR/variable/process/inter/std/fldmean/{names[i-1]}.nc'
    data = xr.open_dataset(file_path)['variable'][:, 0, 0]
    
    percentage_change = (data / data.mean() - 1) * 100
    markers = ['o', 's', 'D', '^']

    ax.plot(x_values, percentage_change, marker=markers[i-1], linestyle='-', markersize=16, label=f'{titles_line[i-1]}', linewidth=3.5)

ax.legend(loc='best', fontsize=55, ncol=4, frameon=False, bbox_to_anchor=(0.57, 0.67))

ax.text(0.035, 0.8, '(e)', fontsize=80, transform=ax.transAxes, ha="center")
ax.text(1.06, 0.5, '%', fontsize=70, transform=ax.transAxes, ha="right")

plt.subplots_adjust(wspace=-0.02, hspace=0)

plt.savefig('/stu01/baif/job/test/2.jpg', format='jpg', dpi=300, bbox_inches='tight')
input_file  = '/stu01/baif/job/test/2.jpg'
output_file = '/stu01/baif/job/test/2.jpg'
subprocess.run(['convert', input_file, '-trim', output_file])

# plt.savefig('/stu01/baif/job/test/2.pdf', format='pdf', dpi=300, bbox_inches='tight')
# plt.savefig('/stu01/baif/job/test/2.eps', format='eps', dpi=300, bbox_inches='tight')