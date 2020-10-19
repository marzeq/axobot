import discord
from discord.ext import commands
import logging
import traceback


class Console(commands.Cog):

    def __init__(self, client):
        self.client = client
        latest_error = ""
        while True:
            try:
                inpt = input("rm> ")
                if inpt == "lste":
                    logging.error(latest_error)
                elif inpt == "exec":
                    exec(input("exec> "))
                elif inpt == "eval":
                    eval(input("eval> "))
            except Exception as e:
                latest_error = traceback.format_exc()
                print("Error! Type `lste` to show it!")


def setup(client):
    client.add_cog(Console(client))
