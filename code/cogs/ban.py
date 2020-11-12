import discord
from discord.ext import commands
import time
import json


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
        # Getting all translations
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["ban"]

        # If user has perms to ban
        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:

            # Ban the member
            await member.ban(reason=reason)

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
            args = args.split(" ")
            topop = 0
            endtime = time.time()
            for arg in args:
                if [arg.endswith(char) for char in "smhdMy"]:
                    if not arg[:-1].isdigit():
                        break
                    topop += 1
                    if arg.endswith("s"):
                        endtime += int(arg.replace("s", ""))
                    elif arg.endswith("m"):
                        endtime += int(arg.replace("m", "")) * 60
                    elif arg.endswith("h"):
                        endtime += int(arg.replace("h", "")) * 3600
                    elif arg.endswith("d"):
                        endtime += int(arg.replace("d", "")) * 86400
                    elif arg.endswith("M"):
                        endtime += int(arg.replace("M", "")) * 2629800
                    elif arg.endswith("y"):
                        endtime += int(arg.replace("y", "")) * 31556952
            if topop == 0:
                await ctx.send(embed=discord.Embed(title=useful["invalid_format"], color=0xff0000))
                return

            args = args[topop:]
            args = " ".join(args)
            if args == "":
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
            await member.ban(reason=reason)
            with open("config/tasks.json", "w") as f:
                reminders[str(round(endtime))] = {"unban": {"user": f"{user.name}#{user.discriminator}", "guild": ctx.guild.id}}
                json.dump(reminders, f, indent=4)
            await ctx.send(embed=discord.Embed(title=useful["tempbanned"].format(member, reason), color=0x00ff00))


def setup(client):
    client.add_cog(Ban(client))
