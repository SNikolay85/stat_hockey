import asyncio
from datetime import datetime

import os
import json

from backend.src.models import Point, Team, TournamentTeam, Tournament, Player
from backend.src.models import Parameter, PlayerParameter, Session


current = os.getcwd()
file_name_base = '../download_stat.json'
full_path = os.path.join(current, file_name_base)

with open(full_path, 'r', encoding='utf-8') as file:
    data_base = json.load(file)


session = Session()


async def load_db(data_trans):
    for record in data_trans:
        if record['model'] == 'point':
            point = Point(
                id=record['fields']['id'],
                name_point=record['fields']['name_point']
            )
            session.add(point)
            await session.commit()
        elif record['model'] == 'team':
            team = Team(
                id=record['fields']['id'],
                name_team=record['fields']['name_team'],
                id_point=record['fields']['id_point']
            )
            session.add(team)
            await session.commit()
        elif record['model'] == 'tournament':
            date_format_start = datetime.strptime(record['fields']['date_start'], '%Y-%m-%d').date()
            date_format_finish = datetime.strptime(record['fields']['date_finish'], '%Y-%m-%d').date()
            tournament = Tournament(
                id=record['fields']['id'],
                name_tournament=record['fields']['name_tournament'],
                date_start=date_format_start,
                date_finish=date_format_finish,
                id_point=record['fields']['id_point']
            )
            session.add(tournament)
            await session.commit()
        elif record['model'] == 'tournament_team':
            tournament_team = TournamentTeam(
                id=record['fields']['id'],
                id_tournament=record['fields']['id_tournament'],
                id_team=record['fields']['id_team']
            )
            session.add(tournament_team)
            await session.commit()
        elif record['model'] == 'player':
            player = Player(
                id=record['fields']['id'],
                first_name=record['fields']['first_name'],
                last_name=record['fields']['last_name'],
                patronymic=record['fields']['patronymic'],
                id_team=record['fields']['id_team']
            )
            session.add(player)
            await session.commit()
        elif record['model'] == 'parameter':
            parameter = Parameter(
                id=record['fields']['id'],
                name=record['fields']['name']
            )
            session.add(parameter)
            await session.commit()
        elif record['model'] == 'player_parameter':
            player_parameter = PlayerParameter(
                id=record['fields']['id'],
                id_player=record['fields']['id_player'],
                id_parameter=record['fields']['id_parameter'],
                id_team=record['fields']['id_team'],
                count=record['fields']['count']
            )
            session.add(player_parameter)
            await session.commit()

    await asyncio.shield(session.close())
    return print('Данные считаны и загружены в БД')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(load_db(data_base))
