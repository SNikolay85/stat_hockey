from pprint import pprint

import pandas as pd
import os

current = os.getcwd()
file_name_base = '../stat_xls/stat.xlsx'
full_path = os.path.join(current, file_name_base)
print(full_path)

def load_stat_of_game(base_path):
    xl = pd.ExcelFile(base_path)
    all_game = {}
    for sheet_name in xl.sheet_names:
        foul_s = 0
        player_dict = {}
        goalie_dict = {}
        goalie_s_dict = {}
        if 'game' in sheet_name:
            df_player = xl.parse(sheet_name, usecols='B:P', header=1, nrows=200)
            df_game = xl.parse(sheet_name, usecols='B, D, G')
            info_game = list(df_game.head(0))
            list_player = list(filter(lambda x: type(x) is not float, df_player['игрок'].unique()))
            if 'соперник' in list_player:
                foul_s = len(df_player[(df_player['вид'] == 'фол')
                                       & (df_player['точность'] == '+')
                                       & (df_player['игрок'] == 'соперник')])
                list_player.remove('соперник')

            b_all_s = len(df_player[(df_player['вид_в'] == 'б')]) + len(df_player[(df_player['вид_в'] == 'бул')])
            b_all_s_target = (len(df_player[(df_player['вид_в'] == 'б') & (df_player['точность_в'] == '+')])
                              + len(df_player[(df_player['вид_в'] == 'бул') & (df_player['точность_в'] == '+')]))
            g_all_s = len(df_player[(df_player['вид_в'] == 'б')
                                    & (df_player['точность_в'] == '+')
                                    & (df_player['результат_в'] == '+')])
            g_all_bul_s = len(df_player[(df_player['вид_в'] == 'бул')
                                        & (df_player['точность_в'] == '+')
                                        & (df_player['результат_в'] == '+')])
            info_opponent = {
                'foul_s': foul_s,
                'b_all_s': b_all_s,
                'b_all_s_target': b_all_s_target,
                'g_all_s': g_all_s,
                'g_all_bul_s': g_all_bul_s
            }
            list_goalie = list(filter(lambda x: type(x) is not float, df_player['вратарь'].unique()))
            list_goalie_s = list(filter(lambda x: type(x) is not float, df_player['вратарь_с'].unique()))

            for i in list_player:
                stat = {
                    'b_all': len(df_player[(df_player['вид'] == 'б')
                                           & (df_player['игрок'] == i)]),
                    'b_target': len(df_player[(df_player['вид'] == 'б')
                                              & (df_player['точность'] == '+')
                                              & (df_player['игрок'] == i)]),
                    'goal': len(df_player[(df_player['вид'] == 'б')
                                          & (df_player['точность'] == '+')
                                          & (df_player['результат'] == '+')
                                          & (df_player['игрок'] == i)]),
                    'p_all': len(df_player[(df_player['вид'] == 'п')
                                           & (df_player['игрок'] == i)]),
                    'p_target': len(df_player[(df_player['вид'] == 'п')
                                              & (df_player['точность'] == '+')
                                              & (df_player['игрок'] == i)]),
                    'foul': len(df_player[(df_player['вид'] == 'фол')
                                          & (df_player['точность'] == '+')
                                          & (df_player['игрок'] == i)]),
                    'vb_all': len(df_player[(df_player['вид'] == 'вб')
                                            & (df_player['игрок'] == i)]),
                    'vb_target': len(df_player[(df_player['вид'] == 'вб')
                                               & (df_player['точность'] == '+')
                                               & (df_player['игрок'] == i)]),
                    'mistake': len(df_player[(df_player['вид'] == 'ош')
                                             & (df_player['точность'] == '+')
                                             & (df_player['игрок'] == i)]),
                    'block': len(df_player[(df_player['вид'] == 'блок')
                                           & (df_player['точность'] == '+')
                                           & (df_player['игрок'] == i)]),
                    'bul': len(df_player[(df_player['вид'] == 'бул')
                                         & (df_player['точность'] == '+')
                                         & (df_player['игрок'] == i)]),
                    'bul_target': len(df_player[(df_player['вид'] == 'бул')
                                                & (df_player['точность'] == '+')
                                                & (df_player['результат'] == '+')
                                                & (df_player['игрок'] == i)]),
                    'assist': len(df_player[df_player['ассистент'] == i]),
                    'take_puck': len(df_player[(df_player['вид'] == 'отбор')
                                               & (df_player['точность'] == '+')
                                               & (df_player['игрок'] == i)]),
                    'kp': int(df_player.loc[df_player['игрок_кп'] == i, 'кп'].mean()),
                    }
                player_dict[i] = stat

            for i in list_goalie:
                stat = {
                    'b_target': len(df_player[(df_player['вид_в'] == 'б')
                                              & (df_player['точность_в'] == '+')
                                              & (df_player['вратарь'] == i)]),
                    'goal': len(df_player[(df_player['вид_в'] == 'б')
                                          & (df_player['точность_в'] == '+')
                                          & (df_player['результат_в'] == '+')
                                          & (df_player['вратарь'] == i)]),
                    'bul': len(df_player[(df_player['вид_в'] == 'бул')
                                         & (df_player['точность_в'] == '+')
                                         & (df_player['вратарь'] == i)]),
                    'bul_target': len(df_player[(df_player['вид_в'] == 'бул')
                                                & (df_player['точность_в'] == '+')
                                                & (df_player['результат_в'] == '+')
                                                & (df_player['вратарь'] == i)]),
                    }
                goalie_dict[i] = stat

            for i in list_goalie_s:
                stat = {
                    'b_target': len(df_player[(df_player['вид'] == 'б')
                                              & (df_player['точность'] == '+')
                                              & (df_player['вратарь_с'] == i)]),
                    'goal': len(df_player[(df_player['вид'] == 'б')
                                          & (df_player['точность'] == '+')
                                          & (df_player['результат'] == '+')
                                          & (df_player['вратарь_с'] == i)]),
                    'bul': len(df_player[(df_player['вид'] == 'бул')
                                         & (df_player['точность'] == '+')
                                         & (df_player['вратарь_с'] == i)]),
                    'bul_target': len(df_player[(df_player['вид'] == 'бул')
                                                & (df_player['точность'] == '+')
                                                & (df_player['результат'] == '+')
                                                & (df_player['вратарь_с'] == i)]),
                    }
                goalie_s_dict[i] = stat

            all_data = {'info_game': info_game, 'player_dict': player_dict, 'goalie_dict': goalie_dict,
                        'goalie_s_dic': goalie_s_dict, 'info_opponent': info_opponent}
            all_game[sheet_name] = all_data
    return all_game


if __name__ == '__main__':
    pprint(load_stat_of_game(full_path))
