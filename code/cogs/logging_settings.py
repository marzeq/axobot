import discord  # noqa
from discord.ext import commands
import json


class LoggingSettings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def log(self, ctx, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            # Getting all translations
            lang = self.client.get_server_lang(ctx.guild)
            useful = lang["translations"]["logging"]
            with open('config/config.json', 'r') as f:
                config = json.load(f)
            with open("config/config.json", "w") as f:
                config[str(ctx.message.guild.id)]["logging"]["channel"] = channel.id
                json.dump(config, f, indent=4)
            embed = discord.Embed(title=useful["success"], color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command(aliases=["bl"])
    @commands.guild_only()
    async def blacklist(self, ctx, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels or ctx.author.guild_permissions.administrator:
            # Getting all translations
            lang = self.client.get_server_lang(ctx.guild)
            useful = lang["translations"]["logging"]
            with open('config/config.json', 'r') as f:
                config = json.load(f)
            if channel.id in config[str(ctx.message.guild.id)]["logging"]["blacklist-channels"]:
                with open("config/config.json", "w") as f:
                    config[str(ctx.message.guild.id)]["logging"]["blacklist-channels"].remove(channel.id)
                    json.dump(config, f, indent=4)
            else:
                with open("config/config.json", "w") as f:
                    config[str(ctx.message.guild.id)]["logging"]["blacklist-channels"].append(channel.id)
                    json.dump(config, f, indent=4)
            embed = discord.Embed(title=useful["success"], color=0x00ff00)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(LoggingSettings(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
