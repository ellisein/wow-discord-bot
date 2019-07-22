import aiohttp
from functools import wraps
from datetime import datetime, timedelta

import logger


class Session:
    def __init__(self):
        self._session = aiohttp.ClientSession()
        logger.info("Initialized a new aiohttp session.")

    def __del__(self):
        self._session.close()
        logger.info("Closed the aiohttp session.")

s = Session()

def get_session():
    return s._session


_instant_result = dict()

def static_result(refresh_time):
    """
    이 데코레이터는 여러 사용자가 명령어를 입력해도 같은 값이 나올 때 사용합니다.
    해당 명령어가 처음 불리면 API와의 통신을 통해 결과를 리턴하고 임시 메모리에 해당
    결과와 현재 시간을 저장합니다. 이후 refresh_time(초)가 지나기 전에 다시 동일한
    명령어가 호출되면 API를 사용하지 않고 저장된 결과를 대신 리턴합니다. 초기화 시간을
    초과했다면 다음 명령어 호출에 다시 새로운 결과를 메모리에 저장합니다.
    """
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            if f.__name__ in _instant_result:
                last_updated = _instant_result[f.__name__]["last_updated"]
                last_updated = datetime.fromtimestamp(last_updated)
                if datetime.now() > last_updated + timedelta(seconds=refresh_time):
                    result = await f(*args, **kwargs)
                    _instant_result[f.__name__] = {
                        "last_updated": datetime.now().timestamp(),
                        "result": result}
                    return result
                else:
                    return _instant_result[f.__name__]["result"]
            else:
                result = await f(*args, **kwargs)
                _instant_result[f.__name__] = {
                    "last_updated": datetime.now().timestamp(),
                    "result": result}
                return result
        return wrapper
    return decorator
