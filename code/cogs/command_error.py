import discord
from discord.ext import commands
from time import time


class CommandError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):  # noqa
        try:
            error.original
        except: # noqa
            error.original = type(error)
        # Getting all translations
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["command_error"]

        # Setting the emoji so I dont need to type it all the time
        emoji = '🚫'

        # If command does not exist
        if type(error) == discord.ext.commands.CommandNotFound:
            # Adds emoji
            await ctx.message.add_reaction(emoji)

            # Creates and sends the response embed
            response_embed = discord.Embed(title=useful["nonexistent_command"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)

        # If user doesn't have required perms for the command
        elif type(error) == discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["missing_argument"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)

        # If the bot doesn't have required perms for a specified command
        elif type(error) == discord.ext.commands.errors.BotMissingPermissions:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["bot_missing_permissions"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)

        elif type(error) == discord.ext.commands.errors.BadArgument:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["bad_format"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)

        elif type(error.original) == self.client.NoItemFound:
            await ctx.message.add_reaction(emoji)
            response_embed = discord.Embed(title=useful["item_doesnt_exist"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)

        # Raise the error so I can see it
        else:
            errorid = round(time())
            explain_embed = discord.Embed(title=useful["explain"].format(errorid))
            await ctx.send(embed=explain_embed)
            raise error
            # Rest of the command handler in /code/main.py/on_error

def setup(client):
    client.add_cog(CommandError(client))
