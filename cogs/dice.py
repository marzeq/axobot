import discord
from discord.ext import commands
import random
from utils import commands as command


class Dice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dice(self, ctx: commands.Context, start: int = 1, end: int = 6):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if start < end:
            val = random.randint(start, end)
        else:
            val = random.randint(end, start)
        if len(str(val)) > 1024:
            response_embed = discord.Embed(title="This number is too big!", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return
        embed = discord.Embed(title="🎲 Rolling the dice...")
        embed.add_field(name="Your number:", value=f"```{val}```")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Dice(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
