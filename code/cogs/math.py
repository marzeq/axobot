import discord
from discord.ext import commands
import simpleeval
import ast
import random
import re
import time
class Funcs:
    pass


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
            list=lambda *args: list(args),
            time=time.time,
            round=round
        )
        if len(expr) >= 3 and await self.client.is_owner(ctx.author):
            fc = expr[2:]
            for func in fc:
                func = func.replace("`", "").replace("py\n", "")
                exec(f"{func}\nFuncs.{func.split(' ')[1].split('(')[0]} = {func.split(' ')[1].split('(')[0]}")
                funcs.update({func.split(' ')[1].split('(')[0]: getattr(globals()["Funcs"](), func.split(' ')[1].split('(')[0])})
        try:
            if len(expr) >= 2:
                names = ast.literal_eval(expr[1])
                if type(simpleeval.simple_eval(expr[0], functions=funcs, names=names)) == bytes:
                    res = simpleeval.simple_eval(expr[0], functions=funcs, names=names).decode("utf-8")
                    ansi_escape = re.compile(r'''
                                   \x1B  # ESC
                                   (?:   # 7-bit C1 Fe (except CSI)
                                       [@-Z\\-_]
                                   |     # or [ for CSI, followed by a control sequence
                                       \[
                                       [0-?]*  # Parameter bytes
                                       [ -/]*  # Intermediate bytes
                                       [@-~]   # Final byte
                                   )
                            ''', re.VERBOSE)
                    res = ansi_escape.sub('', res)
                else:
                    res = simpleeval.simple_eval(expr[0], functions=funcs, names=names)
            else:
                if type(simpleeval.simple_eval(expr[0], functions=funcs)) == bytes:
                    res = simpleeval.simple_eval(expr[0], functions=funcs).decode("utf-8")
                    ansi_escape = re.compile(r'''
                                   \x1B  # ESC
                                   (?:   # 7-bit C1 Fe (except CSI)
                                       [@-Z\\-_]
                                   |     # or [ for CSI, followed by a control sequence
                                       \[
                                       [0-?]*  # Parameter bytes
                                       [ -/]*  # Intermediate bytes
                                       [@-~]   # Final byte
                                   )
                            ''', re.VERBOSE)
                    res = ansi_escape.sub('', res)
                else:
                    res = simpleeval.simple_eval(expr[0], functions=funcs)
            res = str(res)
            if len(res) > 1028:
                res = res[:1013] + "[...]"
            await ctx.send(embed=discord.Embed().add_field(name="**Output:**", value="```" + res + "```"))
        except:
            pass


def setup(client):
    client.add_cog(Math(client))
    Funcs.client = client

if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
