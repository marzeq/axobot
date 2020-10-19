import discord
from discord.ext import commands


class CommandError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # noqa
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["command_error"]
        print(error)
        emoji = '🚫'
        if type(error) == discord.ext.commands.CommandNotFound:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["nonexistent_command"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
        elif type(error) == discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["missing_argument"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
        elif error == discord.ext.commands.errors.BotMissingPermissions:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["bot_missing_permissions"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
        else:
            raise error

def setup(client):
    client.add_cog(CommandError(client))
