import numpy as np
import xarray as xr
import math
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import TimeSeriesSplit
import concurrent.futures
from scipy.stats import t
import sys


###处理 X与Y 数组
#读取数据 300*720*1440
variables = np.zeros([300, 4, 600, 1440], dtype=np.double)
Y = xr.open_dataset("/hard/baif/PLSR/variable/process/mean/le.nc", decode_times=False)['le'][:, 120:720, :]

varible_1 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/dlwrf.nc", decode_times=False)['le'][:, 120:720, :]
varible_2 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/dswrf.nc", decode_times=False)['le'][:, 120:720, :]
varible_3 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/prec.nc", decode_times=False)['le'][:, 120:720, :]
varible_4 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/vpd.nc", decode_times=False)['variable'][:, 120:720, :]

varible = [varible_1, varible_2, varible_3, varible_4]
for i in range(4):
    variables[:, i, :, :] = varible[i][:, :, :]
print("读取X,Y数组完毕")

# 标准化数据
xmean = np.mean(variables, axis=0)
xstd = np.std(variables, axis=0)
xstand = (variables - xmean) / xstd
ymean = np.mean(Y, axis=0)
ystd = np.std(Y, axis=0)
ystand = (Y - ymean) / ystd
print("标准化完毕")

###处理std_mean数组
# 读取数据 600*1440
std_all = np.zeros([4, 600, 1440], dtype=np.double)
std_1 = xr.open_dataset("/hard/baif/PLSR/forcing/process/inter/std_mean/dlwrf.nc", decode_times=False)['std_mean'][:, :]
std_2 = xr.open_dataset("/hard/baif/PLSR/forcing/process/inter/std_mean/dswrf.nc", decode_times=False)['std_mean'][:, :]
std_3 = xr.open_dataset("/hard/baif/PLSR/forcing/process/inter/std_mean/prec.nc", decode_times=False)['std_mean'][:, :]
std_4 = xr.open_dataset("/hard/baif/PLSR/forcing/process/inter/std_mean/vpd.nc", decode_times=False)['std_mean'][:, :]

std = [std_1, std_2, std_3, std_4]
for i in range(4):
    std_all[i, :, :] = std[i][:, :]
print("读取std_all完毕")

###PLSR预设变量
best_n_components_values = np.zeros([600, 1440], dtype=np.double)
tscv = TimeSeriesSplit(n_splits=5)

###计算component
def compute_best_components(lat1, lon1):
    x = xstand[:, :, lat1, lon1]
    y = ystand[:, lat1, lon1]
    if np.isnan(x).any() or np.isnan(y).any():
        return lat1, lon1, np.nan

    scores = []
    for n in range(1, 5):
        pls = PLSRegression(n_components=n, scale=False, max_iter=500)
        score = cross_val_score(pls, x, y, cv=tscv)
        scores.append(score.mean())  # 记录平均分数

    best_n_components = np.argmax(scores) + 1  # 找到最好的主成分数量
    return lat1, lon1, best_n_components

###计算plsr
def compute_plsr(lat1, lon1, n_component):
    plsModel = PLSRegression(n_components=n_component, scale=False)
    x = xstand[:, :, lat1, lon1]
    y = ystand[:, lat1, lon1]
    if np.isnan(x).any() or np.isnan(y).any():
        return lat1, lon1, np.nan, np.nan, np.nan, np.nan

    plsModel.fit(x, y)
    coef = plsModel.coef_.T
    intercept = plsModel.intercept_.T
    residuals = y - plsModel.predict(x)
    mse = np.mean(residuals ** 2)
    coef_std_err = np.sqrt(mse / len(y))
    df = len(y) - 1
    t_vals = np.ravel(coef) / np.ravel(coef_std_err)
    p_vals = 2 * (1 - t.cdf(np.abs(t_vals), df))

    r_squared = plsModel.score(x, y)

    return lat1, lon1, coef.ravel(), intercept.ravel(), p_vals, r_squared



###设定component并行
batch_size_1 = 1000
# 生成分批任务
batches_1 = [(lat1, lon1) for lat1 in range(600) for lon1 in range(1440)]

with concurrent.futures.ProcessPoolExecutor() as executor:
    for batch_start in range(0, len(batches_1), batch_size_1):
        batch_end = batch_start + batch_size_1
        current_batch = batches_1[batch_start:batch_end]

        futures = [executor.submit(compute_best_components, *args)
                   for args in current_batch]

        for future in concurrent.futures.as_completed(futures):
            lat1, lon1, best_n_components = future.result()
            best_n_components_values[lat1, lon1] = best_n_components
            print(f"Finished processing lat {lat1}, lon {lon1}: best_n_components is {best_n_components}.")

###设定plsr并行
components        = best_n_components_values.astype(int)
coef_values       = np.zeros([4, 600, 1440], dtype=np.double)
intercept_values  = np.zeros([4, 600, 1440], dtype=np.double)
p_values          = np.zeros([4, 600, 1440], dtype=np.double)
r_squared_values  = np.zeros([600, 1440], dtype=np.double)

print("执行并行")


# 设置每个批次的任务数量
batch_size_2 = 1000
# 生成分批任务
batches_2 = [(lat1, lon1, components[lat1, lon1])
           for lat1 in range(600) for lon1 in range(1440)]

with concurrent.futures.ProcessPoolExecutor() as executor:
    for batch_start in range(0, len(batches_2), batch_size_2):
        batch_end = batch_start + batch_size_2
        current_batch = batches_2[batch_start:batch_end]

        plsr_futures = [executor.submit(compute_plsr, *args)
                        for args in current_batch]

        for plsr_future in concurrent.futures.as_completed(plsr_futures):
            lat1, lon1, coef, intercept, p_vals, r_squared = plsr_future.result()
            coef_values[:, lat1, lon1] = coef
            intercept_values[:, lat1, lon1] = intercept
            p_values[:, lat1, lon1] = p_vals
            r_squared_values[lat1, lon1] = r_squared
            print(f"Finished processing lat {lat1}, lon {lon1}")


