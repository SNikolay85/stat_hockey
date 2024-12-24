from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend.src.router import router_stat as stat


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print('Server started, Redis run')
    yield
    print('Выключение')


app_stat = FastAPI(title='Statistics', lifespan=lifespan)


app_stat.include_router(stat)


origins = [
    'http://localhost:8000',
    'http://localhost:8001',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8001',
]

app_stat.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"],
    allow_headers=["Set-Cookie", "Access-Control-Allow-Headers", "Authorization", "Accept", "Accept-Language", "Content-Language", "Content-Type"],
)


# if __name__ == '__main__':
#     uvicorn.run(app_route, host="0.0.0.0", port=8000, log_level="info")

# uvicorn trips.main:app_route --host 0.0.0.0 --port 8000 --reload