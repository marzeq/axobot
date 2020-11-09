import discord
from discord.ext import commands
import os

class BotStats(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Dont translate or add to help command, lets make this a secret
    @commands.command()
    async def botstats(self, ctx):
        files = 1
        lines = int()
        for file in os.listdir(f"./cogs"):
            files += 1
            if file == "__pycache__":
                continue
            with open(f"cogs/{file}") as f:
                lines += len(f.readlines())
        with open("main.py") as f:
            lines += len(f.readlines())
        response_embed = discord.Embed(title=f"Current bot version: `{self.client.__version__}`\nNumber of files with code in them: `{files}`\nNumber of lines of code: `{lines}`")
        await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(BotStats(client))
