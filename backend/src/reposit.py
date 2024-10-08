from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from backend.src.models import Session, Point, Player, Team, Role, Parameter, Tournament
from backend.src.models import TournamentPlayer, TournamentTeam, Stat
from backend.src.schema import PlayerAdd, PlayerRe


class UtilityFunction:
    @classmethod
    async def stat_params(cls) -> dict:
        async with Session() as session:
            result = await session.execute(select(Parameter))
            models = result.unique().scalars().all()
            dict_params = {i.name: i.id for i in models}
            return dict_params

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
        async with Session() as session:
            query = (
                select(TournamentTeam.id)
                .filter(and_(TournamentTeam.id_tournament == int(tournament),
                             TournamentTeam.id_team == int(team)))
            )
            result = await session.execute(query)
            models = result.unique().scalars().first()

            query = (
                select(TournamentPlayer.id)
                .filter(and_(TournamentPlayer.id_tournament_team == models),
                        TournamentPlayer.id_player == int(player))
            )
            result = await session.execute(query)
            models = result.unique().scalars().first()
            if models is None:
                raise HTTPException(status_code=422, detail='Данного игрока нет в заявке')
            query = (
                select(Stat)
                .filter(Stat.id_player == models)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            res = await UtilityFunction.all_param(models)
            name_player = await UtilityFunction.get_name_player(int(player))
            return res, name_player

