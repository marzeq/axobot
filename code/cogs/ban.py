import discord
from discord.ext import commands


class Ban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["ban"]
        if ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:
            await member.ban(reason=reason)


def setup(client):
    client.add_cog(Ban(client))
