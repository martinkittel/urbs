import os
import shutil
import urbs
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import itertools

global dict_tech
global dict_countries
global dict_season

# User preferences
result_folder = os.path.join("result", "SunCable-20201227T0415")#SunCable-20201212T1056")
scenario_years = [2019, 2030]
stf_min = 2019

def group_technologies(list_tech):
    grouped_tech = {}
    for elem in list_tech:
        if elem == "Shunt":
            grouped_tech[elem] = elem
        elif elem == "Senoko_Energy_ST":
            grouped_tech[elem] = "Oil_ST"
        elif elem.split("_")[-1] in ["PV", "WTE"]:
            grouped_tech[elem] = elem.split("_")[-1]
        else:
            grouped_tech[elem] = "Gas_" + elem.split("_")[-1]
    return grouped_tech

def group_seasons():
    dict_season = {}  
    # Singapore
    for t in range(0, 8761):
        if (t <= 1416) or (t>=5833):
            dict_season[t] = "wet (SIN)"
        else:
            dict_season[t] = "dry (SIN)"
    return dict_season
        
        
def group_sites(list_sites):
    """
    """
    grouped_sites = {}
    for elem in list_sites:
        if (elem not in ["Singapore", "Jambi"]):
            grouped_sites[elem] = "total_AUS"
        elif elem == "Jambi":
            grouped_sites[elem] = "total_IDN"
        else:
            grouped_sites[elem] = "total_SGP"
    return grouped_sites
    
        
def extend_to_year(df):
    # Get column names
    if isinstance(df, pd.DataFrame):
        col_names = df.columns
    elif isinstance(df, pd.Series):
        col_names = [df.name]
    
    # Get new multiindices (for all hours)
    total_list = []
    total_names = []
    for idx_name in df.index.names:
        if idx_name != "t":
            partial_list = list(set([x for x in df.index.get_level_values(level=idx_name)]))
            total_names = total_names + [idx_name]
            total_list = total_list + [partial_list]
    # Add t_new at the end
    total_list = total_list + [[x for x in range(0,8761)]]
    total_names = total_names + ["t_new"]
    
    index_new = pd.MultiIndex.from_product(total_list, names=total_names)
    
    # Prepare dataframe
    df_empty = pd.DataFrame(0, index=index_new, columns=["t"])
    df_empty = df_empty.reset_index().set_index("t_new")
    
    t = df_empty.index
    df_empty.loc[(t <= 1416) | (t>=8017), "t"] = (df_empty.index[(t <= 1416) | (t>=8017)]) # winter
    df_empty.loc[0, "t"] = 0
    df_empty.loc[(t <= 3624) & (t>=1417), "t"] = (df_empty.index[(t <= 3624) & (t>=1417)]) # Spring
    df_empty.loc[(t <= 5832) & (t>=3625), "t"] = (df_empty.index[(t <= 5832) & (t>=3625)])# Summer
    df_empty.loc[(t <= 8016) & (t>=5833), "t"] = (df_empty.index[(t <= 8016) & (t>=5833)]) # Autumn
    
    df_empty = df_empty.reset_index().set_index(df.index.names)
    df_new = df_empty.join(df).dropna(axis=0).reset_index().drop(columns="t").rename(columns={"t_new":"t"})
    df_new = df_new.set_index(df.index.names).sort_index()
    
    return df_new
    
    
def add_weight(df):
    # Get column names
    if isinstance(df, pd.DataFrame):
        col_names = df.columns
    elif isinstance(df, pd.Series):
        col_names = [df.name]
    
    # Prepare dataframe
    index_new = pd.Index(range(0,8761), name="t_new")
    df_empty = pd.DataFrame(0, index=index_new, columns=["t"])
    df_empty = df_empty.reset_index().set_index("t_new")
    
    t = df_empty.index
    df_empty.loc[(t <= 1416) | (t>=8017), "t"] = (df_empty.index[(t <= 1416) | (t>=8017)]) # winter
    df_empty.loc[0, "t"] = 0
    df_empty.loc[(t <= 3624) & (t>=1417), "t"] = (df_empty.index[(t <= 3624) & (t>=1417)]) # Spring
    df_empty.loc[(t <= 5832) & (t>=3625), "t"] = (df_empty.index[(t <= 5832) & (t>=3625)])# Summer
    df_empty.loc[(t <= 8016) & (t>=5833), "t"] = (df_empty.index[(t <= 8016) & (t>=5833)]) # Autumn
    
    weights = df_empty["t"].value_counts().reset_index().rename(columns={"t": "weight"}).rename(columns={"index":"t"})
    weights = weights.set_index("t")
    df_new = df.reset_index().join(weights, on="t")
    for col in col_names:
        df_new[col] = df_new[col] * df_new["weight"]
    df_new = df_new.drop(columns="weight").set_index(df.index.names)
    
    return df_new

   
def get_emissions_data(urbs_results):
    """
    description
    """
    multiindex = pd.MultiIndex.from_product([report_sites, scenario_years], names=["Site", "scenario-year"])
    # Prepare dataframe of emissions
    emissions = pd.DataFrame(index=multiindex, columns=["CO2 emissions (Mt)", "CO2 captured (Mt)"])
    # Prepare dataframe of emissions by fuel
    filter = df_data["process_commodity"].reset_index()
    aux_process = filter.loc[filter["Commodity"]=="CO2", "Process"].tolist()
    pro_com = filter.loc[(filter["Process"].isin(aux_process)) & (filter["Direction"] == "In"), ["Process", "Commodity"]].set_index("Process")["Commodity"].to_dict()
    emissions_by_fuel = pd.DataFrame(0, index=multiindex, columns=list(set(pro_com.values())))
    if "Emissions" in urbs_results.keys():
        urbs_results["Emissions"].set_index(["Site", "scenario-year"], inplace=True)
        urbs_results["Emissions by fuel"].set_index(["Site", "scenario-year"], inplace=True)
        emissions.loc[urbs_results["Emissions"].index.intersection(emissions.index)] = urbs_results["Emissions"].loc[urbs_results["Emissions"].index.intersection(emissions.index)]
        emissions_by_fuel.loc[urbs_results["Emissions by fuel"].index.intersection(emissions_by_fuel.index)] = urbs_results["Emissions by fuel"].loc[urbs_results["Emissions by fuel"].index.intersection(emissions_by_fuel.index)]
    
    co2 = df_result["e_pro_out"].unstack()['CO2'].reorder_levels(['sit', 'stf', 'pro', 't']).sort_index().fillna(0)
    co2 = add_weight(co2)
    co2 = co2.unstack(level=3).sum(axis=1)
    co2 = co2.reset_index().rename(columns={"sit":"Site", "stf": "scenario-year", "pro": "Technology"})
    co2 = co2.groupby(["Site", "scenario-year", "Technology"]).sum()
    co2 = co2.unstack(level=2).droplevel(0, axis=1).fillna(0) / 10**6 # unit: Mt_CO2
    emissions.loc[co2.index, "CO2 emissions (Mt)"] = co2.sum(axis=1)
    
    for pro in pro_com.keys():
        try:
            emissions_by_fuel.loc[co2.index, pro_com[pro]] = emissions_by_fuel.loc[co2.index, pro_com[pro]] + co2[pro]
        except:
            pass
    
    try: # Bio_CCS negative
        co2_neg = df_result["e_pro_in"].unstack()['CO2'].reorder_levels(['sit', 'stf', 'pro', 't']).sort_index().fillna(0)
        co2_neg = add_weight(co2_neg)
        co2_neg = co2_neg.unstack(level=3).sum(axis=1)
        co2_neg = co2_neg.reset_index().rename(columns={"sit":"Site", "stf": "scenario-year", "pro": "Technology"})
        co2_neg["Technology"] = co2_neg["pro"]
        co2_neg = co2_neg.groupby(["Site", "scenario-year", "Technology"]).sum()
        co2_neg = co2_neg.unstack(level=2).droplevel(0, axis=1).fillna(0) / 10**6# unit: t_CO2
        emissions.loc[co2_neg.index, "CO2 emissions (Mt)"] = emissions.loc[co2_neg.index, "CO2 emissions (Mt)"] - co2_neg.sum(axis=1)
    
        for pro in pro_com.keys():
            try:
                emissions_by_fuel.loc[co2.index, pro_com[pro]] = emissions_by_fuel.loc[co2.index, pro_com[pro]] - co2_neg[pro]
            except:
                pass
        print("flag")
    except KeyError:
        pass
    
    co2_regions = co2.reset_index()
    co2_regions["Site"] = [dict_countries[x] for x in co2_regions["Site"]]
    co2_regions = co2_regions.groupby(["Site", "scenario-year"]).sum(axis=0)
    emissions.loc[co2_regions.index, "CO2 emissions (Mt)"] = co2_regions.sum(axis=1)
    
    for pro in pro_com.keys():
        try:
            emissions_by_fuel.loc[co2_regions.index, pro_com[pro]] = emissions_by_fuel.loc[co2_regions.index, pro_com[pro]] + co2_regions[pro]
        except:
            pass
        
    try: # Bio_CCS negative
        co2_neg_regions = co2_neg.reset_index()
        co2_neg_regions["Site"] = [dict_countries[x] for x in co2_neg_regions["Site"]]
        co2_neg_regions = co2_neg_regions.groupby(["Site", "scenario-year"]).sum(axis=0)
        emissions.loc[co2_neg_regions.index.difference(co2_neg.index), "CO2 emissions (Mt)"] = emissions.loc[co2_neg_regions.index.difference(co2_neg.index), "CO2 emissions (Mt)"] - co2_neg_regions.sum(axis=1)
    
        for pro in pro_com.keys():
            try:
                emissions_by_fuel.loc[co2_regions.index, pro_com[pro]] = emissions_by_fuel.loc[co2_regions.index, pro_com[pro]] - co2_neg_regions[pro]
            except:
                pass
    except:
        pass
    
    # CCS_CO2
    emissions.loc[co2.index, "CO2 captured (Mt)"] = 0
    emissions.loc[co2_regions.index, "CO2 captured (Mt)"] = 0
    try:
        ccs_co2 = df_result["e_pro_out"].unstack()['CCS_CO2'].fillna(0)
        ccs_co2 = add_weight(ccs_co2)
        ccs_co2 = ccs_co2.droplevel([0,3]).reorder_levels(['sit', 'stf']).sort_index()
        ccs_co2 = ccs_co2.reset_index().rename(columns={"sit":"Site", "stf": "scenario-year"}).groupby(["Site", "scenario-year"]).sum() # unit: t_CO2
        emissions.loc[ccs_co2.index, "CO2 captured (Mt)"] = ccs_co2["CCS_CO2"]
        
        ccs_co2_regions = ccs_co2.reset_index()
        ccs_co2_regions["Site"] = [dict_countries[x] for x in ccs_co2_regions["Site"]]
        ccs_co2_regions = ccs_co2_regions.groupby(["Site", "scenario-year"]).sum(axis=0)
        emissions.loc[ccs_co2_regions.index, "CO2 captured (Mt)"] = ccs_co2_regions["CCS_CO2"]
    except KeyError:
        pass
            
    # Save results
    emissions.fillna(0, inplace=True)
    emissions_by_fuel.fillna(0, inplace=True)
    
    urbs_results["Emissions"] = emissions.astype("float").round(2).copy()
    urbs_results["Emissions by fuel"] = emissions_by_fuel.round(2).copy()
    # Sort index
    urbs_results["Emissions"] = urbs_results["Emissions"].sort_index(level="scenario-year")
    urbs_results["Emissions by fuel"] = urbs_results["Emissions by fuel"].sort_index(level="scenario-year")
    return urbs_results
    
    
