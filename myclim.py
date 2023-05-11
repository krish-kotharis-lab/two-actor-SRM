import random
import xarray as xr
import numpy as np
import sys
#
#-----------------------------------------------------
#--routine to initialise the AOD response to emissions
#-----------------------------------------------------
def initialise_aod_responses():
   #--data
   dirin="/thredds/tgcc/store/oboucher/S3A/"
   #--experiments 
   exps=['eq','15S','15N','30S','30N']
   #--pulse injection 
   nbmthinyr=12 #--number of months in yr
   #
   #--reference experiment
   exp='ref'
   file=dirin+'LMDZOR-S3A-'+exp+'_19950101_20041231_1M_od550_STRAT.nc'
   xrfile=xr.open_dataset(file)
   lons=xrfile.lon
   lats=xrfile.lat
   #--select SH and NH latitudes
   lats_nh=lats[np.where(lats>=0.0)]
   lats_sh=lats[np.where(lats<=0.0)]
   #--length of pulse experiment (in yr)
   nbyr_irf=len(xrfile.time_counter)//nbmthinyr
   #--select and hemispherically-average AOD for ref experiment
   aod_ref_strat_sh=np.average(xrfile.sel(lat=lats_sh)['od550_STRAT'].values,axis=(1,2))
   aod_ref_strat_nh=np.average(xrfile.sel(lat=lats_nh)['od550_STRAT'].values,axis=(1,2))
   #
   #--prepare AOD time series for 10 GtS injection experiments for 1 yr
   aod_strat_sh={}
   aod_strat_nh={}
   for exp in exps: 
      file=dirin+'LMDZOR-S3A-'+exp+'_19950101_20041231_1M_od550_STRAT.nc'
      xrfile=xr.open_dataset(file)
      aod_strat_sh[exp]=np.maximum(0,np.average(xrfile.sel(lat=lats_sh)['od550_STRAT'].values,axis=(1,2))-aod_ref_strat_sh)
      aod_strat_nh[exp]=np.maximum(0,np.average(xrfile.sel(lat=lats_nh)['od550_STRAT'].values,axis=(1,2))-aod_ref_strat_nh)
   #
   #--compute annual means
   for exp in exps: 
      aod_strat_sh[exp]=np.average(aod_strat_sh[exp].reshape((nbyr_irf,nbmthinyr)),axis=1)
      aod_strat_nh[exp]=np.average(aod_strat_nh[exp].reshape((nbyr_irf,nbmthinyr)),axis=1)
   #
   #--return responses
   return aod_strat_sh, aod_strat_nh, nbyr_irf
#
#-----------------------------------------------------------------
#--routine to convolve emissions with IRF to produce SH and NH AOD
#-----------------------------------------------------------------
def emi2aod(emits,aod_strat_sh,aod_strat_nh,nbyr_irf):
    #--GtS injected in pulse experiments
    emi0=10.0    
    #--initialise
    AOD_SH=0.0 ; AOD_NH=0.0
    #--check length of time series of emissions
    yrend=nbyr_irf
    for exp in emits.keys():
       yrend=min(yrend,len(emits[exp])) #--length (in yrs) of past injection time series
    #--loop on experiments
    for exp in emits.keys():
       #--loop on time series, only consider last nbyr years
       for yr,emi in enumerate(emits[exp][-nbyr_irf:]):     
           #--AODs by summing on injection points and years by convolving with IRF
           AOD_SH += aod_strat_sh[exp][yrend-1-yr]*emi/emi0
           AOD_NH += aod_strat_nh[exp][yrend-1-yr]*emi/emi0
    return AOD_SH, AOD_NH
#
#--------------------------------------
#--routine to compute RF from emissions
#--------------------------------------
def emi2rf(emits,aod_strat_sh,aod_strat_nh,nbyr_irf):
    #--Kleinschmitt et al ACP (2018)
    #-- -10 Wm-2 per unit AOD (positive because our AODs are negative)
    aod2rf = 10.0  
    AOD_SH, AOD_NH = emi2aod(emits,aod_strat_sh,aod_strat_nh,nbyr_irf)
    return AOD_SH*aod2rf, AOD_NH*aod2rf
