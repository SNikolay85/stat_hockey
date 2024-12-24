import os

from utils import load_game_from_excell

current = os.getcwd()
file_name_excell = 'backend/static/stat.xlsx'
file_name_data = 'data1.json'
full_path_excell = os.path.join(current, file_name_excell)
full_path_data = os.path.join(current, file_name_data)

print(load_game_from_excell.load_stat_of_game(full_path_excell))
