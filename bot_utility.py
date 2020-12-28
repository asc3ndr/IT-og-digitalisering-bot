import discord
from discord.utils import get


class Utility:
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
