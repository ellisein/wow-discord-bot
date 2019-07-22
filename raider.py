import asyncio
import aiohttp

from utils import encode
import logger
import config
from params import *
from session import get_session, static_result


_session = aiohttp.ClientSession()

class Raider:
    BASE = "https://raider.io/api/v1"

    @classmethod
    @static_result(600)
    async def get_weekly_affixes(cls):
        query = "?region={}&locale={}".format(REGION, LOCALE)
        url = encode("{}/mythic-plus/affixes".format(cls.BASE), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error("Failed to get weekly affixes.")
                return None

    @classmethod
    async def get_character(cls, server_name, character_name):
        query = "?region={}".format(REGION) \
                + "&realm={}".format(SERVER.EN(server_name)) \
                + "&name={}".format(character_name) \
                + "&fields=gear,mythic_plus_scores_by_season:current," \
                + "mythic_plus_weekly_highest_level_runs"
        url = encode("{}/characters/profile".format(cls.BASE), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error("Failed to get character from raider.")
                return None
