#!/usr/bin/python3

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.tasks import loop

from dotenv import load_dotenv
from datetime import datetime
from os import getenv

from bot_canvas_api import CanvasAPI
from bot_utility import Utility
from bot_poll import Poll
from bot_db import DigitDB


# INITIALIZE


load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
AMR_TOKEN = getenv("AMR_TOKEN")
SIG_TOKEN = getenv("SIG_TOKEN")
KNU_TOKEN = getenv("KNU_TOKEN")
CANVAS_TOKENS = {"AMR": AMR_TOKEN, "SIG": SIG_TOKEN, "KNU": KNU_TOKEN}
DATABASE = DigitDB()
COMMAND_PREFIX = "$"
TIME = lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S")

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


# BOT EVENTS


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"for {COMMAND_PREFIX}help"
        )
    )
    print(f"[{TIME()}]\t{bot.user} is ready!")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user:
        return

    if payload.message_id != DATABASE.WELCOME_CHANNEL_MSG_ID:
        return

    for course in DATABASE.get_all_courses():
        if payload.emoji.name == course["icon"]:
            user = payload.member
            guild = bot.get_guild(DATABASE.GUILD_ID)
            role = get(guild.roles, name=course["role"])
            try:
                await discord.Member.add_roles(user, role)
                print(f"[{TIME()}]\t{user} assigned to {role}")
            except:
                pass


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user:
        return

    if payload.message_id != DATABASE.WELCOME_CHANNEL_MSG_ID:
        return

    for course in DATABASE.get_all_courses():
        if payload.emoji.name == course["icon"]:
            guild = bot.get_guild(DATABASE.GUILD_ID)
            user = guild.get_member(payload.user_id)
            role = get(guild.roles, name=course["role"])
            try:
                await discord.Member.remove_roles(user, role)
                print(f"[{TIME()}]\t{user} removed from {role}")
            except:
                pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(
        error, discord.ext.commands.errors.MissingRequiredArgument
    ) or isinstance(error, Exception):
        if hasattr(ctx.command, "name"):
            help_message = f"```{COMMAND_PREFIX}{ctx.command.name} {ctx.command.signature}\n\n{ctx.command.help}```"
            await ctx.author.send(help_message)

    print(f"[{TIME()}]\t{error}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id in DATABASE.COURSE_TASK_CHANNEL_IDS:
        content = message.content
        forbidden_domains = ["https://tenor.com/", "https://giphy.com/"]

        for forbidden_domain in forbidden_domains:
            if forbidden_domain in content:
                await message.delete()
                await message.author.send(
                    "Vi ønsker å holde oppgavekanalene ryddig og av den grunn ble din gif automatisk fjernet. Takk for at du hjelper til og er aktiv i kanalen! :-)"
                )

    await bot.process_commands(message)


# BOT COMMANDS


@bot.command(
    name="poll",
    help=f'Creates a poll.\nTakes 1 question and up to 9 alternatives.\nCreates a yes/no poll if it received only the question.\n\nSingle words can be input without quotes\nSentences must be wrapped in quotes.\n\nExample use:\n{COMMAND_PREFIX}poll "How awesome is the bot?" "Amazing!" "Awesome!" "Superb!"',
)
async def make_poll(ctx, question: str, *alternatives: str):
    poll = Poll(ctx, question, alternatives=alternatives, thumbnail=bot.user.avatar_url)
    await poll.create_poll()
    print(f"[{TIME()}]\tPoll by {ctx.message.author} in {ctx.channel.name}")


@bot.command(
    name="updatecourses",
    help="Updates the embed in #emner to show the available active courses",
)
@commands.has_role("Admin")
async def update_courses(ctx):
    channel = bot.get_channel(DATABASE.WELCOME_CHANNEL_ID)
    message = await channel.fetch_message(DATABASE.WELCOME_CHANNEL_MSG_ID)
    courses = DATABASE.get_all_courses()

    title = "Tilgjengelige Emnekanaler, Vår 2021"
    title_url = ""
    author = "Høgskolen i Molde"
    author_url = ""
    thumbnail = bot.user.avatar_url
    body = "".join(
        [
            f"\n\t{course['icon']}\t{course['role']}\t{course['name']}"
            if course["active"] and course["role"] not in ["Admin", "Student"]
            else ""
            for course in courses
        ]
    )
    body = f"""
    klikk på de korresponderende emojiene under meldingen for å få tilgang til emnets kanaler. Du kan fjerne medlemskap fra et emne ved å klikke på den samme emojien om igjen.
    ```{body}```
    """
    footer = ""

    new_embed = Utility.create_embed(
        title, title_url, author, author_url, thumbnail, body, footer
    )

    if not message:
        new_message = await channel.send(embed=new_embed)
        DATABASE.WELCOME_CHANNEL_MSG_ID = new_message.id
        print("Remember to set WELCOME_CHANNEL_MSG_ID")

        for course in courses:
            if course["active"] and course["role"] not in ["Admin", "Student"]:
                await new_message.add_reaction(course["icon"])

    if message:
        await message.edit(embed=new_embed)

        reactions = [reaction.emoji for reaction in message.reactions]
        course_icons = DATABASE.get_all_courses(key="icon")

        for reaction in reactions:
            if reaction not in course_icons:
                reaction = get(message.reactions, emoji=reaction)
                await reaction.clear()

        for course in courses:
            if course["role"] in ["Admin", "Student"]:
                continue

            if not course["active"] and course["icon"] in reactions:
                reaction = get(message.reactions, emoji=course["icon"])
                await reaction.clear()

            elif course["active"] and course["icon"] not in reactions:
                await message.add_reaction(course["icon"])


@bot.command(
    name="updateroles",
    help="Removes inactive course roles and adds new, active course roles.",
)
@commands.has_role("Admin")
async def update_course_roles(ctx):
    guild = bot.get_guild(DATABASE.GUILD_ID)
    guild_roles = [role.name for role in guild.roles]

    for course in DATABASE.get_all_courses():
        if course["role"] in ["Student", "Admin"]:
            continue

        if not course["active"] and course["role"] in guild_roles:
            role = get(guild.roles, name=course["role"])
            await role.delete()

        elif course["active"] and not course["role"] in guild_roles:
            await guild.create_role(
                name=course["role"], permissions=discord.Permissions(67175424)
            )

    course_roles = DATABASE.get_all_courses(key="role")

    for guild_role in guild_roles:
        if len(guild_role) == 6 and guild_role not in course_roles:
            role = get(guild.roles, name=guild_role)
            await role.delete()


@loop(seconds=60)
async def check_for_announcements():
    for course in DATABASE.get_all_courses():

        if course["active"] and course["_id"] > 10:
            token = CANVAS_TOKENS[course["token"]]
            announcements = await CanvasAPI.fetch_announcements(course, token)

            if announcements:
                for announcement in announcements:
                    if announcement["id"] in course["announcements"]:
                        continue

                    await CanvasAPI.print_announcement(
                        bot, DATABASE.GUILD_ID, course, announcement
                    )
                    print(f"[{TIME()}]\t{course['role']} announcement fetched!")
                    DATABASE.add_course_announcement(course["_id"], announcement["id"])


@check_for_announcements.before_loop
async def check_for_announcements_before():
    await bot.wait_until_ready()
    print(f"[{TIME()}]\tBackground Task Running!")


# RUN

check_for_announcements.start()
bot.run(DISCORD_TOKEN)
