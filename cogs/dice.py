import discord
from discord.ext import commands
import random
from utils import commands as command
from utils import language


class Dice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dice(self, ctx: commands.Context, start: int = 1, end: int = 6):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        # Getting all translations
        lang = language.get_server_lang(ctx.guild)
        useful = lang["translations"]["dice"]
        if start < end:
            val = random.randint(start, end)
        else:
            val = random.randint(end, start)
        if len(str(val)) > 1024:
            response_embed = discord.Embed(title=useful["number_too_big"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return
        embed = discord.Embed(title=useful["rolling"].replace("%%emoji%%", "🎲"))
        embed.add_field(name=useful["ur_number"], value=f"```{val}```")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Dice(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
