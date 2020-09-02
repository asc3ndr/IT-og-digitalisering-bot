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
DB = Custom.read_JSON("db.json")

GUILD_ID = 749001540886462664
WELCOME_CHANNEL_ID = 750774345109995583
WELCOME_MSG_ID = 750839901414752327
WELCOME_MSG = f"""

For å kunne bruke chat eller voice kanaler på denne serveren må du bli tildelt en Student-rolle av Admin. Vi ber deg vennligst skifte ditt kallenavn ved å finne deg selv i 'medlemslisten' til høyre, høyreklikke på deg selv, og bytte til ditt virkelige navn. Det kan ta litt tid for Admin å oppdage deg, så ta gjerne kontakt når du er klar. :slight_smile:

For å få tilgang til emne-kanalene; klikk på de korresponderende emojiene under denne meldingen. Du kan fjerne ditt medlemskap fra et emne ved å klikke på den samme emojien om igjen.

Merk: Selv om du har tilgang til kanalen vil du kun ha lese-rettigheter før du har fått innvilget student-rolle fra Admin.

```
\N{DRAGON}\tIBE205 Agile Methods
\N{MONKEY FACE}\tIBE102 Webutvikling
\N{WATERMELON}\tIBE151 Practical Programming
\N{GRAPES}\tIBE110 Information Technology
\N{BANANA}\tLOG206 Elektronisk Handel
\N{ROOSTER}\tIBE120 Virksomhetsdata
\N{PENGUIN}\tIBE211 Databaser
\N{SUN WITH FACE}\tADM100 Organisasjon
\N{FIRE}\tBØK105 Finansregnskap
\N{HOT PEPPER}\tMAT100 Matematikk
\N{COOKIE}\tIBE320 Virtuell Virkelighet
\N{ICE CUBE}\tSCM110 Innføring i SCM
\N{MONEY WITH WINGS}\tIBE430 Forretningsprosesser
```
    """


async def print_embed():
    embed = discord.Embed(title="Velkommen!", description=WELCOME_MSG, color=0xEDEDED,)
    embed.set_author(name="IT og digitalisering")
    embed.set_thumbnail(url=bot.user.avatar_url)

    WELCOME_CHANNEL = bot.get_channel(WELCOME_CHANNEL_ID)
    msg = await WELCOME_CHANNEL.send(embed=embed)

    for key in DB.keys():
        await msg.add_reaction(key)

    if DB


@bot.event
async def on_ready():
    print(f"{bot.user} is ready!")
    # await print_embed()


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != WELCOME_MSG_ID:
        return

    for key in DB.keys():
        if payload.emoji.name == key:
            user = payload.member
            guild = bot.get_guild(GUILD_ID)
            role = get(guild.roles, name=DB[key]["code"])
            try:
                await discord.Member.add_roles(user, role)
            except:
                pass


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user:
        pass

    for key in DB.keys():
        if payload.emoji.name == key:
            guild = bot.get_guild(GUILD_ID)
            user = guild.get_member(payload.user_id)
            role = get(guild.roles, name=DB[key]["code"])
            try:
                await discord.Member.remove_roles(user, role)
            except:
                pass


bot.run(ENV_TOKEN)
