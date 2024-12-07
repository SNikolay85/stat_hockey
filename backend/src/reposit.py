from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from backend.src.models import Session, Point, Player, Team, Role, Parameter, Tournament
from backend.src.models import GamePlayer, Game, Arena, Stat
from backend.src.schema import PlayerAdd, PlayerRe
from utils.load_game_from_excell import load_stat_of_game
import os
import pandas as pd

# current = os.getcwd()
# file_name_base = r'..\stat_xls\stat.xlsx'
# full_path = os.path.join(current, file_name_base)

#
# xl = pd.ExcelFile(full_path)


class UtilityFunction:
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
        current = os.getcwd()
        file_name_base = r'stat_xls/stat.xlsx'
        full_path = os.path.join(current, file_name_base)
        # full_path = r'\//wsl.localhost/Ubuntu - 22.04/home/nikolay_speshilov/stat_hockey/stat_xls/stat.xlsx'
        # file_name_base = r'stat_xls/stat.xlsx'
        # data_base = load_stat_of_game(full_path)
        return full_path#data_base


