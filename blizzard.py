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

    item_info = dict()

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
    async def get_character(cls, realm_name, character_name, revisited=False):
        query = "?access_token={}".format(cls._token) \
                + "&fields=items,stats,talents,guild,progression"
        url = encode("{}/wow/character/{}/{}".format(
            cls.BASE, REALM.EN(realm_name), character_name), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_character(
                        realm_name, character_name, revisited=True)
                logger.error("Failed to get character from blizzard.")
                return None

    @classmethod
    async def get_auction_url(cls, realm_name, revisited=False):
        query = "?access_token={}&locale=ko_KR".format(cls._token)
        url = encode("{}/wow/auction/data/{}".format(cls.BASE, realm_name), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_auction_url(realm_name, revisited=True)
                logger.error("Failed to get auction url from blizzard.")
                return None

    @classmethod
    async def get_auction_data(cls, url, revisited=False):
        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_auction_data(url, revisited=True)
                logger.error("Failed to get auction data from blizzard.")
                return None

    @classmethod
    async def get_item(cls, item_id, revisited=False):
        query = "?access_token={}".format(cls._token) \
                + "namespace=static-kr&locale=ko_KR"
        url = encode("{}/data/wow/item/{}".format(cls.BASE, item_id), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_item(item_id, revisited=True)
                logger.error("Failed to get item from blizzard.")
                return None

    @classmethod
    async def get_auction(cls, item_flag, realm_name):
        auction = await cls.get_auction_url(realm_name)
        if aution is None:
            return None
        res = await cls.get_auction_data(auction["files"][0]["url"])
        if res is None:
            return None

        for i in res["auctions"]:
            if not i["item"] in cls.auction_info:
                item = await cls.get_item(i["item"])
                if item is not None:
                    cls.auction_info[i["item"]] = {
                        "name": item["name"],
                        "level": item["level"],
                        "class": item["item_class"]["name"],
                        "sub_class": item["item_subclass"]["name"]}
            else:
                item = cls.auction_info[i["item"]]

        # TODO : 경매장 아이템과 해당 아이템의 최저가격 정리
        #        임시 메모리에 저장하여 일정 기간 저장

    @classmethod
    async def get_races(cls, revisited=False):
        query = "?access_token={}".format(cls._token) \
                + "&namespace=static-kr&locale=ko_KR"
        url = encode("{}/data/wow/playable-race/index".format(cls.BASE), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_races(revisited=True)
                logger.error("Failed to get races from blizzard.")
                return None

    @classmethod
    async def get_realms(cls, revisited=False):
        query = "?access_token={}".format(cls._token) \
                + "&namespace=dynamic-kr&locale=ko_KR"
        url = encode("{}/data/wow/realm/index".format(cls.BASE), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_realms(revisited=True)
                logger.error("Failed to get realms from blizzard.")
                return None

    @classmethod
    async def get_classes(cls, revisited=False):
        query = "?access_token={}".format(cls._token) \
                + "&namespace=static-kr&locale=ko_KR"
        url = encode("{}/data/wow/playable-class/index".format(cls.BASE), query)

        async with get_session().get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                if not revisited and await cls.check_access_token():
                    return await cls.get_classes(revisited=True)
                logger.error("Failed to get classes from blizzard.")
                return None


async def init_params():
    races = await Blizzard.get_races()
    for i in races["races"]:
        RACE._races[i["id"]] = i["name"]

    realms = await Blizzard.get_realms()
    for i in realms["realms"]:
        REALM._realms[i["name"]] = i["slug"]

    classes = await Blizzard.get_classes()
    for i in classes["classes"]:
        CLASS._classes[i["id"]] = i["name"]