def get_electricity_data(urbs_results, year_built):
    
    # Prepare dataframe of electricity
    multiindex = pd.MultiIndex.from_product([report_sites, scenario_years], names=["Site", "scenario-year"])
    list_cols = ["price-avg"] + ["price-avg-" + season for season in set(dict_season.values())] + ["price-median", "price-max", "price-min", "elec-demand"]
    electricity = pd.DataFrame(index=multiindex, columns=list_cols)
    
    # Prepare dataframe of hourly prices
    multiindex = pd.MultiIndex.from_product([range(1,8761), scenario_years], names=["Hour", "scenario-year"])
    hourly_prices = pd.DataFrame(index=multiindex, columns=report_sites)
    
    if "Electricity" in urbs_results.keys():
        urbs_results["Electricity"].set_index(["Site", "scenario-year"], inplace=True)
        electricity.loc[urbs_results["Electricity"].index.intersection(electricity.index)] = urbs_results["Electricity"]
        urbs_results["Hourly prices"].set_index(["Hour", "scenario-year"], inplace=True)
        hourly_prices.loc[urbs_results["Hourly prices"].index.intersection(hourly_prices.index)] = urbs_results["Hourly prices"][hourly_prices.columns]
    
    # Get cost factor
    if year_built > stf_min:
        discount = 0 #df_data["global_prop"].droplevel(0).loc["Discount rate", "value"]
    else:
        discount = 0
    cost_factor = (1 + discount) ** (stf_min - year_built)
    
    prices = df_result["res_vertex"].xs(('Elec', 'Demand'), level=('com', 'com_type')).reorder_levels(['sit', 'stf', 't']).sort_index()
    prices = extend_to_year(prices)/df_result["weight"][0]
    prices = prices.reset_index().rename(columns={"sit": "Site", "stf": "scenario-year"})
    prices["season"] = [dict_season[x] for x in prices["t"]]
    demand = df_data["demand"].droplevel(1, axis=1).stack().reorder_levels([2, 0, 1])
    demand = demand.reset_index().rename(columns={"level_0": "Site", "support_timeframe": "scenario-year"}).set_index(["Site", "scenario-year", "t"])
    demand = extend_to_year(demand)
    demand = demand.reset_index()
    demand["season"] = [dict_season[x] for x in demand["t"]]
    
    # Averages
    prices_avg = prices[["Site", "scenario-year", "res_vertex"]].groupby(["Site", "scenario-year"]).mean()
    electricity.loc[prices_avg.index, "price-avg"] = prices_avg["res_vertex"] * cost_factor
    for season in set(dict_season.values()):
        prices_avg_season = prices.loc[prices["season"]==season, ["Site", "scenario-year", "res_vertex"]].groupby(["Site", "scenario-year"]).mean()
        electricity.loc[prices_avg_season.index, "price-avg-" + season] = prices_avg_season["res_vertex"] * cost_factor
    # Median
    prices_median = prices[["Site", "scenario-year", "res_vertex"]].groupby(["Site", "scenario-year"]).median()
    electricity.loc[prices_median.index, "price-median"] = prices_median["res_vertex"] * cost_factor
    # Max
    prices_max = prices[["Site", "scenario-year", "res_vertex"]].groupby(["Site", "scenario-year"]).max()
    electricity.loc[prices_max.index, "price-max"] = prices_max["res_vertex"] * cost_factor
    # Min
    prices_min = prices[["Site", "scenario-year", "res_vertex"]].groupby(["Site", "scenario-year"]).min()
    electricity.loc[prices_min.index, "price-min"] = prices_min["res_vertex"] * cost_factor
    # Demand
    demand = demand.loc[demand["Site"]!="Unnamed: 11"]
    dem = demand[["Site", "scenario-year", 0]].groupby(["Site", "scenario-year"]).sum()
    electricity.loc[dem.index, "elec-demand"] = dem[0]
    # Hourly prices
    prices_h = prices.rename(columns={"t":"Hour"}).drop(columns=["season"]).set_index(["Hour", "scenario-year", "Site"]).unstack()["res_vertex"]
    hourly_prices.loc[prices_h.index, prices_h.columns] = prices_h * cost_factor
    
    # Repeat for groups of countries
    prices_weighted = prices.set_index(["Site", "scenario-year", "t"])["res_vertex"]
    prices_weighted = demand.set_index(["Site", "scenario-year", "t"]).loc[prices_weighted.index][0] * prices_weighted
    prices_weighted_regions = prices_weighted.reset_index()
    prices_weighted_regions["Site"] = [dict_countries[x] for x in prices_weighted_regions["Site"]]
    prices_weighted_regions = prices_weighted_regions.groupby(["Site", "scenario-year", "t"]).sum(axis=0)
    
    dem_regions = demand.drop(columns=["season"])
    dem_regions["Site"] = [dict_countries[x] for x in dem_regions["Site"]]
    dem_regions = dem_regions.groupby(["Site", "scenario-year","t"]).sum()
    
    prices_weighted_regions = prices_weighted_regions / dem_regions.loc[prices_weighted_regions.index]
    prices_weighted_regions = prices_weighted_regions.reset_index()
    prices_weighted_regions["season"] = [dict_season[x] for x in prices_weighted_regions["t"]]
    
    # Averages
    prices_weighted_avg = prices_weighted_regions[["Site", "scenario-year", 0]].groupby(["Site", "scenario-year"]).mean()
    electricity.loc[prices_weighted_avg.index, "price-avg"] = prices_weighted_avg[0] * cost_factor
    for season in set(dict_season.values()):
        prices_weighted_season = prices_weighted_regions.loc[prices_weighted_regions["season"]==season, ["Site", "scenario-year", 0]].groupby(["Site", "scenario-year"]).mean()
        electricity.loc[prices_weighted_season.index, "price-avg-" + season] = prices_weighted_season[0] * cost_factor
    # Median
    prices_weighted_median = prices_weighted_regions[["Site", "scenario-year", 0]].groupby(["Site", "scenario-year"]).median()
    electricity.loc[prices_weighted_median.index, "price-median"] = prices_weighted_median[0] * cost_factor
    # Max
    prices_weighted_max = prices_weighted_regions[["Site", "scenario-year", 0]].groupby(["Site", "scenario-year"]).max()
    electricity.loc[prices_weighted_max.index, "price-max"] = prices_weighted_max[0] * cost_factor
    # Min
    prices_weighted_min = prices_weighted_regions[["Site", "scenario-year", 0]].groupby(["Site", "scenario-year"]).min()
    electricity.loc[prices_weighted_min.index, "price-min"] = prices_weighted_min[0] * cost_factor
    # Demand
    dem_regions = dem_regions.unstack().sum(axis=1)
    electricity.loc[dem_regions.index, "elec-demand"] = dem_regions
    # Hourly prices
    prices_h_regions = prices_weighted_regions.rename(columns={"scenario-year":"Year", "t":"Hours"}).drop(columns=["season"]).set_index(["Hours", "Year", "Site"]).unstack()[0]
    hourly_prices.loc[prices_h_regions.index, prices_h_regions.columns] = prices_h_regions * cost_factor
    
    # Save results
    electricity.fillna(0, inplace=True)
    hourly_prices.fillna(0, inplace=True)
    urbs_results["Electricity"] = electricity.astype("float").round(2)
    urbs_results["Hourly prices"] = hourly_prices.round(2)
    # Sort index
    urbs_results["Electricity"] = urbs_results["Electricity"].sort_index(level="scenario-year")
    urbs_results["Hourly prices"] = urbs_results["Hourly prices"].sort_index(level="scenario-year")
    
    return urbs_results
    

