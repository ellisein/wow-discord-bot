import asyncio
import aiohttp

from utils import encode
import logger
import config
from params import *


class Warcraftlogs:
    BASE = "https://www.warcraftlogs.com/v1"

    @classmethod
    async def get_classes(cls):
        query = "?api_key={}".format(config.get("warcraftlogs_token"))
        url = encode("{}/class".format(cls.BASE), query)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error("Failed to get classes from warcraftlogs.")
                    return None
