import asyncio
from datetime import datetime
from sqlalchemy import select, and_

import os
import json
import pandas as pd

from backend.src.schema import GameAdd
from utils.load_game_from_excell import load_stat_of_game

from backend.src.models import Point, Team, Arena, Tournament, Player, Role, GamePlayer, Game
from backend.src.models import Parameter, Stat, Session, create_tables, delete_tables


# session = Session()
# data_base = load_stat_of_game()

# async def reboot_tables():
#     await delete_tables()
#     await create_tables()


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
        date_game = info[0].date()
        print(date_game)
        data = GameAdd(id_first_team=first_team,
                       id_second_team=second_team,
                       date_game=date_game,
                       id_tournament=id_tournament)
        if await cls.check_double_game(data):
            await DataLoads.add_game(data)
            return 'success'
        else:
            return 'такая игра уже есть в базе'


class DataLoads:
    @classmethod
    async def add_game(cls, data: GameAdd) -> dict:
        async with Session() as session:
            query = select(Game.id)
            result = await session.execute(query)
            models = result.unique().scalars().all()
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


async def load_db(id_tournament):
    base = load_stat_of_game()
    for record in base.keys():
        info_game = base[record]['info_game']
        print(info_game)
        await UtilityFunction.fff(id_tournament, info_game)

    return print('Данные считаны и загружены в БД')

if __name__ == '__main__':
    # asyncio.get_event_loop().run_until_complete(reboot_tables())
    print('Таблицы пересозданы')
    # asyncio.get_event_loop().run_until_complete(load_db(1))
