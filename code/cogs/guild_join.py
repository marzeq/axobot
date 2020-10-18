import discord
from discord.ext import commands
import json
import random


class GuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        toupdate = {str(guild.id): {"prefix": "--", "lang": "en_US"}}
        with open("config/config.json", "r+") as f:
            config = json.load(f)
            config.update(toupdate)
            f.seek(0)
            json.dump(config, f, indent=4)

        list1 = guild.text_channels
        channel = random.choice(list1)
        lang = self.client.get_server_lang(str(guild.id))
        useful = lang["translations"]["guild_join"]
        embed = discord.Embed(title=useful["welcome"], color=0x00ff00)
        embed.add_field(name=useful["thx_for_invite"], value=useful["prefix"],)
        await channel.send(embed=embed)


def setup(client):
    client.add_cog(GuildJoin(client))
