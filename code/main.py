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
os.chdir(f"{pathlib.Path(__file__).parent.absolute()}")

# Determining if we need to send a restart alert after everything is finished
if len(sys.argv) >= 2:
    channel_to_send = sys.argv[1]
else:
    channel_to_send = 0

with open("config/token.txt", "r") as f:
    TOKEN = f.read()


# Returns the custom prefix for a specified guild
def get_prefix(client, message):  # noqa
    if message.guild is None:
        return "--"
    with open('config/config.json', 'r') as f:  # noqa
        config = json.load(f)

    return config[str(message.guild.id)]["prefix"]


# Returns the provided servers language file
def get_server_lang(guild: discord.Guild) -> dict:
    if guild is None:
        with open(f"translations/en_US.json", "r") as langf:
            lng = json.load(langf)
            return lng
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        lang_code = cfg[str(guild.id)]["lang"]
        with open(f"translations/{lang_code}.json", "r") as langf:
            lng = json.load(langf)
    return lng


def get_server_lang_code(guild: discord.Guild) -> str:
    if guild is None:
        return "en_US"
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        lang_code = cfg[str(guild.id)]["lang"]
    return lang_code


# Creates the client instance
client = commands.Bot(command_prefix=get_prefix)

# So you can access the functions from cogs
client.get_server_lang = get_server_lang
client.get_server_lang_code = get_server_lang_code

# Setting up connection between Reddit and the bot
with open("config/reddit.json", "r") as f:
    reddit = json.load(f)

client.reddit = praw.Reddit(client_id=reddit["id"],
                            client_secret=reddit["secret"],
                            user_agent='RoboMarzeq by u/Marzeq_')

client.__version__ = "0.1.11b"

# Admin command descriptions. It's here because it shouldn't be translated
client.admin_command_descriptions = \
    {
        "admin_help": {
            "args": {
                "command": {
                    "required": False
                }
            },
            "desc": "Shows all admin commands and their respective arguments, aliases and its description. If a command name is passed, it will show help about the specified admin command",
            "aliases": ["adminhelp", "admhelp"]
        },
        "load": {
            "args": {
                "extension": {
                    "required": False
                }
            },
            "desc": "Loads all cogs avalible. If an extension (cog) is provided, it will load only the specified cog.",
            "aliases": ["l"]
        },
        "unload": {
            "args": {
                "extension": {
                    "required": False
                }
            },
            "desc": "Unoads all cogs avalible. If an extension (cog) is provided, it will unload only the specified cog.",
            "aliases": ["ul"]
        },
        "reload": {
            "args": {
                "extension": {
                    "required": False
                }
            },
            "desc": "Reoads all cogs avalible. If an extension (cog) is provided, it will reload only the specified cog.",
            "aliases": ["rl"]
        },
        "update": {
            "args": {},
            "desc": "Updates the internal files from the git repo and reruns the program",
            "aliases": ["up"]
        },
        "hardreload": {
            "args": {},
            "desc": "Reruns the program",
            "aliases": ["hr"]
        },
        "presence": {
            "args": {
                "type": {"required": True},
                "presence": {"required": True}
            },
            "desc": "Changes the bot presence. Set type 0 for watching, 1 for listening, 2 for playing and 3 to reset.",
            "aliases": []
        }
    }

# All valid language codes
client.valid_langs = ["en_US", "es_ES", "pl_PL", "pt_BR", "ru_RU"]


# Shows that the bot is working
@client.event
async def on_ready():
    print("The bot is ready.")
    await do_undone_tasks()
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
        for extensionname in os.listdir(f"./cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.load_extension(f"cogs.{extensionname[:-3]}")
                except commands.errors.ExtensionAlreadyLoaded or commands.errors.ExtensionNotFound:
                    pass
        await ctx.message.channel.send(f"Loaded all extensions!")


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
        for extensionname in os.listdir(f"./cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.unload_extension(f"cogs.{extensionname[:-3]}")
                except commands.ExtensionNotLoaded or commands.errors.ExtensionNotFound:
                    pass
        await ctx.message.channel.send("Unloaded all extensions!")


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
        for extensionname in os.listdir(f"./cogs"):
            if extensionname.endswith(".py"):
                try:
                    client.reload_extension(f"cogs.{extensionname[:-3]}")
                except commands.errors.ExtensionNotFound:
                    pass
        await ctx.message.channel.send("Reloaded all extensions!")


for filename in os.listdir(f"./cogs"):
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


@client.command(aliases=["hr"])
async def hardreload(ctx):
    if not await client.is_owner(ctx.author):
        return
    await ctx.send(embed=discord.Embed(title="🟡  Restarting..", color=0xdaed2d))
    os.system(f"{sys.executable} {os.path.dirname(os.path.realpath(__file__))}/main.py {ctx.channel.id}")


async def do_undone_tasks():
    with open("config/tasks.json", "r+") as file:
        tasksjson: dict = json.load(file)
    action = False
    for pos in range(len(tasksjson)):
        if list(int(n) for n in list(tasksjson.keys()))[pos] <= round(time.time()):
            key = list(str(n) for n in list(tasksjson.keys()))[pos]
            dct = tasksjson[key]
            instruction = list(str(n) for n in list(dct.keys()))[0]
            if instruction == "print":
                print(dct[instruction])
            elif instruction == "remind":
                user = await client.fetch_user(dct[instruction]["who"])
                embed = discord.Embed(title=dct[instruction]["value"])
                await user.send(embed=embed)
            elif instruction == "unban":
                guild: discord.Guild = await client.fetch_guild(dct[instruction]["guild"])
                await guild.unban(user=dct[instruction]["who"])
            tasksjson.pop(key)
            action = True
            break
        else:
            pass
    if action:
        with open("config/tasks.json", "w") as file:
            json.dump(tasksjson, file, indent=4)


client.logger = Logger("log")


# Thanks to mini_bomba for helping me with this part of code
@client.event
async def on_error(name, *args, **_):
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


class NoItemFound(Exception):
    pass


client.NoItemFound = NoItemFound

# Run the bot
client.run(TOKEN)
