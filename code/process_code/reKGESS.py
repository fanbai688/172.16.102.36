###fig8
import xarray as xr
import numpy as np
import math
from joblib import Parallel, delayed

names = ["Latent_Heat", "Sensible_Heat", "Surface_Net_Radiation", "Runoff"]
runs = ["Latent_Heat___FLUXCOM", "Sensible_Heat___FLUXCOM", "Surface_Net_Radiation___CERESed4.1", "Runoff___LORA"]
titles = ["le", "sh", "rns", "mrro"]

def process_task(k):

    variables = np.zeros([6, 600, 1440], dtype=np.double)
    varible_1 = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/validation/geo/CRUJRA/{names[k]}/{runs[k]}/output/{titles[k]}_KGESS.nc')['KGESS'][120:720,:]
    varible_2 = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/validation/geo/ERA5/{names[k]}/{runs[k]}/output/{titles[k]}_KGESS.nc')['KGESS'][120:720,:]
    varible_3 = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/validation/geo/ERA5LAND/{names[k]}/{runs[k]}/output/{titles[k]}_KGESS.nc')['KGESS'][120:720,:]
    varible_4 = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/validation/geo/JRA55/{names[k]}/{runs[k]}/output/{titles[k]}_KGESS.nc')['KGESS'][120:720,:]
    varible_5 = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/validation/geo/MSWX/{names[k]}/{runs[k]}/output/{titles[k]}_KGESS.nc')['KGESS'][120:720,:]
    varible_6 = xr.open_dataset(f'/tera11/zhwei/students/Baifan/hard/validation/geo/WFDE5/{names[k]}/{runs[k]}/output/{titles[k]}_KGESS.nc')['KGESS'][120:720,:]

    varible = [varible_1, varible_2, varible_3, varible_4, varible_5, varible_6]
    for i in range(6):
        variables[i, :, :] = varible[i][:,:]
    variables = np.where(np.isclose(variables, 9.96921e+36), np.nan, variables)

    forcing = np.zeros([600, 1440], dtype=np.double)
    for lat1 in range(600):
        for lon1 in range(1440):
            max_abs = -1  
            max_abs_var = float('nan')  
            for var in range(6):
                abs_val = variables[var, lat1, lon1]
                if math.isnan(abs_val):
                    max_abs_var = float('nan')
                elif abs_val > max_abs:
                    max_abs = abs_val
                    max_abs_var = var + 1  
            forcing[lat1, lon1] = max_abs_var
            
    lat = np.linspace(-57.5, 87.5, 30)
    lon = np.linspace(-177.5, 177.5, 72)
    result_grid = np.zeros([30, 72], dtype=np.double)


    for i in range(30):
        for j in range(72):
            subgrid = forcing[i*20:(i+1)*20, j*20:(j+1)*20]
            
            count_non_nan = np.count_nonzero(~np.isnan(subgrid))

            if count_non_nan < 100:
                result_grid[i, j] = np.nan
            else:
                counts = np.bincount(subgrid[~np.isnan(subgrid)].astype(int).ravel())
                if counts.size == 0:
                    max_count = np.nan
                else:
                    max_count = np.argmax(counts)
                result_grid[i, j] = max_count


    lat = np.linspace(-57.5, 87.5, 30)
    lon = np.linspace(-177.5, 177.5, 72)

    # 写入文件
    ds = xr.Dataset()
    ds['lat'] = lat
    ds['lon'] = lon
    ds['variable'] = xr.DataArray(result_grid, dims=('lat', 'lon'))

    ds['variable'].attrs['standard_name'] = ' '
    ds['variable'].attrs['long_name'] = 'best KGESS'
    ds['variable'].attrs['units'] = ' '

    ds['lat'].attrs['units'] = 'degrees_north'
    ds['lat'].attrs['long_name'] = 'latitude'
    ds['lon'].attrs['units'] = 'degrees_east'
    ds['lon'].attrs['long_name'] = 'longitude'

    ds.to_netcdf(f'/stu01/baif/PLSR/code/fig8/{titles[k]}.nc', format='NETCDF4')

    print(f"写入{titles[k]}完毕")


