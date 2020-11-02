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
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["ban"]

        # If user has perms to ban
        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:

            # Ban the member
            await member.ban(reason=reason)

            # Creates and sends the response embed
            response_embed = discord.Embed(title=useful["banned"].format(member, reason), color=0xdb2a2a)
            await ctx.send(embed=response_embed)

    @commands.command()
    async def tempban(self, ctx: commands.Context, when: str, user: discord.User, *, reason: str = "No reason provided."):
        # If user has perms to ban
        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:
            if ''.join([i for i in when if not i.isdigit()]) != "[,,,,]":
                await ctx.send(embed=discord.Embed(
                    title="The time for the tempban should be in this format: [months,days,hours,minutes,seconds]",
                    color=0xff0000))
                pass
            else:
                whenl = when.strip('][').split(',')
                months = int(whenl[0]) * 2629800
                days = int(whenl[1]) * 86400
                hours = int(whenl[2]) * 3600
                minutes = int(whenl[3]) * 60
                seconds = int(whenl[4])
                endtime = time.time() + months + days + hours + minutes + seconds
                with open("config/tasks.json", "r") as f:
                    reminders = json.load(f)
                member: discord.Member = ctx.guild.get_membed(user.id)
                await member.ban(reason=reason)
                with open("config/tasks.json", "w") as f:
                    reminders[str(round(endtime))] = {"unban": {"user": f"{user.name}#{user.discriminator}", "guild": ctx.guild.id}}
                    json.dump(reminders, f, indent=4)
                await ctx.send(embed=discord.Embed(title="This member is now temp-banned.", color=0x00ff00))


def setup(client):
    client.add_cog(Ban(client))
