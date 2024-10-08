from backend.src.reposit import DataGet
from fastapi import APIRouter

router_stat = APIRouter(prefix='/stat', tags=['Stat'])


@router_stat.get('/{tournament}/{team}/{player}')
async def get_stat(tournament, team, player):
    stat = await DataGet.find_stat(tournament, team, player)
    return {
        'player': stat[1],
        'shot': stat[0][0],
        'shot_ac': stat[0][1],
        'goal': stat[0][2],
        'pas': stat[0][3],
        'pas_ac': stat[0][4],
        'face_off': stat[0][5],
        'face_off_ac': stat[0][6],
        'block': stat[0][7],
        'mistake': stat[0][8],
        'penalty': stat[0][9],
        'shootout': stat[0][10],
        'shootout_ac': stat[0][11],
        'shootout_goal': stat[0][12]
    }
