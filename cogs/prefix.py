import discord
from discord.ext import commands
import json
from utils import language
from utils import commands as command


class Prefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx, *, prefix: str):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            lang = language.get_server_lang(ctx.guild)
            useful = lang["translations"]["prefix"]
            with open('config/config.json', 'r') as f:
                config = json.load(f)

            with open("config/config.json", "w") as f:
                config[str(ctx.message.guild.id)]["prefix"] = prefix
                json.dump(config, f, indent=4)
            embed = discord.Embed(title=useful["changed_prefix"].replace("%%prefix%%", prefix), color=0x00ff00)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Prefix(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
