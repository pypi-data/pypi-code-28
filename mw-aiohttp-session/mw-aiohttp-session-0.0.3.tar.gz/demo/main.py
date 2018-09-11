import asyncio
import aioredis
import time
from mw_aiohttp_session import mw_setup_handle_session_middleware

from aiohttp import web



async def handler(request):
    # session = await get_session(request)

    return web.Response(text='hello')


async def make_redis_pool():
    redis_address = ('192.168.101.70', '6380')
    return await aioredis.create_redis_pool(redis_address, timeout=1)


def make_app():
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())


    async def dispose_redis_pool(app):
        redis_pool.close()
        await redis_pool.wait_closed()

    app = web.Application()
    mw_setup_handle_session_middleware(app,redis_pool)
    app.on_cleanup.append(dispose_redis_pool)
    app.router.add_get('/', handler)
    return app


web.run_app(make_app())