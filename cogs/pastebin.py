import discord
from discord.ext import commands
import aiohttp
import json


class Pastebin(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open("config/pastebinapi.json", "r") as f:
            cfg = json.load(f)
            self.key = cfg["api_key"]
            self.name = cfg["username"]
            self.password = cfg["password"]

    @commands.command(aliases=["paste"])
    async def pastebin(self, ctx: commands.Context, *, content: str):
        async with aiohttp.ClientSession() as session:
            data = {
                'api_dev_key': self.key,
                'api_user_name': self.name,
                'api_user_password': self.password
            }
            async with session.post(f"https://pastebin.com/api/api_login.php", data=data) as r:
                if r.status != 200:
                    await ctx.send(embed=discord.Embed(title="Something went wrong here! Contact the developer to resolve this issue!"))
                    return
        async with aiohttp.ClientSession() as session:
            data = {
                'api_option': 'paste',
                'api_dev_key': self.key,
                'api_paste_code': content,
                'api_paste_name': f"{ctx.author.name}'s paste",
                "api_paste_private": 1
            }
            async with session.post(f"https://pastebin.com/api/api_post.php", data=data) as r:
                if r.status == 200:
                    resp = await r.text()
                else:
                    resp = "Something went wrong here! Contact the developer to resolve this issue!"
        await ctx.send(embed=discord.Embed(title=resp))



def setup(client):
    client.add_cog(Pastebin(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
