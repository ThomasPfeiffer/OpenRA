from datetime import datetime

base_path = "C:/dev/OpenRA"
workspace_path = base_path + "/workspace"
database = workspace_path + "/fitness.db"
map_directory = base_path + "/Game/mods/ra/maps/ma_temperat/"
game_log = workspace_path + "/logs/{0}_gen_openra.yaml".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
ra_game_executable = "C:/dev/OpenRA/Game/OpenRA.exe"
headless = True
max_ticks = 100000
map_name = "ma_temperat"