import discord
from discord.ext import commands


class Kick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["kick"]
        if ctx.author.guild_permissions.kick_members or ctx.author.guild_permissions.administrator:
            response_embed = discord.Embed(title=useful["kicked"].format(member, reason), color=0xdb2a2a)
            await member.ban(reason=reason)
            await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Kick(client))
