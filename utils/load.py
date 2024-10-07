import asyncio
from datetime import datetime

import os
import json

from backend.src.models import Point, Team, TournamentTeam, Tournament, Player, Role, PlayerTeam
from backend.src.models import Parameter, PlayerParameter, Session, create_tables, delete_tables


current = os.getcwd()
file_name_base = '../download_stat.json'
full_path = os.path.join(current, file_name_base)

with open(full_path, 'r', encoding='utf-8') as file:
    data_base = json.load(file)


session = Session()


async def reboot_tables():
    await delete_tables()
    await create_tables()


def format_date(date_cut=None, date_time=None, date=None):
    if date is not None:
        return datetime.strptime(date, '%Y-%m-%d').date()
    elif date_time is not None:
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S.%f%z')
    else:
        return datetime.strptime(date_cut, '%Y-%m-%d %H:%M:%S')


async def load_db(data_stat):
    for record in data_stat:
        if record['model'] == 'point':
            point = Point(
                id=record['fields']['id'],
                name_point=record['fields']['name_point'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(point)
            await session.commit()
        elif record['model'] == 'role':
            role = Role(
                id=record['fields']['id'],
                name_role=record['fields']['name_role'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(role)
            await session.commit()
        elif record['model'] == 'team':
            team = Team(
                id=record['fields']['id'],
                name_team=record['fields']['name_team'],
                id_point=record['fields']['id_point'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(team)
            await session.commit()
        elif record['model'] == 'tournament':
            tournament = Tournament(
                id=record['fields']['id'],
                name_tournament=record['fields']['name_tournament'],
                date_start=format_date(date=record['fields']['date_start']),
                date_finish=format_date(date=record['fields']['date_finish']),
                id_point=record['fields']['id_point'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(tournament)
            await session.commit()
        elif record['model'] == 'tournament_team':
            tournament_team = TournamentTeam(
                id=record['fields']['id'],
                id_tournament=record['fields']['id_tournament'],
                id_team=record['fields']['id_team'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(tournament_team)
            await session.commit()
        elif record['model'] == 'player':
            player = Player(
                id=record['fields']['id'],
                first_name=record['fields']['first_name'],
                last_name=record['fields']['last_name'],
                patronymic=record['fields']['patronymic'],
                birth=format_date(date=record['fields']['birth']),
                id_role=record['fields']['id_role'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(player)
            await session.commit()
        elif record['model'] == 'player_team':
            player_team = PlayerTeam(
                id=record['fields']['id'],
                id_player=record['fields']['id_player'],
                id_team=record['fields']['id_team'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(player_team)
            await session.commit()
        elif record['model'] == 'parameter':
            parameter = Parameter(
                id=record['fields']['id'],
                name=record['fields']['name'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(parameter)
            await session.commit()
        elif record['model'] == 'player_parameter':
            player_parameter = PlayerParameter(
                id=record['fields']['id'],
                id_player=record['fields']['id_player'],
                id_parameter=record['fields']['id_parameter'],
                id_team=record['fields']['id_team'],
                count=record['fields']['count'],
                created_on=format_date(date_time=record['fields']['created_on']),
                updated_on=format_date(date_time=record['fields']['updated_on'])
            )
            session.add(player_parameter)
            await session.commit()

    await asyncio.shield(session.close())
    return print('Данные считаны и загружены в БД')

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(reboot_tables())
    print('Таблицы пересозданы')
    asyncio.get_event_loop().run_until_complete(load_db(data_base))
