from datetime import datetime
from pprint import pprint

import pandas as pd
import os
from utils.load_game_from_excell import load_stat_of_game


# current = os.getcwd()
# file_name = r'stat_xls\stat.xlsx'
# full_path = os.path.join(current, file_name_base)
#
# xl = pd.ExcelFile(full_path)



# top_players = pd.read_excel(full_path, sheet_name='game1', skiprows = range(20, 200), usecols = "B:F")
# print(top_players.head(200))

# # Load spreadsheet
# xl = pd.ExcelFile(full_path)
#
# # Print the sheet names
# print(xl.sheet_names)
#
# # Load a sheet into a DataFrame by name: df1
# df1 = xl.parse('game1')
#
# print(df1)