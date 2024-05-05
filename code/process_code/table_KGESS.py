# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from pylab import rcParams

# sns.set(font='Times New Roman')
# rcParams.update({'font.size': 15, 'legend.fontsize': 75, 'xtick.labelsize': 75, 'ytick.labelsize': 75})

# titles = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDE5", "WFDEI", "CRUNCEPV4", "CRUNCEPV7", "GSWP3", "PRINCETON", "QIAN"]
# names = ["le", "sh"]
# variables = ["Qle", "Qh"]
# metrics = ["KGESS", "correlation"]


# for i in range(0,12):
#     for j in range(0,2):
#         for k in range(0,2):
#             fig, ax = plt.subplots(figsize=(30, 15))
            
#             colors_list = ['#7ED0F8']
#             colors_bar = ['#336699']

#             ax.set_xlim(0, 1)

#             pathin = f"/tera07/zhwei/For_BaiFan/validation/stn/{names[j]}/{titles[i]}/FLUXNET/output/"

#             data = pd.read_csv(f"{pathin}/{variables[j]}_cor_metric.csv").dropna(subset=[f"{metrics[k]}"])
#             data[f"{metrics[k]}"] = np.clip(data[f"{metrics[k]}"], 0, 1)
#             sns.histplot(data, x=f"{metrics[k]}", bins=np.arange(0, 1.05, 0.05), element="bars", stat="probability", common_norm=True, kde=True,
#                         color=colors_list[0], ax=ax, edgecolor=colors_bar[0], linewidth=5,
#                         line_kws={'color': colors_bar[0], 'linestyle': 'solid', 'linewidth': 8, 'label': "KDE"})

#             ax.grid(True, linestyle='--', linewidth=2, color='grey', alpha=0.6)
#             ax.set_ylabel('Density', fontsize=75, labelpad=60)
#             ax.set_xlabel('', fontsize=70, labelpad=60)
#             ax.set_xticks(np.arange(0.2, 1.2, 0.2))
#             ax.legend(fontsize=70, loc='upper left', frameon=False)

#             for spine in ax.spines.values():
#                 spine.set_linewidth(4) 
#                 spine.set_color('black')
                
#             plt.tight_layout()
#             plt.savefig(f'/stu01/baif/PLSR/plot/fig7/{names[j]}/{metrics[k]}/{titles[i]}.png', format='png', dpi=300, bbox_inches='tight')
#             plt.close()
#             print(f"{names[j]}-{metrics[k]}-{titles[i]}")



# import numpy as np
# import pandas as pd

# titles = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDE5", "WFDEI", "CRUNCEPV4", "CRUNCEPV7", "GSWP3", "PRINCETON", "QIAN"]
# names = ["le", "sh"]
# variables = ["Qle", "Qh"]
# metrics = ["KGESS"]

# for i in range(0,12):
#     for j in range(0,2):
#         for k in range(0,1):
            
#             pathin = f"/tera11/zhwei/students/Baifan/hard/validation/stn_r/{names[j]}/{titles[i]}/FLUXNET/output/"

#             data = pd.read_csv(f"{pathin}/{variables[j]}_cor_metric.csv").dropna(subset=[f"{metrics[k]}"])
#             data[f"{metrics[k]}"] = np.clip(data[f"{metrics[k]}"], 0, 1)
#             data = np.mean(data[f"{metrics[k]}"])
            
#             print(f"{names[j]}-{metrics[k]}-{titles[i]}: {data:.3f}")



import numpy as np
import pandas as pd

titles = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDEI", "CRUNCEPV4", "CRUNCEPV7", "GSWP3", "PRINCETON", "QIAN"]
names = ["discharge"]
variables = ["discharge"]
metrics = ["KGESS"]

for i in range(0,11):
    for j in range(0,1):
        for k in range(0,1):
            
            pathin = f"/tera11/zhwei/students/Baifan/hard/validation/stn_r/{names[j]}/{titles[i]}/StreamFlow/GRDC/output/"

            data = pd.read_csv(f"{pathin}/{variables[j]}_metric.csv").dropna(subset=[f"{metrics[k]}"])
            data[f"{metrics[k]}"] = np.clip(data[f"{metrics[k]}"], -1, 1)
            data = np.mean(data[f"{metrics[k]}"])
            
            print(f"{names[j]}-{metrics[k]}-{titles[i]}: {data:.3f}")