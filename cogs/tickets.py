import discord
from discord.ext import commands
import json
import random
from utils import commands as command


class Tickets(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command()
    async def ticket_category(self, ctx: commands.Context, category: discord.CategoryChannel):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            with open("config/config.json", "r+") as f:
                # Get the file
                config = json.load(f)
                try:
                    config[str(ctx.guild.id)]["tickets"]
                except KeyError:
                    config[str(ctx.guild.id)]["tickets"] = {}
                    f.seek(0)
                    json.dump(config, f, indent=4)

                config[str(ctx.guild.id)]["tickets"]["category"] = category.id

                # Replace current config with updated one
                f.seek(0)
                json.dump(config, f, indent=4)
            embed = discord.Embed(title="Successfully updated this setting!", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    async def ticket_role(self, ctx: commands.Context, role: discord.Role):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            with open("config/config.json", "r+") as f:
                # Get the file
                config = json.load(f)
                try:
                    config[str(ctx.guild.id)]["tickets"]
                except KeyError:
                    config[str(ctx.guild.id)]["tickets"] = {}
                    f.seek(0)
                    json.dump(config, f, indent=4)

                config[str(ctx.guild.id)]["tickets"]["role"] = role.id

                # Replace current config with updated one
                f.seek(0)
                json.dump(config, f, indent=4)
            embed = discord.Embed(title="Successfully updated this setting!", color=0x00ff00)
            await ctx.send(embed=embed)

    @commands.command()
    async def ticket(self, ctx: commands.Context):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        with open("config/config.json", "r+") as f:
            # Get the file
            config = json.load(f)
            try:
                config[str(ctx.guild.id)]["tickets"]
            except KeyError:
                config[str(ctx.guild.id)]["tickets"] = {}
                f.seek(0)
                json.dump(config, f, indent=4)
            try:
                category_id = config[str(ctx.guild.id)]["tickets"]["category"]
            except KeyError:
                category_id = 0
            try:
                role_id = config[str(ctx.guild.id)]["tickets"]["role"]
            except KeyError:
                role_id = 0

        if role_id == 0 or category_id == 0:
            response_embed = discord.Embed(title="The role or the category for tickets was setup incorrectly or is invalid!", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return

        category = self.client.get_channel(category_id)
        channel: discord.TextChannel = await category.create_text_channel(f"ticket-{ctx.author.name}")
        role: discord.Role = ctx.guild.get_role(role_id)
        try:
            assigned_staff: discord.Member = random.choice(role.members)
        except IndexError:
            response_embed = discord.Embed(title="There are no users that have the tickets role!", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await channel.set_permissions(assigned_staff, read_messages=True)
        await channel.set_permissions(ctx.author, read_messages=True)
        await channel.send(f"✅ {ctx.author.mention} your ticket was assigned to: {assigned_staff.mention}")

    @commands.command()
    async def close(self, ctx: commands.Context, channel=None):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if channel is None:
            channel: discord.TextChannel = ctx.channel
        else:
            channel: discord.TextChannel = channel
        with open("config/config.json", "r+") as f:
            # Get the file
            config = json.load(f)
            try:
                category_id = config[str(ctx.guild.id)]["tickets"]["category"]
            except KeyError:
                category_id = 0
            try:
                role_id = config[str(ctx.guild.id)]["tickets"]["role"]
            except KeyError:
                role_id = 0

        if role_id == 0 or category_id == 0:
            response_embed = discord.Embed(title="The role or the category for tickets was setup incorrectly or is invalid!", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return

        category = self.client.get_channel(category_id)
        if category.id != channel.category.id:
            response_embed = discord.Embed(title="This is not a ticket channel!", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return
        role: discord.Role = ctx.guild.get_role(role_id)
        if role in ctx.author.roles or ctx.author.name.replace("-", " ") in channel.name.replace("-", " "):
            await channel.delete()


def setup(client):
    client.add_cog(Tickets(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
