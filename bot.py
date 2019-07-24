import sys
import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks

import utils
import config
import logger
from params import *
from raider import Raider
from blizzard import Blizzard, init_params


bot = commands.Bot(command_prefix=config.get("command_prefix"))

"""
명령어

!명령어 : 모든 가능한 명령어 출력
!캐릭터 (캐릭터이름)-(서버이름) : 캐릭터 정보 조회
!어픽스 : 금주의 쐐기돌 던전 어픽스 조회
!경매장 (종류) (서버) : 경매장 각 아이템의 최저가격 조회
!장신구 (직업) : 장신구 순위 조회
!아제특성 (직업) : 아제라이트 특성 순위 조회
!특성 (직업) : 특성 순위 조회
!정수 (직업) : 정수 순위 조회
!스탯 (직업) : 2차 스탯 우선순위 조회
!토큰 : 토큰 가격 조회
"""


@bot.event
async def on_ready():
    logger.info("Logged in as {}".format(bot.user.name))
    await init_params()

    game = discord.Game(name=config.get("profile_playing"))
    await bot.change_presence(activity=game)


@bot.event
async def on_command_error(ctx, exception):
    if type(exception) == commands.errors.CommandOnCooldown:
        await ctx.send(
            embed=discord.Embed(
                title="명령어 오류",
                color=COLOR.RED,
                description="짧은 시간 동안 너무 많은 명령어를 입력하였습니다." \
                    + "\n잠시 후 다시 시도해주세요."))
    elif type(exception) == commands.errors.CommandNotFound:
        pass
    else:
        await ctx.send(
            embed=discord.Embed(
                title="명령어 오류",
                color=COLOR.RED,
                description=str(exception)))


@bot.command(name="명령어")
@commands.cooldown(10, 60, commands.BucketType.user)
async def _commands(ctx, *args):
    commands = ["!{}".format(c.name) for c in bot.commands]
    if "!help" in commands:
        commands.remove("!help")

    await ctx.send(
        embed=discord.Embed(
            title="사용 가능한 명령어",
            color=COLOR.BLUE,
            description=", ".join(commands)))


@bot.command(name="캐릭터")
@commands.cooldown(10, 60, commands.BucketType.user)
async def _character(ctx, *args):
    await ctx.trigger_typing()
    if len(args) == 0:
        embed = discord.Embed(
            title="명령어 오류",
            color=COLOR.RED,
            description="명령어 뒤에 '캐릭터 이름-서버 이름'을 적어야 합니다.")
        embed.add_field(
            name="사용 예시",
            value="!캐릭터 실바나스-아즈샤라")
        if REALM.exists(config.get("default_realm")):
            embed.set_footer(
                text="서버 이름을 명시하지 않으면 {} 서버로 간주합니다.".format(
                    REALM.KR(config.get("default_realm"))))
        await ctx.send(embed=embed)
        return

    character_name, realm_name = utils.parse_character_name(args[0])
    if not REALM.exists(realm_name):
        await ctx.send(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="존재하지 않는 서버 이름입니다."))
        return

    async def run():
        return await asyncio.gather(
            Raider.get_character(realm_name, character_name),
            Blizzard.get_character(realm_name, character_name))
    res = await run()

    if None in res:
        await ctx.send(
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

    await ctx.send(embed=embed)


@bot.command(name="어픽스")
@commands.cooldown(10, 60, commands.BucketType.user)
async def _affixes(ctx):
    await ctx.trigger_typing()

    async def run():
        return await asyncio.gather(
            Raider.get_weekly_affixes(),
            Blizzard.get_mythic_keystone_period())
    res = await run()

    if res[0] is None:
        await ctx.send(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="이번주 쐐기 던전 어픽스 정보를 불러오는 데 실패했습니다."))
        return

    period = ""
    if res[1] is not None:
        start = datetime.fromtimestamp(int(res[1]["start_timestamp"] / 1000))
        end = datetime.fromtimestamp(int(res[1]["end_timestamp"] / 1000))
        period = "{} ~ {}".format(
            start.strftime("%Y-%m-%d %H:%M"),
            end.strftime("%Y-%m-%d %H:%M"))

    embed = discord.Embed(
        title="이번주 쐐기 던전 어픽스",
        color=COLOR.BLUE,
        description=period)
    embed.set_thumbnail(url=GAME_ICON.MYTHIC_PLUS)

    for affix in res[0]["affix_details"]:
        embed.add_field(
            name=affix["name"],
            value=affix["description"])

    await ctx.send(embed=embed)


@bot.command(name="경매장")
@commands.cooldown(10, 60, commands.BucketType.user)
async def _auction(ctx, *args):
    await ctx.trigger_typing()
    if len(args) == 0:
        embed = discord.Embed(
            title="명령어 오류",
            color=COLOR.RED,
            description="명령어 뒤에 '(약초/광석/영약/물약/요리) 서버 이름'을 적어야 합니다.")
        embed.add_field(
            name="사용 예시",
            value="!경매장 영약 아즈샤라")
        if REALM.exists(config.get("default_realm")):
            embed.set_footer(
                text="서버 이름을 명시하지 않으면 {} 서버로 간주합니다.".format(
                    REALM.KR(config.get("default_realm"))))
        await ctx.send(embed=embed)
        return

    item_flag = args[0]
    realm_name = args[1] if len(args) > 1 else REALM.EN(config.get("default_realm"))
    
    if not REALM.exists(realm_name):
        await ctx.send(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="존재하지 않는 서버 이름입니다."))
        return

    # TODO


@bot.command(name="토큰")
@commands.cooldown(10, 60, commands.BucketType.user)
async def _token(ctx, *args):
    await ctx.trigger_typing()
    res = await Blizzard.get_token_price()

    if res is None:
        await ctx.send(
            embed=discord.Embed(
                title="실행 오류",
                color=COLOR.RED,
                description="토큰 가격 정보를 불러오는 데 실패했습니다."))
        return

    await ctx.send(
        embed=discord.Embed(
            title="한국 서버 토큰 시세",
            color=COLOR.BLUE,
            description="{}골드".format(int(res["price"] / 10000))))


@tasks.loop(seconds=60)
async def timing_task():
    # EXAMPLE
    await Blizzard.change_access_token()


if __name__ == "__main__":
    token = config.get("discord_token")
    if token is None:
        logger.error("Failed to get discord token.")
    else:
        bot.run(token)
