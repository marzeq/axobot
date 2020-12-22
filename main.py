import json
import os
import sys
import time
import traceback
from logging import Logger
import discord
import praw
from discord.ext import commands
import pathlib
import utils
from utils import main
os.chdir(f"{pathlib.Path(__file__).parent.absolute()}")

# Determining if we need to send a restart alert after everything is finished
if len(sys.argv) >= 2:
    channel_to_send = sys.argv[1]
else:
    channel_to_send = 0

with open("config/token.txt", "r") as f:
    TOKEN = f.read()


# Creates the client instance
client = commands.Bot(command_prefix=main.get_prefix, intents=discord.Intents.all())


# Setting up connection between Reddit and the bot
with open("config/reddit.json", "r") as f:
    reddit = json.load(f)

client.reddit = praw.Reddit(client_id=reddit["id"],
                            client_secret=reddit["secret"],
                            user_agent='MarzeqsUtilities by u/Marzeq_')

client.__version__ = "0.2b"


# Shows that the bot is working
@client.event
async def on_ready():
    print("The bot is ready.")
    await utils.tasks.do_undone_tasks(client)
    if channel_to_send != 0:
        channel = await client.fetch_channel(channel_to_send)
        await channel.send(embed=discord.Embed(title="✅  Restarted the bot", color=0x2be040))


# Basic cog control commands and auto cog loading
# I basically stole this from youtube but it's fine
@client.command(aliases=["l"])
async def load(ctx, extension=None):
    if not await client.is_owner(ctx.author):
        return
    if extension:
        try:
            client.load_extension(f"cogs.{extension}")
            await ctx.message.channel.send(f"Loaded {extension}")
        except commands.errors.ExtensionAlreadyLoaded or commands.errors.ExtensionNotFound:
            await ctx.message.channel.send(f"The cog {extension} is already loaded or does not exist!")
    else:
        for extensionname in os.listdir(f"cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.load_extension(f"cogs.{extensionname[:-3]}")
                except commands.errors.ExtensionAlreadyLoaded or commands.errors.ExtensionNotFound:
                    pass
        await ctx.send(embed=discord.Embed(title="✅  Loaded all extensions", color=0x2be040))


@client.command(aliases=["ul"])
async def unload(ctx, extension=None):
    if not await client.is_owner(ctx.author):
        return
    if extension:
        try:
            client.unload_extension(f"cogs.{extension}")
            await ctx.message.channel.send(f"Unloaded {extension}")
        except commands.ExtensionNotLoaded or commands.errors.ExtensionNotFound:
            await ctx.message.channel.send(f"The cog {extension} is not loaded or does not exist!")
    else:
        for extensionname in os.listdir(f"cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.unload_extension(f"cogs.{extensionname[:-3]}")
                except commands.ExtensionNotLoaded or commands.errors.ExtensionNotFound:
                    pass
        await ctx.send(embed=discord.Embed(title="✅  Unloaded all extensions", color=0x2be040))


@client.command(aliases=["rl"])
async def reload(ctx, extension=None):
    if not await client.is_owner(ctx.author):
        return
    if extension:
        try:
            client.reload_extension(f"cogs.{extension}")
            await ctx.message.channel.send(f"Reloaded {extension}")
        except commands.errors.ExtensionNotFound:
            await ctx.message.channel.send(f"The cog {extension} is not loaded or does not exist!")
    else:
        for extensionname in os.listdir(f"cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.reload_extension(f"cogs.{extensionname[:-3]}")
                except commands.errors.ExtensionNotFound:
                    pass
        await ctx.send(embed=discord.Embed(title="✅  Reloaded all extensions", color=0x2be040))


for filename in os.listdir(f"cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# Update the internal files from the git repo and rerun the program
@client.command(aliases=["up"])
async def update(ctx):
    if not await client.is_owner(ctx.author):
        return
    await ctx.send(embed=discord.Embed(title="🟡  Pulling from the GitHub repo..", color=0xdaed2d))
    os.system(f"git pull")
    await ctx.send(embed=discord.Embed(title="🟡  Restarting..", color=0xdaed2d))
    os.system(f"{sys.executable} {os.path.dirname(os.path.realpath(__file__))}/main.py {ctx.channel.id}")


@client.command(aliases=["prl"])
async def pull_reload(ctx):
    if not await client.is_owner(ctx.author):
        return
    await ctx.send(embed=discord.Embed(title="🟡  Pulling from the GitHub repo..", color=0xdaed2d))
    os.system(f"git pull")
    for extensionname in os.listdir(f"cogs"):
        if extensionname.endswith(".py"):
            try:
                client.reload_extension(f"cogs.{extensionname[:-3]}")
            except commands.errors.ExtensionNotFound:
                pass
    await ctx.send(embed=discord.Embed(title="✅  Reloaded all extensions", color=0x2be040))


@client.command(aliases=["hr"])
async def hardreload(ctx):
    if not await client.is_owner(ctx.author):
        return
    await ctx.send(embed=discord.Embed(title="🟡  Restarting..", color=0xdaed2d))
    os.system(f"{sys.executable} {os.path.dirname(os.path.realpath(__file__))}/main.py {ctx.channel.id}")


@client.command(aliases=["udpy"])
async def up_discordpy(ctx: commands.Context):
    if not await client.is_owner(ctx.author):
        return
    await ctx.send(embed=discord.Embed(title="🟡  Cloning from discord.pys' remote repo..", color=0xdaed2d))
    os.system(f"git clone https://github.com/Rapptz/discord.py")
    await ctx.send(embed=discord.Embed(title="🟡  Updating discord.py to the newest dev version..", color=0xdaed2d))
    os.chdir("discord.py")
    os.system(f"{sys.executable} -m pip install -U .[voice]")
    os.chdir("..")
    await ctx.send(embed=discord.Embed(title="🟡  Restarting..", color=0xdaed2d))
    os.system(f"{sys.executable} {os.path.dirname(os.path.realpath(__file__))}/main.py {ctx.channel.id}")


client.logger = Logger("log")


# Thanks to mini_bomba for helping me with this part of code
@client.event
async def on_error(name, *args, **_): # noqa
    errorid = round(time.time())
    etype, value, tb = sys.exc_info()
    tb = traceback.TracebackException(type(value), value, tb)
    ready = ["" for _ in range(1000)]
    n = 0
    for line in tb.format():
        if len(ready[n] + line + "\n") > 1024:
            n += 1
        ready[n] += line + "\n"
    ready = [x for x in ready if x != ""]
    embed = discord.Embed(title=f"Error id: `{errorid}`")
    lnenum = 0
    for lne in ready:
        lnenum += 1
        embed.add_field(name=f"Traceback part {lnenum}:", value=f"```{lne}```", inline=False)
    user = await client.fetch_user(500669086947344384)
    await user.send(embed=embed)
    client.logger.critical("".join(ready) + "Error id: " + str(errorid))

# Run the bot
client.run(TOKEN)
