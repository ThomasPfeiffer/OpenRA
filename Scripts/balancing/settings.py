from datetime import datetime

base_path = "C:/dev/OpenRA"
ra_game_executable = base_path + "/Game/OpenRA.exe"
workspace_path = base_path + "/workspace"
map_directory = base_path + "/Game/mods/ra/maps/ma_temperat/"
database = workspace_path + "/fitness.db"
game_log = workspace_path + "/logs/{0}_gen_openra.yaml".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

headless = True
max_ticks = 100000
timestep = 1
map_name = "ma_temperat"
ai1 = "Basic Unit AI"
ai1_faction = "england"
ai2 = "Rush AI"
ai2_faction = "ukraine"
fitness_function = 1
run_description = "Only basic units with very large parameter bounds. ESReproduction, popsize 5. Only asexual reproduction."

paramless_games = 20