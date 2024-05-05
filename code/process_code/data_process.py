# # ###写入标准差处理结果 std_25year, std_global
# import numpy as np
# from os.path import join
# from netCDF4 import Dataset

# runs = ["CRUJRA", "ERA5", "ERA5LAND", "MSWX", "JRA55", "WFDE5"]
# # names = ["dlwrf", "dswrf", "tmp", "wind", "spfh", "prec", "pres"]
# # runs = ["MSWX"]
# # names = ["dlwrf", "dswrf", "tmp", "wind", "spfh", "prec", "pres"]
# names = ["le", "sh", "rns", "mrro"]
# for run in runs:
#     for name in names:
#         file_path = join("/hard/baif/PLSR/variable/process/year", f"{run}_{name}.nc")
#         variables = Dataset(file_path, 'r')[f"{name}"][:, 120:720, :]

#         std_25year = np.nanstd(variables, axis=0)
#         std_global = np.nanstd(variables, axis=(1, 2))

#         # 写入 std_25year 文件
#         std_25year_file = f'/hard/baif/PLSR/variable/process/std_25year/{run}_{name}.nc'
#         with Dataset(std_25year_file, 'w', format='NETCDF4') as dataset:
#             lat = np.linspace(-59.875, 89.875, 600)
#             lon = np.linspace(-179.875, 179.875, 1440)

#             dataset.createDimension('lat', len(lat))
#             dataset.createDimension('lon', len(lon))

#             variable = dataset.createVariable('std_25year', 'f8', ('lat', 'lon'), fill_value=-1e+36)
#             variable[:, :] = std_25year
#             variable.setncattr('standard_name', ' ')
#             variable.setncattr('long_name', 'std of 25year')
#             variable.setncattr('units', ' ')

#             lat_var = dataset.createVariable('lat', 'f8', ('lat'))
#             lat_var[:] = lat
#             lon_var = dataset.createVariable('lon', 'f8', ('lon'))
#             lon_var[:] = lon
#             lat_var.setncattr('units', 'degrees_north')
#             lat_var.setncattr('long_name', 'latitude')
#             lon_var.setncattr('units', 'degrees_east')
#             lon_var.setncattr('long_name', 'longitude')

#         print(f"写入 {std_25year_file} 文件完毕")

#         # 写入 std_global 文件
#         std_global_file = f'/hard/baif/PLSR/variable/process/std_global/{run}_{name}.nc'
#         with Dataset(std_global_file, 'w', format='NETCDF4') as dataset:
#             year = np.arange(1995, 2020, 1)
#             dataset.createDimension('year', len(year))
#             variable = dataset.createVariable('std_global', 'f8', ('year'), fill_value=-1e+36)
#             variable[:] = std_global
#             variable.setncattr('standard_name', ' ')
#             variable.setncattr('long_name', 'std of global')
#             variable.setncattr('units', ' ')
#             year_var = dataset.createVariable('year', 'f8', ('year'))
#             year_var[:] = year
#             year_var.setncattr('units', 'year')
#             year_var.setncattr('long_name', 'year')

#         print(f"写入 {std_global_file} 文件完毕")

        
        


###写入驱动间处理结果 std_mean, mean_mean
import numpy as np
from os.path import join
from netCDF4 import Dataset

variables = np.zeros([4, 25, 600, 1440], dtype=np.double)

varible_1 = Dataset(join("/hard/baif/PLSR/variable/process/year", "CRUJRA_sh.nc"), 'r')['sh'][:,120:720,:]
varible_2 = Dataset(join("/hard/baif/PLSR/variable/process/year", "ERA5_sh.nc"), 'r')['sh'][:,120:720,:]
varible_3 = Dataset(join("/hard/baif/PLSR/variable/process/year", "ERA5LAND_sh.nc"), 'r')['sh'][:,120:720,:]
varible_4 = Dataset(join("/hard/baif/PLSR/variable/process/year", "MSWX_sh.nc"), 'r')['sh'][:,120:720,:]


#存在数据的转存，属性没有读取，所以处理缺测麻烦一点
varible = [varible_1, varible_2, varible_3, varible_4]
for i in range(4):
    variables[i, :, :, :] = varible[i][:,:,:]
variables = np.where(np.isclose(variables, -1e+36), np.nan, variables)

