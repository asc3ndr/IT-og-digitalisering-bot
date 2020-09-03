#!/usr/bin/python3
import discord
from discord.ext import commands
from discord.utils import get

from os import getenv
from dotenv import load_dotenv

from custom import Custom


bot = commands.Bot(command_prefix="!")

load_dotenv()
ENV_TOKEN = getenv("DISCORD_TOKEN")
DB_CONSTANTS = Custom.read_JSON("constants.json")
DB_COURSES = Custom.read_JSON("courses.json")


async def print_welcome_message():
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

    WELCOME_CHANNEL = bot.get_channel(DB_CONSTANTS["WELCOME_CHANNEL_ID"])
    msg = await WELCOME_CHANNEL.send(embed=welcome_embed)

    for value in DB_COURSES.values():
        await msg.add_reaction(value["icon"])

    DB_CONSTANTS["WELCOME_CHANNEL_MSG_ID"] = msg.id
    Custom.write_JSON("constants.json", DB_CONSTANTS)


async def create_roles():
    guild = bot.get_guild(DB_CONSTANTS["GUILD_ID"])
    for key in DB_COURSES.keys():
        if not get(guild.roles, name=key):
            await guild.create_role(name=key, permissions=discord.Permissions(67175424))


async def create_channels():
    guild = bot.get_guild(DB_CONSTANTS["GUILD_ID"])

    if not get(guild.categories, name="Test"):
        category = await discord.Guild.create_category(guild, name="Test")

    channel_overwrites = {
        guild.student: discord.PermissionOverwrite(
            read_messages=False, send_messages=True
        )
    }
    for key in DB_COURSES.keys():
        channel_overwrites = {
            "Student": discord.PermissionOverwrite(  # NOTE: Student is not a property of guild. This is broken.
                read_messages=False, send_messages=True
            ),
            key: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        }
        await guild.create_text_channel(
            name=key, category="Test", overwrites=channel_overwrites
        )


@bot.event
async def on_ready():
    # await print_welcome_message()
    # await create_roles()
    # # await create_channels() # NOTE: Not fully implemented. Don't use.
    print(f"{bot.user} is ready!")


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


bot.run(ENV_TOKEN)
