from sqlalchemy import select, and_

from backend.src.models import Session, Point, Player, Team, Role, Parameter, Tournament
from backend.src.models import TournamentPlayer, TournamentTeam, Stat



class CountStat:
    @classmethod
    async def stat_params(cls):
        async with (Session() as session):
            result = await session.execute(select(Parameter))
            models = result.unique().scalars().all()
            return models


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

        a = await CountStat.stat_params()
        # for i in a:
        #     print(i.)
        s = {'бросок': 1, 'пас': 2}

        for i in list_stat:
            if i.id_parameter == s['бросок']:
                shot += 1
                if i.accuracy:
                    shot_ac += 1
                if i.result:
                    goal += 1
            elif i.id_parameter == 2:
                pas += 1
                if i.accuracy:
                    pas_ac += 1
            elif i.id_parameter == 3:
                face_off += 1
                if i.accuracy:
                    face_off_ac += 1
            elif i.id_parameter == 4:
                block += 1
            elif i.id_parameter == 5:
                mistake += 1
            elif i.id_parameter == 6:
                penalty += 1
            elif i.id_parameter == 7:
                shootout += 1
                if i.accuracy:
                    shootout_ac += 1
                if i.result:
                    shootout_goal += 1
        return shot, shot_ac, goal, pas, pas_ac, face_off, face_off_ac, block, mistake, penalty, shootout, shootout_ac, shootout_goal

class DataGet:
    @staticmethod
    async def find_stat(tournament: int, team: int):
        async with Session() as session:
            query = (
                select(TournamentTeam.id)
                .filter(and_(TournamentTeam.id_tournament == tournament,
                             TournamentTeam.id_team == team))
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()

            query = (
                select(TournamentPlayer.id)
                .filter(and_(TournamentPlayer.id_tournament_team == models[0]),
                        TournamentPlayer.id_player == 2)
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            query = (
                select(Stat)
                .filter(Stat.id_player == models[0])
            )
            result = await session.execute(query)
            models = result.unique().scalars().all()
            res = await CountStat.all_param(models)
            return (f'Dushaev: '
                    f'бросоков всего = {res[0]}'
                    f'бросков в створ = {res[1]}'
                    f'голы = {res[2]}'
                    f'пасов всего = {res[3]}'
                    f'точных пасов = {res[4]}')

