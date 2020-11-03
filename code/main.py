import discord
from discord.ext import commands
import os
from os import system as cmd
import json
import praw
from sys import executable
import time

with open("config/token.txt", "r") as f:
    TOKEN = f.read()

# Returns the custom prefix for a specified guild
def get_prefix(client, message):  # noqa
    with open('config/config.json', 'r') as f:  # noqa
        config = json.load(f)  # noqa

    return config[str(message.guild.id)]["prefix"]


# Returns the provided servers language file
def get_server_lang(guild_id: int) -> dict:
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        lang_code = cfg[guild_id]["lang"]
        with open(f"translations/{lang_code}.json", "r") as langf:
            lng = json.load(langf)
    return lng


def get_server_lang_code(guild_id: int) -> str:
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        lang_code = cfg[str(guild_id)]["lang"]
    return lang_code


# Creates the client instance
client = commands.Bot(command_prefix=get_prefix)

if executable.endswith(".exe"):
    client.os = "win"
else:
    client.os = "linux/macos"


# Setting up connection between Reddit and the bot
with open("config/reddit.json", "r") as f:
    reddit = json.load(f)

client.reddit = praw.Reddit(client_id=reddit["id"],
                            client_secret=reddit["secret"],
                            user_agent='RoboMarzeq by u/Marzeq_')


# So you can access the functions from cogs
client.get_server_lang = get_server_lang
client.get_server_lang_code = get_server_lang_code


# Admin command descriptions because it shouldn't be translated
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
    }
}

# All valid language codes
client.valid_langs = ["en_US", "es_ES", "pl_PL", "pr_BR", "ru_RU"]


# Shows that the bot is working
@client.event
async def on_ready():
    print("The bot is ready.")
    await do_undone_tasks()


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
    if client.os == "win":
        await ctx.send("Ok. [using windows]")
        cmd("reload.bat")
    elif client.os == "linux/macos":
        await ctx.send("Ok. [using linux/macos]")
        cmd("./reload.sh")
    else:
        await ctx.send("Couldn't determine the machine os... Returning...")
        return
@client.command(aliases=["hr"])
async def hardreload(ctx):
    if not await client.is_owner(ctx.author):
        return
    if client.os == "win":
        await ctx.send("Ok. [using windows]")
        cmd("python main.py")
    elif client.os == "linux/macos":
        await ctx.send("Ok. [using linux/macos]")
        cmd("python3 main.py")
    else:
        await ctx.send("Couldn't determine the machine os... Returning...")
        return


async def do_undone_tasks():
    with open("config/tasks.json", "r+") as f:
        tasksjson: dict = json.load(f)
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
        with open("config/tasks.json", "w") as f:
            json.dump(tasksjson, f, indent=4)


# Run the bot
client.run(TOKEN)
