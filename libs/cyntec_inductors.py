import pandas as pd
import numpy as np
import copy

thermal_coeff_rdson = 3500e-6

filename = "inductor_data.xlsx"
df_inductors  = pd.read_excel(filename)

inductorlist  = list(df_inductors.columns.values)[4:]
units    = dict(df_inductors[['parameter','units']].values)
scalefactors = dict(df_inductors[['parameter','multiplier']].values)

def inductorparams(partnumber):
    return dict(df_inductors[['parameter',partnumber]].values)

baseparams   = {partnumber:{parameter:value for parameter,value in inductorparams(partnumber).items()} for partnumber in inductorlist}
scaledparams = copy.deepcopy(baseparams)

for inductor in inductorlist:
    for param in scaledparams[inductor].keys():
            if units[param] != 'na':
                scaledparams[inductor][param]=scalefactors[param]*scaledparams[inductor][param] 

def pdis(partnumber,fs,iripple,idc):
    dcr_nom = scaledparams[partnumber]['rdc_nom']
    k1 = scaledparams[partnumber]['k1']
    k2 = scaledparams[partnumber]['k2']
    k3 = scaledparams[partnumber]['k3']
    k4 = scaledparams[partnumber]['k4']
    pdcr  = idc**2*dcr_nom
    pcore = k1*fs**k2*(iripple*k3)**k4
    return {'dcr'  : np.round(pdcr,3),
            'core' : np.round(pcore,3),
            'total': np.round(pdcr+pcore,3)}