xmean = np.nanmean(variables,axis=0)
xstd  = np.nanstd(variables, axis=0)
mean_mean = np.nanmean(xmean,axis=0)
std_mean  = np.nanstd(xstd,axis=0)
mean_mean[np.isnan(mean_mean)] = -1e+36
std_mean[np.isnan(std_mean)] = -1e+36

###
mean_mean_file = '/hard/baif/PLSR/variable/process/inter/mean_mean/sh.nc'
with Dataset(mean_mean_file, 'w', format='NETCDF4') as dataset:
    lat = np.linspace(-59.875, 89.875, 600)
    lon = np.linspace(-179.875, 179.875, 1440)

    dataset.createDimension('lat', len(lat))
    dataset.createDimension('lon', len(lon))

    variable = dataset.createVariable('mean_mean', 'f8', ('lat', 'lon'), fill_value=-1e+36)
    variable[:, :] = mean_mean
    variable.setncattr('standard_name', ' ')
    variable.setncattr('long_name', 'mean_mean')
    variable.setncattr('units', ' ')

    lat_var = dataset.createVariable('lat', 'f8', ('lat'))
    lat_var[:] = lat
    lon_var = dataset.createVariable('lon', 'f8', ('lon'))
    lon_var[:] = lon
    lat_var.setncattr('units', 'degrees_north')
    lat_var.setncattr('long_name', 'latitude')
    lon_var.setncattr('units', 'degrees_east')
    lon_var.setncattr('long_name', 'longitude')

print(f"写入 {mean_mean_file} 文件完毕")

###
std_mean_file = '/hard/baif/PLSR/variable/process/inter/std_mean/sh.nc'
with Dataset(std_mean_file, 'w', format='NETCDF4') as dataset:
    
    lat = np.linspace(-59.875, 89.875, 600)
    lon = np.linspace(-179.875, 179.875, 1440)

    dataset.createDimension('lat', len(lat))
    dataset.createDimension('lon', len(lon))
    
    variable = dataset.createVariable('std_mean', 'f8', ('lat', 'lon'), fill_value=-1e+36)
    variable[:, :] = std_mean
    variable.setncattr('standard_name', ' ')
    variable.setncattr('long_name', 'std_mean')
    variable.setncattr('units', ' ')

    lat_var = dataset.createVariable('lat', 'f8', ('lat'))
    lat_var[:] = lat
    lon_var = dataset.createVariable('lon', 'f8', ('lon'))
    lon_var[:] = lon
    lat_var.setncattr('units', 'degrees_north')
    lat_var.setncattr('long_name', 'latitude')
    lon_var.setncattr('units', 'degrees_east')
    lon_var.setncattr('long_name', 'longitude')

print(f"写入 {std_mean_file} 文件完毕")





###写入数据间25年每年的std
import numpy as np
from os.path import join
from netCDF4 import Dataset
import xarray as xr

variables = np.zeros([6, 25, 600, 1440], dtype=np.double)

varible_1 = Dataset(join("/hard/baif/PLSR/variable/process/year", "CRUJRA_le.nc"), 'r')['le'][:,120:720,:]
varible_2 = Dataset(join("/hard/baif/PLSR/variable/process/year", "ERA5_le.nc"), 'r')['le'][:,120:720,:]
varible_3 = Dataset(join("/hard/baif/PLSR/variable/process/year", "ERA5LAND_le.nc"), 'r')['le'][:,120:720,:]
varible_4 = Dataset(join("/hard/baif/PLSR/variable/process/year", "MSWX_le.nc"), 'r')['le'][:,120:720,:]
varible_5 = Dataset(join("/hard/baif/PLSR/variable/process/year", "JRA55_le.nc"), 'r')['le'][:,120:720,:]
varible_6 = Dataset(join("/hard/baif/PLSR/variable/process/year", "WFDE5_le.nc"), 'r')['le'][:,120:720,:]

#存在数据的转存，属性没有读取，所以处理缺测麻烦一点
varible = [varible_1, varible_2, varible_3, varible_4, varible_5, varible_6]
for i in range(6):
    variables[i, :, :, :] = varible[i][:,:,:]
variables = np.where(np.isclose(variables, -1e+36), np.nan, variables)

### mrro转化为mm/year
# variables = variables*365*86400

xstd  = np.nanstd(variables, axis=0)
xstd[np.isnan(xstd)] = -1e+36
xstd = np.where(np.isclose(xstd, -1e+36), np.nan, xstd)
###
ds = xr.Dataset()