def get_generation_data(urbs_results):
    """
    """
    multiindex = pd.MultiIndex.from_product([report_sites, scenario_years], names=["Site", "scenario-year"])
    # Prepare dataframe of generation by power plant type
    filter = df_data["process_commodity"].reset_index()
    aux_process = filter.loc[(filter["Commodity"]=="Elec") & (filter["Direction"] == "Out"), "Process"].tolist()
    dict_tech = group_technologies(aux_process)
    generation = pd.DataFrame(0, index=multiindex, columns=sorted(list(set(dict_tech.values()))))
    if "Electricity generation" in urbs_results.keys():
        urbs_results["Electricity generation"].set_index(["Site", "scenario-year"], inplace=True)
        generation.loc[urbs_results["Electricity generation"].index.intersection(generation.index)] = urbs_results["Electricity generation"]
    
    prod = df_result["e_pro_out"].unstack()['Elec'].reorder_levels(['sit', 'stf', 'pro', 't']).sort_index().fillna(0)
    prod = add_weight(prod)
    prod = prod.fillna(0).unstack(level=3).sum(axis=1)
    prod = prod.reset_index().rename(columns={"sit":"Site", "stf": "scenario-year"})
    prod["Technology"] = prod["pro"]
    for pro in prod["pro"].index:
        prod.loc[pro, "Technology"] = dict_tech[prod.loc[pro, "Technology"]]

    #prod = prod.drop(index= prod.loc[prod["Technology"]=="Slack"].index)
    prod = prod.drop(columns=["pro"]).groupby(["Site", "scenario-year", "Technology"]).sum().unstack()[0].fillna(0)
    generation.loc[prod.index, prod.columns] = prod
    generation.loc[prod.index] = generation.loc[prod.index].fillna(0)
    
    prod_regions = prod.reset_index()
    prod_regions["Site"] = [dict_countries[x] for x in prod_regions["Site"]]
    prod_regions = prod_regions.groupby(["Site", "scenario-year"]).sum(axis=0)
    generation.loc[prod_regions.index, prod_regions.columns] = prod_regions
    generation.loc[prod_regions.index] = generation.loc[prod_regions.index].fillna(0)
    
    # Save results
    generation.fillna(0, inplace=True)
    urbs_results["Electricity generation"] = generation.round(2)
    # Sort index
    urbs_results["Electricity generation"] = urbs_results["Electricity generation"].sort_index(level="scenario-year")
    
    return urbs_results


def get_capacities_data(urbs_results):
    """
    """
    multiindex = pd.MultiIndex.from_product([report_sites, scenario_years], names=["Site", "scenario-year"])
    # Prepare dataframes of power plant capacities
    filter = df_data["process_commodity"].reset_index()
    aux_process = filter.loc[(filter["Commodity"]=="Elec") & (filter["Direction"] == "Out"), "Process"].tolist()
    dict_tech = group_technologies(aux_process)
    capacities_total = pd.DataFrame(index=multiindex, columns=sorted(list(set(dict_tech.values()))))
    capacities_new = pd.DataFrame(index=multiindex, columns=sorted(list(set(dict_tech.values()))))
    capacities_retired = pd.DataFrame(index=multiindex, columns=sorted(list(set(dict_tech.values()))))
    if "Installed capacities" in urbs_results.keys():
        urbs_results["Installed capacities"].set_index(["Site", "scenario-year"], inplace=True)
        urbs_results["Added capacities"].set_index(["Site", "scenario-year"], inplace=True)
        urbs_results["Retired capacities"].set_index(["Site", "scenario-year"], inplace=True)
        capacities_total.loc[urbs_results["Installed capacities"].index.intersection(capacities_total.index)] = urbs_results["Installed capacities"].loc[urbs_results["Installed capacities"].index.intersection(capacities_total.index), capacities_total.columns]
        capacities_new.loc[urbs_results["Added capacities"].index.intersection(capacities_new.index)] = urbs_results["Added capacities"].loc[urbs_results["Added capacities"].index.intersection(capacities_new.index), capacities_new.columns]
        capacities_retired.loc[urbs_results["Retired capacities"].index.intersection(capacities_retired.index)] = urbs_results["Retired capacities"].loc[urbs_results["Retired capacities"].index.intersection(capacities_retired.index), capacities_retired.columns]
    
    # New capacities
    cap_new = df_result["cap_pro_new"].reset_index().rename(columns={"stf": "scenario-year", "sit":"Site", "pro":"Process", "cap_pro_new":"inst-cap"})
    cap_new["Technology"] = cap_new["Process"]
    for pro in cap_new["Process"].index:
        try:
            cap_new.loc[pro, "Technology"] = dict_tech[cap_new.loc[pro, "Technology"]]
        except:
            continue
    cap_new = cap_new.drop(columns=["Process"]).groupby(["Site", "scenario-year", "Technology"]).sum()
    cap_new_regions = cap_new.reset_index()
    cap_new_regions["Site"] = [dict_countries[x] for x in cap_new_regions["Site"]]
    cap_new_regions = cap_new_regions.groupby(["Site", "scenario-year", "Technology"]).sum()
    
    # Total capacity, Retired capacity
    cap_total = df_data["process"][["inst-cap"]].reset_index().rename(columns={"support_timeframe": "scenario-year"})
    cap_total["Technology"] = cap_total["Process"]
    for pro in cap_total["Process"].index:
        try:
            cap_total.loc[pro, "Technology"] = dict_tech[cap_total.loc[pro, "Technology"]]
        except:
            continue
    year_now = cap_total["scenario-year"].unique()[0]
    cap_total = cap_total.drop(columns=["Process"]).groupby(["Site", "scenario-year", "Technology"]).sum()
    cap_retired = - cap_total.copy()
    cap_total = cap_total + cap_new
    cap_total_regions = cap_total.reset_index()
    cap_total_regions["Site"] = [dict_countries[x] for x in cap_total_regions["Site"]]
    cap_total_regions = cap_total_regions.groupby(["Site", "scenario-year", "Technology"]).sum()
    
    # Save results
    cap_new = cap_new.unstack()["inst-cap"].fillna(0)
    capacities_new.loc[cap_new.index, cap_new.columns.intersection(capacities_new.columns)] = cap_new[capacities_new.columns]
    cap_total = cap_total.unstack()["inst-cap"].fillna(0)
    capacities_total.loc[cap_total.index, cap_total.columns.intersection(capacities_total.columns)] = cap_total[capacities_total.columns]
    
    # Repeat for groups of regions
    cap_new_regions = cap_new_regions.unstack()["inst-cap"].fillna(0)
    capacities_new.loc[cap_new_regions.index, cap_new_regions.columns.intersection(capacities_new.columns)] = cap_new_regions[capacities_new.columns]
    cap_total_regions = cap_total_regions.unstack()["inst-cap"].fillna(0)
    capacities_total.loc[cap_total_regions.index, cap_total_regions.columns.intersection(capacities_total.columns)] = cap_total_regions[capacities_total.columns]
    
    # Retired capacity (continued)
    if year_now == stf_min:
        capacities_retired.loc[cap_total.index, :] = 0
        capacities_retired.loc[cap_total_regions.index, :] = 0
    else:
        index_past = pd.MultiIndex.from_product([[*dict_countries], [scenario_years[scenario_years.index(year_now)-1]]], names=["Site", "scenario-year"])
        cap_total_past = capacities_total.loc[index_past].stack().reset_index().rename(columns={"level_2": "Technology", 0:"inst-cap-past"})
        cap_total_past["scenario-year"] = year_now
        cap_total_past = cap_total_past.set_index(["Site", "scenario-year", "Technology"])
        cap_retired = cap_retired.join(cap_total_past).fillna(0)
        cap_retired["inst-cap"] = cap_retired["inst-cap"] + cap_retired["inst-cap-past"]
        cap_retired.loc[abs(cap_retired["inst-cap"])<0.00001, "inst-cap"] = 0

        cap_retired = cap_retired.drop(columns=["inst-cap-past"])
        cap_retired_regions = cap_retired.reset_index()
        cap_retired_regions["Site"] = [dict_countries[x] for x in cap_retired_regions["Site"]]
        cap_retired_regions = cap_retired_regions.groupby(["Site", "scenario-year", "Technology"]).sum()
    
        cap_retired = cap_retired.unstack()["inst-cap"].fillna(0)
        capacities_retired.loc[cap_retired.index, cap_retired.columns.intersection(capacities_retired.columns)] = cap_retired[capacities_retired.columns]
        cap_retired_regions = cap_retired_regions.unstack()["inst-cap"].fillna(0)
        capacities_retired.loc[cap_retired_regions.index, cap_retired_regions.columns.intersection(capacities_retired.columns)] = cap_retired_regions[capacities_retired.columns]
    
    # Save results
    capacities_total.fillna(0, inplace=True)
    capacities_new.fillna(0, inplace=True)
    capacities_retired.fillna(0, inplace=True)
    
    urbs_results["Installed capacities"] = capacities_total.round(2)
    urbs_results["Added capacities"] = capacities_new.round(2)
    urbs_results["Retired capacities"] = capacities_retired.round(2)

    # Sort index
    urbs_results["Installed capacities"] = urbs_results["Installed capacities"].sort_index(level="scenario-year")
    urbs_results["Added capacities"] = urbs_results["Added capacities"].sort_index(level="scenario-year")
    urbs_results["Retired capacities"] = urbs_results["Retired capacities"].sort_index(level="scenario-year")
    
    return urbs_results


