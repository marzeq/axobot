import discord
from discord.ext import commands
import simpleeval
import ast


class BotStats(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client
        simpleeval.MAX_POWER = 100

    @commands.command()
    async def math(self, ctx: commands.Context, *, expr: str):
        expr = expr.split(" | ")
        try:
            if len(expr) >= 3 and self.client.is_owner(ctx.author):
                names = ast.literal_eval(expr[1])
                defaultfuncs = simpleeval.DEFAULT_FUNCTIONS.copy()
                funcs = defaultfuncs.update(ast.literal_eval(expr[2]))
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0], names=names, functions=funcs)}"))
            elif len(expr) >= 2:
                names = ast.literal_eval(expr[1])
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0], names=names)}"))
            else:
                await ctx.send(embed=discord.Embed(title=f"{simpleeval.simple_eval(expr[0])}"))
        except:
            pass


def setup(client):
    client.add_cog(BotStats(client))
