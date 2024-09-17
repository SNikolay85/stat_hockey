from sqlalchemy import select
import asyncio
import os
import json

from backend.src.models import Session, Point, Team, TournamentTeam, Tournament, Player
from backend.src.models import Parameter, PlayerParameter

from backend.src.schema import FullPoint, FullTeam, FullTournamentTeam, FullTournament, FullPlayer
from backend.src.schema import FullParameter, FullPlayerParameter

current = os.getcwd()
file_name_base = '../download_stat.json'
full_path = os.path.join(current, file_name_base)

async def download_all():
    all_data = []
    async with Session() as session:
        query = select(Point)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullPoint.model_validate(row, from_attributes=True) for row in models]
        for i in dto:
            dict_temp = {'model': 'point', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['name_point'] = i.name_point
            all_data.append(dict_temp)

        query = select(Team)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullTeam.model_validate(row, from_attributes=True) for row in models]
        for i in dto:
            dict_temp = {'model': 'team', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['name_team'] = i.name_team
            dict_temp['fields']['id_point'] = i.id_point
            all_data.append(dict_temp)

        query = select(Tournament)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullTournament.model_validate(row, from_attributes=True) for row in models]
        for i in dto:
            dict_temp = {'model': 'tournament', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['name_tournament'] = i.name_tournament
            dict_temp['fields']['date_start'] = str(i.date_start)
            dict_temp['fields']['date_finish'] = str(i.date_finish)
            dict_temp['fields']['id_point'] = i.id_point
            all_data.append(dict_temp)

        query = select(TournamentTeam)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullTournamentTeam.model_validate(row, from_attributes=True) for row in models]
        for i in dto:
            dict_temp = {'model': 'tournament_team', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['id_tournament'] = i.id_tournament
            dict_temp['fields']['id_team'] = i.id_team
            all_data.append(dict_temp)

        query = select(Player)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullPlayer.model_validate(row, from_attributes=True) for row in models]
        print(dto)
        for i in dto:
            dict_temp = {'model': 'player', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['first_name'] = i.first_name
            dict_temp['fields']['last_name'] = i.last_name
            dict_temp['fields']['patronymic'] = i.patronymic
            dict_temp['fields']['id_team'] = i.id_team
            all_data.append(dict_temp)

        query = select(Parameter)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullParameter.model_validate(row, from_attributes=True) for row in models]
        print(dto)
        for i in dto:
            dict_temp = {'model': 'parameter', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['name'] = i.name
            all_data.append(dict_temp)

        query = select(PlayerParameter)
        result = await session.execute(query)
        models = result.unique().scalars().all()
        dto = [FullPlayerParameter.model_validate(row, from_attributes=True) for row in models]
        for i in dto:
            dict_temp = {'model': 'player_parameter', 'fields': {}}
            dict_temp['fields']['id'] = i.id
            dict_temp['fields']['id_player'] = i.id_player
            dict_temp['fields']['id_parameter'] = i.id_parameter
            dict_temp['fields']['id_team'] = i.id_team
            dict_temp['fields']['count'] = i.count
            all_data.append(dict_temp)

        return all_data



if __name__ == '__main__':
    with open(full_path, "w") as write_file:
        json.dump(asyncio.get_event_loop().run_until_complete(download_all()), write_file)