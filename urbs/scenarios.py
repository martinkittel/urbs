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
    
    # change maximum installable capacity of PV in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'cap-up'] = np.inf
    
    # change maximum installable capacity of transmission lines
    tra = data['transmission']
    tra.loc[(2030, 'Tennant Creek', 'Darwin', 'DC_OHL', 'Elec'), 'cap-up'] = np.inf
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'cap-up'] = np.inf
    
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
     
def scenario_2030_lifetime_20years(data):
    data = scenario_2030_base(data)
    # change lifetime of PV
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'depreciation'] = 20
    return data
    
def scenario_2030_imports_00pc(data):
    data = scenario_2030_base(data)
    # change minimum share of imports
    prop = data['global_prop']
    prop.loc[(2030, 'Share of imports'), 'value'] = 0
    return data
    
def scenario_2030_imports_10pc(data):
    data = scenario_2030_base(data)
    # change minimum share of imports
    prop = data['global_prop']
    prop.loc[(2030, 'Share of imports'), 'value'] = 0.1
    return data
    
def scenario_2030_imports_30pc(data):
    data = scenario_2030_base(data)
    # change minimum share of imports
    prop = data['global_prop']
    prop.loc[(2030, 'Share of imports'), 'value'] = 0.3
    return data
    
def scenario_2030_imports_40pc(data):
    data = scenario_2030_base(data)
    # change minimum share of imports
    prop = data['global_prop']
    prop.loc[(2030, 'Share of imports'), 'value'] = 0.4
    return data
    
def scenario_2030_solar_eff_050pc(data):
    data = scenario_2030_base(data)
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = 0.5
    return data

def scenario_2030_solar_eff_065pc(data):
    data = scenario_2030_base(data)
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = 0.65
    return data
    
def scenario_2030_solar_eff_070pc(data):
    data = scenario_2030_base(data)
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = 0.7
    return data
    
def scenario_2030_solar_eff_080pc(data):
    data = scenario_2030_base(data)
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = 0.8
    return data
    
def scenario_2030_solar_eff_085pc(data):
    data = scenario_2030_base(data)
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = 0.85
    return data
    
def scenario_2030_solar_eff_100pc(data):
    data = scenario_2030_base(data)
    # change efficiency of solar system in Australia
    pro = data['process']
    pro.loc[(2030, 'Tennant Creek', 'Solar_PV'), 'reliability'] = 1
    return data


def scenario_2030_cable_0000km(data):
    data = scenario_2030_base(data)
    # change length of cable
    cab = 0
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = 0
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 0
    return data
    
    
def scenario_2030_cable_1000km(data):
    data = scenario_2030_base(data)
    # change length of cable
    cab = 1000
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    return data
    
def scenario_2030_cable_2000km(data):
    data = scenario_2030_base(data)
    # change length of cable
    cab = 2000
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    return data

def scenario_2030_cable_3000km(data):
    data = scenario_2030_base(data)
    # change length of cable
    cab = 3000
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    return data

def scenario_2030_cable_4000km(data):
    data = scenario_2030_base(data)
    # change length of cable
    cab = 4000
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    return data
    
def scenario_2030_cable_5000km(data):
    data = scenario_2030_base(data)
    # change length of cable
    cab = 5000
    tra = data['transmission']
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'eff'] = 0.95**(cab/1000)
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'inv-cost'] = (160000 + 1152 * cab) * 1.1
    tra.loc[(2030, 'Darwin', 'Singapore', 'DC_CAB', 'Elec'), 'fix-cost'] = 21 * cab * 1.1
    return data

def scenario_stock_prices(data):
    # change stock commodity prices
    co = data['commodity']
    stock_commodities_only = (co.index.get_level_values('Type') == 'Stock')
    co.loc[stock_commodities_only, 'price'] *= 1.5
    return data


def scenario_co2_limit(data):
    # change global CO2 limit
    global_prop = data['global_prop']
    for stf in global_prop.index.levels[0].tolist():
        global_prop.loc[(stf, 'CO2 limit'), 'value'] *= 0.05
    return data


def scenario_co2_tax_mid(data):
    # change CO2 price in Mid
    co = data['commodity']
    for stf in data['global_prop'].index.levels[0].tolist():
        co.loc[(stf, 'Mid', 'CO2', 'Env'), 'price'] = 50
    return data


def scenario_north_process_caps(data):
    # change maximum installable capacity
    pro = data['process']
    for stf in data['global_prop'].index.levels[0].tolist():
        pro.loc[(stf, 'North', 'Hydro plant'), 'cap-up'] *= 0.5
        pro.loc[(stf, 'North', 'Biomass plant'), 'cap-up'] *= 0.25
    return data


def scenario_no_dsm(data):
    # empty the DSM dataframe completely
    data['dsm'] = pd.DataFrame()
    return data


def scenario_all_together(data):
    # combine all other scenarios
    data = scenario_stock_prices(data)
    data = scenario_co2_limit(data)
    data = scenario_north_process_caps(data)
    return data