def get_storage_data(urbs_results):
    """
    """
    try:
        storage_types = sorted(list(set(df_data["storage"].reset_index()["Storage"])))
    except KeyError:
        return urbs_results
    multiindex = pd.MultiIndex.from_product([report_sites, storage_types, scenario_years], names=["Site", "Storage type", "scenario-year"])
    
    # Prepare dataframe of storage
    storage = pd.DataFrame(0, index=multiindex, columns=["inst-cap-p", "new-inst-cap-p", "retired-cap-p", "inst-cap-c", "new-inst-cap-c", "retired-cap-c", "avg-state-of-charge", "full-load cycles", "stored-energy"])
    
    try:
        # New capacities
        cap_p_new = df_result["cap_sto_p_new"].droplevel(3).reset_index().rename(columns={"stf": "scenario-year", "sit":"Site", "sto":"Storage type", "cap_sto_p_new":"new-inst-cap-p"}).fillna(0)
        cap_p_new = cap_p_new.set_index(["Site", "Storage type", "scenario-year"])
        cap_c_new = df_result["cap_sto_c_new"].droplevel(3).reset_index().rename(columns={"stf": "scenario-year", "sit":"Site", "sto":"Storage type", "cap_sto_c_new":"new-inst-cap-c"}).fillna(0)
        cap_c_new = cap_c_new.set_index(["Site", "Storage type", "scenario-year"])
    except:
        return urbs_results
        
    # Old capacity
    cap_p_old = df_data["storage"][["inst-cap-p"]].droplevel(3).reset_index().rename(columns={"support_timeframe": "scenario-year", "Storage": "Storage type"})
    year_now = cap_p_old["scenario-year"].unique()[0]
    cap_p_old = cap_p_old.set_index(["Site", "Storage type", "scenario-year"])
    cap_c_old = df_data["storage"][["inst-cap-c"]].droplevel(3).reset_index().rename(columns={"support_timeframe": "scenario-year", "Storage": "Storage type"})
    cap_c_old = cap_c_old.set_index(["Site", "Storage type", "scenario-year"])
    
    # Retired capacity
    cap_p_retired = - cap_p_old.rename(columns={"inst-cap-p": "retired-cap-p"})
    cap_c_retired = - cap_c_old.rename(columns={"inst-cap-c": "retired-cap-c"})
    
    storage_cap = cap_p_old.join([cap_c_old, cap_p_new, cap_c_new, cap_p_retired, cap_c_retired])
    storage_cap["inst-cap-p"] = storage_cap["inst-cap-p"] + storage_cap["new-inst-cap-p"]
    storage_cap["inst-cap-c"] = storage_cap["inst-cap-c"] + storage_cap["new-inst-cap-c"]
    
    # Rename storage types
    storage_cap = storage_cap.reset_index()
    for idx in storage_cap.index:
        if storage_cap.loc[idx, "Storage type"].startswith("Storage_"):
            storage_cap.loc[idx, "Storage type"] = storage_cap.loc[idx, "Storage type"][:-5]
    storage_types = storage_cap["Storage type"].unique()
    storage_cap = storage_cap.groupby(["Site", "Storage type", "scenario-year"]).sum()
            
    # Retired capacity (continued)
    if year_now == stf_min:
        storage_cap["retired-cap-p"] = 0
        storage_cap["retired-cap-c"] = 0
    else:
        index_past = pd.MultiIndex.from_product([[*dict_countries], storage_types, [scenario_years[scenario_years.index(year_now)-1]]], names=["Site", "Storage type", "scenario-year"])
        cap_p_past = storage.loc[index_past, "inst-cap-p"].fillna(0).reset_index().rename(columns={"inst-cap-p": "retired-cap-p"})
        cap_c_past = storage.loc[index_past, "inst-cap-c"].fillna(0).reset_index().rename(columns={"inst-cap-c": "retired-cap-c"})
        cap_p_past["scenario-year"] = year_now
        cap_c_past["scenario-year"] = year_now
        cap_p_past = cap_p_past.set_index(["Site", "Storage type", "scenario-year"])
        cap_c_past = cap_c_past.set_index(["Site", "Storage type", "scenario-year"])
        storage_cap["retired-cap-p"] = (storage_cap["retired-cap-p"] + cap_p_past.T.squeeze()).dropna()
        storage_cap["retired-cap-c"] = (storage_cap["retired-cap-c"] + cap_c_past.T.squeeze()).dropna()
        storage_cap = storage_cap.fillna(0)
        
    storage_cap_regions = storage_cap.reset_index()
    storage_cap_regions["Site"] = [dict_countries[x] for x in storage_cap_regions["Site"]]
    storage_cap_regions = storage_cap_regions.groupby(["Site", "Storage type", "scenario-year"]).sum()
        
    storage_con = df_result["e_sto_con"].droplevel([4])
    storage_con = storage_con.reset_index().rename(columns={"stf":"scenario-year", "sit":"Site", "sto": "Storage type", "e_sto_con":"avg-state-of-charge"})
    storage_con_regions = storage_con.copy()
    storage_con_regions["Site"] = [dict_countries[x] for x in storage_con_regions["Site"]]
    storage_con_regions = storage_con_regions.groupby(["Site", "Storage type", "scenario-year", "t"]).sum().droplevel(3).reset_index()
    storage_con = storage_con.groupby(["Site", "Storage type", "scenario-year"]).mean().drop(columns=["t"])
    storage_con_regions = storage_con_regions.groupby(["Site", "Storage type", "scenario-year"]).mean()
    
    # Correct storage type
    storage_con = storage_con.reset_index()
    for idx in storage_con.index:
        if storage_con.loc[idx, "Storage type"].startswith("Storage_"):
            storage_con.loc[idx, "Storage type"] = storage_con.loc[idx, "Storage type"][:-5]
    storage_con = storage_con.set_index(["Site", "Storage type", "scenario-year"])
    storage_con_regions = storage_con_regions.reset_index()
    for idx in storage_con_regions.index:
        if storage_con_regions.loc[idx, "Storage type"].startswith("Storage_"):
            storage_con_regions.loc[idx, "Storage type"] = storage_con_regions.loc[idx, "Storage type"][:-5]
    storage_con_regions = storage_con_regions.set_index(["Site", "Storage type", "scenario-year"])
    
    # SOC in %
    storage_con["avg-state-of-charge"] = storage_con["avg-state-of-charge"]/storage_cap["inst-cap-c"]*100
    storage_con_regions["avg-state-of-charge"] = storage_con_regions["avg-state-of-charge"] / storage_cap_regions["inst-cap-c"] * 100
    
    # Get stored in energy
    storage_in = add_weight(df_result["e_sto_in"]).droplevel([0,4]).reset_index().rename(columns={"stf":"scenario-year", "sit":"Site", "e_sto_in":"stored-energy", "sto": "Storage type"})
    storage_in = storage_in.groupby(["Site", "Storage type", "scenario-year"]).sum()
    
    # Correct storage type
    # storage_in = storage_in.reset_index()
    # for idx in storage_in.index:
        # if storage_in.loc[idx, "Storage type"].startswith("Storage_"):
            # storage_in.loc[idx, "Storage type"] = storage_in.loc[idx, "Storage type"][:-5]
    # storage_in = storage_in.set_index(["Site", "Storage type", "scenario-year"])
    
    storage_in_regions = storage_in.reset_index()
    storage_in_regions["Site"] = [dict_countries[x] for x in storage_in_regions["Site"]]
    storage_in_regions = storage_in_regions.groupby(["Site", "Storage type", "scenario-year"]).sum()
    
    # Save results
    storage.loc[storage_cap.index, storage_cap.columns] = storage_cap.fillna(0)
    storage.loc[storage_cap_regions.index, storage_cap_regions.columns] = storage_cap_regions.fillna(0)
    storage.loc[storage_con.index, storage_con.columns] = storage_con
    storage.loc[storage_con_regions.index, storage_con_regions.columns] = storage_con_regions
    storage.loc[storage_in.index, storage_in.columns] = storage_in
    storage.loc[storage_in_regions.index, storage_in_regions.columns] = storage_in_regions
    
    storage.fillna(0, inplace=True)
    if "Storage" in urbs_results.keys():
        urbs_results["Storage"].set_index(["Site", "Storage type", "scenario-year"], inplace=True)
        try: # Update values in sheet
            urbs_results["Storage"].loc[storage.index] = storage.round(2)
        except: # Append values in sheet
            urbs_results["Storage"] = urbs_results["Storage"].append(storage.round(2))
    else: # Create sheet
        urbs_results["Storage"] = storage.round(2)
    # Sort index
    urbs_results["Storage"] = urbs_results["Storage"].sort_index(level="scenario-year")
    
    return urbs_results
    
    
