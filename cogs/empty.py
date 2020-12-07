import discord
from discord.ext import commands
from utils import commands as command


class Empty(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def empty(self, ctx: commands.Context):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        await ctx.send("Nothing to see here :O")


def setup(client):
    client.add_cog(Empty(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
