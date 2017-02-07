from datetime import datetime

# Environment settings
base_path = "C:/dev/OpenRA"
ra_game_executable = base_path + "/Game/OpenRA.exe"
workspace_path = base_path + "/workspace"
map_directory = base_path + "/Game/mods/ra/maps/ma_temperat/"
database = workspace_path + "/fitness.db"
game_log = workspace_path + "/logs/{0}_gen_openra.yaml".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
param_list=workspace_path+'/param_list.csv'
show_msgbox = True # Specifies whether a Message box "Execution is finished" is shown upon termination

# Execution settings
headless = False
max_ticks = 100000 # Maximal number of milliseconds the game may take
timestep = 10 # Game speed - Default is 40

# Autostart settings
map_name = "ma_temperat"
ai1 = "Rush AI"
ai1_faction = "ukraine"
ai2 = "Rush AI"
ai2_faction = "england"

# Storage documentation
run_description = "Test the environment"

# Settings for execution without optimization
games_to_play = 2 # Amount of games played without changing parameters
game_for_replay = 5
individual_for_replay = 4148

# Evolutionary Algorithm
fitness_function_id = 1 # Fitness function assigned to games in database, does not affect algorithm
start_values_fixed=False
recombination_prob=0.2
num_parents=2
max_age=1
popsize=3
offspring=15
max_generations=20
games_per_evaluation=3
reevaluate=False
individual="RandomMutationIndividual"



