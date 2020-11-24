# https://pastebin.com/vX9PVLqf
import discord
from discord.ext import commands
import json


class Embed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ebd"])
    async def embed(self, ctx, *, jsonstr: str):
        # # Getting all translations
        # lang = self.client.get_server_lang(ctx.guild)
        # useful = lang["translations"]["embed"]

        if jsonstr.startswith("```json"):
            jsonstr = jsonstr[7:]
        elif jsonstr.startswith("```"):
            jsonstr = jsonstr[3:]
        if jsonstr.endswith("```"):
            jsonstr = jsonstr[:-3]

        try:
            jsondict: dict = json.loads(jsonstr)
            if jsondict.get("color") is not None:
                jsondict["color"] = int(jsondict["color"], 16)

        except:
            await ctx.send(embed=discord.Embed(
                title="This embeds` code is invalid. Try using the example one here: https://pastebin.com/vX9PVLqf !", color=0xdb2a2a
            ))
            return

        try:
            # Creates and sends the created embed
            response_embed = discord.Embed.from_dict(jsondict)
            await ctx.send(embed=response_embed)
        except:
            await ctx.send(embed=discord.Embed(
                title="Something went wrong here! Make sure that this embed is valid! Try checking with the example here!",
                color=0xdb2a2a
            ))
            return


def setup(client):
    client.add_cog(Embed(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