def get_curtailment_data(urbs_results):
    """
    """
    multiindex = pd.MultiIndex.from_product([report_sites, scenario_years], names=["Site", "scenario-year"])
    # Prepare dataframe of curtailed energy
    filter = df_data["process_commodity"].reset_index()
    aux_process = filter.loc[(filter["Commodity"]=="Elec") & (filter["Direction"] == "Out"), "Process"].tolist()
    dict_tech = group_technologies(aux_process)
    
    curtailed = df_result["e_pro_in"].unstack()["Elec"].dropna().droplevel(3).reorder_levels(['sit', 'stf', 't']).sort_index()
    curtailed = add_weight(curtailed)
    curtailed = curtailed.reset_index().rename(columns={"sit": "Site", "stf": "scenario-year"})
    year_now = curtailed["scenario-year"].unique()[0]
    curtailed = curtailed.set_index(["Site", "scenario-year", "t"])
    
    prod = df_result["e_pro_out"].unstack()['Elec'].unstack().reorder_levels(['sit', 'stf', 't']).sort_index().fillna(0)
    prod = add_weight(prod)

    for pro in prod.columns:
        prod = prod.rename(columns={pro: dict_tech[pro]})
    try:
        prod = prod.stack().reset_index().rename(columns={"sit":"Site", "stf": "scenario-year", "level_3": "pro"}).groupby(["Site", "scenario-year", "t", "pro"]).sum()
        prod = prod.unstack().fillna(0)[0]
    except IndexError:
        return urbs_results
    
    curtailed = curtailed.join(prod)
    curtailed = curtailed.loc[curtailed["Elec"]>0]
    curtailed = curtailed.drop(curtailed.columns[curtailed.sum(axis=0) == 0], axis=1)
    
    list_columns = list(curtailed.columns)
    try:
        list_columns.remove("Elec")
    except:
        return urbs_results
    # Order of curtailment: unspecified
    for idx in curtailed.index:
        for pp in list_columns:
            try:
                curtailed.loc[idx, pp] = min(curtailed.loc[idx, "Elec"], curtailed.loc[idx, pp])
                curtailed.loc[idx, "Elec"] = curtailed.loc[idx, "Elec"] - curtailed.loc[idx, pp]
            except KeyError:
                pass
            
    curtailed = curtailed.drop(columns=["Elec"]).droplevel(2).reset_index().groupby(["Site", "scenario-year"]).sum()
    curtailed_regions = curtailed.reset_index()
    curtailed_regions["Site"] = [dict_countries[x] for x in curtailed_regions["Site"]]
    curtailed_regions = curtailed_regions.groupby(["Site", "scenario-year"]).sum()
    
    # Save results
    curtailment = pd.DataFrame(index=multiindex, columns=list_columns).reset_index()
    curtailment.loc[curtailment["scenario-year"]==year_now] = curtailment.loc[curtailment["scenario-year"]==year_now].fillna(0)
    curtailment = curtailment.set_index(["Site", "scenario-year"])
    curtailment.loc[curtailed.index, curtailed.columns] = curtailed
    curtailment.loc[curtailed_regions.index, curtailed_regions.columns] = curtailed_regions
    
    curtailment.fillna(0, inplace=True)
    if "Curtailment" in urbs_results.keys():
        urbs_results["Curtailment"].set_index(["Site", "scenario-year"], inplace=True)
        try: # Update values in sheet
            urbs_results["Curtailment"].loc[curtailment.index] = curtailment.round(2)
        except: # Append values in sheet
            urbs_results["Curtailment"] = urbs_results["Curtailment"].append(curtailment.round(2))
    else: # Create sheet
        urbs_results["Curtailment"] = curtailment.round(2)
    # Sort index
    urbs_results["Curtailment"] = urbs_results["Curtailment"].sort_index(level="scenario-year")
    
    return urbs_results
    

def get_transfer_data(urbs_results):
    """
    """
    multiindex = pd.MultiIndex.from_product([report_sites, [int(year)]], names=["Site", "scenario-year"])
    # Prepare dataframe of electricity transfer
    transfers = pd.DataFrame(index=multiindex, columns=report_sites)
    
    try:
        tra_out = df_result["e_tra_out"]
    except KeyError:
        return urbs_results
    tra_out = add_weight(tra_out)
    tra_out = tra_out.droplevel([0,4,5]).reset_index().rename(columns={"stf": "scenario-year", "sit": "Site", "sit_": "Site Out"})
    tra_out = tra_out.groupby(["Site", "scenario-year", "Site Out"]).sum().reset_index()
    
    tra_out_regions = tra_out.copy()
    tra_out_regions["Site"] = [dict_countries[x] for x in tra_out_regions["Site"]]
    tra_out_regions["Site Out"] = [dict_countries[x] for x in tra_out_regions["Site Out"]]
    
    idx_drop = []
    for idx in tra_out_regions.index:
        if tra_out_regions.loc[idx, "Site"] == tra_out_regions.loc[idx, "Site Out"]:
            idx_drop = idx_drop + [idx]
    tra_out_regions = tra_out_regions.drop(index=idx_drop)
    
    tra_out = tra_out.set_index(["Site", "scenario-year", "Site Out"]).unstack()["e_tra_out"]
    tra_out_regions = tra_out_regions.groupby(["Site", "scenario-year", "Site Out"]).sum().unstack()["e_tra_out"]
    
    transfers.loc[tra_out.index, tra_out.columns] = tra_out
    transfers.loc[tra_out_regions.index, tra_out_regions.columns] = tra_out_regions
    
    # Save results
    transfers.fillna(0, inplace=True)
    if "Transfers" in urbs_results.keys():
        urbs_results["Transfers"].set_index(["Site", "scenario-year"], inplace=True)
        try: # Update values in sheet
            urbs_results["Transfers"].loc[transfers.index] = transfers.round(2)
        except: # Append values in sheet
            urbs_results["Transfers"] = urbs_results["Transfers"].append(transfers.round(2))
    else: # Create sheet
        urbs_results["Transfers"] = transfers.round(2)
    # Sort index
    urbs_results["Transfers"] = urbs_results["Transfers"].sort_index(level="scenario-year")
    
    return urbs_results
    
    
