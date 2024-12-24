import json
import os
import shutil
import pandas as pd

from starlette import status

from backend.src.reposit import DataGet, DataLoad, UtilityFunctions
from fastapi import APIRouter, UploadFile, HTTPException

# from utils.load_game_from_excell import load_stat_of_game
from utils import load_game_from_excell
# from utils.load_game_to_base import load_db

router_stat = APIRouter(prefix='/stat', tags=['Stat'])


@router_stat.get('/{tournament}')
async def add_game(tournament):
    game = await DataLoad.load_game(tournament)
    return game


@router_stat.get('/stat')
async def get_stat():
    return UtilityFunctions.load_stat_of_game()


@router_stat.post('/add_stat', status_code=status.HTTP_200_OK)
async def add_stat(file: UploadFile):
    if file.content_type not in [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f'File {file.filename} не поддерживается!',
        )
    with open(f"backend/static/stat.xlsx", "wb+") as stat:
        shutil.copyfileobj(file.file, stat)
    return f'{file.filename} успешно загружен'


# @router_stat.get('/{tournament}/{team}/{player}')
# async def get_stat(tournament, team, player):
#     stat = await DataGet.find_stat(tournament, team, player)
#     return {
#         'player': stat[1],
#         'shot': stat[0][0],
#         'shot_ac': stat[0][1],
#         'goal': stat[0][2],
#         'pas': stat[0][3],
#         'pas_ac': stat[0][4],
#         'face_off': stat[0][5],
#         'face_off_ac': stat[0][6],
#         'block': stat[0][7],
#         'mistake': stat[0][8],
#         'penalty': stat[0][9],
#         'shootout': stat[0][10],
#         'shootout_ac': stat[0][11],
#         'shootout_goal': stat[0][12]
#     }
