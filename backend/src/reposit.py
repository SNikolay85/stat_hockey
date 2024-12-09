import json
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from backend.src.models import Session, Point, Player, Team, Role, Parameter, Tournament
from backend.src.models import GamePlayer, Game, Arena, Stat
from backend.src.schema import PlayerAdd, PlayerRe, GameAdd

import os
import pandas as pd


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
    async def check_double_game(data: GameAdd) -> bool:
        async with Session() as session:
            a, b = data.id_first_team, data.id_second_team
            id_tournament = data.id_tournament
            date_game = data.date_game
            one = await session.execute(select(Game).filter(Game.id_first_team == int(a),
                                                            Game.id_second_team == int(b),
                                                            Game.id_tournament == id_tournament,
                                                            Game.date_game == date_game))
            one_way = one.unique().scalars().first()
            two = await session.execute(select(Game).filter(Game.id_first_team == int(b),
                                                             Game.id_second_team == int(a),
                                                            Game.id_tournament == id_tournament,
                                                            Game.date_game == date_game))
            other_way = two.unique().scalars().first()
            if one_way is None and other_way is None:
                return True
            else:
                return False

    @classmethod
    async def fff(cls, id_tournament: int, info: list):
        first_team = await cls.get_id_team(info[1])
        second_team = await cls.get_id_team(info[2])
        date_game = info[0]
        data = GameAdd(id_first_team=first_team,
                       id_second_team=second_team,
                       date_game=cls.format_date(date=date_game),
                       id_tournament=id_tournament)
        if await cls.check_double_game(data):
            return data
            # await DataLoad.add_game(data)
        else:
            return 'такая игра уже есть в базе'


class UtilityFunctions:
    @classmethod
    async def stat_params(cls) -> dict:
        async with Session() as session:
            result = await session.execute(select(Parameter))
            models = result.unique().scalars().all()
            dict_params = {i.name: i.id for i in models}
            return dict_params

    @classmethod
    async def get_id_team(cls, name: str) -> int:
        async with Session() as session:
            result = await session.execute(select(Team.id))
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

    @classmethod
    async def all_param(cls, list_stat: list):
        shot = 0
        shot_ac = 0
        goal = 0
        pas = 0
        pas_ac = 0
        face_off = 0
        face_off_ac = 0
        block = 0
        mistake = 0
        penalty = 0
        shootout = 0
        shootout_ac = 0
        shootout_goal = 0

        dict_params = await UtilityFunction.stat_params()
        for i in list_stat:
            if i.id_parameter == dict_params['Бросок']:
                shot += 1
                if i.accuracy:
                    shot_ac += 1
                if i.result:
                    goal += 1
            elif i.id_parameter == dict_params['Пас']:
                pas += 1
                if i.accuracy:
                    pas_ac += 1
            elif i.id_parameter == dict_params['Вбрасывание']:
                face_off += 1
                if i.accuracy:
                    face_off_ac += 1
            elif i.id_parameter == dict_params['Блокировка']:
                block += 1
            elif i.id_parameter == dict_params['Ошибка']:
                mistake += 1
            elif i.id_parameter == dict_params['Штраф']:
                penalty += 1
            elif i.id_parameter == dict_params['Буллит']:
                shootout += 1
                if i.accuracy:
                    shootout_ac += 1
                if i.result:
                    shootout_goal += 1
        return shot, shot_ac, goal, pas, pas_ac, face_off, face_off_ac, block, mistake, penalty, shootout, shootout_ac, shootout_goal


class DataGet:
    @staticmethod
    async def find_stat(tournament: int, team: int, player: int):
        pass


class DataLoad:
    @staticmethod
    async def load_game(id_tournament):
        data_base = await get_data()
        for record in data_base.keys():
            info_game = data_base[record]['info_game']
            print(info_game)
            dd = await UtilityFunction.fff(id_tournament, info_game)
            # print(dd)
            if type(dd) is not str:
                # print(dd)
                await DataLoad.add_game(dd)
        return print('Данные считаны и загружены в БД')

    @classmethod
    async def add_game(cls, data: GameAdd) -> dict:
        async with Session() as session:
            query = select(Game.id)
            result = await session.execute(query)
            models = result.unique().scalars().all()
            print(data)
            game = Game(**(data.model_dump()), id=await UtilityFunction.get_id(models))
            session.add(game)
            await session.flush()
            await session.commit()
            return {
                "id": game.id,
                "id_first_team": game.first_team,
                "id_second_team": game.second_team,
                "date_game": game.date_game,
                "id_tournament": game.id_tournament
            }