def get_NTC_data(urbs_results):
    """
    """
    multiindex = pd.MultiIndex.from_product([report_sites, [int(year)]], names=["Site", "scenario-year"])
    # Prepare dataframe of electricity net transfer capacities
    NTC = pd.DataFrame(index=multiindex, columns=report_sites)
    
    ntc_inst = df_data["transmission"]["inst-cap"].reset_index().rename(columns={"support_timeframe": "scenario-year", "Site In": "Site"})
    ntc_inst = ntc_inst.set_index(["Site", "scenario-year", "Transmission", "Commodity", "Site Out"])
    try:
        ntc_new = df_result["cap_tra_new"].reset_index().rename(columns={"stf": "scenario-year", "sit": "Site", "sit_": "Site Out", "tra": "Transmission", "com": "Commodity", "cap_tra_new": "inst-cap"})
        ntc_new = ntc_new.set_index(["Site", "scenario-year", "Transmission", "Commodity", "Site Out"])
        ntc_inst = ntc_inst + ntc_new
    except KeyError: # No new capacities
        pass
    ntc_inst = ntc_inst.droplevel([2,3]).reset_index().groupby(["Site", "scenario-year", "Site Out"]).sum().unstack()["inst-cap"]
    
    ntc_inst_regions = ntc_inst.stack().reset_index()
    ntc_inst_regions["Site"] = [dict_countries[x] for x in ntc_inst_regions["Site"]]
    ntc_inst_regions["Site Out"] = [dict_countries[x] for x in ntc_inst_regions["Site Out"]]
    
    idx_drop = []
    for idx in ntc_inst_regions.index:
        if ntc_inst_regions.loc[idx, "Site"] == ntc_inst_regions.loc[idx, "Site Out"]:
            idx_drop = idx_drop + [idx]
    ntc_inst_regions = ntc_inst_regions.drop(index=idx_drop)
    
    ntc_inst_regions = ntc_inst_regions.groupby(["Site", "scenario-year", "Site Out"]).sum().unstack()[0]
    
    NTC.loc[ntc_inst.index, ntc_inst.columns] = ntc_inst
    NTC.loc[ntc_inst_regions.index, ntc_inst_regions.columns] = ntc_inst_regions
    
    # Save results
    NTC.fillna(0, inplace=True)
    if "NTC" in urbs_results.keys():
        urbs_results["NTC"].set_index(["Site", "scenario-year"], inplace=True)
        try: # Update values in sheet
            urbs_results["NTC"].loc[NTC.index] = NTC.round(2)
        except: # Append values in sheet
            urbs_results["NTC"] = urbs_results["NTC"].append(NTC.round(2))
    else: # Create sheet
        urbs_results["NTC"] = NTC.round(2)
    # Sort index
    urbs_results["NTC"] = urbs_results["NTC"].sort_index(level="scenario-year")
    
    return urbs_results


def invcost_factor(dep_prd, interest, discount=None, year_built=None,
                   stf_min=None):
    """Investment cost factor formula.
    Evaluates the factor multiplied to the invest costs
    for depreciation duration and interest rate.
    Args:
        dep_prd: depreciation period (years)
        interest: interest rate (e.g. 0.06 means 6 %)
        year_built: year utility is built
        discount: discount rate for intertmeporal planning
    """
    # invcost factor for non intertemporal planning
    if (discount is None) or (discount == 0):
        return ((1 + interest) ** dep_prd * interest /
               ((1 + interest) ** dep_prd - 1))
    # invcost factor for intertemporal planning
    else:
        return ((1 + discount) ** (1 - (year_built-stf_min)) *
               (interest * (1 + interest) ** dep_prd *
               ((1 + discount) ** dep_prd - 1)) /
               (discount * (1 + discount) ** dep_prd *
               ((1+interest) ** dep_prd - 1)))
                    
                    
