import os
import pandas as pd
import pyomo.environ
import shutil
import urbs
from datetime import datetime
from pyomo.opt.base import SolverFactory


# SCENARIOS
def scenario_base(data):
    # do nothing
    return data


def scenario_co2_25(data):
    # change CO2 price
    co = data['commodity']
    co2_only = (co.index.get_level_values('Commodity') == 'CO2')
    co.loc[co2_only, 'price'] = 25
    return data
	

def scenario_co2_50(data):
    # change CO2 price
    co = data['commodity']
    co2_only = (co.index.get_level_values('Commodity') == 'CO2')
    co.loc[co2_only, 'price'] = 50
    return data
	
	
def scenario_co2_75(data):
    # change CO2 price
    co = data['commodity']
    co2_only = (co.index.get_level_values('Commodity') == 'CO2')
    co.loc[co2_only, 'price'] = 75
    return data
	
	
def scenario_co2_100(data):
    # change CO2 price
    co = data['commodity']
    co2_only = (co.index.get_level_values('Commodity') == 'CO2')
    co.loc[co2_only, 'price'] = 100
    return data
	
def scenario_cheaper_bat_and_pv(data):
    # change investment and fix costs
    sto = data['storage']
    batteries_only = (sto.index.get_level_values('Storage') == 'Li-ion battery')
    sto.loc[batteries_only, 'inv-cost-c'] *= 0.5
    sto.loc[batteries_only, 'fix-cost-c'] *= 0.5
    pro = data['process']
    photovoltaics_only = (pro.index.get_level_values('Process').map(lambda x: x.startswith('Solar')))
    pro.loc[photovoltaics_only, 'inv-cost'] *= 0.5
    pro.loc[photovoltaics_only, 'fix-cost'] *= 0.5
    return data
	
	
def scenario_hydrogen(data):
    # change investment and fix costs
    pro = data['process']
    electrolysis_only = (pro.index.get_level_values('Process') == 'Electrolysis')
    pro.loc[electrolysis_only, 'inv-cost'] *= 0.5
    pro.loc[electrolysis_only, 'fix-cost'] *= 0.5
    fc_only = (pro.index.get_level_values('Process') == 'Fuel cell')
    pro.loc[fc_only, 'inv-cost'] *= 0.5
    pro.loc[fc_only, 'fix-cost'] *= 0.5
    return data
	

def scenario_process_caps(data):
    # change maximum installable capacity
    pro = data['process']
    photovoltaics_only = (pro.index.get_level_values('Process') == 'Photovoltaics')
    pro.loc[photovoltaics_only, 'cap-up'] = [max(20, pro.loc[i, 'inst-cap']*1.5) for i in pro.loc[photovoltaics_only].index]
    onshore_wind_only = (pro.index.get_level_values('Process') == 'Onshore wind park')
    pro.loc[onshore_wind_only, 'cap-up'] = [max(10, pro.loc[i, 'inst-cap']*1.25) for i in pro.loc[onshore_wind_only].index]
    return data


def scenario_for_pv(data):
    # combine three scenarios
    data = scenario_co2_100(data)
    data = scenario_cheaper_bat_and_pv(data)
    data = scenario_no_wind(data)
    return data
	
	
def scenario_for_wind(data):
    # combine three scenarios
    data = scenario_co2_100(data)
    data = scenario_hydrogen(data)
    data = scenario_no_pv(data)
    return data
	

def scenario_stock_prices(data):
    # change stock commodity prices
    co = data['commodity']
    stock_commodities_only = (co.index.get_level_values('Type') == 'Stock')
    co.loc[stock_commodities_only, 'price'] *= 1.5
    return data
	
	
def scenario_no_dsm(data):
    # empty the DSM dataframe completely
    data['dsm'] = pd.DataFrame()
    return data


def prepare_result_directory(result_name):
    """ create a time stamped directory within the result folder """
    # timestamp for result directory
    now = datetime.now().strftime('%Y%m%dT%H%M')

    # create result directory if not existent
    result_dir = os.path.join('result', '{}-{}'.format(result_name, now))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    return result_dir


def setup_solver(optim, logfile='solver.log'):
    """ """
    if optim.name == 'gurobi':
        # reference with list of option names
        # http://www.gurobi.com/documentation/5.6/reference-manual/parameters
        optim.set_options("logfile={}".format(logfile))
        # optim.set_options("timelimit=7200")  # seconds
        # optim.set_options("mipgap=5e-4")  # default = 1e-4
    elif optim.name == 'glpk':
        # reference with list of options
        # execute 'glpsol --help'
        optim.set_options("log={}".format(logfile))
        # optim.set_options("tmlim=7200")  # seconds
        # optim.set_options("mipgap=.0005")
    else:
        print("Warning from setup_solver: no options set for solver "
              "'{}'!".format(optim.name))
    return optim