#
#----------------
#--monsoon precip 
#----------------
def Monsoon(AOD_SH,AOD_NH,noise=10):
    #--Roose et al., Climate Dynamics, 2023, https://doi.org/10.1007/s00382-023-06799-3
    #--precip change in % as a function of the interhemispheric difference in AOD
    #--since our AODs are negative, we change the sign
    precip_change=-78.6*(AOD_SH-AOD_NH)-10.6 + random.gauss(0.,1.)*noise
    return precip_change
#
#----------------------
#--simple climate model
#----------------------
def clim(T,T0,f=1.,g=0.,geff=1.,C=7.,C0=100.,lam=1.,gamma=0.7, ndt=10, noise=0.05):
# simple climate model from Eq 1 and 2 in Geoffroy et al 
# https://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00195.1
# T = surface air temperature anomaly in K 
# T0 = ocean temperature anomaly in K
# f = GHG forcing in Wm-2 
# g = applied SRM forcing in Wm-2
# geff = efficacy of SRM forcing 
# lam = lambda = feedback parameter Wm-2K-1
# gamma = heat exchange coefficient in Wm-2K-1
# C = atmosphere/land/upper-ocean heat capacity 
# C0 = deep-ocean heat capacity in W.yr.m-2.K-1
# ndt = number of timesteps in 1 yr
# dt = timestep in yr
# noise = noise in T - needs to put a more realistic climate noise
# also noise is only on Tf, should we put noise on T0f as well ?
#
#--test sign geff 
  if geff<0:
    sys.exit('SRM efficacy geff has to be a positive number')
#--discretize yearly timestep
  dt = 1./float(ndt)
#--initial T and TO
  Ti = T ; T0i = T0
# time loop
  for i in range(ndt):
     Tf  = Ti + dt/C*(f+geff*g-lam*Ti-gamma*(Ti-T0i))
     T0f = T0i + dt/C0*gamma*(Ti-T0i)
     Ti = Tf 
     T0i = T0f
# add noise on final Tf
  Tf = Tf + random.gauss(0.,1.)*noise
  return Tf, T0f
#
#----------------------------
#--simple climate NH/SH model
#----------------------------
def clim_nh_sh(Tnh,Tsh,T0nh,T0sh,f=1.,gnh=0.,gsh=0.,geff=1.,tau_nh_sh=20.,C=7.,C0=100.,lam=1.,gamma=0.7, ndt=10, noise=0.05):
# simple climate model from Eq 1 and 2 in Geoffroy et al 
# https://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00195.1
# Tnh,Tsh = surface air temperature anomaly in K 
# T0nh,T0sh = ocean temperature anomaly in K
# f = global GHG forcing in Wm-2 
# gnh,gsh = applied hemispheric SRM forcing in Wm-2
# geff = efficacy of SRM forcing 
# lam = lambda = feedback parameter Wm-2K-1
# gamma = heat exchange coefficient in Wm-2K-1
# tau_nh_sh = timescale (yrs) of interhemispheric heat transfer
# C = atmosphere/land/upper-ocean heat capacity 
# C0 = deep-ocean heat capacity in W.yr.m-2.K-1
# ndt = number of timesteps in 1 yr
# dt = timestep in yr
# noise = noise in T - needs to put a more realistic climate noise
# also noise is only on Tf, should we put noise on T0f as well ?
#
#--test sign geff 
  if geff<0:
    sys.exit('SRM efficacy geff has to be a positive number')
#--discretize yearly timestep
  dt = 1./float(ndt)
#--initial T and TO
  Ti_nh = Tnh ; T0i_nh = T0nh
  Ti_sh = Tsh ; T0i_sh = T0sh
# time loop
  for i in range(ndt):
     #--nh
     Tf_nh  = Ti_nh + dt/C*(f+geff*gnh-lam*Ti_nh-gamma*(Ti_nh-T0i_nh))
     T0f_nh = T0i_nh + dt/C0*gamma*(Ti_nh-T0i_nh)
     #--sh
     Tf_sh  = Ti_sh + dt/C*(f+geff*gsh-lam*Ti_sh-gamma*(Ti_sh-T0i_sh))
     T0f_sh = T0i_sh + dt/C0*gamma*(Ti_sh-T0i_sh)
     #--reducing inter-hemispheric T gradient
     dT  = Tf_nh - Tf_sh
     dT0 = T0f_nh - T0f_sh
     Tf_nh = Tf_nh - dt/tau_nh_sh * dT
     Tf_sh = Tf_sh + dt/tau_nh_sh * dT
     T0f_nh = T0f_nh - dt/tau_nh_sh * dT0
     T0f_sh = T0f_sh + dt/tau_nh_sh * dT0
     #--preparing for next time substep
     Ti_nh  = Tf_nh 
     T0i_nh = T0f_nh
     Ti_sh  = Tf_sh 
     T0i_sh = T0f_sh
