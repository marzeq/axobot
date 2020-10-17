import discord
from discord.ext import commands
import os

with open("token.txt", "r") as f:
    TOKEN = f.read()

PREFIX = "--"

client = commands.Bot(command_prefix=PREFIX)

client.command_descriptions = \
{
    "help": {
        "args": {
            "command": {
                "required": False
            }
        },
        "desc": "Shows all commands and their respective arguments, aliases and its description. If a command name is passed, it will show help about the specified command",
        "aliases": [],
        "required_perms": None
    },
    "ban": {
        "args": {
            "member": {
                "required": True
            },
            "reason": {
                "required": False
            }
        },
        "desc": "Bans a specified member. If provided, sends a ban reason to the server audit log.",
        "aliases": [],
        "required_perms": "Ban Members or Administrator"
    },
    "kick": {
        "args": {
            "member": {
                "required": True
            },
            "reason": {
                "required": False
            }
        },
        "desc": "Kick a specified member. If provided, sends a kick reason to the server audit log.",
        "aliases": [],
        "required_perms": "Kick Members or Administrator"
    }
}

client.admin_command_descriptions = \
{
    "admin_help": {
        "args": {
            "command": {
                "required": False
            }
        },
        "desc": "Shows all admin commands and their respective arguments, aliases and its description. If a command name is passed, it will show help about the specified admin command",
        "aliases": ["adminhelp", "admhelp"],
        "required_perms": "Bot Owner"
    },
    "load": {
        "args": {
            "extension": {
                "required": False
            }
        },
        "desc": "Loads all cogs avalible. If an extension (cog) is provided, it will load only the specified cog.",
        "aliases": ["l"],
        "required_perms": "Bot Owner"
    },
    "unload": {
        "args": {
            "extension": {
                "required": False
            }
        },
        "desc": "Unoads all cogs avalible. If an extension (cog) is provided, it will unload only the specified cog.",
        "aliases": ["ul"],
        "required_perms": "Bot Owner"
    },
    "reload": {
        "args": {
            "extension": {
                "required": False
            }
        },
        "desc": "Reoads all cogs avalible. If an extension (cog) is provided, it will reload only the specified cog.",
        "aliases": ["rl"],
        "required_perms": "Bot Owner"
    }
}


@client.event
async def on_ready():
    print("The bot is ready.")


# Basic cog control commands

@client.command(aliases=["l"])
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
@client.command(aliases=["ul"])
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
@client.command(aliases=["rl"])
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
