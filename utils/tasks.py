import json
import time
from typing import Any
import discord
from discord.ext import commands


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
                await guild.unban(user=await client.fetch_user(dct[instruction]["user"]))
            tasksjson.pop(key)
            action = True
            break
        else:
            pass
    if action:
        with open("config/tasks.json", "w") as file:
            json.dump(tasksjson, file, indent=4)