time = np.arange(1,26,1)
lat = np.arange(-60, 90, 0.25)
lon = np.arange(-180, 180, 0.25)

ds['time'] = time
ds['lat'] = lat
ds['lon'] = lon
ds['variable'] = xr.DataArray(xstd, dims=('time', 'lat', 'lon'))

ds['variable'].attrs['standard_name'] = ' '
ds['variable'].attrs['long_name'] = 'xstd'
ds['variable'].attrs['units'] = ' '
ds['lat'].attrs['units'] = 'degrees_north'
ds['lat'].attrs['long_name'] = 'latitude'
ds['lon'].attrs['units'] = 'degrees_east'
ds['lon'].attrs['long_name'] = 'longitude'
ds['time'].attrs['units'] = ' '
ds['time'].attrs['long_name'] = ' '

ds.to_netcdf("/hard/baif/PLSR/variable/process/inter/std/le.nc", format='NETCDF4')
print("写入")




# ###读取std_global文件，算不同驱动每个变量的min/max/mean
# import xarray as xr
# import os

# folder_path = '/hard/baif/PLSR/forcing/process/std_global'

# # 模型名称和变量名称列表
# names = ["CRUJRA", "ERA5", "ERA5LAND", "JRA55", "MSWX", "WFDE5"]
# titles = ["prec"]
# # titles = ["dlwrf", "dswrf", "prec", "spfh", "tmp", "pres", "wind"]
# # titles = ["mrro"]
# # 存储结果的字典
# result_dict = {}

# # 遍历所有模型和变量组合
# for name in names:
#     for title in titles:
#         # 构建文件名
#         file_name = f"{name}_{title}.nc"
#         file_path = os.path.join(folder_path, file_name)

#         # 读取NetCDF文件
#         ds = xr.open_dataset(file_path)
#         ds = ds*365
#         min_value = ds.min().std_global.item()
#         max_value = ds.max().std_global.item()
#         mean_value = ds.mean().std_global.item()

#         # 存储结果到字典
#         result_dict[f"{name}_{title}"] = {'min': min_value, 'max': max_value, 'mean': mean_value}

#         # 关闭数据集
#         ds.close()

# # 打印结果
# for key, values in result_dict.items():

#     print(f"{key}: Min={values['min']}, Max={values['max']}, Mean={values['mean']}")




# -----------------------------------------------------------------------------------------
# ###处理MSWX的数据时间维度问题
# import xarray as xr
# import numpy as np

# ### downward_longwave_radiation, downward_shortwave_radiation, precipitation, surface_pressure, specific_humidity, wind_speed, air_temperature
# # 读取原始数据
# ds = xr.open_dataset("/hard/baif/PLSR/forcing/MSWX/process/prec_r.nc", decode_times=False)

# # 保持前60个时间步的数据不变
# first_60_time_steps = ds["precipitation"][0:60, :, :].values

# # 翻转后240个时间步的数据
# last_240_time_steps = ds["precipitation"][60:300, :, :].values
# last_240_time_steps_r = last_240_time_steps[:, ::-1, :]

# variables = np.zeros([300, 720, 1440], dtype=np.double)
# variables[0:60 ,: ,:] = first_60_time_steps
# variables[60:300 ,: ,:] = last_240_time_steps_r

# ###
# ds = xr.Dataset()

# time = np.arange(0, 300, 1)
# lat = np.arange(-89.875, 90, 0.25)
# lon = np.arange(-179.875, 180, 0.25)

# ds['time'] = time
# ds['lat'] = lat
# ds['lon'] = lon
# ds['variable'] = xr.DataArray(variables, dims=('time', 'lat', 'lon'))

# ds['variable'].attrs['standard_name'] = ' '
# ds['variable'].attrs['long_name'] = 'le'
# ds['variable'].attrs['units'] = ' '
# ds['lat'].attrs['units'] = 'degrees_north'
# ds['lat'].attrs['long_name'] = 'latitude'
# ds['lon'].attrs['units'] = 'degrees_east'
# ds['lon'].attrs['long_name'] = 'longitude'
# ds['time'].attrs['units'] = ' '
# ds['time'].attrs['long_name'] = ' '

# ds.to_netcdf("/hard/baif/PLSR/forcing/MSWX/process/1/prec.nc", format='NETCDF4')
# print("写入")