Parallel(n_jobs=4)(delayed(process_task)(k) for k in range(4))







# ###fig7
# import xarray as xr
# import numpy as np
# import math
# import sys

# titles = ["le", "sh", "rns", "mrro"]
# for k in range(4):
#     variables = np.zeros([4, 600, 1440], dtype=np.double)
#     varible_1 = xr.open_dataset(f'/stu01/baif/test/test9/{titles[k]}/anomaly.nc')['variable'][0, :, :]
#     varible_2 = xr.open_dataset(f'/stu01/baif/test/test9/{titles[k]}/anomaly.nc')['variable'][1, :, :]
#     varible_3 = xr.open_dataset(f'/stu01/baif/test/test9/{titles[k]}/anomaly.nc')['variable'][2, :, :]
#     varible_4 = xr.open_dataset(f'/stu01/baif/test/test9/{titles[k]}/anomaly.nc')['variable'][3, :, :]

#     varible = [varible_1, varible_2, varible_3, varible_4]
#     for i in range(4):
#         variables[i, :, :] = varible[i][:,:]
#     variables = np.where(np.isclose(variables, 9.96921e+36), np.nan, variables)
#     variables = np.abs(variables)

#     # print(np.nanmin(variables))

#     forcing = np.zeros([600, 1440], dtype=np.double)
#     for lat1 in range(600):
#         for lon1 in range(1440):
#             max_abs = -1  
#             max_abs_var = float('nan')  
#             for var in range(4):
#                 abs_val = variables[var, lat1, lon1]
#                 if math.isnan(abs_val):
#                     max_abs_var = float('nan')
#                 elif abs_val > max_abs:
#                     max_abs = abs_val
#                     max_abs_var = var + 1  
#             forcing[lat1, lon1] = max_abs_var
            
#     lat = np.linspace(-57.5, 87.5, 30)
#     lon = np.linspace(-177.5, 177.5, 72)
#     result_grid = np.zeros([30, 72], dtype=np.double)

#     # for i in range(30):
#     #     for j in range(72):

#     #         subgrid = forcing[i*20:(i+1)*20, j*20:(j+1)*20]
#     #         counts = np.bincount(subgrid[~np.isnan(subgrid)].astype(int).ravel())
            
#     #         if counts.size == 0:
#     #             max_count = np.nan
#     #         else:
#     #             max_count = np.argmax(counts)
#     #         result_grid[i, j] = max_count

#     for i in range(30):
#         for j in range(72):
#             subgrid = forcing[i*20:(i+1)*20, j*20:(j+1)*20]
            
#             count_non_nan = np.count_nonzero(~np.isnan(subgrid))

#             if count_non_nan < 100:
#                 result_grid[i, j] = np.nan
#             else:
#                 counts = np.bincount(subgrid[~np.isnan(subgrid)].astype(int).ravel())
#                 if counts.size == 0:
#                     max_count = np.nan
#                 else:
#                     max_count = np.argmax(counts)
#                 result_grid[i, j] = max_count


#     lat = np.linspace(-57.5, 87.5, 30)
#     lon = np.linspace(-177.5, 177.5, 72)

#     # 写入文件
#     ds = xr.Dataset()
#     ds['lat'] = lat
#     ds['lon'] = lon
#     ds['variable'] = xr.DataArray(result_grid, dims=('lat', 'lon'))

#     ds['variable'].attrs['standard_name'] = ' '
#     ds['variable'].attrs['long_name'] = 'best KGESS'
#     ds['variable'].attrs['units'] = ' '

#     ds['lat'].attrs['units'] = 'degrees_north'
#     ds['lat'].attrs['long_name'] = 'latitude'
#     ds['lon'].attrs['units'] = 'degrees_east'
#     ds['lon'].attrs['long_name'] = 'longitude'

#     ds.to_netcdf(f'/stu01/baif/PLSR/code/fig13/{titles[k]}.nc', format='NETCDF4')

#     print(f"写入{titles[k]}完毕")