def run_scenario(input_file, timesteps, scenario, result_dir,
                 plot_tuples=None, plot_periods=None, report_tuples=None):
    """ run an urbs model for given input, time steps and scenario

    Args:
        input_file: filename to an Excel spreadsheet for urbs.read_excel
        timesteps: a list of timesteps, e.g. range(0,8761)
        scenario: a scenario function that modifies the input data dict
        result_dir: directory name for result spreadsheet and plots
        plot_tuples: (optional) list of plot tuples (c.f. urbs.result_figures)
        plot_periods: (optional) dict of plot periods (c.f. urbs.result_figures)
        report_tuples: (optional) list of (sit, com) tuples (c.f. urbs.report)

    Returns:
        the urbs model instance
    """

    # scenario name, read and modify data for scenario
    sce = scenario.__name__
    data = urbs.read_excel(input_file)
    data = scenario(data)

    # create model
    prob = urbs.create_model(data, timesteps)

    # refresh time stamp string and create filename for logfile
    now = prob.created
    log_filename = os.path.join(result_dir, '{}.log').format(sce)

    # solve model and read results
    optim = SolverFactory('gurobi')  # cplex, glpk, gurobi, ...
    optim = setup_solver(optim, logfile=log_filename)
    result = optim.solve(prob, tee=True)

    # copy input file to result directory
    shutil.copyfile(input_file, os.path.join(result_dir, input_file))
    
    # save problem solution (and input data) to HDF5 file
    #urbs.save(prob, os.path.join(result_dir, '{}.h5'.format(sce)))

    # write report to spreadsheet
    urbs.report(
        prob,
        os.path.join(result_dir, '{}.xlsx').format(sce),
        report_tuples=report_tuples)

    # result plots
    urbs.result_figures(
        prob,
        os.path.join(result_dir, '{}'.format(sce)),
        plot_title_prefix=sce.replace('_', ' '),
        plot_tuples=plot_tuples,
        periods=plot_periods,
        figure_size=(24, 9))
    return prob

if __name__ == '__main__':
    input_file = 'CA_v05.5j_2016.xlsx'
    result_name = os.path.splitext(input_file)[0]  # cut away file extension
    result_dir = prepare_result_directory(result_name)  # name + time stamp

    # simulation timesteps
    (offset, length) = (0, 8760) # time step selection
    timesteps = range(offset, offset+length+1)

    # plotting commodities/sites
    plot_tuples = []
        #('LAA', 'Elec'),
        #('SCA', 'Elec'),
        #('SWB', 'Elec'),
        #('NCA', 'Elec')]

    # detailed reporting commodity/sites
    report_tuples = [
        ('CCT', 'Elec'),
        ('CVA', 'Elec'),
        ('ECA', 'Elec'),
        ('ELU', 'Elec'),
        ('FRE', 'Elec'),
        ('LAX', 'Elec'),
        ('NCT', 'Elec'),
        ('NVA', 'Elec'),
        ('PAC', 'Elec'),
        ('SDG', 'Elec'),
        ('MX', 'Elec'),
        ('NE', 'Elec'),
        ('NW', 'Elec'), 
        ('SW', 'Elec'),
        #('CCT', 'CO2'),
        #('CVA', 'CO2'),
        #('ECA', 'CO2'),
        #('ELU', 'CO2'),
        #('FRE', 'CO2'),
        #('LAX', 'CO2'),
        #('NCT', 'CO2'),
        #('NVA', 'CO2'),
        #('PAC', 'CO2'),
        #('SDG', 'CO2'),
        #('MX', 'CO2'),
        #('NE', 'CO2'),
        #('NW', 'CO2'), 
        #('SW', 'CO2'),
        ]

    # plotting timesteps
    plot_periods = {
        'all': timesteps[1:]
    }

    # add or change plot colors
    my_colors = {
        'South': (230, 200, 200),
        'Mid': (200, 230, 200),
        'North': (200, 200, 230)}
    for country, color in my_colors.items():
        urbs.COLORS[country] = color

    # select scenarios to be run
    scenarios = [
        scenario_base,
        #scenario_stock_prices,
        #scenario_co2_limit,
        #scenario_co2_tax_mid,
        #scenario_no_dsm,
        #scenario_north_process_caps,
        #scenario_all_together
        ]

    for scenario in scenarios:
        prob = run_scenario(input_file, timesteps, scenario, result_dir,
                            plot_tuples=plot_tuples,
                            plot_periods=plot_periods,
                            report_tuples=report_tuples)
