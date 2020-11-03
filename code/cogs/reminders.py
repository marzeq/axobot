import discord
from discord.ext import commands
import json
import time


class Reminders(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remind(self, ctx: commands.Context, when: str, *, reminder: str):
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["reminders"]
        if ''.join([i for i in when if not i.isdigit()]) != "[,,,,]":
            await ctx.send(embed=discord.Embed(title=useful["invalid_format"], color=0xff0000))
            pass
        else:
            whenl = when.strip('][').split(',')
            months = int(whenl[0]) * 2629800
            days = int(whenl[1]) * 86400
            hours = int(whenl[2]) * 3600
            minutes = int(whenl[3]) * 60
            seconds = int(whenl[4])
            endtime = time.time() + months + days + hours + minutes + seconds
            with open("config/tasks.json", "r") as f:
                reminders = json.load(f)

            with open("config/tasks.json", "w") as f:
                reminders[str(round(endtime))] = {"remind": {"value": reminder, "who": ctx.author.id}}
                json.dump(reminders, f, indent=4)
            await ctx.send(embed=discord.Embed(title=useful["result"], color=0x00ff00))


def setup(client):
    client.add_cog(Reminders(client))
