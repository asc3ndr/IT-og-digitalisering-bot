import discord


class Poll:
    def __init__(self, ctx, question, alternatives="", thumbnail=""):
        self.icons = {
            0: "\u0031\uFE0F\u20E3",
            1: "\u0032\uFE0F\u20E3",
            2: "\u0033\uFE0F\u20E3",
            3: "\u0034\uFE0F\u20E3",
            4: "\u0035\uFE0F\u20E3",
            5: "\u0036\uFE0F\u20E3",
            6: "\u0037\uFE0F\u20E3",
            7: "\u0038\uFE0F\u20E3",
            8: "\u0039\uFE0F\u20E3",
        }
        self.ctx = ctx
        self.question = question
        self.alternatives = alternatives
        self.thumbnail = thumbnail

    async def create_poll_embed(self):
        poll_embed = discord.Embed(title=self.question, color=0xEDEDED)
        poll_embed.set_author(name="POLL")
        poll_embed.set_thumbnail(url=self.thumbnail)

        if self.alternatives:
            for key, alternative in enumerate(self.alternatives):
                poll_embed.add_field(
                    name=self.icons[key], value=alternative, inline=False
                )
        else:
            poll_embed.add_field(name=self.icons[0], value="Ja", inline=False)
            poll_embed.add_field(name=self.icons[1], value="Nei", inline=False)

        return poll_embed

    async def create_poll(self):
        if len(self.alternatives) > 9:
            raise Exception("Poll received too many args.")

        poll_embed = await self.create_poll_embed()
        poll_message = await self.ctx.send(embed=poll_embed)

        if self.alternatives:
            for key, alternative in enumerate(self.alternatives):
                await poll_message.add_reaction(self.icons[key])
        else:
            await poll_message.add_reaction(self.icons[0])
            await poll_message.add_reaction(self.icons[1])
