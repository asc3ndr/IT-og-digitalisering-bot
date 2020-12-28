import requests
import re

import discord
from discord.utils import get

from bot_utility import Utility


class CanvasAPI:
    @staticmethod
    async def fetch_announcements(course: dict, access_token: str):
        response = requests.get(
            f"https://himolde.instructure.com/api/v1/announcements?context_codes[]=course_{course['_id']}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code == 200:
            return response.json()

        print(f"{response.status_code}: {response.json()}")
        return None

    @staticmethod
    async def create_announcement(bot: object, course: dict, announcement: dict):
        title = re.sub("<[^<]+?>", "", announcement["title"])
        title_url = announcement["url"]

        author_name = f"{course['role']} {course['name']}"
        author_url = announcement["url"]

        thumbnail = bot.user.avatar_url

        message = announcement["message"].replace("</p>", "\n")
        message = re.sub("<[^<]+?>", "", message)
        message = message.strip()
        message = f"{message}"
        if len(message) > 1900:
            message = message[0:1900] + "..."

        footer = announcement["posted_at"]
        footer = footer.replace("T", " ")
        footer = footer.replace("Z", "")
        footer = f"Posted by: {announcement['user_name']}\nPosted on: {footer}"

        embed = Utility.create_embed(
            title, title_url, author_name, author_url, thumbnail, message, footer
        )
        return embed

    @staticmethod
    async def print_announcement(
        bot: object, guild_id: int, course: dict, announcement: dict
    ):
        announcement_embed = await CanvasAPI.create_announcement(
            bot, course, announcement
        )
        guild = bot.get_guild(guild_id)

        if not get(guild.roles, name=course["role"]):
            role_id = get(guild.roles, name="Student").id
        else:
            role_id = get(guild.roles, name=course["role"]).id

        news_channel = bot.get_channel(course["announcement_channel_id"])

        await news_channel.send(f"<@&{role_id}>")
        await news_channel.send(embed=announcement_embed)

        print(f"{course['role']} announcement fetched!")
