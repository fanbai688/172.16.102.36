import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas  as pd
import skill_metrics as sm
import sys 
from matplotlib.colors import ListedColormap
import subprocess

plt.rcParams['font.family'] = 'Times New Roman'
params = {
    'backend': 'ps',
    'axes.labelsize': 12,
    'grid.linewidth': 0.2,
    'font.size': 12,
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

MARKERS = {
        "CRUJRA": {
            "labelColor": "k",
            "symbol": "+",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "r",
        },
        "ERA5": {
            "labelColor": "k",
            "symbol": ".",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "b",
        },
        "ERA5LAND": {
            "labelColor": "k",
            "symbol": "x",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "g",
        },
        "JRA55": {
            "labelColor": "k",
            "symbol": "s",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "c",
        },
        "MSWX": {
            "labelColor": "k",
            "symbol": "d",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "m",
        },
        "WFDE5": {
            "labelColor": "k",
            "symbol": "^",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "y",
        },
        "WFDEI": {
            "labelColor": "k",
            "symbol": "v",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "r",
        },
        "CRUNCEPV7": {
            "labelColor": "k",
            "symbol": "p",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "b",
        },
        "GSWP3": {
            "labelColor": "k",
            "symbol": "h",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "g",
        },
        "CRUNCEPV4": {
            "labelColor": "k",
            "symbol": "*",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "c",
        },
        "PRINCETON": {
            "labelColor": "k",
            "symbol": "+",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "m",
        },
        "QIAN": {
            "labelColor": "k",
            "symbol": ".",
            "size": 10,
            "faceColor": "w",
            "edgeColor": "y",
        },
    }

# MARKERS = {
#         "CRUJRA": {
#             "labelColor": "k",
#             "symbol": "d",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "r",
#         },
#         "ERA5": {
#             "labelColor": "k",
#             "symbol": "d",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "b",
#         },
#         "ERA5LAND": {
#             "labelColor": "k",
#             "symbol": "d",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "g",
#         },
#         "JRA55": {
#             "labelColor": "k",
#             "symbol": "d",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "y",
#         },
#         "MSWX": {
#             "labelColor": "k",
#             "symbol": "d",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "m",
#         },
#         "WFDE5": {
#             "labelColor": "k",
#             "symbol": "d",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "c",
#         },
#         "WFDEI": {
#             "labelColor": "k",
#             "symbol": ".",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "r",
#         },
#         "CRUNCEPV7": {
#             "labelColor": "k",
#             "symbol": ".",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "b",
#         },
#         "GSWP3": {
#             "labelColor": "k",
#             "symbol": ".",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "g",
#         },
#         "CRUNCEPV4": {
#             "labelColor": "k",
#              "symbol": ".",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "y",
#         },
#         "PRINCETON": {
#             "labelColor": "k",
#             "symbol": ".",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "m",
#         },
#         "QIAN": {
#             "labelColor": "k",
#             "symbol": ".",
#             "size": 10,
#             "faceColor": "w",
#             "edgeColor": "c",
#         },
#     }


fig, ax = plt.subplots(figsize=(6, 6))

titles = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDE5", "WFDEI", "CRUNCEPV7", "GSWP3", "CRUNCEPV4", "PRINCETON", "QIAN"]
metrics = ["std_s", "RMSE", "correlation"]

result = np.zeros((len(metrics), len(titles)))
for i, title in enumerate(titles):
    for j, metric in enumerate(metrics):
        
        # pathin = f"/tera11/zhwei/students/Baifan/hard/validation/stn/{title}/Latent_Heat/case1___PLUMBER2/output/"
        pathin = f"/tera11/zhwei/students/Baifan/hard/validation/stn/{title}/Sensible_Heat/case2___PLUMBER2/output/"
        
        file_path = f"{pathin}/Qh_cor_metric.csv"
        data = pd.read_csv(file_path).dropna(subset=[metric])

        mean_value = data[metric].mean()
        result[j, i] = mean_value
        
# data_std_o = pd.read_csv("/tera11/zhwei/students/Baifan/hard/validation/stn/CRUJRA/Latent_Heat/case1___PLUMBER2/output/Qle_cor_metric.csv").dropna(subset=["std_o"])  
data_std_o = pd.read_csv("/tera11/zhwei/students/Baifan/hard/validation/stn/CRUJRA/Sensible_Heat/case2___PLUMBER2/output/Qh_cor_metric.csv").dropna(subset=["std_o"])
std_o = data_std_o["std_o"].mean()

###数组第一组值默认为标准值，所以画图一般不会生成
std_s = np.zeros(13)
rmse = np.zeros(13)
corr = np.zeros(13)

std_s[1:] = result[0, :]
rmse[1:] = result[1, :]
corr[1:] = result[2, :]
std_s[0] = std_o

sm.taylor_diagram(std_s, rmse, corr, markers = MARKERS,
                  titleRMS = 'off', markerLegend = 'on',
                  colRMS = 'grey', colSTD = 'k', colCOR = 'k',
                  styleRMS = ':', styleSTD = '-', styleCOR = '--',
                  widthRMS = 2.0, widthSTD = 1.0, widthCOR = 1.0,
                  tickRMS = range(0,50,10), tickSTD = range(0,50,10), 
                  tickRMSangle = 150, axismax = 45.0,
                  styleOBS = '-', colOBS = 'm', markerobs = 'o',
                  )

# plt.title("(b) Sensible Heat Flux", fontsize=18, pad=25, loc='left')
plt.savefig('/stu01/baif/job/test/3_sh_tylor.jpg', format='jpg', dpi=300, bbox_inches='tight')
input_file  = '/stu01/baif/job/test/3_sh_tylor.jpg'
output_file = '/stu01/baif/job/test/3_sh_tylor.jpg'
subprocess.run(['convert', input_file, '-trim', output_file])