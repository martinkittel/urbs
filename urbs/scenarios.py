import pandas as pd
import numpy as np

# SCENARIO GENERATORS
# In this script a variety of scenario generator functions are defined to
# facilitate scenario definitions.


def scenario_2019(data):
    # do nothing
    return data
    
    
def scenario_2030_base(data):
    # change support timeframe
    for sheet in data.keys():
        df = data[sheet]
        df_index = df.index.names
        df.reset_index(inplace=True)
        df['support_timeframe'] = 2030
        try:
            df.set_index(df_index, inplace=True)
        except:
            continue
            
    # change minimum share of imports
    prop = data['global_prop']
    prop.loc[(2030, 'Share of imports'), 'value'] = 0.2
    
    # change maximum installable capacity of PV
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'cap-up'] = np.inf
    pro.loc[(2030, 'Jambi', 'Solar_PV'), 'cap-up'] = np.inf
    
    # change maximum installable capacity of transmission lines
    tra = data['transmission']
    tra.loc[(2030, slice(None), slice(None), slice(None), 'Elec'), 'cap-up'] = np.inf
    
    # change ramping limit
    tra.loc[(2030, slice(None), 'Singapore', 'DC_CAB', 'Elec'), 'ramp-arrival'] /= 1.02**(2030-2019)
    
    # change maximum installable capacity of batteries
    sto = data['storage']
    sto['cap-up-p'] = np.inf
    sto['cap-up-c'] = np.inf

    # increase demand by 2% yearly
    dem = data['demand']
    dem *= 1.02**(2030-2019)
    
    return data
     

def scenario_2030_australia(data):
    data = scenario_2030_base(data)
    
    # Delete Jambi
    data['site'].drop('Jambi', level = 'Name', inplace = True)
    data['commodity'].drop('Jambi', level = 'Site', inplace = True)
    data['process'].drop('Jambi', level = 'Site', inplace = True)
    data['transmission'].drop('Jambi', level = 'Site In', inplace = True)
    data['storage'].drop('Jambi', level = 'Site', inplace = True)
    data['demand'].drop('Jambi', axis = 1, level = 0, inplace = True)
    data['supim'].drop('Jambi', axis = 1, level = 0, inplace = True)
    
    return data
    
    
def scenario_2030_jambi(data):
    data = scenario_2030_base(data)
    
    # Delete Australia
    data['site'].drop(['Darwin', 'Tennant Creek'], level = 'Name', inplace = True)
    data['commodity'].drop(['Darwin', 'Tennant Creek'], level = 'Site', inplace = True)
    data['process'].drop('Tennant Creek', level = 'Site', inplace = True)
    data['transmission'].drop(['Darwin', 'Tennant Creek'], level = 'Site In', inplace = True)
    data['storage'].drop('Darwin', level = 'Site', inplace = True)
    data['demand'].drop(['Darwin', 'Tennant Creek'], axis = 1, level = 0, inplace = True)
    data['supim'].drop('Tennant Creek', axis = 1, level = 0, inplace = True)
        
    return data


class scenario_2030:
    def __init__(self, eff, cab):
        self.eff = eff
        self.cab = cab
        if self.eff >= 0:
            self.newname  = 'scenario_2030_p' + str(eff) + '_cab' + str(cab)
        else:
            self.newname  = 'scenario_2030_m' + str(-eff) + '_cab' + str(cab)
    
    def __getattr__(self, name):
        def customfun(data):
            data = scenario_2030_australia(data)
            
            # change efficiency of solar system in Australia
            pro = data['process']
            pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] *= (1 + self.eff/100)
            
            # change length of cable
            tra = data['transmission']
            tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(self.cab/1000)
            if self.cab == 0:
                tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
            else:
                tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * self.cab) * 1.1
            tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * self.cab * 1.1
            
            return data
            
        customfun.__name__ = self.newname
        #self.customfun.__qualname__ = __class__.__qualname__ + '.' + self.newname
        
        return customfun