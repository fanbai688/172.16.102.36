###写入驱动间处理结果 std_mean, mean_mean
import numpy as np
from os.path import join
from netCDF4 import Dataset
from joblib import Parallel, delayed

names = ["dlwrf", "dswrf", "prec", "spfh", "tmp", "pres", "wind"]

def process_task(i):
    variables = np.zeros([10, 16, 600, 1440], dtype=np.double)

    varible_1 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/CRUJRA_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_2 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/ERA5_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_3 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/ERA5LAND_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_4 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/MSWX_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_5 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/JRA55_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_6 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/WFDE5_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_7 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/WFDEI_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_8 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/CRUNCEPV7_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_9 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/GSWP3_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
    varible_10 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/CRUNCEPV4_{names[i]}.nc", 'r')['le'][0:16,120:720,:]

    varible = [varible_1, varible_2, varible_3, varible_4, varible_5, varible_6, varible_7, varible_8, varible_9, varible_10]
    for j in range(10):
        variables[j, :, :, :] = varible[j][:,:,:]
    variables = np.where(np.isclose(variables, -1e+36), np.nan, variables)

    xstd  = np.nanstd(variables, axis=0)
    std_mean  = np.nanstd(xstd,axis=0)
    std_mean[np.isnan(std_mean)] = -1e+36

    std_mean_file = f'/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/inter/std_mean/{names[i]}.nc'
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

Parallel(n_jobs=7)(delayed(process_task)(i) for i in range(7))
        
        





##写入数据间25年每年的std，更新图一的线图，尽可能保证所有数据的完备
# import numpy as np
# from netCDF4 import Dataset
# import xarray as xr

# names = ["dlwrf", "dswrf", "prec", "spfh", "tmp", "pres", "wind"]
# for i in range(7):
#     variables = np.zeros([10, 16, 600, 1440], dtype=np.double)

#     varible_1 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/CRUJRA_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_2 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/ERA5_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_3 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/ERA5LAND_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_4 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/MSWX_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_5 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/JRA55_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_6 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/WFDE5_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_7 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/WFDEI_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_8 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/CRUNCEPV7_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_9 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/GSWP3_{names[i]}.nc", 'r')['le'][0:16,120:720,:]
#     varible_10 = Dataset(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/CRUNCEPV4_{names[i]}.nc", 'r')['le'][0:16,120:720,:]

#     #存在数据的转存，属性没有读取，所以处理缺测麻烦一点
#     varible = [varible_1, varible_2, varible_3, varible_4, varible_5, varible_6, varible_7, varible_8, varible_9, varible_10]
#     for j in range(10):
#         variables[j, :, :, :] = varible[j][:,:,:]
#     variables = np.where(np.isclose(variables, -1e+36), np.nan, variables)

#     if names[i] == "prec":
#         variables *= 365
    
#     xstd  = np.nanstd(variables, axis=0)
#     xstd[np.isnan(xstd)] = -1e+36
#     xstd = np.where(np.isclose(xstd, -1e+36), np.nan, xstd)
#     ###

#     ds = xr.Dataset()

#     time = np.arange(0,16,1)
#     lat = np.arange(-60, 90, 0.25)
#     lon = np.arange(-180, 180, 0.25)

#     ds['time'] = time
#     ds['lat'] = lat
#     ds['lon'] = lon
#     ds['variable'] = xr.DataArray(xstd, dims=('time', 'lat', 'lon'))

#     ds['variable'].attrs['standard_name'] = ' '
#     ds['variable'].attrs['long_name'] = 'xstd'
#     ds['variable'].attrs['units'] = ' '
#     ds['lat'].attrs['units'] = 'degrees_north'
#     ds['lat'].attrs['long_name'] = 'latitude'
#     ds['lon'].attrs['units'] = 'degrees_east'
#     ds['lon'].attrs['long_name'] = 'longitude'
#     ds['time'].attrs['units'] = ' '
#     ds['time'].attrs['long_name'] = ' '

#     ds.to_netcdf(f"/tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/inter/std/{names[i]}.nc", format='NETCDF4')
#     print("写入")

