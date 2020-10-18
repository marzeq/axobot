import discord
from discord.ext import commands
import json


class Prefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx, *, prefix: str):
        with open('config/config.json', 'r') as f:
            config = json.load(f)

        with open("config/config.json", "w") as f:
            config[str(ctx.message.guild.id)]["prefix"] = prefix
            json.dump(config, f, indent=4)
        embed = discord.Embed(title=f"**Changed the custom prefix to `{prefix}`.**", color=0x00ff00)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Prefix(client))
