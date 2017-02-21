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
max_ticks = 500000 # Maximal number of milliseconds the game may take
timestep = 3 # Game speed - Default is 40

# Autostart settings
map_name = "ma_temperat"
ai1 = "Rush AI"
ai1_faction = "ukraine"
ai2 = "Rush AI"
ai2_faction = "england"

# Storage documentation
run_description = "Test the environment"

# Settings for execution without optimization
games_to_play = 1 # Number of games played, during simulation, csvlist or replay
game_for_replay = 2

# Evolutionary Algorithm
fitness_function_id = 1 # Fitness function assigned to games in database, does not affect algorithm
start_values_fixed=True # Whether parameters are initialized with random values -> set True when start values are predefined
recombination_prob=0.2
num_parents=2
max_age=1000 # Maximal age of an Individuum
popsize=3
offspring=3
max_generations=5
games_per_evaluation=1 # Number of games executed for each solution, if > 1 the median of calculated fitness values is taken
reevaluate=False # Calculate fitness function again each time an individual survives a generation
individual="RandomMutationIndividual" # RandomMutationIndividual or FixedMutationIndividual as in individual.py



