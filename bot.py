#!/usr/bin/python3
import discord
from discord.ext import commands
from discord.utils import get

from os import getenv
from dotenv import load_dotenv

load_dotenv()

ENV_TOKEN = getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")


@bot.event
async def on_member_join(member):

    WELCOME_MSG = f"""\
        Hi {member.name}, welcome to Asc3ndR's Devspace!\
    """

    await member.create_dm()
    await member.dm_channel.send(WELCOME_MSG)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "x":
        await message.channel.send("x")

    await bot.process_commands(message)
    print(f"Message from {message.author}: {message.content}")


@bot.command(name="join", help="example: !join IBE151")
async def join(ctx, subject: str):

    user = ctx.author

    if subject.lower() == "student":
        await user.create_dm()
        await user.dm_channel.send(
            f"Student role cannot be assigned via bot command. Please contact an administrator."
        )
        return

    subject = subject.upper()
    desired_role = get(ctx.guild.roles, name=subject)
    student_role = get(ctx.guild.roles, name="Student")

    if not desired_role:
        await user.create_dm()
        await user.dm_channel.send(
            f"No subject by name {subject}, are you sure you spelled it correctly?"
        )
        return

    if desired_role.permissions > student_role.permissions:
        await user.create_dm()
        await user.dm_channel.send(
            f"{subject} role cannot be assigned via bot command. Please contact an administrator."
        )
        return

    await discord.Member.add_roles(user, desired_role)


@bot.command(name="leave", help="example: !leave IBE151")
async def leave(ctx, subject: str):

    subject = subject.upper()
    user = ctx.author
    role = get(ctx.guild.roles, name=subject)

    if not role:
        await user.create_dm()
        await user.dm_channel.send(f"No subject by name {subject} exist!")
        return

    await discord.Member.add_roles(user, role)


bot.run(ENV_TOKEN)
