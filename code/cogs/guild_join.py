import discord
from discord.ext import commands
import json
import random


class GuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        # Dict that we update the json file with
        toupdate = {str(guild.id): {"prefix": "--", "lang": "en_US", "logging": {"channel": 0, "blacklist-channels": []}}, "tickets": {"category": 0}, "disabled_commands": []}
        with open("config/config.json", "r+") as f:

            # Get the file
            config = json.load(f)

            # Update the config
            config.update(toupdate)

            # Replace current config with updated one
            f.seek(0)
            json.dump(config, f, indent=4)

        # Choose a random txt channel to send the welcome message to
        list1 = guild.text_channels
        channel = random.choice(list1)

        # Getting all translations
        lang = self.client.get_server_lang(guild)
        useful = lang["translations"]["guild_join"]

        # Creates and sends the response embed
        embed = discord.Embed(title=useful["welcome"], color=0x00ff00)
        embed.add_field(name=useful["thx_for_invite"], value=useful["prefix"],)
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(GuildJoin(client))

if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")