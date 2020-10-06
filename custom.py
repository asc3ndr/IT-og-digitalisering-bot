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
    def create_embed(
        title_text, title_url, author_name, author_url, thumbnail, message, footer
    ):
        if len(message) > 1900:
            message = message[0:1900] + "..."
        embed = discord.Embed(
            title=title_text, description=message, url=title_url, color=0xEDEDED,
        )
        embed.set_author(
            name=author_name, url=author_url,
        )
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=footer)
        return embed

