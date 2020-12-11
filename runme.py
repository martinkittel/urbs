import os
import shutil
import urbs


input_files = 'SunCable.xlsx'  # for single year file name, for intertemporal folder name
input_dir = os.path.join('Input', 'SunCable')
input_path = os.path.join(input_dir, input_files)

result_name = 'SunCable'
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
             # cab 3800 km
             urbs.scenario_2030_eff050_cab3800,
             urbs.scenario_2030_eff065_cab3800,
             urbs.scenario_2030_eff070_cab3800,
             urbs.scenario_2030_eff075_cab3800, # base case
             urbs.scenario_2030_eff080_cab3800,
             urbs.scenario_2030_eff085_cab3800,
             urbs.scenario_2030_eff100_cab3800,
             # cab 0000 km
             urbs.scenario_2030_eff050_cab0000,
             urbs.scenario_2030_eff065_cab0000,
             urbs.scenario_2030_eff070_cab0000,
             urbs.scenario_2030_eff075_cab0000,
             urbs.scenario_2030_eff080_cab0000,
             urbs.scenario_2030_eff085_cab0000,
             urbs.scenario_2030_eff100_cab0000,
             # cab 1000 km
             urbs.scenario_2030_eff050_cab1000,
             urbs.scenario_2030_eff065_cab1000,
             urbs.scenario_2030_eff070_cab1000,
             urbs.scenario_2030_eff075_cab1000,
             urbs.scenario_2030_eff080_cab1000,
             urbs.scenario_2030_eff085_cab1000,
             urbs.scenario_2030_eff100_cab1000,
             # cab 2000 km
             urbs.scenario_2030_eff050_cab2000,
             urbs.scenario_2030_eff065_cab2000,
             urbs.scenario_2030_eff070_cab2000,
             urbs.scenario_2030_eff075_cab2000,
             urbs.scenario_2030_eff080_cab2000,
             urbs.scenario_2030_eff085_cab2000,
             urbs.scenario_2030_eff100_cab2000,
             # cab 3000 km
             urbs.scenario_2030_eff050_cab3000,
             urbs.scenario_2030_eff065_cab3000,
             urbs.scenario_2030_eff070_cab3000,
             urbs.scenario_2030_eff075_cab3000,
             urbs.scenario_2030_eff080_cab3000,
             urbs.scenario_2030_eff085_cab3000,
             urbs.scenario_2030_eff100_cab3000,
             # cab 0000 km
             urbs.scenario_2030_eff050_cab4000,
             urbs.scenario_2030_eff065_cab4000,
             urbs.scenario_2030_eff070_cab4000,
             urbs.scenario_2030_eff075_cab4000,
             urbs.scenario_2030_eff080_cab4000,
             urbs.scenario_2030_eff085_cab4000,
             urbs.scenario_2030_eff100_cab4000,
             # cab 0000 km
             urbs.scenario_2030_eff050_cab5000,
             urbs.scenario_2030_eff065_cab5000,
             urbs.scenario_2030_eff070_cab5000,
             urbs.scenario_2030_eff075_cab5000,
             urbs.scenario_2030_eff080_cab5000,
             urbs.scenario_2030_eff085_cab5000,
             urbs.scenario_2030_eff100_cab5000,
            ]

for scenario in scenarios:
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name)
