import asyncio
import aiohttp
from functools import wraps
from datetime import datetime, timedelta
from discord.ext import commands

import logger
import config


_instant_result = dict()

def static_result(refresh_time:int):
    """
    이 데코레이터는 여러 사용자가 명령어를 입력해도 같은 값이 나올 때 사용합니다.
    해당 명령어가 처음 불리면 API와의 통신을 통해 결과를 리턴하고 임시 메모리에 해당
    결과와 현재 시간을 저장합니다. 이후 refresh_time(초)가 지나기 전에 다시 동일한
    명령어가 호출되면 API와 통신하지 않고 저장된 결과를 대신 리턴합니다. 초기화 시간을
    초과했다면 다음 명령어 호출에 다시 새로운 결과를 메모리에 저장합니다.
    명령어에 파라미터가 있다면 결과 데이터는 파라미터마다 따로 저장됩니다.

    Parameters
    ---
    refresh_time : 명령어를 통해 새로 저장한 결과 데이터가 유효한 시간 (초)
    """
    def decorator(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            ctx = args[0]
            fname = "{}({})".format(f.__name__, ",".join(args[1:]))
            if fname in _instant_result:
                last_updated = _instant_result[fname]["last_updated"]
                if datetime.now() > last_updated + timedelta(seconds=refresh_time):
                    result = await f(*args, **kwargs)
                    if result is not None:
                        _instant_result[fname] = {
                            "last_updated": datetime.now(),
                            "result": result}
                    return result
                else:
                    logger.debug("Returned previous data for '{}'.".format(fname))
                    await ctx.send(embed=_instant_result[fname]["result"])
                    return _instant_result[fname]["result"]
            else:
                result = await f(*args, **kwargs)
                if result is not None:
                    _instant_result[fname] = {
                        "last_updated": datetime.now(),
                        "result": result}
                return result
        return wrapper
    return decorator

def is_in_guild():
    """
    특정 명령어가 자신의 길드 디스코드 채널에서만 사용 가능하도록 합니다.
    이외의 채널에 초대된 봇은 해당 명령어를 사용할 수 없습니다.
    """
    async def predicate(ctx):
        return ctx.guild and ctx.guild.id == config.get("guild_channel")
    return commands.check(predicate)
