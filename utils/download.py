from sqlalchemy import select
import asyncio
import os
import json

from backend.src.models import Session, Point, Team, TournamentTeam, Tournament, Player, Role
from backend.src.models import Parameter, PlayerParameter, PlayerTeam

current = os.getcwd()
file_name_base = '../download_stat.json'
full_path = os.path.join(current, file_name_base)


async def query_data(table):
    async with Session() as session:
        query = select(table)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        return models


async def download_all():
    all_data = []
    for i in await query_data(Point):
        dict_temp = {'model': 'point', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['name_point'] = i.name_point
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Team):
        dict_temp = {'model': 'team', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['name_team'] = i.name_team
        dict_temp['fields']['id_point'] = i.id_point
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Role):
        dict_temp = {'model': 'role', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['name_role'] = i.name_role
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Tournament):
        dict_temp = {'model': 'tournament', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['name_tournament'] = i.name_tournament
        dict_temp['fields']['date_start'] = str(i.date_start)
        dict_temp['fields']['date_finish'] = str(i.date_finish)
        dict_temp['fields']['id_point'] = i.id_point
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(TournamentTeam):
        dict_temp = {'model': 'tournament_team', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['id_tournament'] = i.id_tournament
        dict_temp['fields']['id_team'] = i.id_team
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Player):
        dict_temp = {'model': 'player', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['first_name'] = i.first_name
        dict_temp['fields']['last_name'] = i.last_name
        dict_temp['fields']['patronymic'] = i.patronymic
        dict_temp['fields']['birth'] = str(i.birth)
        dict_temp['fields']['id_role'] = i.id_role
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(PlayerTeam):
        dict_temp = {'model': 'player_team', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['id_player'] = i.id_player
        dict_temp['fields']['id_team'] = i.id_team
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(Parameter):
        dict_temp = {'model': 'parameter', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['name'] = i.name
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    for i in await query_data(PlayerParameter):
        dict_temp = {'model': 'player_parameter', 'fields': {}}
        dict_temp['fields']['id'] = i.id
        dict_temp['fields']['id_player'] = i.id_player
        dict_temp['fields']['id_parameter'] = i.id_parameter
        dict_temp['fields']['id_team'] = i.id_team
        dict_temp['fields']['count'] = i.count
        dict_temp['fields']['created_on'] = str(i.created_on)
        dict_temp['fields']['updated_on'] = str(i.updated_on)
        all_data.append(dict_temp)

    return all_data


if __name__ == '__main__':
    with open(full_path, "w") as write_file:
        json.dump(asyncio.get_event_loop().run_until_complete(download_all()), write_file)
