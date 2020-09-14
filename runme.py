import os
import shutil
import urbs


input_files = 'Sin-Aus-urbs_v4.0.xlsx'  # for single year file name, for intertemporal folder name
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
             # urbs.scenario_2019,
             urbs.scenario_2030_base,
             # # imports
             # urbs.scenario_2030_imports_00pc,
             # urbs.scenario_2030_imports_10pc,
             # urbs.scenario_2030_imports_30pc,
             # urbs.scenario_2030_imports_40pc,
             # # solar efficiency
             # urbs.scenario_2030_solar_eff_050pc,
             # urbs.scenario_2030_solar_eff_065pc,
             # urbs.scenario_2030_solar_eff_070pc,
             # urbs.scenario_2030_solar_eff_080pc,
             # urbs.scenario_2030_solar_eff_085pc,
             # urbs.scenario_2030_solar_eff_100pc,
             # # cable length
             # urbs.scenario_2030_cable_0000km,
             # urbs.scenario_2030_cable_1000km,
             # urbs.scenario_2030_cable_2000km,
             # urbs.scenario_2030_cable_3000km,
             # urbs.scenario_2030_cable_4000km,
             # urbs.scenario_2030_cable_5000km,
            ]

for scenario in scenarios:
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name)
