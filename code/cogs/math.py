import discord
from discord.ext import commands
import simpleeval
import ast


class BotStats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def math(self, ctx: commands.Context, *, expr: str):
        expr = expr.split(" | ")
        try:
            if len(expr) >= 2:
                names = ast.literal_eval(expr[1])
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0], names=names)}"))
            else:
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0])}"))
        except:
            pass


def setup(client):
    client.add_cog(BotStats(client))
