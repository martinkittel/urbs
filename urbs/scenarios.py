import pandas as pd
import numpy as np
import inspect

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
    
    # change maximum installable capacity of PV in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'cap-up'] = np.inf
    
    # change maximum installable capacity of transmission lines
    tra = data['transmission']
    tra.loc[(2030, 'Tennant Creek', 'Darwin', 'DC_OHL', 'Elec'), 'cap-up'] = np.inf
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'cap-up'] = np.inf
    
    # change ramping limit
    if tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'ramp-arrival'] != "inf":
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'ramp-arrival'] /= 1.02**(2030-2019)
    
    # change maximum installable capacity of batteries
    sto = data['storage']
    sto['cap-up-p'] = np.inf
    sto['cap-up-c'] = np.inf

    # increase demand by 2% yearly
    dem = data['demand']
    dem *= 1.02**(2030-2019)
    
    # change slack commodity limits in Australia
    co = data['commodity']
    slack_commodities_only = (co.index.get_level_values('Type') == 'Slack')
    co.loc[slack_commodities_only, 'max'] *= 1.02**(2030-2019)
    return data
     
    
def scenario_2030_eff050_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff050_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff050_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff050_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff050_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff050_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff050_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff065_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff065_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff065_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff065_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff065_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff065_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff065_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff070_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff070_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff070_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff070_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff070_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff070_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff070_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff075_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff075_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff075_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff075_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff075_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff075_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff075_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff080_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff080_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff080_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff080_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff080_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff080_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff080_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff085_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff085_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff085_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff085_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff085_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff085_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff085_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff100_cab0000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff100_cab1000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff100_cab2000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data
    

def scenario_2030_eff100_cab3000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff100_cab3800(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff100_cab4000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


def scenario_2030_eff100_cab5000(data):
    data = scenario_2030_base(data)
    fun_name = inspect.currentframe().f_code.co_name
    
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = float(fun_name[-11:-8])/100
    
    # change length of cable
    cab = float(fun_name[-4:])
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    if cab == 0:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    else:
        tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    
    return data


