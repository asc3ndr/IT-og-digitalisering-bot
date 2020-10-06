import discord


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

    @staticmethod
    async def create_welcome_message(bot, DATA: dict):
        courses = "".join(
            [
                f"\n\t{value['ICON']}\t{key}\t{value['NAME']}"
                for key, value in DATA["COURSES"].items()
            ]
        )
        welcome_message_text = f"""
        For å kunne bruke chat eller voice kanaler på denne serveren må du bli tildelt en Student-rolle av Admin. Før du kontakter oss ber vi deg vennligst bytte til ditt virkelige navn ved å finne deg selv i 'medlemslisten' til høyre, høyreklikke på deg selv, og klikk på "Bytt Kallenavn / Change Nickname".

        Deretter kan du få tilgang til dine emne-kanaler ved å klikk på de korresponderende emojiene under denne meldingen. Du kan fjerne ditt medlemskap fra et emne ved å klikke på den samme emojien om igjen. **Merk:** Selv om du har tilgang til en kanal vil du kun ha lese-rettigheter inntil du får innvilget student-rollen fra Admin.

        Ta gjerne kontakt når du er klar, da det kan ta litt tid før vi går igjennom medlemslisten. Takk! :slight_smile:

        ```
        {courses}
        ```
        """

        welcome_embed = discord.Embed(
            title="Velkommen!", description=welcome_message_text, color=0xEDEDED,
        )
        welcome_embed.set_author(name="IT og digitalisering")
        welcome_embed.set_thumbnail(url=bot.user.avatar_url)

        welcome_channel = bot.get_channel(DATA["DISCORD"]["WELCOME_CHANNEL_ID"])
        welcome_message = await welcome_channel.send(embed=welcome_embed)

        for value in DATA["COURSES"].values():
            await welcome_message.add_reaction(value["ICON"])

        DATA["DISCORD"]["WELCOME_CHANNEL_MSG_ID"] = welcome_message.id
        Custom.write_JSON("data/database.json", DATA)

    @staticmethod
    async def create_subject_roles(bot, DATA: dict):
        guild = bot.get_guild(DATA["DISCORD"]["GUILD_ID"])
        for key in DATA["COURSES"].keys():
            if not get(guild.roles, name=key):
                await guild.create_role(
                    name=key, permissions=discord.Permissions(67175424)
                )
