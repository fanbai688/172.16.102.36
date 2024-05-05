import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
import cmaps
from matplotlib.colors import ListedColormap
import subprocess

titles = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDE5", "WFDEI", "CRUNCEPV7", "GSWP3", "CRUNCEPV4", "PRINCETON", "QIAN"]
names = ["LH", "SH", "Rn", "Tro"]

csv_path = '/stu01/baif/ILAMB/ILAMB-org/MODELS_new/scores_r.csv'
df = pd.read_csv(csv_path, index_col=0, header=0)

df_normalized = df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)
df_normalized = df_normalized.reindex(columns=titles)

plt.figure(figsize=(15, 7))
sns.set(font='Times New Roman')

cmap_segment = cmaps.MPL_PuOr
vmin, vmax = -3, 2
colors_segment = plt.get_cmap(cmap_segment)(np.linspace(0, 1, 256))
segment_colors = colors_segment[0:200]
cmap_segmented = ListedColormap(segment_colors)
heatmap = sns.heatmap(df_normalized, cmap=cmap_segmented, annot=True, fmt=".2f", linewidths=1, cbar_kws={'label': '',"pad":0.02})

for text in heatmap.texts:
    text.set_color('black')
    text.set_fontsize(23)

cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=23, width=1.5, pad=3)

plt.title('ILAMB Relative Scores', fontsize=35, pad=10, y=1.01)
plt.xlabel('', fontsize=20)
plt.ylabel('', fontsize=20)

plt.xticks(ticks=[i + 0.5 for i in range(len(titles))], labels=titles, fontsize=23, rotation=90, ha='center') 
plt.yticks(ticks=[i + 0.5 for i in range(len(names))], labels=names, fontsize=23, rotation=0, va='center')

plt.tight_layout()
plt.savefig('/stu01/baif/job/test/S5.jpg', format='jpg', dpi=300, bbox_inches='tight')
input_file  = '/stu01/baif/job/test/S5.jpg'
output_file = '/stu01/baif/job/test/S5.jpg'
subprocess.run(['convert', input_file, '-trim', output_file])

# plt.savefig('/stu01/baif/job/test/4.pdf', format='pdf', dpi=300, bbox_inches='tight')
# plt.savefig('/stu01/baif/job/test/4.eps', format='eps', dpi=300, bbox_inches='tight')