import discord
from discord.ext import commands


class Empty(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def empty(self, ctx: commands.Context):
        if self.client.if_command_disabled(ctx.command.name, ctx.guild):
            return
        print(ctx.command.name)


def setup(client):
    client.add_cog(Empty(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
