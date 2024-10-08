from backend.src.reposit import DataGet
from fastapi import APIRouter

router_stat = APIRouter(prefix='/stat', tags=['Stat'])


@router_stat.get('/')
async def get_stat():
    stat = await DataGet.find_stat(2, 1)
    return stat