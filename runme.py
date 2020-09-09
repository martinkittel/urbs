import os
import shutil
import urbs


input_files = 'Sin-Aus-urbs_v3.0.xlsx'  # for single year file name, for intertemporal folder name
input_dir = os.path.join('Input', 'SunCable')
input_path = os.path.join(input_dir, input_files)

result_name = input_files.split("_")[1][:-5]
result_dir = urbs.prepare_result_directory(result_name)  # name + time stamp

# copy input file to result directory
try:
    shutil.copytree(input_path, os.path.join(result_dir, input_dir))
except NotADirectoryError:
    shutil.copyfile(input_path, os.path.join(result_dir, input_files))
# copy run file to result directory
shutil.copy(__file__, result_dir)

# objective function
objective = 'cost'  # set either 'cost' or 'CO2' as objective

# Choose Solver (cplex, glpk, gurobi, ...)
solver = 'gurobi'

# simulation timesteps
(offset, length) = (0, 8760)  # time step selection
timesteps = range(offset, offset+length+1)
dt = 1  # length of each time step (unit: hours)

# detailed reporting commodity/sites
report_tuples = []

# optional: define names for sites in report_tuples
report_sites_name = {}

# plotting commodities/sites
plot_tuples = []

# optional: define names for sites in plot_tuples
plot_sites_name = {}

# plotting timesteps
plot_periods = {
    'all': timesteps[1:]
}

# add or change plot colors
my_colors = {}
for country, color in my_colors.items():
    urbs.COLORS[country] = color

# select scenarios to be run
scenarios = [
             urbs.scenario_2019,
             urbs.scenario_2030_base,
             # imports
             urbs.scenario_2030_no_imports,
             urbs.scenario_2030_10pc_imports,
             urbs.scenario_2030_30pc_imports,
             urbs.scenario_2030_40pc_imports,
             # solar efficiency
             urbs.scenario_2030_50pc_solar_efficiency,
             urbs.scenario_2030_65pc_solar_efficiency,
             urbs.scenario_2030_70pc_solar_efficiency,
             urbs.scenario_2030_80pc_solar_efficiency,
             urbs.scenario_2030_85pc_solar_efficiency,
             urbs.scenario_2030_100pc_solar_efficiency,
             # cable length
             urbs.scenario_2030_0km_cable,
             urbs.scenario_2030_1000km_cable,
             urbs.scenario_2030_2000km_cable,
             urbs.scenario_2030_3000km_cable,
             urbs.scenario_2030_4000km_cable,
             urbs.scenario_2030_5000km_cable,
            ]

for scenario in scenarios:
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name)
