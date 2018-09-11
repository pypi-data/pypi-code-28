__author__ = 'candyabc'
__email__ = 'hfcandyabc@163.com'

__all__ = ["mw_setup_session_middleware",
           "get_session",
           "default_handle_session_middleware"]

__version__ = '0.0.3'

from aiohttp import web
import json

STORAGE_KEY='mw_aio_storage'
SESSION_KEY='mw_aio_session'
COOKIE_NAME ='sessionid'

async def get_session(request):
    return await request[STORAGE_KEY].load_session(request)

def session_middleware(storage):
    @web.middleware
    async def factory(request, handler):
        request[STORAGE_KEY]=storage

        # print("in session middleware")
        # 仅检查session 是否合法，并不做产生和保存session动作
        #
        raise_response = False
        try:
            response = await handler(request)
        except web.HTTPException as exc:
            response = exc
            raise_response = True
        if raise_response:
            raise response
        return response
    return factory

class SessionRedisStorage():
    def __init__(self,redis_pool,cookie_name=COOKIE_NAME):
        self._redis =redis_pool
        self.cookie_name =cookie_name

    async def load_session(self,request):
        session = request.get(SESSION_KEY)
        if session is None:
            #对kong内的服务是带了 header ,不要再去取cookie
            uid =request.headers.get('X-Consumer-ID')
            if uid is not None:
                request[SESSION_KEY]={'uid':uid}
                return request[SESSION_KEY]
            cookieid = request.cookies.get(self.cookie_name)
            if cookieid is not None:
                with await self._redis as conn:
                    data = await conn.get('session:%s' % str(cookieid))
                    if data is not None:
                        data = data.decode('utf-8')
                        try:
                            data = json.loads(data)
                        except ValueError:
                            data = None
                        if data is not None:
                            request[SESSION_KEY]= data
                            return data
        return session

@web.middleware
async def default_handle_session_middleware(request,handler):
    session =await get_session(request)
    if session is None:
        return web.Response(text="no session",status=403)
    else:
        raise_response = False
        try:
            response = await handler(request)
        except web.HTTPException as exc:
            response = exc
            raise_response = True
        if raise_response:
            raise response
        return response


def mw_setup_session_middleware(app,redis_pool):
    '''
    设定从redisstorge取session,但在handle中主动调用get_session方法，此处不处理
    :param app: 
    :param redis_pool: 
    :return: 
    '''
    storage =SessionRedisStorage(redis_pool)
    # app[STORAGE_KEY]=storage
    app.middlewares.append(session_middleware(storage))

def mw_setup_handle_session_middleware(app,redis_pool):
    '''
    对每个request取得session，并检查是否存在session,不存在则表示没有权限，返回403
    :param app: 
    :param redis_pool: 
    :return: 
    '''
    mw_setup_session_middleware(app,redis_pool)
    app.middlewares.append(default_handle_session_middleware)