import discord
from discord.ext import commands
import simpleeval
import ast
import random
import time
from utils import language
from utils import commands as command


class Math(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client
        simpleeval.MAX_POWER = 100

    @commands.command(aliases=["safe_eval", "se"])
    async def math(self, ctx: commands.Context, *, expr: str):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        # Make a list of expressions [expression to be evaluated | variables (optional)]
        expr = expr.split(" | ")

        # Add some custom default funcs
        funcs = simpleeval.DEFAULT_FUNCTIONS.copy()
        funcs.update(
            choice=random.choice,
            list=lambda *args: list(args),
            time=time.time,
            round=round
        )

        # Empty variables dict
        names = {}

        # Update the names with custom names if provided
        try:
            names.update(ast.literal_eval(expr[1]))
        except IndexError:
            pass
        res = str(simpleeval.simple_eval(expr[0], functions=funcs, names=names))
        if len(res) > 1028:
            res = res[:1013] + "[...]"
        # TODO: Translate this
        await ctx.send(embed=discord.Embed().add_field(name="**Output:**", value="```" + res + "```"))


def setup(client):
    client.add_cog(Math(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
