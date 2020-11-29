import discord
from discord.ext import commands
import json


class Reminders(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.utils = __import__("utils")

    @commands.command()
    async def remind(self, ctx: commands.Context, *, args: str):
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["reminders"]
        args, endtime = await self.utils.process_time(ctx, args, useful["invalid_format"])
        if args == "err":
            return
        elif args == "":
            raise discord.ext.commands.errors.MissingRequiredArgument(ReminderArg())
        if len(args) > 256:
            response_embed = discord.Embed(title=useful["too_long"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return
        with open("config/tasks.json", "r") as f:
            reminders = json.load(f)

        with open("config/tasks.json", "w") as f:
            reminders[str(round(endtime))] = {"remind": {"value": args, "who": ctx.author.id}}
            json.dump(reminders, f, indent=4)
        await ctx.send(embed=discord.Embed(title=useful["result"], color=0x00ff00))


class ReminderArg:
    name = "reminder"


def setup(client):
    client.add_cog(Reminders(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
