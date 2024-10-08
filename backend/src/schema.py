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
    players: list['FullPlayer']
    tournaments: list['FullTournament']


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
    point: 'FullPoint'


# --------------------------
# schemes for model Team
class TeamAdd(BaseModel):
    name_team: str
    id_point: int


class FullTeam(TeamAdd):
    id: int


class FullTeamRe(FullTeam):
    point: FullPoint
    players: list['FullPlayer']


# --------------------------
# schemes for model TournamentTeam
class TournamentTeamAdd(BaseModel):
    id_tournament: int
    id_team: int


class FullTournamentTeam(TournamentTeamAdd):
    id: int


# --------------------------
# schemes for model PlayerTeam
class PlayerTeamAdd(BaseModel):
    id_player: int
    id_team: int


class FullPlayerTeam(PlayerTeamAdd):
    id: int


# --------------------------
# schemes for model Player
class PlayerAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    birth: date


class FullPlayer(PlayerAdd):
    id: int

class PlayerRe(PlayerAdd):
    role: 'RoleAdd'


# --------------------------
# schemes for model Parameter
class ParameterAdd(BaseModel):
    name: str


class FullParameter(ParameterAdd):
    id: int


# --------------------------
# schemes for model PlayerParameter
class PlayerParameterAdd(BaseModel):
    id_player: int
    id_parameter: int
    id_team: int
    count: int


class FullPlayerParameter(PlayerParameterAdd):
    id: int


# --------------------------
# schemes for modelRole
class RoleAdd(BaseModel):
    name_role: str


class FullRole(RoleAdd):
    id: int



