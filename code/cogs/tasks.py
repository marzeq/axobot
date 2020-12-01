import discord
import time
import json
from discord.ext import commands, tasks


class Tasks(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client
        self.do_tasks.start()

    @tasks.loop(seconds=1)
    async def do_tasks(self):
        with open("config/tasks.json", "r+") as f:
            tasksjson: dict = json.load(f)
        action = False
        if round(time.time()) not in (list(int(n) for n in list(tasksjson.keys()))):
            pass
        else:
            for pos in range(len(tasksjson)):
                if list(int(n) for n in list(tasksjson.keys()))[pos] == round(time.time()):
                    key = list(str(n) for n in list(tasksjson.keys()))[pos]
                    dct = tasksjson[key]
                    instruction = list(str(n) for n in list(dct.keys()))[0]
                    if instruction == "print":
                        print(dct[instruction])
                    elif instruction == "remind":
                        await self.client.get_user(dct[instruction]["who"]).send(embed=discord.Embed(title=dct[instruction]["value"]))
                    elif instruction == "unban":
                        await self.client.get_guild(dct[instruction]["guild"]).unban(user=dct[instruction]["who"])
                    tasksjson.pop(key)
                    action = True
                    break
                else:
                    pass
        if action:
            with open("config/tasks.json", "w") as f:
                json.dump(tasksjson, f, indent=4)


def setup(client):
    client.add_cog(Tasks(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
