#!/usr/bin/python3

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.tasks import loop

from dotenv import load_dotenv
from os import getenv

from bot_canvas_api import CanvasAPI
from bot_utility import Utility
from bot_poll import Poll
from bot_db import DB


# INITIALIZE


load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
CANVAS_TOKEN = getenv("CANVAS_TOKEN")
DATA = DB.read_JSON("data/database.json")
MAKE_CANVAS_API_CALLS = True
COMMAND_PREFIX = "$"

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


# BOT EVENTS


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="for $help")
    )
    print(f"{bot.user} is ready!")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user:
        return

    if payload.message_id != DATA["DISCORD"]["WELCOME_CHANNEL_MSG_ID"]:
        return

    for key, value in DATA["COURSES"].items():
        if payload.emoji.name == value["ICON"]:
            user = payload.member
            guild = bot.get_guild(DATA["DISCORD"]["GUILD_ID"])
            role = get(guild.roles, name=key)
            try:
                await discord.Member.add_roles(user, role)
                print(f"{user} assigned to {role}")
            except:
                pass


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user:
        return

    if payload.message_id != DATA["DISCORD"]["WELCOME_CHANNEL_MSG_ID"]:
        return

    for key, value in DATA["COURSES"].items():
        if payload.emoji.name == value["ICON"]:
            guild = bot.get_guild(DATA["DISCORD"]["GUILD_ID"])
            user = guild.get_member(payload.user_id)
            role = get(guild.roles, name=key)
            try:
                await discord.Member.remove_roles(user, role)
                print(f"{user} removed from {role}")
            except:
                pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(
        error, discord.ext.commands.errors.MissingRequiredArgument
    ) or isinstance(error, Exception):
        if hasattr(ctx.command, "name"):
            help_message = f"```${ctx.command.name} {ctx.command.signature}\n\n{ctx.command.help}```"
            await ctx.author.send(help_message)

    print(f"[ERROR]: {error}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in DATA["DISCORD"]["SUBJECT_TASK_CHANNEL_IDS"]:
        content = message.content
        forbidden_domains = ["https://tenor.com/", "https://giphy.com/"]

        for forbidden_domain in forbidden_domains:
            if forbidden_domain in content:
                await message.delete()

    await bot.process_commands(message)


# BOT COMMANDS


@bot.command(
    name="poll",
    help='Creates a poll.\nTakes 1 question and up to 9 alternatives.\nCreates a yes/no poll if it received only the question.\n\nSingle words can be input without quotes\nSentences must be wrapped in quotes.\n\nExample use:\n$poll "How awesome is the bot?" "Amazing!" "Awesome!" "Superb!"',
)
async def make_poll(ctx, question: str, *alternatives: str):
    poll = Poll(ctx, question, alternatives=alternatives, thumbnail=bot.user.avatar_url)
    await poll.create_poll()
    print(f"Poll created by {ctx.message.author} in {ctx.channel.name}")


@bot.command(
    name="updatesubjects", help="Updates the subjects embed in #emner",
)
@commands.has_role("Admin")
async def update_subjects(ctx):
    message_id = DATA["DISCORD"]["WELCOME_CHANNEL_MSG_ID"]
    subjects_channel = bot.get_channel(DATA["DISCORD"]["WELCOME_CHANNEL_ID"])
    subjects_message = await subjects_channel.fetch_message(message_id)

    if subjects_message:
        title_text = "Tilgjengelige Emnekanaler"
        title_url = ""
        author_name = "Høgskolen i Molde"
        author_url = ""
        thumbnail = bot.user.avatar_url
        message = "".join(
            [
                f"\n\t{value['ICON']}\t{key}\t{value['NAME']}"
                if key not in ["Admin", "Student"]
                else ""
                for key, value in DATA["COURSES"].items()
            ]
        )
        message = f"""
        klikk på de korresponderende emojiene under meldingen for å få tilgang til emnets kanaler. Du kan fjerne medlemskap fra et emne ved å klikke på den samme emojien om igjen.
        ```{message}```
        """
        footer = ""

        new_embed = Utility.create_embed(
            title_text, title_url, author_name, author_url, thumbnail, message, footer
        )
        await subjects_message.edit(embed=new_embed)


# BACKGROUND TASKS


@loop(seconds=60)
async def check_for_announcements():
    if MAKE_CANVAS_API_CALLS:
        for course_key in DATA["COURSES"].keys():
            if not course_key:
                continue

            data = await CanvasAPI.canvas_api_fetch_announcements(
                DATA, course_key, CANVAS_TOKEN
            )
            await CanvasAPI.canvas_api_print_announcements(bot, DATA, course_key, data)


@check_for_announcements.before_loop
async def check_for_announcements_before():
    await bot.wait_until_ready()
    print("background task running!")


# RUN

check_for_announcements.start()
bot.run(DISCORD_TOKEN)
