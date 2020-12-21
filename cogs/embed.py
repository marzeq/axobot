# https://pastebin.com/vX9PVLqf
import discord
from discord.ext import commands
import json
from utils import commands as command
from utils import language


class Embed(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command(aliases=["ebd"])
    async def embed(self, ctx, *, jsonstr: str):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return

        # Getting all translations
        lang = language.get_server_lang(ctx.guild)
        useful = lang["translations"]["embed"]

        # Clear the string from code block indicators
        if jsonstr.startswith("```json"):
            jsonstr = jsonstr[7:]
        elif jsonstr.startswith("```"):
            jsonstr = jsonstr[3:]
        if jsonstr.endswith("```"):
            jsonstr = jsonstr[:-3]

        # If the json is valid
        try:
            # Make the string into a dictionary
            jsondict: dict = json.loads(jsonstr)

            # Check if a color is provided and convert it from str to base 16 int
            if jsondict.get("color") is not None:
                jsondict["color"] = int(jsondict["color"], 16)

        except:
            await ctx.send(embed=discord.Embed(
                title=useful["invalid"], color=0xdb2a2a
            ))
            return

        try:
            # Creates and sends the created embed
            response_embed = discord.Embed.from_dict(jsondict)
            await ctx.send(embed=response_embed)
        except:
            await ctx.send(embed=discord.Embed(
                title=useful["no_title"],
                color=0xdb2a2a
            ))
            return

    @commands.command(aliases=["eebd"])
    async def editembed(self, ctx: commands.Context, id: str, chid: str, *, jsonstr: str):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        # Getting all translations
        lang = language.get_server_lang(ctx.guild)
        useful = lang["translations"]["embed"]

        # If channel id is a valid int
        try:
            chid = int(chid)

        # Else
        except ValueError:
            chid = 0

        # Raise error if bad argument
        if chid == 0:
            raise discord.ext.commands.errors.BadArgument(ctx.message)

        # If channel id is a valid channel id
        try:
            chnl = await self.client.fetch_channel(chid)

        # Else
        except:
            raise discord.ext.commands.errors.BadArgument(ctx.message)

        # Same as above but with the message that's getting edited
        try:
            id = int(id)
        except ValueError:
            id = 0

        if id == 0:
            raise discord.ext.commands.errors.BadArgument(ctx.message)

        try:
            msg = await chnl.fetch_message(id)
        except:
            raise discord.ext.commands.errors.BadArgument(ctx.message)

        # For comments check the previous function
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
                title=useful["invalid"], color=0xdb2a2a
            ))
            return

        try:
            # Creates and sends the created embed
            response_embed = discord.Embed.from_dict(jsondict)
            await msg.edit(embed=response_embed)
        except:
            await ctx.send(embed=discord.Embed(
                title=useful["no_title"],
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
