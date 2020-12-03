import discord
from discord.ext import commands
import json


class BlacklistCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def blacklist_command(self, ctx: commands.Context, mode: str, name: str):
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            with open("config/config.json", "r+") as f:
                config = json.load(f)
                try:
                    disabled = config[str(ctx.guild.id)]["disabled_commands"]
                except KeyError:
                    config[str(ctx.guild.id)]["disabled_commands"] = []
                    f.seek(0)
                    json.dump(config, f, indent=4)
                    disabled = []
            if mode == "rem" or mode == "remove":
                disabled.remove(name)
                response_embed = discord.Embed(title=f"Enabled the command `{name}` on the server!", color=0x00ff00)
                await ctx.send(embed=response_embed)
            elif mode == "add":
                disabled.append(name) if name not in disabled else lambda: None
                response_embed = discord.Embed(title=f"Disabled the command `{name}` on the server!", color=0xdb2a2a)
                await ctx.send(embed=response_embed)
            config[str(ctx.guild.id)]["disabled_commands"] = disabled
            with open("config/config.json", "r+") as f:
                open("config/config.json", "w").close()
                json.dump(config, f, indent=4)


def setup(client):
    client.add_cog(BlacklistCommand(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
