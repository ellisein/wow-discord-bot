import sys
import asyncio
import discord
from discord.ext import commands, tasks

import utils
import config
import logger
from params import *
from raider import Raider
from blizzard import Blizzard


bot = commands.Bot(command_prefix=config.get("command_prefix"))


@bot.event
async def on_ready():
    logger.info("Logged in as {}".format(bot.user.name))
    game = discord.Game(name=config.get("profile_playing"))
    await bot.change_presence(activity=game)


@bot.event
async def on_error(event, *args, **kwargs):
    logger.error("Error occurred from event '{}'".format(event))


@bot.command(name="캐릭터")
async def _character(ctx, arg:str):
    character_name, server_name = utils.parse_character_name(arg)
    if not SERVER.exists(server_name):
        msg = await ctx.send(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="존재하지 않는 서버 이름입니다."))
        return

    msg = await ctx.send(
        embed=discord.Embed(
            title="불러오는 중",
            color=COLOR.GRAY,
            description="캐릭터 정보를 불러오는 중입니다."))

    async def run():
        return await asyncio.gather(
            Raider.get_character(server_name, character_name),
            Blizzard.get_character(server_name, character_name))
    res = await run()

    if None in res:
        msg = await msg.edit(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="플레이어를 찾을 수 없습니다."))
        return

    embed = discord.Embed(
        title=character_name,
        color=COLOR.BLUE,
        description="<{}>\n{} {}".format(
            res[1]["guild"]["name"],
            RACE.KR(res[1]["race"]),
            CLASS.KR(res[1]["class"])))
    embed.set_thumbnail(url="{}/{}".format(
        Blizzard.THUMBNAIL_BASE, res[1]["thumbnail"]))

    embed.add_field(
        name="아이템 레벨",
        value="최대 {}, 착용 {}, 아제로스의 심장 {} ({})".format(
            res[1]["items"]["averageItemLevel"],
            res[1]["items"]["averageItemLevelEquipped"],
            res[1]["items"]["neck"]["azeriteItem"]["azeriteLevel"],
            res[1]["items"]["neck"]["itemLevel"]))

    embed.add_field(
        name="2차 스탯",
        value="치명타 {:.2f}%, 가속 {:.2f}%, 특화 {:.2f}%, 유연성 {:.2f}%".format(
            res[1]["stats"]["crit"],
            res[1]["stats"]["haste"],
            res[1]["stats"]["mastery"],
            res[1]["stats"]["versatilityDamageDoneBonus"]))

    embed.add_field(
        name="레이더 점수",
        value="현재 시즌 {}점".format(res[0]["mythic_plus_scores_by_season"][0]["scores"]["all"]))

    embed.add_field(
        name="이번주 쐐기 던전 최고기록",
        value="기록 없음" if len(res[0]["mythic_plus_weekly_highest_level_runs"]) == 0 \
            else "{} {}단 {}".format(
                DUNGEON.KR(res[0]["mythic_plus_weekly_highest_level_runs"][0]["dungeon"]),
                res[0]["mythic_plus_weekly_highest_level_runs"][0]["mythic_level"],
                MYTHIC_PLUS_RESULTS[res[0]["mythic_plus_weekly_highest_level_runs"][0]["num_keystone_upgrades"]]))

    boss_count = len(res[1]["progression"]["raids"][-1]["bosses"])
    normal_kills, heroic_kills, mythic_kills = 0, 0, 0
    for boss in res[1]["progression"]["raids"][-1]["bosses"]:
        normal_kills += (1 if boss["normalKills"] > 0 else 0)
        heroic_kills += (1 if boss["heroicKills"] > 0 else 0)
        mythic_kills += (1 if boss["mythicKills"] > 0 else 0)
    embed.add_field(
        name="{} 진행도".format(res[1]["progression"]["raids"][-1]["name"]),
        value="일반 {}/{}, 영웅 {}/{}, 신화 {}/{}".format(
            normal_kills, boss_count,
            heroic_kills, boss_count,
            mythic_kills, boss_count))

    msg = await msg.edit(embed=embed)


@bot.command(name="어픽스")
async def _affixes(ctx):
    msg = await ctx.send(
        embed=discord.Embed(
            title="불러오는 중",
            color=COLOR.GRAY,
            description="이번주 쐐기 던전 어픽스 정보를 불러오는 중입니다."))

    res = await Raider.get_weekly_affixes()
    if res is None:
        msg = await msg.edit(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="이번주 쐐기 던전 어픽스 정보를 불러오는 데 실패했습니다."))
        return

    embed = discord.Embed(
        title="이번주 쐐기 던전 어픽스",
        color=COLOR.BLUE,
        description="")
    embed.set_thumbnail(url=GAME_ICON.MYTHIC_PLUS)

    for affix in res["affix_details"]:
        embed.add_field(
            name=affix["name"],
            value=affix["description"])

    msg = await msg.edit(embed=embed)


@tasks.loop(seconds=60)
async def change_token():
    # Changes Blizzard api access token every 60 seconds.
    await Blizzard.change_access_token()


if __name__ == "__main__":
    token = config.get("discord_token")
    if token is None:
        logger.error("Failed to get discord token.")
    else:
        change_token.start()
        bot.run(token)