def get_cost_data(urbs_results, year_built):
    """
    description
    """
    multiindex = pd.MultiIndex.from_product([report_sites, [int(year)]], names=["Site", "scenario-year"])
    # Prepare dataframe of costs
    costs = pd.DataFrame(0, index=multiindex, columns=["Fix costs", "Variable costs", "Fuel costs", "Environmental costs",
                                                       "Annualized inv costs", "Annualized total costs"])
    
    # Get helping factors
    if year_built > stf_min:
        discount = 0 #df_data["global_prop"].droplevel(0).loc["Discount rate", "value"]
    else:
        discount = 0
    cost_factor = (1 + discount) ** (stf_min - year_built)
    
    process = df_data["process"].drop(columns="support_timeframe").reset_index().rename(columns={"support_timeframe": "scenario-year"}).set_index(["Site", "scenario-year", "Process"])
    process["invcost-factor"] = invcost_factor(process["depreciation"], process["wacc"], 0, year_built, stf_min) * cost_factor
    
    try:
        storage = df_data["storage"].reset_index().rename(columns={"support_timeframe": "scenario-year"}).set_index(["Site", "scenario-year", "Storage", "Commodity"])
        storage["invcost-factor"] = invcost_factor(storage["depreciation"], storage["wacc"], 0, year_built, stf_min) * cost_factor
    except KeyError: # No storage
        pass
    
    try:
        transmission = df_data["transmission"].reset_index().rename(columns={"support_timeframe": "scenario-year"}).set_index(["Site In", "scenario-year", "Transmission", "Commodity", "Site Out"])
        transmission["invcost-factor"] = invcost_factor(transmission["depreciation"], transmission["wacc"], 0, year_built, stf_min) * cost_factor
    except KeyError: # No transmission
        pass
        
    # Get newly installed capacities
    cap_pro_new = df_result["cap_pro_new"].reset_index().rename(columns={"stf": "scenario-year", "sit":"Site", "pro":"Process"}).set_index(["Site", "scenario-year", "Process"])
    process = process.join(cap_pro_new)
    
    if "storage" in locals():
        try:
            cap_sto_p_new = df_result["cap_sto_p_new"].reset_index().rename(columns={"stf": "scenario-year", "sit":"Site", "sto":"Storage", "com":"Commodity"}).fillna(0)
            cap_sto_p_new = cap_sto_p_new.set_index(["Site", "scenario-year", "Storage", "Commodity"])
            cap_sto_c_new = df_result["cap_sto_c_new"].reset_index().rename(columns={"stf": "scenario-year", "sit":"Site", "sto":"Storage", "com":"Commodity"}).fillna(0)
            cap_sto_c_new = cap_sto_c_new.set_index(["Site", "scenario-year", "Storage", "Commodity"])
            storage = storage.join([cap_sto_p_new, cap_sto_c_new])
        except KeyError:
            storage["cap_sto_p_new"] = 0
            storage["cap_sto_c_new"] = 0
    
    if "transmission" in locals():
        try:
            cap_tra_new = df_result["cap_tra_new"].reset_index().rename(columns={"stf": "scenario-year", "sit": "Site In", "sit_": "Site Out", "tra": "Transmission", "com": "Commodity"})
            cap_tra_new = cap_tra_new.set_index(["Site In", "scenario-year", "Transmission", "Commodity", "Site Out"])
            transmission = transmission.join(cap_tra_new)
        except:
            transmission["cap_tra_new"] = 0
    
    # Correct total installed capacity
    process["inst-cap"] = process["inst-cap"] + process["cap_pro_new"]
    if "storage" in locals():
        storage["inst-cap-p"] = storage["inst-cap-p"] + storage["cap_sto_p_new"]
        storage["inst-cap-c"] = storage["inst-cap-c"] + storage["cap_sto_c_new"]
    if "transmission" in locals():
        transmission["inst-cap"] = transmission["inst-cap"] + transmission["cap_tra_new"]
    
    # Get produced energy
    prod = df_result["e_pro_out"].unstack()['Elec'].reorder_levels(['sit', 'stf', 'pro', 't']).sort_index().fillna(0)
    prod = add_weight(prod)
    prod = prod.unstack(level=3).sum(axis=1).reset_index().rename(columns={"sit":"Site", "stf": "scenario-year", "pro": "Process", 0: "prod"}).set_index(["Site", "scenario-year", "Process"])
    process = process.join(prod)
    
    # Get consumed fuels
    fuel = df_result["e_pro_in"]
    fuel = add_weight(fuel)
    fuel = fuel.droplevel(0).reset_index().rename(columns={"sit":"Site", "stf": "scenario-year", "pro": "Process", "com": "Commodity"})
    fuel = fuel.groupby(["Site", "scenario-year", "Process", "Commodity"]).sum().reset_index().set_index(["Site", "scenario-year", "Commodity"])
    fuel_price = df_data["commodity"]["price"].reset_index().rename(columns={"support_timeframe": "scenario-year"}).drop(columns="Type").set_index(["Site", "scenario-year", "Commodity"])
    fuel = fuel.join(fuel_price).reset_index().set_index(["Site", "scenario-year", "Process"]).fillna(0).drop(columns=["Commodity"])
    process = process.join(fuel)
    
    # Get emissions
    emissions = df_result["e_pro_out"].unstack()[df_result["com_env"].index].reorder_levels(['sit', 'stf', 'pro', 't']).sort_index().fillna(0).stack().rename("emissions")
    emissions = add_weight(emissions)
    emissions = emissions.reset_index().rename(columns={"sit":"Site", "stf": "scenario-year", "pro": "Process", "com": "Commodity", 0: "emissions"}).groupby(["Site", "scenario-year", "Process", "Commodity"]).sum()
    emissions = emissions.reset_index().set_index(["Site", "scenario-year", "Commodity"]).join(fuel_price.rename(columns={"price": "emissions_price"}))
    emissions["Environmental costs"] = emissions["emissions"] * emissions["emissions_price"]
    emissions = emissions.reset_index().drop(columns=["Commodity", "t", "emissions", "emissions_price"]).groupby(["Site", "scenario-year", "Process"]).sum()
    process = process.join(emissions)
    
    # Get storage flow
    if "storage" in locals():
        try:
            storage_in = add_weight(df_result["e_sto_in"]).droplevel(0).reset_index().rename(columns={"stf":"scenario-year", "sit":"Site", "sto": "Storage", "com":"Commodity"})
            storage_in = storage_in.groupby(["Site", "scenario-year", "Storage", "Commodity"]).sum()
            storage_out = add_weight(df_result["e_sto_out"]).droplevel(0).reset_index().rename(columns={"stf":"scenario-year", "sit":"Site", "sto": "Storage", "com":"Commodity"})
            storage_out = storage_out.groupby(["Site", "scenario-year", "Storage", "Commodity"]).sum()
            storage = storage.join([storage_in, storage_out])
        except KeyError:
            storage["e_sto_in"] = 0
            storage["e_sto_out"] = 0
    
    # Fill nan
    process = process.fillna(0)
    if "storage" in locals():
        storage = storage.fillna(0)
    if "transmission" in locals():
        transmission = transmission.fillna(0)
    
    # Investment costs
    process["Annualized inv costs"] = process["cap_pro_new"] * process["inv-cost"] * process["invcost-factor"] # alt for intertemporal: 'overpay-factor'
    
    if "storage" in locals():
        storage["Annualized inv costs"] = (storage["cap_sto_p_new"] * storage["inv-cost-p"] + storage["cap_sto_c_new"] * storage["inv-cost-c"]) * storage["invcost-factor"] # alt for intertemporal: 'overpay-factor'
            
    if "transmission" in locals():
        transmission["Annualized inv costs"] = transmission["cap_tra_new"] * transmission["inv-cost"] * transmission["invcost-factor"] # alt for intertemporal: 'overpay-factor'
        
    # Fix costs
    process["Fix costs"] = process["inst-cap"] * process["fix-cost"] * cost_factor
    
    if "storage" in locals():
        storage["Fix costs"] = (storage["inst-cap-p"] * storage["fix-cost-p"] + storage["inst-cap-c"] * storage["fix-cost-c"]) * cost_factor
    
    if "transmission" in locals():
        transmission["Fix costs"] = transmission["inst-cap"] * transmission["fix-cost"] * cost_factor
     
    # Variable costs
    process["Variable costs"] = process["prod"] * process["var-cost"] * cost_factor
    
    if "storage" in locals():
        # To do: add variable costs due to e_sto_c
        storage["Variable costs"] = (storage["e_sto_in"] + storage["e_sto_out"]) * storage["var-cost-p"] * cost_factor
        
    if "transmission" in locals():
        # To do: add variable costs due to transmission
        transmission["Variable costs"] = 0
    
    # Fuel costs
    process["Fuel costs"] = process["e_pro_in"] * process["price"] * cost_factor
    
    # Reindex and plit transmission costs between regions equally
    process = process.droplevel([2]).reset_index().groupby(["Site", "scenario-year"]).sum()
    if "storage" in locals():
        if len(storage):
            storage = storage.droplevel([2,3]).reset_index().groupby(["Site", "scenario-year"]).sum()
        else:
            storage = storage.droplevel([2,3])
    if "transmission" in locals():
        transmission_1 = transmission.droplevel([2,3,4]).reset_index().rename(columns={"Site In": "Site"}).groupby(["Site", "scenario-year"]).agg({"Annualized inv costs": "sum", "Fix costs": "sum", "Variable costs": "sum"})/2
        transmission_2 = transmission.droplevel([0,2,3]).reset_index().rename(columns={"Site Out": "Site"}).groupby(["Site", "scenario-year"]).agg({"Annualized inv costs": "sum", "Fix costs": "sum", "Variable costs": "sum"})/2
    
    # Report costs
    costs.loc[process.index, ["Fix costs", "Variable costs", "Fuel costs", "Environmental costs", "Annualized inv costs"]] = costs.loc[process.index, ["Fix costs", "Variable costs", "Fuel costs", "Environmental costs", "Annualized inv costs"]] + process.loc[process.index, ["Fix costs", "Variable costs", "Fuel costs", "Environmental costs", "Annualized inv costs"]]
    if "storage" in locals():
        costs.loc[storage.index, ["Fix costs", "Variable costs", "Annualized inv costs"]] = costs.loc[storage.index, ["Fix costs", "Variable costs", "Annualized inv costs"]] + storage[["Fix costs", "Variable costs", "Annualized inv costs"]]
    if "transmission" in locals():
        costs.loc[transmission_1.index, ["Fix costs", "Variable costs", "Annualized inv costs"]] = costs.loc[transmission_1.index, ["Fix costs", "Variable costs", "Annualized inv costs"]] + transmission_1[["Fix costs", "Variable costs", "Annualized inv costs"]]
        costs.loc[transmission_2.index, ["Fix costs", "Variable costs", "Annualized inv costs"]] = costs.loc[transmission_2.index, ["Fix costs", "Variable costs", "Annualized inv costs"]] + transmission_2[["Fix costs", "Variable costs", "Annualized inv costs"]] 
    
    costs['Annualized total costs'] = costs["Fix costs"] + costs["Variable costs"] + costs["Fuel costs"] + costs["Environmental costs"] + costs["Annualized inv costs"]
    
    # Regions
    costs_regions = costs.loc[list(set(dict_countries.keys()))].reset_index()
    costs_regions["Site"] = [dict_countries[x] for x in costs_regions["Site"]]
    costs_regions = costs_regions.groupby(["Site", "scenario-year"]).sum()
    costs.loc[costs_regions.index] = costs_regions
    
    # Save results
    costs.fillna(0, inplace=True)
    if "System costs" in urbs_results.keys():
        urbs_results["System costs"].set_index(["Site", "scenario-year"], inplace=True)
        try: # Update values in sheet
            urbs_results["System costs"].loc[costs.index] = costs.round(2)
        except: # Append values in sheet
            urbs_results["System costs"] = urbs_results["System costs"].append(costs.round(2))
    else: # Create sheet
        urbs_results["System costs"] = costs.round(2)
    # Sort index
    urbs_results["System costs"] = urbs_results["System costs"].sort_index(level="scenario-year")
    
    return urbs_results
  

