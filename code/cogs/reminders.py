import discord
from discord.ext import commands
import json
import time


class Reminders(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remind(self, ctx: commands.Context, *, args: str):
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["reminders"]
        args = args.split(" ")
        topop = 0
        endtime = time.time()
        for arg in args:
            if [arg.endswith(char) for char in "smhdMy"]:
                if not arg[:-1].isdigit():
                    break
                topop += 1
                if arg.endswith("s"):
                    endtime += int(arg.replace("s", ""))
                elif arg.endswith("m"):
                    endtime += int(arg.replace("m", "")) * 60
                elif arg.endswith("h"):
                    endtime += int(arg.replace("h", "")) * 3600
                elif arg.endswith("d"):
                    endtime += int(arg.replace("d", "")) * 86400
                elif arg.endswith("M"):
                    endtime += int(arg.replace("M", "")) * 2629800
                elif arg.endswith("y"):
                    endtime += int(arg.replace("y", "")) * 31556952
        if topop == 0:
            await ctx.send(embed=discord.Embed(title=useful["invalid_format"], color=0xff0000))
            return

        args = args[topop:]
        args = " ".join(args)
        if args == "":
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