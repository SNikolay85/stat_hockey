from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

'''
gt - больше, чем
lt - меньше, чем
ge - больше или равно
le - меньше или равно
multiple_of - кратно заданному числу
allow_inf_nan - разрешать 'inf', '-inf', 'nan' значения
'''


# --------------------------
# schemes for model Point
class PointAdd(BaseModel):
    name_point: str = Field(max_lenght=100)


class FullPoint(PointAdd):
    id: int


class FullPointRe(FullPoint):
    teams: list['FullTeam']
    arenas: list['FullPlayer']


# --------------------------
# schemes for model Arena
class ArenaAdd(BaseModel):
    name_arena: str = Field(max_lenght=100)


class FullArena(ArenaAdd):
    id: int


class FullArenaRe(FullArena):
    point: 'FullPoint'
    tournaments: list['FullTournament']


# --------------------------
# schemes for model Game
class GameAdd(BaseModel):
    id_first_team: int
    id_second_team: int
    id_tournament: int


class FullGame(GameAdd):
    id: int


class FullGameRe(FullGame):
    tournament: 'FullTournament'


# --------------------------
# schemes for model Tournament
class TournamentAdd(BaseModel):
    name_tournament: str
    date_start: date
    date_finish: date
    id_point: int


class FullTournament(TournamentAdd):
    id: int


class FullTournamentRe(FullTournament):
    games: list['FullGame']
    arena: 'FullArena'


# --------------------------
# schemes for model Team
class TeamAdd(BaseModel):
    name_team: str
    id_point: int


class FullTeam(TeamAdd):
    id: int


class FullTeamRe(FullTeam):
    point: FullPoint


# --------------------------
# schemes for model Player
class PlayerAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    birth: date
    id_role: int


class FullPlayer(PlayerAdd):
    id: int


class PlayerRe(PlayerAdd):
    role: 'FullRole'


# --------------------------
# schemes for model Parameter
class ParameterAdd(BaseModel):
    name: str


class FullParameter(ParameterAdd):
    id: int


# --------------------------
# schemes for modelRole
class RoleAdd(BaseModel):
    name_role: str


class FullRole(RoleAdd):
    id: int