def get_interface_LCA(urbs2lca_results, urbs_results, scen):
    """ description"""
    urbs2lca_results[scen] = 0

    try: # Australia
        urbs2lca_results.loc[("Energy produced abroad", "GWh/a"), scen] = urbs_results["Electricity generation"].loc[("Tennant Creek", 2030), "PV"] / 1000
        urbs2lca_results.loc[("Energy sent to Singapore (start of cable)", "GWh/a"), scen] = urbs_results["Transfers"].loc[("Darwin", 2030), "Singapore"] / df_data["transmission"].loc[(2030, "Darwin", "Singapore", "DC_CAB", "Elec"), "eff"] / 1000
        urbs2lca_results.loc[("Energy consumed in Singapore", "GWh/a"), scen] = urbs_results["Transfers"].loc[("Darwin", 2030), "Singapore"] / 1000
        urbs2lca_results.loc[("Installed PV capacity (total)", "GW"), scen] = urbs_results["Installed capacities"].loc[("Tennant Creek", 2030), "PV"] / 1000
        urbs2lca_results.loc[("Installed battery storage capacity (total)", "GWh"), scen] = urbs_results["Storage"].loc[("total_AUS", "Battery", 2030), "inst-cap-c"] / 1000
        urbs2lca_results.loc[("Installed cable capacity (total)", "GW"), scen] = urbs_results["NTC"].loc[("total_AUS", 2030), "total_SGP"] / 1000
        urbs2lca_results.loc[("Lifetime PV", "a"), scen] = df_data["process"].loc[(2030, "Tennant Creek", "Solar_PV"), "depreciation"]
        urbs2lca_results.loc[("Lifetime battery", "a"), scen] = df_data["storage"].loc[(2030, "Darwin", "Battery", "Elec"), "depreciation"]
        urbs2lca_results.loc[("Lifetime cable", "a"), scen] = df_data["transmission"].loc[(2030, "Darwin", "Singapore", "DC_CAB", "Elec"), "depreciation"]
    
    except: # Indonesia
        urbs2lca_results.loc[("Energy produced abroad", "GWh/a"), scen] = urbs_results["Electricity generation"].loc[("Jambi", 2030), "PV"] / 1000
        urbs2lca_results.loc[("Energy sent to Singapore (start of cable)", "GWh/a"), scen] = urbs_results["Transfers"].loc[("Jambi", 2030), "Singapore"] / df_data["transmission"].loc[(2030, "Jambi", "Singapore", "DC_CAB", "Elec"), "eff"] / 1000
        urbs2lca_results.loc[("Energy consumed in Singapore", "GWh/a"), scen] = urbs_results["Transfers"].loc[("Jambi", 2030), "Singapore"] / 1000
        urbs2lca_results.loc[("Installed PV capacity (total)", "GW"), scen] = urbs_results["Installed capacities"].loc[("Jambi", 2030), "PV"] / 1000
        urbs2lca_results.loc[("Installed battery storage capacity (total)", "GWh"), scen] = urbs_results["Storage"].loc[("total_IDN", "Battery", 2030), "inst-cap-c"] / 1000
        urbs2lca_results.loc[("Installed cable capacity (total)", "GW"), scen] = urbs_results["NTC"].loc[("total_IDN", 2030), "total_SGP"] / 1000
        urbs2lca_results.loc[("Lifetime PV", "a"), scen] = df_data["process"].loc[(2030, "Jambi", "Solar_PV"), "depreciation"]
        urbs2lca_results.loc[("Lifetime battery", "a"), scen] = df_data["storage"].loc[(2030, "Jambi", "Battery", "Elec"), "depreciation"]
        urbs2lca_results.loc[("Lifetime cable", "a"), scen] = df_data["transmission"].loc[(2030, "Jambi", "Singapore", "DC_CAB", "Elec"), "depreciation"]
    
    urbs2lca_results.loc[("Energy demand in Singapore", "GWh/a"), scen] = urbs_results["Electricity"].loc[("total_SGP", 2030), "elec-demand"] / 1000
    # Cable length is 3800, unless scenario changes that
    try:
        urbs2lca_results.loc[("Cable length"), scen] = int(scen[-4:])
    except: # Jambi or cab0
        if scen[-4:] == "cab0":
            urbs2lca_results.loc[("Cable length"), scen] = 0
        else:
            urbs2lca_results.loc[("Cable length"), scen] = 320
    
    # Allocation factor
    urbs2lca_results.loc[("Allocation factor for Singapore", "dimensionless"), scen] = 1
    
    urbs2lca_results.loc[("PV capacity allocated to SG", "GW"), scen] = urbs2lca_results.loc[("Allocation factor for Singapore", "dimensionless"), scen] * urbs2lca_results.loc[("Installed PV capacity (total)", "GW"), scen]
    urbs2lca_results.loc[("Battery storage capacity allocated to SG", "GWh"), scen] = urbs2lca_results.loc[("Allocation factor for Singapore", "dimensionless"), scen] * urbs2lca_results.loc[("Installed battery storage capacity (total)", "GWh"), scen]
    urbs2lca_results.loc[("Cable capacity allocated to SG", "GW"), scen] = urbs2lca_results.loc[("Allocation factor for Singapore", "dimensionless"), scen] * urbs2lca_results.loc[("Installed cable capacity (total)", "GW"), scen]
    
    # Save results
    urbs2lca_results.reset_index(inplace=True)
    return urbs2lca_results
    
    
# Read in data for all scenarios
list_files = [f.name for f in os.scandir(result_folder) if f.name[-3:]==".h5"]

for result_file in list_files:
    
    year = result_file[:-3].split("_")[1]
    scen = "_".join(result_file[:-3].split("_")[2:])
    
    # Read output file
    if year == "2019":
        writer_path = os.path.abspath(os.path.join(result_folder, os.pardir, "URBS_" + year + ".xlsx"))
    else:
        writer_path = os.path.abspath(os.path.join(result_folder, os.pardir, "URBS_" + scen + ".xlsx"))
    writer = pd.ExcelWriter(writer_path, engine='openpyxl') 
    
    # Read in results
    urbs_path = os.path.join(result_folder, result_file)
    helpdf = urbs.load(urbs_path)
    df_result = helpdf._result
    df_data = helpdf._data
    
    # Get dictionaries and list of sites to be used in the report
    dict_season = group_seasons()
    dict_countries = group_sites(df_data["site"].reset_index()["Name"].tolist())
    report_sites = sorted(list(set(dict_countries.keys()))) + sorted(list(set(dict_countries.values())))
    
    if os.path.exists(writer_path):
        # print("the file exists and will be updated")
        urbs_results = pd.read_excel(writer_path, sheet_name=None)
    else:
        writer_path_initial = os.path.abspath(os.path.join(result_folder, os.pardir, "URBS_2019.xlsx"))
        if os.path.exists(writer_path_initial):
            urbs_results = pd.read_excel(writer_path_initial, sheet_name=None)
        else:
            urbs_results = {}
    
    ### SHEETS ###
    print(scen, year, ": Getting CO2 data")
    urbs_results = get_emissions_data(urbs_results)
    
    print(scen, year, ": Getting electricity prices")
    urbs_results = get_electricity_data(urbs_results, int(year))
    
    print(scen, year, ": Getting electricity generation data")
    urbs_results = get_generation_data(urbs_results)
    
    print(scen, year, ": Getting total, new and retired capacities data")
    urbs_results = get_capacities_data(urbs_results)
    
    print(scen, year, ": Getting storage data")
    urbs_results = get_storage_data(urbs_results)
    
    print(scen, year, ": Getting curtailment data")
    urbs_results = get_curtailment_data(urbs_results)
    
    print(scen, year, ": Getting transfer data")
    urbs_results = get_transfer_data(urbs_results)
    
    print(scen, year, ": Getting NTC data")
    urbs_results = get_NTC_data(urbs_results)
    
    print(scen, year, ": Getting system cost data")
    urbs_results = get_cost_data(urbs_results, int(year))
    
    # Save results
    for sheet in list(urbs_results.keys()):
        if len(urbs_results[sheet]):
            urbs_results[sheet].to_excel(writer, sheet_name=sheet, index=True, header=True)
        else:
            urbs_results.pop(sheet)
    writer.save()
    
    ### LCA ###
    if year == "2030":
        lca_path = os.path.abspath(os.path.join(result_folder, os.pardir, "URBS2LCA.csv"))
        lca_path_EN = os.path.abspath(os.path.join(result_folder, os.pardir, "URBS2LCA_EN.csv"))
        lca_empty_path = os.path.abspath(os.path.join(result_folder, os.pardir, "Interface_empty.csv"))
        if os.path.exists(lca_path):
            # print("the file exists and will be updated")
            urbs2lca_results = pd.read_csv(lca_path, sep=";", decimal=",")
        else:
            urbs2lca_results = pd.read_csv(lca_empty_path, sep=";", decimal=",")
        urbs2lca_results.set_index(["index", "unit"], inplace=True)
        urbs2lca_results = get_interface_LCA(urbs2lca_results, urbs_results, scen)
        
        urbs2lca_results.to_csv(lca_path, index=False, decimal=",", sep=";")
        urbs2lca_results.to_csv(lca_path_EN, index=False, decimal=".", sep=",")