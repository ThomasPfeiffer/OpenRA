from datetime import datetime
from evoalgosOptimization.individual import RandomMutationIndividual

# Environment settings
base_path = "C:/uni/dev/OpenRA"
ra_game_executable = base_path + "/Game/OpenRA.exe"
workspace_path = base_path + "/workspace"
map_directory = base_path + "/Game/mods/ra/maps/ma_temperat/"
database = workspace_path + "/fitness.db"
game_log = workspace_path + "/logs/{0}_gen_openra.yaml".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
show_msgbox = False

# RA Game settings
headless = False
max_ticks = 100000
timestep = 1
map_name = "ma_temperat"
ai1 = "Rush AI"
ai1_faction = "england"
ai2 = "Rush AI"
ai2_faction = "ukraine"
fitness_function_id = 1
run_description = "Test start params"

# Settings for execution without optimization
games_to_play = 1 # Amount of games played without changing parameters
game_for_replay = 8111 # If id is given reconstructs parameters from database to replay with same settings

max_age=10
popsize=1
max_generations=1
reevaluate=False
individual=RandomMutationIndividual
