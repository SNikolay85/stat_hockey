from time import timezone
from typing import Optional

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
game_fk = Annotated[int, mapped_column(ForeignKey('game.id', ondelete="CASCADE"))]
arena_fk = Annotated[int, mapped_column(ForeignKey('arena.id', ondelete="CASCADE"))]
game_player_fk = Annotated[int, mapped_column(ForeignKey('game_player.id', ondelete="CASCADE"))]

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
    id_arena: Mapped[arena_fk]
    __table_args__ = (UniqueConstraint('name_tournament', 'date_start', 'date_finish', name='tournament_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    games: Mapped[list['Game']] = relationship(back_populates='tournament')
    arena: Mapped['Arena'] = relationship(back_populates='tournaments')

    repr_cols_num = 4
    repr_cols = tuple()


class Point(Base):
    __tablename__ = 'point'

    id: Mapped[intpk]
    name_point: Mapped[str100] = mapped_column(unique=True)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    teams: Mapped[list['Team']] = relationship(back_populates='point')
    arenas: Mapped[list['Arena']] = relationship(back_populates='point')


class Arena(Base):
    __tablename__ = 'arena'

    id: Mapped[intpk]
    name_arena: Mapped[str100]
    id_point: Mapped[point_fk]
    __table_args__ = (UniqueConstraint('name_arena', 'id_point', name='arena_point_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    point: Mapped['Point'] = relationship(back_populates='arenas')
    tournaments: Mapped[list['Tournament']] = relationship(back_populates='arena')


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[intpk]
    name_team: Mapped[str100] = mapped_column(unique=True)
    id_point: Mapped[point_fk]
    __table_args__ = (UniqueConstraint('name_team', 'id_point', name='team_point_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    point: Mapped['Point'] = relationship(back_populates='teams')

    team_first: Mapped[list['Game']] = relationship(back_populates='first_team',
                                                    foreign_keys='[Game.id_first_team]')
    team_second: Mapped[list['Game']] = relationship(back_populates='second_team',
                                                     foreign_keys='[Game.id_second_team]')

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

    role: Mapped['Role'] = relationship(back_populates='players')
    game_players: Mapped[list['GamePlayer']] = relationship(back_populates='player')

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
    count: Mapped[int]
    id_player: Mapped[player_fk]
    id_game: Mapped[game_fk]
    __table_args__ = (UniqueConstraint('id_player', 'id_parameter', 'id_game',  name='stat_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    player: Mapped['Player'] = relationship(back_populates='stats')
    game: Mapped['Game'] = relationship(back_populates='stats')
    parameter: Mapped['Parameter'] = relationship(back_populates='stats')

    repr_cols_num = 5
    repr_cols = tuple()


class Game(Base):
    __tablename__ = 'game'

    id: Mapped[intpk]
    id_first_team: Mapped[team_fk]
    id_second_team: Mapped[team_fk]
    id_tournament: Mapped[tournament_fk]

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    first_team: Mapped['Team'] = relationship(back_populates='team_first', foreign_keys='[Game.id_first_team]')
    second_team: Mapped['Team'] = relationship(back_populates='team_second', foreign_keys='[Game.id_second_team]')

    tournament: Mapped['Tournament'] = relationship(back_populates='games')
    game_players: Mapped[list['GamePlayer']] = relationship(back_populates='game')

    repr_cols_num = 4
    repr_cols = tuple()


class GamePlayer(Base):
    __tablename__ = 'game_player'

    id: Mapped[intpk]
    id_game: Mapped[game_fk]
    id_player: Mapped[player_fk]
    __table_args__ = (UniqueConstraint('id_game', 'id_player', name='game_player_uc'),)

    created_on: Mapped[created_on]
    updated_on: Mapped[updated_on]

    game: Mapped['Game'] = relationship(back_populates='game_players')
    player: Mapped['Player'] = relationship(back_populates='game_players')


async def delete_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


async def create_tables():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

