from typing import Any
from discord.ext import commands
import discord
import time
import json


async def process_time(ctx: commands.Context, args: str, error_msg: str) -> (str, Any):
    args = args.split(" ")
    topop = 0
    endtime = time.time()
    for arg in args:
        if [arg.endswith(char) for char in "smhdMy"]:
            if not arg[:-1].isdigit():
                break
            topop += 1
            if arg.endswith("s"):
                endtime += int(arg.replace("s", ""))
            elif arg.endswith("m"):
                endtime += int(arg.replace("m", "")) * 60
            elif arg.endswith("h"):
                endtime += int(arg.replace("h", "")) * 3600
            elif arg.endswith("d"):
                endtime += int(arg.replace("d", "")) * 86400
            elif arg.endswith("M"):
                endtime += int(arg.replace("M", "")) * 2629800
            elif arg.endswith("y"):
                endtime += int(arg.replace("y", "")) * 31556952
    if topop == 0:
        await ctx.send(embed=discord.Embed(title=error_msg, color=0xff0000))
        return "err", None

    args = args[topop:]
    args = " ".join(args)
    return args, endtime


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


admin_command_descriptions = \
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


async def do_undone_tasks(client):
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


class NoItemFound(Exception):
    pass
