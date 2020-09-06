#!/usr/bin/python3

import discord
from discord.ext import commands
from discord.utils import get

from datetime import datetime
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

DB_ANNOUNCEMENTS = Custom.read_JSON("data/announcements.json")
DB_CONSTANTS = Custom.read_JSON("data/constants.json")
DB_COURSES = Custom.read_JSON("data/courses.json")
MAKE_CANVAS_API_CALLS = True


# FUNCTIONS


async def create_welcome_message():
    welcome_msg_courses = "".join(
        [
            f"\n\t{value['icon']}\t{key}\t{value['name']}"
            for key, value in DB_COURSES.items()
        ]
    )
    welcome_msg = f"""
    For å kunne bruke chat eller voice kanaler på denne serveren må du bli tildelt en Student-rolle av Admin. Vi ber deg vennligst bytte til ditt virkelige navn ved å finne deg selv i 'medlemslisten' til høyre, høyreklikke på deg selv, og klikk på "Bytt Kallenavn / Change Nickname". Det kan ta litt tid før Admin går igjennom medlemslisten, så ta gjerne kontakt når du er klar. :slight_smile:

    For å få tilgang til emne-kanalene; klikk på de korresponderende emojiene under denne meldingen. Du kan fjerne ditt medlemskap fra et emne ved å klikke på den samme emojien om igjen.

    **Merk:** Selv om du har tilgang til en kanal vil du kun ha lese-rettigheter inntil du får innvilget student-rolle fra Admin.

    ```
    {welcome_msg_courses}
    ```
    """

    welcome_embed = discord.Embed(
        title="Velkommen!", description=welcome_msg, color=0xEDEDED,
    )
    welcome_embed.set_author(name="IT og digitalisering")
    welcome_embed.set_thumbnail(url=bot.user.avatar_url)

    welcome_channel = bot.get_channel(DB_CONSTANTS["WELCOME_CHANNEL_ID"])
    msg = await welcome_channel.send(embed=welcome_embed)

    for value in DB_COURSES.values():
        await msg.add_reaction(value["icon"])

    DB_CONSTANTS["WELCOME_CHANNEL_MSG_ID"] = msg.id
    Custom.write_JSON("constants.json", DB_CONSTANTS)


async def create_roles():
    guild = bot.get_guild(DB_CONSTANTS["GUILD_ID"])
    for key in DB_COURSES.keys():
        if not get(guild.roles, name=key):
            await guild.create_role(name=key, permissions=discord.Permissions(67175424))


async def canvas_api_fetch_announcement(course_key: str):

    course_id = DB_COURSES[course_key]["id"]
    if not course_id:
        return

    r = requests.get(
        f"https://himolde.instructure.com/api/v1/announcements?context_codes[]=course_{course_id}&access_token={CANVAS_TOKEN}"
    )

    data = r.json()

    for post in data:
        if post["id"] in DB_ANNOUNCEMENTS[course_id]["ID_HISTORY"]:
            pass
        else:
            announcement_url = post["url"]
            announcement_title = re.sub("<[^<]+?>", "", post["title"])
            announcement_message = post["message"].replace("</p>", "\n")
            announcement_message = re.sub("<[^<]+?>", "", announcement_message)
            announcement_message = announcement_message.strip()
            announcement_message = f"{announcement_message}"

            if len(announcement_message) > 1900:
                announcement_message = (
                    announcement_message[0:1900]
                    + "..."
                    + "\n(meldingen overskrider max antall tegn)"
                )

            announcement_embed = discord.Embed(
                title=announcement_title,
                description=announcement_message,
                color=0xEDEDED,
            )
            announcement_embed.set_author(
                name="CANVAS ANNOUNCEMENT", url=announcement_url,
            )
            announcement_embed.set_thumbnail(url=bot.user.avatar_url)
            announcement_embed.set_footer(
                text=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            )

            subject_channel = bot.get_channel(DB_CONSTANTS["BOT_DEV_CHANNEL_ID"])
            await subject_channel.send(embed=announcement_embed)

            DB_ANNOUNCEMENTS[course_id]["ID_HISTORY"].append(post["id"])

    Custom.write_JSON("data/announcements.json", DB_ANNOUNCEMENTS)


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

    if payload.message_id != DB_CONSTANTS["WELCOME_CHANNEL_MSG_ID"]:
        return

    for key, value in DB_COURSES.items():
        if payload.emoji.name == value["icon"]:
            user = payload.member
            guild = bot.get_guild(DB_CONSTANTS["GUILD_ID"])
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

    for key, value in DB_COURSES.items():
        if payload.emoji.name == value["icon"]:
            guild = bot.get_guild(DB_CONSTANTS["GUILD_ID"])
            user = guild.get_member(payload.user_id)
            role = get(guild.roles, name=key)
            try:
                await discord.Member.remove_roles(user, role)
                print(f"{user} removed from {role}")
            except:
                pass


bot.run(DISCORD_TOKEN)