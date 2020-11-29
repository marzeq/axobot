import discord
from discord.ext import commands
import json


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.utils = __import__("utils")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
        # Getting all translations
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["ban"]

        # If user has perms to ban
        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:

            # Ban the member
            try:
                await member.ban(reason=reason)
            except:
                raise commands.errors.BotMissingPermissions("ban_members")

            # Creates and sends the response embed
            response_embed = discord.Embed(title=useful["banned"].format(member, reason), color=0xdb2a2a)
            await ctx.send(embed=response_embed)

    @commands.command()
    async def tempban(self, ctx: commands.Context, user: discord.User, *, args):
        # Getting all translations
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["ban"]

        # If user has perms to ban
        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:
            args, endtime = await self.utils.process_time(ctx, args, useful["invalid_format"])
            if args == "err":
                return
            elif args == "":
                reason = "No reason provided"
            else:
                reason = args
            if len(reason) > 256:
                response_embed = discord.Embed(title=useful["too_long"], color=0xdb2a2a)
                await ctx.send(embed=response_embed)
                return
            with open("config/tasks.json", "r") as f:
                reminders = json.load(f)
            member: discord.Member = ctx.guild.get_membed(user.id)
            try:
                await member.ban(reason=reason)
            except:
                raise commands.errors.BotMissingPermissions("ban_members")
            with open("config/tasks.json", "w") as f:
                reminders[str(round(endtime))] = {"unban": {"user": f"{user.name}#{user.discriminator}", "guild": ctx.guild.id}}
                json.dump(reminders, f, indent=4)
            await ctx.send(embed=discord.Embed(title=useful["tempbanned"].format(member, reason), color=0x00ff00))


def setup(client):
    client.add_cog(Ban(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
