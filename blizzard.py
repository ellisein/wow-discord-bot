import asyncio
import aiohttp
from datetime import datetime, timedelta

from utils import encode
import logger
import config
from params import *


_session = aiohttp.ClientSession()

class Blizzard:
    BASE = "https://kr.api.blizzard.com"
    OAUTH_BASE = "https://kr.battle.net/oauth/token"
    THUMBNAIL_BASE = "https://render-kr.worldofwarcraft.com/character"
    _token = None
    _last_updated = None

    @classmethod
    async def change_access_token(cls):
        if cls._last_updated:
            if datetime.now() - cls._last_updated < timedelta(0, 30, 0):
                return True

        query = "?grant_type=client_credentials&client_id={}&client_secret={}".format(
            config.get("blizzard_id"), config.get("blizzard_secret"))
        url = encode(cls.OAUTH_BASE, query)

        async with _session.get(url) as response:
            if response.status == 200:
                token = await response.json()
                cls._token = token["access_token"]
                logger.info("Changed the access token for Blizzard API.")
                return True
            else:
                logger.error("Failed to change the access token for Blizzard API.")
                return False

    @classmethod
    async def get_character(cls, server_name, character_name):
        if not await cls.change_access_token():
            return None

        query = "?access_token={}&fields=items,stats,talents,guild".format(cls._token)
        url = encode("{}/wow/character/{}/{}".format(
            cls.BASE, SERVER.EN(server_name), character_name), query)

        async with _session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if changed_token is None:
                    changed_token = await cls.change_access_token()
                logger.error("Failed to get character from blizzard.")
                return None
