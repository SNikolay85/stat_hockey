import pandas as pd
import os

current = os.getcwd()
file_name_base = r'stat_xls\stat.xlsx'
full_path = os.path.join(current, file_name_base)

print(full_path)

xl = pd.ExcelFile(full_path)
df_game1_player = xl.parse('game1', usecols='B:P', header=1, nrows=200)
df_game1_goalie = xl.parse('game1', usecols='I:M', header=1, nrows=100)
# df_game_2 = xl.parse('game2')
# df_game_3 = xl.parse('game3')
# df_game_4 = xl.parse('game4')
print(df_game1_player)
# sheet_to_df_map = {}
# for sheet_name in xl.sheet_names:
#     if 'game' in sheet_name:
#         player = xl.parse(sheet_name, usecols='B:F', header=1, nrows=200)
#         goalkeeper = xl.parse(sheet_name, usecols='I:M', header=1, nrows=100)
#         sheet_to_df_map[sheet_name] = player, goalkeeper
        # sheet_to_df_map[sheet_name]['goalie'] = xl.parse(sheet_name, usecols='I:M', header=1, nrows=100)
# titanic[["Sex", "Age"]].groupby("Sex").mean()
# print(df_game_1[['вид', 'игрок']].groupby('игрок').value_counts())
# , 'точность', 'результат'
# print(df_game_1[['игрок', 'вид']].groupby('игрок').value_counts())
list_player = df_game1_player['игрок'].unique()
list_goalie = df_game1_player['вратарь'].unique()
player_dict = {}
goalie_dict = {}
for i in list_player:
    stat = {'b_all': len(df_game1_player[(df_game1_player['вид'] == 'б') & (df_game1_player['игрок'] == i)]),
          'b_target': len(df_game1_player[(df_game1_player['вид'] == 'б') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'goal': len(df_game1_player[(df_game1_player['вид'] == 'б') & (df_game1_player['точность'] == '+') & (df_game1_player['результат'] == '+') & (df_game1_player['игрок'] == i)]),
          'p_all': len(df_game1_player[(df_game1_player['вид'] == 'п') & (df_game1_player['игрок'] == i)]),
          'p_target': len(df_game1_player[(df_game1_player['вид'] == 'п') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'foul': len(df_game1_player[(df_game1_player['вид'] == 'фол') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'vb_all': len(df_game1_player[(df_game1_player['вид'] == 'вб') & (df_game1_player['игрок'] == i)]),
          'vb_target': len(df_game1_player[(df_game1_player['вид'] == 'вб') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'mistake': len(df_game1_player[(df_game1_player['вид'] == 'ош') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'block': len(df_game1_player[(df_game1_player['вид'] == 'блок') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'bul': len(df_game1_player[(df_game1_player['вид'] == 'бул') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'bul_target': len(df_game1_player[(df_game1_player['вид'] == 'бул') & (df_game1_player['точность'] == '+') & (df_game1_player['результат'] == '+') & (df_game1_player['игрок'] == i)]),
          'assist': len(df_game1_player[df_game1_player['ассистент'] == i]),
          'take_puck': len(df_game1_player[(df_game1_player['вид'] == 'отбор') & (df_game1_player['точность'] == '+') & (df_game1_player['игрок'] == i)]),
          'kp': int(df_game1_player.loc[df_game1_player['игрок_кп'] == i, 'кп'].mean()),
            # titanic.loc[titanic["Age"] > 35, "Name"]
          }
    player_dict[i] = stat
for i in list_goalie:
      print(i)
print(player_dict)
# print(player['яковлев']['kp'].mean())

# print(sheet_to_df_map['game4'])
# fg = {'game': {'Sipatrov': {'b_all': b_all,
#               'b_target' b_target,
#               'goal': goal,
#               'p_all': p_all,
#               'p_target': p_target,
#               'foul': foul,
#               'vb_all': vb_all,
#               'vb_target': vb_target,
#               'mistake': mistake,
#               'block': block,
#               'bul': bul,
#               'bul_target': bul_target,
#               'assist': assist,
#               'take_puck': take_puck,
#               'kp': kp
#               }
# }
# }

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