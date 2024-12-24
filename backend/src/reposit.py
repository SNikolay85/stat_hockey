import json
from datetime import datetime
import os
import pandas as pd


from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from backend.src.models import Session, Point, Player, Team, Role, Parameter, Tournament
from backend.src.models import GamePlayer, Game, Arena, Stat
from backend.src.schema import PlayerAdd, PlayerRe, GameAdd


async def get_data():
    current = os.getcwd()
    file_name_base = r'data.json'
    full_path = os.path.join(current, file_name_base)
    with open(full_path, 'r', encoding='utf-8') as file:
        data_base = json.load(file)
        return data_base


class UtilityFunction:
    @staticmethod
    def format_date(date_cut=None, date_time=None, date=None):
        if date is not None:
            return datetime.strptime(date, '%Y-%m-%d').date()
        elif date_time is not None:
            return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            return datetime.strptime(date_cut, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    async def get_id(list_id: list) -> int:
        return max(list_id) + 1 if len(list_id) != 0 else 1

    @staticmethod
    async def get_id_team(name: str) -> int:
        async with Session() as session:
            result = await session.execute(
                select(Team.id)
                .filter(Team.name_team == name))
            models = result.unique().scalars().first()
            return models

    @staticmethod
    async def get_id_parameter(name: str) -> int:
        async with Session() as session:
            result = await session.execute(
                select(Parameter.id)
                .filter(Parameter.name == name))
            models = result.unique().scalars().first()
            return models

    @staticmethod
    async def check_double_game(id_tournament: int, info: list):
        first_team = await UtilityFunction.get_id_team(info[1])
        second_team = await UtilityFunction.get_id_team(info[2])
        date_game = info[0]
        data = GameAdd(id_first_team=first_team,
                       id_second_team=second_team,
                       date_game=UtilityFunction.format_date(date=date_game),
                       id_tournament=id_tournament)
        async with Session() as session:
            a, b = data.id_first_team, data.id_second_team
            id_tournament = data.id_tournament
            date_game = data.date_game
            one = await session.execute(select(Game).filter(Game.id_first_team == int(a),
                                                            Game.id_second_team == int(b),
                                                            Game.id_tournament == id_tournament,
                                                            Game.date_game == date_game))
            one_game = one.unique().scalars().first()
            two = await session.execute(select(Game).filter(Game.id_first_team == int(b),
                                                            Game.id_second_team == int(a),
                                                            Game.id_tournament == id_tournament,
                                                            Game.date_game == date_game))
            other_game = two.unique().scalars().first()
            if one_game is None and other_game is None:
                return data

    # @classmethod
    # async def fff(cls, id_tournament: int, info: list):
    #     first_team = await cls.get_id_team(info[1])
    #     second_team = await cls.get_id_team(info[2])
    #     date_game = info[0]
    #     data = GameAdd(id_first_team=first_team,
    #                    id_second_team=second_team,
    #                    date_game=cls.format_date(date=date_game),
    #                    id_tournament=id_tournament)
        # if await cls.check_double_game(data):
        #     return True
        #     # return data
        #     # game = await DataLoad.add_game(data)
        #     # return f'{game} игра загружена'
        # else:
        #     return False
            # return 'такая игра уже есть в базе'


class UtilityFunctions:
    @classmethod
    async def stat_params(cls) -> dict:
        async with Session() as session:
            result = await session.execute(select(Parameter))
            models = result.unique().scalars().all()
            dict_params = {i.name: i.id for i in models}
            return dict_params


    @classmethod
    async def get_id_parameter(cls, name: str) -> int:
        async with Session() as session:
            result = await session.execute(select(Parameter.id))
            models = result.unique().scalars().first()
            return models

    @classmethod
    async def get_name_player(cls, id_player):
        async with Session() as session:
            result = await session.execute(
                select(Player)
                .options(joinedload(Player.role))
                .filter(Player.id == id_player))
            models = result.unique().scalars().all()
            dto = [PlayerRe.model_validate(row, from_attributes=True) for row in models]
            return dto

    @staticmethod
    def load_stat_of_game():
        xl = pd.ExcelFile('backend/static/stat.xlsx')
        all_game = {}
        for sheet_name in xl.sheet_names:
            foul_s = 0
            player_dict = {}
            goalie_dict = {}
            goalie_s_dict = {}
            if 'game' in sheet_name:
                df_player = xl.parse(sheet_name, usecols='B:P', header=1, nrows=200)
                df_game = xl.parse(sheet_name, usecols='B, D, G')
                info_game = list(
                    map(lambda x: str(x.date()) if type(x) is datetime else x, list(df_game.head(0))))
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


class DataGet:
    @staticmethod
    async def find_stat(tournament: int, team: int, player: int):
        pass


class DataLoad:
    @staticmethod
    async def load_game(id_tournament):
        data_base = UtilityFunctions.load_stat_of_game()
        for record in data_base.keys():
            info_game = data_base[record]['info_game']
        #     print(info_game)
            ghgh = await UtilityFunction.check_double_game(id_tournament, info_game)
            if ghgh is not None:
                ss = await DataLoad.add_game(ghgh)
                param = data_base[record]['player_dict']
                for parameter in param.keys():
                    print(parameter)
                print(ss)
            else:
                print('pass')
                continue
        #     # print(dd)
        #     if type(dd) is not str:
        #         # print(dd)
        #         await DataLoad.add_game(dd)

            # return dd
        # return data_base
        return print('Данные считаны и загружены в БД')

    # @classmethod
    # async def add_player_stat(cls, data: dict):
    #     id_parameter = await UtilityFunction.get_id_team(info[1])
    #     second_team = await UtilityFunction.get_id_team(info[2])
    #     date_game = info[0]
    #     data = GameAdd(id_first_team=first_team,
    #                    id_second_team=second_team,
    #                    date_game=UtilityFunction.format_date(date=date_game),
    #                    id_tournament=id_tournament)
    #     async with Session() as session:
    #         query = select(Stat.id)
    #         result = await session.execute(query)
    #         models = result.unique().scalars().all()
    #         stat = Stat(**(data.model_dump()), id=await UtilityFunction.get_id(models))

    @classmethod
    async def add_game(cls, data: GameAdd):
        async with Session() as session:
            query = select(Game.id)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            print(data)
            game = Game(**(data.model_dump()), id=await UtilityFunction.get_id(models))
            session.add(game)
            await session.flush()
            await session.commit()
            return game.id
            # return {
            #     "id": game.id,
            #     "id_first_team": game.first_team,
            #     "id_second_team": game.second_team,
            #     "date_game": game.date_game,
            #     "id_tournament": game.id_tournament
            # }


