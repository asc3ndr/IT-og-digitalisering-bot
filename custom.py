from json import dump, load
from pathlib import Path

import discord


class Custom:
    @staticmethod
    def read_JSON(file_name: str):
        """ Returns a dictionary representation of the JSON file """
        with open(f"{Path(__file__).resolve().parent}/{file_name}", "r") as file:
            return load(file)

    @staticmethod
    def write_JSON(file_name: str, obj: dict):
        """ Takes a dictionary and converts it to JSON, then overwrite the file in path """
        with open(f"{Path(__file__).resolve().parent}/{file_name}", "w") as file:
            dump(obj, file)

    @staticmethod
    def create_embed(title, message, url, author_name, author_url, footer):
        title = re.sub("<[^<]+?>", "", title)
        message = message.replace("</p>", "\n")
        message = re.sub("<[^<]+?>", "", message)
        message = message.strip()

        if len(message) > 1900:
            message = message[0:1900] + "..."

        embed = discord.Embed(
            title=title, description=message, url=url, color=0xEDEDED,
        )

        embed.set_author(
            name=f"{course_key} {DB['COURSES'][course_key]['NAME']}",
            url=announcement["url"],
        )

        embed.set_thumbnail(url=bot.user.avatar_url)

        embed.set_footer(text=footer)

        return embed

