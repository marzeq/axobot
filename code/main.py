import discord
from discord.ext import commands

with open("token.txt", "r") as f:
    TOKEN = f.read()

PREFIX = "#!"

client = commands.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    print("The bot is ready.")


client.run(TOKEN)
