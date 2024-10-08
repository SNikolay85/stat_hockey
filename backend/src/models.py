from time import timezone
from typing import Optional

from cryptography.hazmat.backends.openssl import backend
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import Float, String, ForeignKey, MetaData, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from datetime import datetime, date

from typing_extensions import Annotated

from config import PG_DB, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(PG_DSN, echo=True)

Session = async_sessionmaker(engine, expire_on_commit=False)

my_metadata = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True)]
point_fk = Annotated[int, mapped_column(ForeignKey('point.id', ondelete="CASCADE"))]
team_fk = Annotated[int, mapped_column(ForeignKey('team.id', ondelete="CASCADE"))]
tournament_fk = Annotated[int, mapped_column(ForeignKey('tournament.id', ondelete="CASCADE"))]
player_fk = Annotated[int, mapped_column(ForeignKey('player.id', ondelete="CASCADE"))]
parameter_fk = Annotated[int, mapped_column(ForeignKey('parameter.id', ondelete="CASCADE"))]
role_fk = Annotated[int, mapped_column(ForeignKey('role.id', ondelete="CASCADE"))]
tournament_team_fk = Annotated[int, mapped_column(ForeignKey('tournament_team.id', ondelete="CASCADE"))]
tournament_player_fk = Annotated[int, mapped_column(ForeignKey('tournament_player.id', ondelete="CASCADE"))]


str100 = Annotated[str, 100]
str20 = Annotated[str, 20]
str50 = Annotated[str, 50]
date = Annotated[date, mapped_column(Date)]
date_full = Annotated[datetime, mapped_column(DateTime)]

created_on = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
updated_on = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())]


class Base(DeclarativeBase):
    metadata = my_metadata
    type_annotation_map = {
        str100: String(100),
        str20: String(20),
        str50: String(50),
    }

    repr_cols_num = 2
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'


class Tournament(Base):
    __tablename__ = 'tournament'

    id: Mapped[intpk]
    name_tournament: Mapped[str100] = mapped_column(unique=True)
    date_start: Mapped[date]
    date_finish: Mapped[date]
    id_point: Mapped[point_fk]
    __table_args__ = (UniqueConstraint('name_tournament', 'date_start', 'date_finish', name='tournament_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    tournament_teams: Mapped[list['TournamentTeam']] = relationship(back_populates='tournament')
    point: Mapped['Point'] = relationship(back_populates='tournaments')

    repr_cols_num = 4
    repr_cols = tuple()


class Point(Base):
    __tablename__ = 'point'

    id: Mapped[intpk]
    name_point: Mapped[str100] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    teams: Mapped[list['Team']] = relationship(back_populates='point')
    tournaments: Mapped[list['Tournament']] = relationship(back_populates='point')

    repr_cols_num = 2
    repr_cols = tuple()


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[intpk]
    name_team: Mapped[str100] = mapped_column(unique=True)
    id_point: Mapped[point_fk]
    __table_args__ = (UniqueConstraint('name_team', 'id_point', name='team_point_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    point: Mapped['Point'] = relationship(back_populates='teams')
    tournament_teams: Mapped[list['TournamentTeam']] = relationship(back_populates='team')

    repr_cols_num = 3
    repr_cols = tuple()


class TournamentTeam(Base):
    __tablename__ = 'tournament_team'

    id: Mapped[intpk]
    id_tournament: Mapped[tournament_fk]
    id_team: Mapped[team_fk]
    __table_args__ = (UniqueConstraint('id_tournament', 'id_team', name='tournament_team_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    tournament: Mapped['Tournament'] = relationship(back_populates='tournament_teams')
    team: Mapped['Team'] = relationship(back_populates='tournament_teams')
    tournament_players: Mapped[list['TournamentPlayer']] = relationship(back_populates='tournament_team')


    repr_cols_num = 3
    repr_cols = tuple()


class TournamentPlayer(Base):
    __tablename__ = 'tournament_player'

    id: Mapped[intpk]
    id_player: Mapped[player_fk]
    id_tournament_team: Mapped[tournament_team_fk]
    __table_args__ = (UniqueConstraint('id_player', 'id_tournament_team', name='tournament_player_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    stats_player: Mapped[list['Stat']] = relationship(back_populates='player_stat',
                                                      foreign_keys='[Stat.id_player]')
    stats_assistant: Mapped[list['Stat']] = relationship(back_populates='assistant_stat',
                                                       foreign_keys='[Stat.id_assistant]')

    player: Mapped['Player'] = relationship(back_populates='tournament_players')
    tournament_team: Mapped['TournamentTeam'] = relationship(back_populates='tournament_players')

    repr_cols_num = 3
    repr_cols = tuple()


class Role(Base):
    __tablename__ = 'role'

    id: Mapped[intpk]
    name_role: Mapped[str50] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    players: Mapped[list['Player']] = relationship(back_populates='role')


class Player(Base):
    __tablename__ = 'player'

    id: Mapped[intpk]
    first_name: Mapped[str50]
    last_name: Mapped[str50]
    patronymic: Mapped[str50]
    birth: Mapped[date]
    id_role: Mapped[role_fk]
    __table_args__ = (UniqueConstraint('first_name', 'last_name', 'patronymic', 'birth', 'id_role',  name='player_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    tournament_players: Mapped[list['TournamentPlayer']] = relationship(back_populates='player')
    role: Mapped['Role'] = relationship(back_populates='players')

    repr_cols_num = 4
    repr_cols = tuple()


class Parameter(Base):
    __tablename__ = 'parameter'

    id: Mapped[intpk]
    name: Mapped[str50] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    stats: Mapped[list['Stat']] = relationship(back_populates='parameter')


class Stat(Base):
    __tablename__ = 'stat'

    id: Mapped[intpk]
    id_parameter: Mapped[parameter_fk]
    accuracy: Mapped[bool]
    result: Mapped[bool] = mapped_column(nullable=True)
    id_player: Mapped[tournament_player_fk]
    id_assistant: Mapped[tournament_player_fk] = mapped_column(nullable=True)
    #__table_args__ = (UniqueConstraint('id_player', 'id_parameter', 'id_team',  name='player_parameter_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    player_stat: Mapped['TournamentPlayer'] = relationship(back_populates='stats_player', foreign_keys='[Stat.id_player]')
    assistant_stat: Mapped['TournamentPlayer'] = relationship(back_populates='stats_assistant', foreign_keys='[Stat.id_assistant]')
    parameter: Mapped['Parameter'] = relationship(back_populates='stats')

    repr_cols_num = 4
    repr_cols = tuple()


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

