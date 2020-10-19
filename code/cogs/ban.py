import discord
from discord.ext import commands


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


def setup(client):
    client.add_cog(Ban(client))
