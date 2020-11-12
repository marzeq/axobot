import discord
from discord.ext import commands
import simpleeval
import ast
import random


class Math(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client
        simpleeval.MAX_POWER = 100

    @commands.command(aliases=["safe_eval", "se"])
    async def math(self, ctx: commands.Context, *, expr: str):
        expr = expr.split(" | ")
        funcs = simpleeval.DEFAULT_FUNCTIONS.copy()
        funcs.update(
            choice=random.choice,
            list=lambda *args: list(args)
        )
        try:
            if len(expr) >= 2:
                names = ast.literal_eval(expr[1])
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0], names=names, functions=funcs)}"))
            else:
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0], functions=funcs)}"))
        except:
            pass


def setup(client):
    client.add_cog(Math(client))
