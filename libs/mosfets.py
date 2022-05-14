import pandas as pd
import copy

thermal_coeff_rdson = 3500e-6

filename = "./data/mosfetdata.xlsx"
df_fets  = pd.read_excel(filename)

fetlist  = list(df_fets.columns.values)[4:]
units    = dict(df_fets[['parameter','units']].values)
scalefactors = dict(df_fets[['parameter','multiplier']].values)

def fetparams(partnumber):
        return dict(df_fets[['parameter',partnumber]].values)

baseparams   = {partnumber:{parameter:value for parameter,value in fetparams(partnumber).items()} for partnumber in fetlist}
scaledparams = copy.deepcopy(baseparams)

for fet in fetlist:
    for param in scaledparams[fet].keys():
            if units[param] != 'na':
                scaledparams[fet][param]=scalefactors[param]*scaledparams[fet][param] 