import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import subprocess
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter

# 设置默认字体
plt.rcParams['font.family'] = 'Times New Roman'

# 创建子图
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(35, 15), subplot_kw={'projection': ccrs.PlateCarree()})

# 数据文件路径
file_paths = ["/stu01/baif/PLSR/code/fig8/le.nc", "/stu01/baif/PLSR/code/fig8/sh.nc", "/stu01/baif/PLSR/code/fig8/rns.nc", "/stu01/baif/PLSR/code/fig8/mrro.nc"]
titles = ["(a) LH", "(b) SH", "(c) Rn", "(d) Tro"]

for ax, file_path, title in zip(axs.flat, file_paths, titles):
    # 读取数据
    data = xr.open_dataset(file_path)
    KGESS = np.flipud(data['variable'][:,:])
    
    # 设置色彩映射
    colors = ["orange", "purple", "indigo", "turquoise", "red", "pink"]
    cmap = ListedColormap(colors)
    
    # 绘制地图
    im = ax.imshow(KGESS, cmap=cmap, vmin=1, vmax=6, extent=[-180, 180, -60, 90])
    ax.coastlines(linewidth=1.3)
    # ax.set_title(title, fontsize=70, pad=20)
    ax.text(0.12, 0.1, title, fontsize=55, transform=ax.transAxes, ha="center")
    ax.set_xticks([-120,-60,0,60,120])                      
    ax.set_yticks([-60,-30,0,30,60,90])                  
    ax.xaxis.set_major_formatter(LongitudeFormatter())                   
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    ax.tick_params(axis='both', which='both', width=2.5, length=10, labelsize=35)
    ax.spines['geo'].set_linewidth(2.5)

    # axes[0, 1].set_position([0.55, 0.55, 0.4, 0.4])

plt.subplots_adjust(wspace=0, hspace=0.3)

legend_labels = ['CRUJRA', 'ERA5', 'ERA5LAND', 'JRA55', 'MSWX', 'WFDE5']
legend_colors = ["orange", "purple", "indigo", "turquoise", "red", "pink"]
legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]
plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(-0.1, -0.15), ncol=len(legend_patches), fontsize=38, frameon=False)

# 保存图像
plt.savefig('/stu01/baif/job/test/8.jpg', format='jpg', dpi=300, bbox_inches='tight')
input_file  = '/stu01/baif/job/test/8.jpg'
output_file = '/stu01/baif/job/test/8.jpg'
subprocess.run(['convert', input_file, '-trim', output_file])

# plt.savefig('/stu01/baif/job/test/8.pdf', format='pdf', dpi=300, bbox_inches='tight')
# plt.savefig('/stu01/baif/job/test/8.eps', format='eps', dpi=300, bbox_inches='tight')