import matplotlib.pyplot as plt
import xarray as xr
import seaborn as sns
import cartopy.crs as ccrs
from pylab import rcParams
import subprocess

# 设置默认字体
plt.rcParams['font.family'] = 'Times New Roman'

params = {'backend': 'ps',
          'axes.labelsize': 30,
          'grid.linewidth': 0.2,
          'font.size': 15,
          'legend.fontsize': 12,
          'legend.frameon': False,
          'xtick.labelsize': 25,
          'xtick.direction': 'out',
          'ytick.labelsize': 25,
          'ytick.direction': 'out',
          'savefig.bbox': 'tight',
          'axes.unicode_minus': False,
          'text.usetex': False}
rcParams.update(params)

# 创建一个图形和轴
fig, ax = plt.subplots(figsize=(18, 8))

# 读取七个不同的 nc 文件，每个文件一组数据
titles = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDE5"]
data_list = []

for i in range(6):
    # 读取 NetCDF 文件
    file_path = f'/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process/std_global/{titles[i]}_prec.nc'
    data = xr.open_dataset(file_path)['std_global']
    data = data*365
    data_list.append(data)

# 转换数据为 DataFrame
df = xr.concat(data_list, dim='exp').to_dataframe().reset_index()

colors_list = sns.color_palette("Set3", n_colors=6, desat=.9).as_hex()
colors = [colors_list[2], colors_list[0], colors_list[5], colors_list[3], colors_list[4], colors_list[1]]
line_color = sns.color_palette().as_hex()

# 为每个箱子设置不同的颜色
colors = sns.color_palette("Set3", n_colors=len(titles), desat=.7).as_hex()

# 将数据按照实验分组
grouped_data = [group["std_global"] for name, group in df.groupby("exp")]

# 绘制箱型图
bplot = plt.boxplot(grouped_data, patch_artist=True, positions=(1, 1.3, 1.6, 1.9, 2.2, 2.5), widths=0.15,
                    medianprops={'color': f'{line_color[3]}', 'linewidth': '2.0'},
                    showmeans=True, meanline=True, meanprops={'color': 'black'})

for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)  
    
# 设置图标题和轴标签
# plt.title('P (mm/year)', fontsize=65, pad=16, y=1.03)
# ax.text(0.5, 1.03, "P", fontsize=75, transform=ax.transAxes, ha="center")
ax.text(0.98, 0.9, 'mm/year', fontsize=40, transform=ax.transAxes, ha="right")
    
for i, mean_val in enumerate(df.groupby("exp")["std_global"].mean()):
    plt.text(1 + i * 0.3, bplot['whiskers'][2 * i + 1].get_ydata()[1] + 0, f'{mean_val:.2f}', ha='center', va='bottom', color='black', fontsize=30)
# 调整图形边框大小
ax.spines['top'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

ax.set_xlim(0.8, 2.7)

plt.ylim(630, 899)
plt.yticks(fontsize=30)

ax.set_xticks([])
ax.tick_params(axis='y', which='both', width=2)

plt.legend(bplot['boxes'], titles, loc='best', fontsize=22)  

# 保存图像
plt.savefig('/stu01/baif/job/test/S3.jpg', format='jpg', dpi=300, bbox_inches='tight')
input_file  = '/stu01/baif/job/test/S3.jpg'
output_file = '/stu01/baif/job/test/S3.jpg'
subprocess.run(['convert', input_file, '-trim', output_file])

# plt.savefig('/stu01/baif/job/test/S4.pdf', format='pdf', dpi=300, bbox_inches='tight')
# plt.savefig('/stu01/baif/job/test/S4.eps', format='eps', dpi=300, bbox_inches='tight')