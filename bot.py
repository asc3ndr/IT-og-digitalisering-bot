#!/usr/bin/python3

import discord
from discord.ext import commands
from discord.utils import get

from dotenv import load_dotenv
from os import getenv
import requests
import re

from custom import Custom


# INITIALIZE

bot = commands.Bot(command_prefix="!")

load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
CANVAS_TOKEN = getenv("CANVAS_TOKEN")
# NOTE: Before commit, restructure to data/d.json
DB = Custom.read_JSON("test.json")
MAKE_CANVAS_API_CALLS = True


# FUNCTIONS


async def create_welcome_message():
    courses = "".join(
        [
            f"\n\t{value['ICON']}\t{key}\t{value['NAME']}"
            for key, value in DB["COURSES"].items()
        ]
    )
    welcome_msg = f"""
    For å kunne bruke chat eller voice kanaler på denne serveren må du bli tildelt en Student-rolle av Admin. Men f;r du roper på Admin så vil vi be deg vennligst bytte til ditt virkelige navn ved å finne deg selv i 'medlemslisten' til høyre, høyreklikke på deg selv, og klikk på "Bytt Kallenavn / Change Nickname".

    Deretter kan du få tilgang til dine emne-kanaler ved å klikk på de korresponderende emojiene under denne meldingen. Du kan fjerne ditt medlemskap fra et emne ved å klikke på den samme emojien om igjen. **Merk:** Selv om du har tilgang til en kanal vil du kun ha lese-rettigheter inntil du får innvilget student-rolle fra Admin.

    Ta gjerne kontakt med Admin når du er klar, da det kan ta litt tid før vi går igjennom medlemslisten. Takk! :slight_smile:

    ```
    {courses}
    ```
    """

    welcome_embed = discord.Embed(
        title="Velkommen!", description=welcome_msg, color=0xEDEDED,
    )
    welcome_embed.set_author(name="IT og digitalisering")
    welcome_embed.set_thumbnail(url=bot.user.avatar_url)

    welcome_channel = bot.get_channel(DB["DISCORD"]["WELCOME_CHANNEL_ID"])
    msg = await welcome_channel.send(embed=welcome_embed)

    for value in DB["COURSES"].values():
        await msg.add_reaction(value["ICON"])

    DB["DISCORD"]["WELCOME_CHANNEL_MSG_ID"] = msg.id
    Custom.write_JSON("test.json", DB)


async def create_roles():
    guild = bot.get_guild(DB["DISCORD"]["GUILD_ID"])
    for key in DB["COURSES"].keys():
        if not get(guild.roles, name=key):
            await guild.create_role(name=key, permissions=discord.Permissions(67175424))


async def canvas_api_fetch_announcement(course_key: str):

    course_id = DB["COURSES"][course_key]["CANVAS_ID"]
    if not course_id:
        return

    r = requests.get(
        f"https://himolde.instructure.com/api/v1/announcements?context_codes[]=course_{course_id}&access_token={CANVAS_TOKEN}"
    )

    data = r.json()

    for announcement in data:
        if announcement["id"] in DB["COURSES"][course_key]["ID_HISTORY"]:
            continue
        else:
            announcement_title = re.sub("<[^<]+?>", "", announcement["title"])
            announcement_message = announcement["message"].replace("</p>", "\n")
            announcement_message = re.sub("<[^<]+?>", "", announcement_message)
            announcement_message = announcement_message.strip()
            announcement_message = f"{announcement_message}"

            if len(announcement_message) > 1900:
                announcement_message = announcement_message[0:1900] + "..."

            announcement_embed = discord.Embed(
                title=announcement_title,
                description=announcement_message,
                color=0xEDEDED,
            )
            announcement_embed.set_author(
                name="CANVAS ANNOUNCEMENT", url=announcement["url"],
            )
            announcement_embed.set_thumbnail(url=bot.user.avatar_url)
            announcement_embed.set_footer(
                text=f"{announcement['posted_at']} by {announcement['user_name']}"
            )

            subject_channel = bot.get_channel(DB["DISCORD"]["DEV_CHANNEL_ID"])
            await subject_channel.send(embed=announcement_embed)

            DB["COURSES"][course_key]["CANVAS_PAST_ANNOUNCEMENT_IDS"].append(
                announcement["id"]
            )

    Custom.write_JSON("test.json", DB)


# EVENTS


@bot.event
async def on_ready():
    # await create_welcome_message()
    # await create_roles()
    print(f"{bot.user} is ready!")

    if MAKE_CANVAS_API_CALLS:
        await canvas_api_fetch_announcement("IBE151")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user:
        pass

    if payload.message_id != DB["DISCORD"]["WELCOME_CHANNEL_MSG_ID"]:
        return

    for key, value in DB["COURSES"].items():
        if payload.emoji.name == value["ICON"]:
            user = payload.member
            guild = bot.get_guild(DB["DISCORD"]["GUILD_ID"])
            role = get(guild.roles, name=key)
            try:
                await discord.Member.add_roles(user, role)
                print(f"{user} assigned to {role}")
            except:
                pass


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user:
        pass

    for key, value in DB["COURSES"].items():
        if payload.emoji.name == value["ICON"]:
            guild = bot.get_guild(DB["DISCORD"]["GUILD_ID"])
            user = guild.get_member(payload.user_id)
            role = get(guild.roles, name=key)
            try:
                await discord.Member.remove_roles(user, role)
                print(f"{user} removed from {role}")
            except:
                pass


bot.run(DISCORD_TOKEN)
