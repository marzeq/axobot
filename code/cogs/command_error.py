import discord
from discord.ext import commands


class CommandError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # noqa
        print(error)
        emoji = '🚫'
        if type(error) == discord.ext.commands.CommandNotFound:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=f"**This command does not exist!**", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
        elif type(error) == discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=f"**You didn't provide a argument that is required!**", color=0xdb2a2a)
            await ctx.send(embed=response_embed)
        elif error == discord.ext.commands.errors.BotMissingPermissions:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=f"**I'm missing the required permissions for this comamnd!**",
                                           color=0xdb2a2a)
            await ctx.send(embed=response_embed)
        else:
            raise error

def setup(client):
    client.add_cog(CommandError(client))
