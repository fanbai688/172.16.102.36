import netCDF4 as nc
import os
# 1995 2000 2005 2010 2015 2020
input_path  = "/tera07/zhwei/For_BaiFan/cases/extract/WFDE5"
output_path = "/tera07/zhwei/For_BaiFan/cases/extract/runoff"
variables_to_extract = ["f_rnof"]  
for year in range(1995, 2020):    
    for month in range(1, 13):
        input_nc_file = f"{input_path}/Global_IGBP_WFDE5_hist_{year:04d}-{month:02d}.nc"
        output_nc_file = f"{output_path}/Global_IGBP_WFDE5_hist_{year:04d}-{month:02d}.nc"
        with nc.Dataset(output_nc_file, 'w') as output_ds:
            with nc.Dataset(input_nc_file, 'r') as input_ds:
                output_ds.setncatts(input_ds.__dict__)

                output_ds.createDimension('lat')
                output_ds.createDimension('lon')
                output_ds.createDimension('time')

                input_time = input_ds.variables["time"]
                output_time = output_ds.createVariable("time", input_time.dtype, input_time.dimensions)
                output_time[:] = input_time[:]

                input_lat = input_ds.variables["lat"]
                input_lon = input_ds.variables["lon"]
                output_lat = output_ds.createVariable("lat", input_lat.datatype, input_lat.dimensions)
                output_lon = output_ds.createVariable("lon", input_lon.datatype, input_lon.dimensions)
                output_lat[:] = input_lat[:]
                output_lon[:] = input_lon[:]
                                           
                for var_name in variables_to_extract:
                    if var_name in input_ds.variables:
                        input_var = input_ds.variables[var_name]
                        output_var = output_ds.createVariable(var_name, input_var.datatype, input_var.dimensions, fill_value=-1.e+36)  #fill_value=-1.e+36设置了_FillValue的标准格式
                        output_var[:] = input_var[:]
                        for attr_name in input_var.ncattrs():
                            if attr_name != "_FillValue":
                                setattr(output_var, attr_name, getattr(input_var, attr_name))
                    
                    
                for attr_name in input_time.ncattrs():
                    setattr(output_time, attr_name, getattr(input_time, attr_name))
                for attr_name in input_lat.ncattrs():
                    setattr(output_lat, attr_name, getattr(input_lat, attr_name))
                for attr_name in input_lon.ncattrs():
                    setattr(output_lon, attr_name, getattr(input_lon, attr_name))                    

                                           
        print(f"提取完成{year:04d}-{month:02d}")


