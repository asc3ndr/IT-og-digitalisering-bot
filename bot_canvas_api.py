import requests
import re

import discord
from discord.utils import get

from bot_utility import Utility
from bot_db import DB


class CanvasAPI:
    @staticmethod
    async def canvas_api_fetch_announcements(
        DATA: dict, course_key: str, access_token: str
    ):
        course_id = DATA["COURSES"][course_key]["CANVAS_ID"]
        response = requests.get(
            f"https://himolde.instructure.com/api/v1/announcements?context_codes[]=course_{course_id}&access_token={access_token}"
        )
        return response.json()

    @staticmethod
    async def canvas_api_create_announcement(
        bot: object, DATA: dict, course_key: str, announcement: dict
    ):
        title = re.sub("<[^<]+?>", "", announcement["title"])
        title_url = announcement["url"]

        author_name = f"{course_key} {DATA['COURSES'][course_key]['NAME']}"
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
    async def canvas_api_print_announcements(
        bot: object, DATA: dict, course_key: str, data: dict
    ):
        for announcement in data:
            if (
                announcement["id"]
                in DATA["COURSES"][course_key]["CANVAS_PAST_ANNOUNCEMENT_IDS"]
            ):
                continue
            else:
                announcement_embed = await CanvasAPI.canvas_api_create_announcement(
                    bot, DATA, course_key, announcement
                )
                guild = bot.get_guild(DATA["DISCORD"]["GUILD_ID"])
                role_id = get(guild.roles, name=course_key).id
                announcement_notification = f"<@&{role_id}> Ny kunngjøring i <#{DATA['COURSES'][course_key]['DISCORD_ANNOUNCEMENT_CHANNEL_ID']}>."

                news_channel = bot.get_channel(
                    DATA["COURSES"][course_key]["DISCORD_ANNOUNCEMENT_CHANNEL_ID"]
                )
                subject_channel = bot.get_channel(
                    DATA["COURSES"][course_key]["DISCORD_CHANNEL_ID"]
                )

                await news_channel.send(embed=announcement_embed)
                await subject_channel.send(announcement_notification)

                print(course_key, "announcement fetched!")

                DATA["COURSES"][course_key]["CANVAS_PAST_ANNOUNCEMENT_IDS"].append(
                    announcement["id"]
                )
                DB.write_JSON("data/database.json", DATA)
