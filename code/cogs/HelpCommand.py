import discord
from discord.ext import commands


class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        client.remove_command("help")

    @commands.command()
    async def help(self, ctx):
        ctx.send("AAAA")


def setup(client):
    client.add_cog(HelpCommand(client))
