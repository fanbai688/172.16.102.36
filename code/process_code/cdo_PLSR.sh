#CRUJRA数据月平均处理
# runs="dlwrf dswrf pre pres spfh tmp ugrd vgrd"
# names="1995 1996 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019"
# for run in ${runs};do
# for name in ${names};do
# cdo monmean /tera06/zhwei/CoLM_Forcing/crujra/${run}/crujra.v2.4.5d.${run}.${name}.365d.noc.nc /tera07/zhwei/For_BaiFan/tmp/${run}_${name}.nc \
# &
# done
# done

# runs="dlwrf dswrf pre pres spfh tmp ugrd vgrd"
# for run in ${runs};do
# cdo mergetime /tera07/zhwei/For_BaiFan/tmp/${run}_*.nc /tera07/zhwei/For_BaiFan/tmp/${run}.nc \
# && cdo settaxis,1995-01-15,12:00:00,1month  /tera07/zhwei/For_BaiFan/tmp/${run}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/CRUJRA/tmp/${run}.nc \
# &
# done


###处理结果时间信息
# runs="CRUJRA ERA5LAND ERA5 JRA55 MSWX WFDE5"
# names="le sh rns mrro"
# for run in ${runs};do
# for name in ${names};do
# cdo settaxis,1995-01-15,12:00:00,1month /tera07/zhwei/For_BaiFan/PLSR/variable/old/${run}/${name}.nc /tera07/zhwei/For_BaiFan/PLSR/variable/tmp/${run}_${name}.nc \
# &&cdo seldate,1995-01-15,2019-12-15 /tera07/zhwei/For_BaiFan/PLSR/variable/tmp/${run}_${name}.nc /tera07/zhwei/For_BaiFan/PLSR/variable/process/${run}_${name}.nc \
# &
# done
# done


###处理驱动时间信息
# runs="CRUJRA ERA5LAND ERA5 JRA55 MSWX WFDE5"
# names="dlwrf dswrf prec pres spfh tmp wind"
# for run in ${runs};do
# for name in ${names};do
# cdo mergetime /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/tmp/${name}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/${name}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/tmp_r/${name}.nc \
# && cdo seldate,1995-01-15,2019-12-15 /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/tmp_r/${name}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}.nc \
# &
# done
# done


#统一插值，缺测（为避免0值出现，多mul一次）
# cdo -remapbil,/tera07/zhwei/For_BaiFan/PLSR/forcing/grid.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}_r.nc \
# cdo -remapnn,/tera07/zhwei/For_BaiFan/PLSR/forcing/grid.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}_r.nc 
# runs="WFDEI"
# # runs="CRUJRA ERA5 JRA55 MSWX WFDE5 WFDEI CRUNCEPV4 CRUNCEPV7 GSWP3 PRINCETON"
# # names="dlwrf dswrf pres prec spfh tmp wind"
# # names="prec"
# for run in ${runs};do
# # cdo -remapnn,/hard/baif/PLSR/forcing/grid_r.nc /hard/baif/PLSR/PREC/${run}.nc /hard/baif/PLSR/PREC/tmp/${run}_r.nc \
# # && cdo ifthenelse -eqc,-1e+36 /hard/baif/PLSR/forcing/grid_r.nc -setmisstoc,-1e+36 /hard/baif/PLSR/PREC/tmp/${run}_r.nc -mul /hard/baif/PLSR/forcing/grid_r.nc /hard/baif/PLSR/PREC/tmp/${run}_r.nc /hard/baif/PLSR/PREC/tmp/${run}_rr.nc \
# # && cdo mul /hard/baif/PLSR/forcing/grid_r.nc /hard/baif/PLSR/PREC/tmp/${run}_rr.nc /hard/baif/PLSR/PREC/process/${run}.nc \
# # &
# cdo -remapnn,/hard/baif/PLSR/forcing/grid_r.nc /hard/baif/PLSR/PREC/${run}.nc /hard/baif/PLSR/PREC/tmp/${run}_r.nc \
# && cdo mul /hard/baif/PLSR/PREC/tmp/${run}_r.nc /hard/baif/PLSR/forcing/grid_r.nc /hard/baif/PLSR/PREC/process_old/${run}.nc \
# &

# done

# runs="CRUJRA ERA5 JRA55 MSWX WFDE5 WFDEI CRUNCEPV4 CRUNCEPV7 GSWP3 PRINCETON"
# for run in ${runs};do
# cdo ifthenelse -eqc,-1e+36 /hard/baif/PLSR/forcing/grid_r.nc -setmisstoc,-1e+36 /hard/baif/PLSR/PREC/process/${run}.nc -mul /hard/baif/PLSR/PREC/process/${run}.nc /hard/baif/PLSR/forcing/grid_r.nc /hard/baif/PLSR/PREC/process_r/${run}.nc \
# &
# done




# ##统一缺测
# runs="CRUJRA ERA5LAND ERA5 JRA55 MSWX WFDE5"
# names="dlwrf dswrf pres prec spfh tmp wind"
# for run in ${runs};do
# for name in ${names};do
# cdo ifthenelse -eqc,-1e+36 /tera07/zhwei/For_BaiFan/PLSR/forcing/grid_r.nc -setmisstoc,-1e+36 /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}_r.nc -mul /tera07/zhwei/For_BaiFan/PLSR/forcing/grid_r.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/${run}/process/${name}_r.nc /tera07/zhwei/For_BaiFan/PLSR/tmp/${run}_${name}.nc \
# && cdo mul /tera07/zhwei/For_BaiFan/PLSR/forcing/grid_r.nc /tera07/zhwei/For_BaiFan/PLSR/tmp/${run}_${name}.nc /tera07/zhwei/For_BaiFan/PLSR/forcing/process/${run}_${name}.nc \
# &
# done
# done





###处理至25年的年平均结果（排除掉了QIAN和PRINCETON，保留包含1995-2010时间段的几个驱动）
runs="CRUJRA ERA5LAND ERA5 JRA55 MSWX WFDE5 CRUNCEPV4 CRUNCEPV7 WFDEI GSWP3"
names="dlwrf dswrf pres prec spfh tmp wind"
# names="le sh rns mrro"
for run in ${runs};do
for name in ${names};do
cdo yearmean /tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/${run}_${name}.nc /tera11/zhwei/students/Baifan/hard/PLSR/forcing/process_all/year/${run}_${name}.nc \
&
done
done



##处理vpd时间信息
# names="CRUJRA ERA5LAND ERA5 JRA55 MSWX WFDE5"

# for name in ${names};do
# cdo settaxis,1995-01-15,12:00:00,1month /hard/baif/PLSR/forcing/process/${name}_vpd.nc /hard/baif/PLSR/forcing/process/vpd/${name}_vpd.nc \
# &&cdo yearmean /hard/baif/PLSR/forcing/process/vpd/${name}_vpd.nc /hard/baif/PLSR/forcing/process/year/${name}_vpd.nc \
# &
# done

