import discord
from discord.ext import commands
import os

with open("token.txt", "r") as f:
    TOKEN = f.read()

PREFIX = "#!"

client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    print("The bot is ready.")


# Basic cog control commands

@client.command()
async def load(ctx, extension=None):
    if not await client.is_owner(ctx.author):
        return
    if extension:
        try:
            client.load_extension(f"cogs.{extension}")
            await ctx.message.channel.send(f"Loaded {extension}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.message.channel.send(f"The cog {extension} does not exist!")
    else:
        for extensionname in os.listdir(f"./cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.load_extension(f"cogs.{extensionname[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass
        await ctx.message.channel.send(f"Loaded all extensions!")
@client.command()
async def unload(ctx, extension=None):
    if not await client.is_owner(ctx.author):
        return
    if extension:
        try:
            client.unload_extension(f"cogs.{extension}")
            await ctx.message.channel.send(f"Unloaded {extension}")
        except commands.ExtensionNotLoaded:
            await ctx.message.channel.send(f"The cog {extension} is not loaded or does not exist!")
    else:
        for extensionname in os.listdir(f"./cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.unload_extension(f"cogs.{extensionname[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass
        await ctx.message.channel.send("Unloaded all extensions!")
@client.command()
async def reload(ctx, extension=None):
    if not await client.is_owner(ctx.author):
        return
    if extension:
        try:
            client.reload_extension(f"cogs.{extension}")
            await ctx.message.channel.send(f"Reloaded {extension}")
        except:
            await ctx.message.channel.send(f"The cog {extension} is not loaded or does not exist!")
    else:
        for extensionname in os.listdir(f"./cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.reload_extension(f"cogs.{extensionname[:-3]}")
                except:
                    pass
        await ctx.message.channel.send("Reloaded all extensions!")


for filename in os.listdir(f"./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