###求取特定结果
ystd_g = np.tile(ystd.values[np.newaxis, :, :], (4, 1, 1))
# ystd_g      =  ystd.expand_dims(time=np.arange(4), axis=0)

anomaly     =  (coef_values)*(ystd_g)
uncertainty =  (np.abs(coef_values))*(ystd_g)*(std_all)/(xstd)



###写入文件

###写入component文件
ds = xr.Dataset()
lat = np.arange(-60, 90, 0.25)
lon = np.arange(-180, 180, 0.25)

ds['lat'] = lat
ds['lon'] = lon
ds['variable'] = xr.DataArray(best_n_components_values, dims=('lat', 'lon'))

ds['variable'].attrs['standard_name'] = ' '
ds['variable'].attrs['long_name'] = 'components'
ds['variable'].attrs['units'] = ' '
ds['lat'].attrs['units'] = 'degrees_north'
ds['lat'].attrs['long_name'] = 'latitude'
ds['lon'].attrs['units'] = 'degrees_east'
ds['lon'].attrs['long_name'] = 'longitude'

ds.to_netcdf('/stu01/baif/test/test9/le/component.nc', format='NETCDF4')
print("写入component")


###写入coef文件
ds = xr.Dataset()
lat = np.arange(-60, 90, 0.25)
lon = np.arange(-180, 180, 0.25)
forcing = np.arange(1,5,1)

ds['lat'] = lat
ds['lon'] = lon
ds['forcing'] = forcing
ds['variable'] = xr.DataArray(coef_values, dims=('forcing', 'lat', 'lon'))

ds['variable'].attrs['standard_name'] = ' '
ds['variable'].attrs['long_name'] = 'coef'
ds['variable'].attrs['units'] = ' '
ds['lat'].attrs['units'] = 'degrees_north'
ds['lat'].attrs['long_name'] = 'latitude'
ds['lon'].attrs['units'] = 'degrees_east'
ds['lon'].attrs['long_name'] = 'longitude'
ds['forcing'].attrs['units'] = ' '
ds['forcing'].attrs['long_name'] = ' '

ds.to_netcdf('/stu01/baif/test/test9/le/coef.nc', format='NETCDF4')
print("写入coef")


###写入anomaly检验文件
ds = xr.Dataset()
lat = np.arange(-60, 90, 0.25)
lon = np.arange(-180, 180, 0.25)
forcing = np.arange(1,5,1)

ds['lat'] = lat
ds['lon'] = lon
ds['forcing'] = forcing
ds['variable'] = xr.DataArray(anomaly, dims=('forcing', 'lat', 'lon'))

ds['variable'].attrs['standard_name'] = ' '
ds['variable'].attrs['long_name'] = 'anomaly'
ds['variable'].attrs['units'] = ' '
ds['lat'].attrs['units'] = 'degrees_north'
ds['lat'].attrs['long_name'] = 'latitude'
ds['lon'].attrs['units'] = 'degrees_east'
ds['lon'].attrs['long_name'] = 'longitude'
ds['forcing'].attrs['units'] = ' '
ds['forcing'].attrs['long_name'] = ' '

ds.to_netcdf('/stu01/baif/test/test9/le/anomaly.nc', format='NETCDF4')
print("写入anomaly")


###写入uncertainty检验文件
ds = xr.Dataset()
lat = np.arange(-60, 90, 0.25)
lon = np.arange(-180, 180, 0.25)
forcing = np.arange(1,5,1)

ds['lat'] = lat
ds['lon'] = lon
ds['forcing'] = forcing
ds['variable'] = xr.DataArray(uncertainty, dims=('forcing', 'lat', 'lon'))

ds['variable'].attrs['standard_name'] = ' '
ds['variable'].attrs['long_name'] = 'uncertainty'
ds['variable'].attrs['units'] = ' '
ds['lat'].attrs['units'] = 'degrees_north'
ds['lat'].attrs['long_name'] = 'latitude'
ds['lon'].attrs['units'] = 'degrees_east'
ds['lon'].attrs['long_name'] = 'longitude'
ds['forcing'].attrs['units'] = ' '
ds['forcing'].attrs['long_name'] = ' '

ds.to_netcdf('/stu01/baif/test/test9/le/uncertainty.nc', format='NETCDF4')
print("写入uncertainty")



##写入p检验文件
ds = xr.Dataset()
lat = np.arange(-60, 90, 0.25)
lon = np.arange(-180, 180, 0.25)
forcing = np.arange(1,5,1)

ds['lat'] = lat
ds['lon'] = lon
ds['forcing'] = forcing
ds['variable'] = xr.DataArray(p_values, dims=('forcing', 'lat', 'lon'))

ds['variable'].attrs['standard_name'] = ' '
ds['variable'].attrs['long_name'] = 'p'
ds['variable'].attrs['units'] = ' '
ds['lat'].attrs['units'] = 'degrees_north'
ds['lat'].attrs['long_name'] = 'latitude'
ds['lon'].attrs['units'] = 'degrees_east'
ds['lon'].attrs['long_name'] = 'longitude'
ds['forcing'].attrs['units'] = ' '
ds['forcing'].attrs['long_name'] = ' '

ds.to_netcdf('/stu01/baif/test/test9/le/p.nc', format='NETCDF4')
print("写入p检验")

