import discord
from discord.ext import commands
import json
import time


class Reminders(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remind(self, ctx: commands.Context, *, args: str):
        lang = self.client.get_server_lang(str(ctx.guild.id))
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
        with open("config/tasks.json", "r") as f:
            reminders = json.load(f)

        with open("config/tasks.json", "w") as f:
            reminders[str(round(endtime))] = {"remind": {"value": args, "who": ctx.author.id}}
            json.dump(reminders, f, indent=4)
        await ctx.send(embed=discord.Embed(title=useful["result"], color=0x00ff00))


def setup(client):
    client.add_cog(Reminders(client))
