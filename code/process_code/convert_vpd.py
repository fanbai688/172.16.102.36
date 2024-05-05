# import numpy as np
# import xarray as xr
# import math
# import sys

# varible_1 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/spfh.nc", decode_times=False)['le'][:, :, :].values
# varible_2 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/tmp.nc", decode_times=False)['le'][:, :, :].values
# varible_3 = xr.open_dataset("/hard/baif/PLSR/forcing/process/mean/pres.nc", decode_times=False)['le'][:, :, :].values

# ###计算vpd， 单位: hPa
# q = varible_1
# tas = varible_2 - 273.15
# p = varible_3/100
# es = 6.112 * np.exp((17.67 * tas)/(tas + 243.5))
# e  = q * p / (0.378 * q + 0.622)
# rh =  e / es
# rh =  np.where(rh <= 1.0, rh, 1.0)
# rh =  np.where(rh > 0.0,  rh, 0.1)
# vpd = es * (1-rh)

# vpd = np.where(np.isclose(vpd, 9.96921e+36), np.nan, vpd)
# vpd[np.isnan(vpd)] = -1e+36

# ###写入vpd文件
# ds = xr.Dataset()
# time = np.arange(0,300,1)
# lat = np.arange(-89.875, 90.125, 0.25)
# lon = np.arange(-179.875, 180.125, 0.25)

# ds['time'] = time
# ds['lat'] = lat
# ds['lon'] = lon
# ds['variable'] = xr.DataArray(vpd, dims=('time', 'lat', 'lon'), attrs={'_FillValue': -1e+36})

# ds['variable'].attrs['standard_name'] = ' '
# ds['variable'].attrs['long_name'] = 'le'
# ds['variable'].attrs['units'] = ' '
# ds['lat'].attrs['units'] = 'degrees_north'
# ds['lat'].attrs['long_name'] = 'latitude'
# ds['lon'].attrs['units'] = 'degrees_east'
# ds['lon'].attrs['long_name'] = 'longitude'
# ds['time'].attrs['units'] = ' '
# ds['time'].attrs['long_name'] = ' '

# ds.to_netcdf('/hard/baif/PLSR/forcing/process/mean/vpd.nc', format='NETCDF4')
# print("写入vpd文件完成")






# import numpy as np
# import xarray as xr
# import math
# import sys

# varible_1 = xr.open_dataset("/hard/baif/PLSR/forcing/process/MSWX_spfh.nc", decode_times=False)['le'][:, :, :].values
# varible_2 = xr.open_dataset("/hard/baif/PLSR/forcing/process/MSWX_tmp.nc", decode_times=False)['le'][:, :, :].values
# varible_3 = xr.open_dataset("/hard/baif/PLSR/forcing/process/MSWX_pres.nc", decode_times=False)['le'][:, :, :].values

# ###计算vpd
# q = varible_1
# tas = varible_2 - 273.15
# p = varible_3/100
# es = 6.112 * np.exp((17.67 * tas)/(tas + 243.5))
# e  = q * p / (0.378 * q + 0.622)
# rh =  e / es
# rh =  np.where(rh <= 1.0, rh, 1.0)
# rh =  np.where(rh > 0.0,  rh, 0.1)
# vpd = es * (1-rh)

# vpd = np.where(np.isclose(vpd, 9.96921e+36), np.nan, vpd)
# vpd[np.isnan(vpd)] = -1e+36

# ###写入vpd文件
# ds = xr.Dataset()
# time = np.arange(0,300,1)
# lat = np.arange(-89.875, 90.125, 0.25)
# lon = np.arange(-179.875, 180.125, 0.25)

# ds['time'] = time
# ds['lat'] = lat
# ds['lon'] = lon
# ds['variable'] = xr.DataArray(vpd, dims=('time', 'lat', 'lon'), attrs={'_FillValue': -1e+36})

# ds['variable'].attrs['standard_name'] = ' '
# ds['variable'].attrs['long_name'] = 'le'
# ds['variable'].attrs['units'] = ' '
# ds['lat'].attrs['units'] = 'degrees_north'
# ds['lat'].attrs['long_name'] = 'latitude'
# ds['lon'].attrs['units'] = 'degrees_east'
# ds['lon'].attrs['long_name'] = 'longitude'
# ds['time'].attrs['units'] = ' '
# ds['time'].attrs['long_name'] = ' '

# ds.to_netcdf('/hard/baif/PLSR/forcing/process/MSWX_vpd.nc', format='NETCDF4')
# print("写入vpd文件完成")