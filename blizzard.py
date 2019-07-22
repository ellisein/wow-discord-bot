import asyncio
import aiohttp
from datetime import datetime, timedelta

from utils import encode
import logger
import config
from params import *
from session import get_session


class Blizzard:
    BASE = "https://kr.api.blizzard.com"
    OAUTH_BASE = "https://kr.battle.net/oauth"
    THUMBNAIL_BASE = "https://render-kr.worldofwarcraft.com/character"
    _token = None

    @classmethod
    async def change_access_token(cls):
        query = "?grant_type=client_credentials&client_id={}&client_secret={}".format(
            config.get("blizzard_id"), config.get("blizzard_secret"))
        url = encode("{}/token".format(cls.OAUTH_BASE), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                token = await response.json()
                if cls._token != token["access_token"]:
                    cls._token = token["access_token"]
                    logger.info("Changed the access token for Blizzard API.")
                    return True
            else:
                logger.error("Failed to change the access token for Blizzard API.")
        return False

    @classmethod
    async def check_access_token(cls):
        query = "?token={}".format(cls._token)
        url = encode("{}/check_token".format(cls.OAUTH_BASE), query)

        async with get_session().get(url) as response:
            if response.status == 400:
                await cls.change_access_token()
                return True
            elif response.status == 200:
                return True
        return False

    @classmethod
    async def get_character(cls, server_name, character_name, revisited=False):
        query = "?access_token={}".format(cls._token) \
                + "&fields=items,stats,talents,guild,progression"
        url = encode("{}/wow/character/{}/{}".format(
            cls.BASE, SERVER.EN(server_name), character_name), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if await cls.check_access_token() and not revisited:
                    return await cls.get_character(
                        server_name, character_name, revisited=True)
                logger.error("Failed to get character from blizzard.")
                return None