# add noise on final Tf
  #Tnoise = random.gauss(0.,noise)
  #Tf_nh = Tf_nh + Tnoise
  #Tf_sh = Tf_sh + Tnoise
  Tf_nh = Tf_nh + random.gauss(0.,noise)
  Tf_sh = Tf_sh + random.gauss(0.,noise)
  return Tf_nh, Tf_sh, T0f_nh, T0f_sh
#
#-------------------------------
#--simple climate NH/SH model v2
#-------------------------------
def clim_nh_sh_v2(Tnh,Tsh,T0nh,T0sh,emits,aod_strat_sh,aod_strat_nh,nbyr_irf, \
                  f=1.,geff=1.,tau_nh_sh=20.,C=7.,C0=100.,lam=1.,gamma=0.7, ndt=10, noise=0.05):
# simple climate model from Eq 1 and 2 in Geoffroy et al 
# https://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00195.1
# Tnh,Tsh = surface air temperature anomaly in K 
# T0nh,T0sh = ocean temperature anomaly in K
# emits = dictionary of past years of strat aerosol emissions (counted negative)
# aod_strat_sh = IRF to convert emissions into SH AOD
# aod_strat_nh = IRF to convert emissions into NH AOD
# f = global GHG forcing in Wm-2 
# geff = efficacy of SRM forcing 
# lam = lambda = feedback parameter Wm-2K-1
# gamma = heat exchange coefficient in Wm-2K-1
# tau_nh_sh = timescale (yrs) of interhemispheric heat transfer
# C = atmosphere/land/upper-ocean heat capacity 
# C0 = deep-ocean heat capacity in W.yr.m-2.K-1
# ndt = number of timesteps in 1 yr
# dt = timestep in yr
# noise = noise in T - needs to put a more realistic climate noise
# also noise is only on Tf, should we put noise on T0f as well ?
# gnh,gsh = applied hemispheric SRM forcing in Wm-2
#
  gsh,gnh=emi2rf(emits,aod_strat_sh,aod_strat_nh,nbyr_irf)
  #--test sign geff 
  if geff<0:
    sys.exit('SRM efficacy geff has to be a positive number')
  #--discretize yearly timestep
  dt = 1./float(ndt)
  #--initial T and TO
  Ti_nh = Tnh ; T0i_nh = T0nh
  Ti_sh = Tsh ; T0i_sh = T0sh
  # time loop
  for i in range(ndt):
     #--nh
     Tf_nh  = Ti_nh + dt/C*(f+geff*gnh-lam*Ti_nh-gamma*(Ti_nh-T0i_nh))
     T0f_nh = T0i_nh + dt/C0*gamma*(Ti_nh-T0i_nh)
     #--sh
     Tf_sh  = Ti_sh + dt/C*(f+geff*gsh-lam*Ti_sh-gamma*(Ti_sh-T0i_sh))
     T0f_sh = T0i_sh + dt/C0*gamma*(Ti_sh-T0i_sh)
     #--reducing inter-hemispheric T gradient
     dT  = Tf_nh - Tf_sh
     dT0 = T0f_nh - T0f_sh
     Tf_nh = Tf_nh - dt/tau_nh_sh * dT
     Tf_sh = Tf_sh + dt/tau_nh_sh * dT
     T0f_nh = T0f_nh - dt/tau_nh_sh * dT0
     T0f_sh = T0f_sh + dt/tau_nh_sh * dT0
     #--preparing for next time substep
     Ti_nh  = Tf_nh 
     T0i_nh = T0f_nh
     Ti_sh  = Tf_sh 
     T0i_sh = T0f_sh
  # add noise on final Tf
  Tf_nh = Tf_nh + random.gauss(0.,noise)
  Tf_sh = Tf_sh + random.gauss(0.,noise)
  #--return outputs
  return Tf_nh, Tf_sh, T0f_nh, T0f_sh
