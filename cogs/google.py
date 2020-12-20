import discord
from discord.ext import commands
from urllib.parse import quote as valid_url
import random
from utils import language
from utils import commands as command


class Google(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ggl = "https://google.com/"

    @commands.command(aliases=["ggl"])
    async def google(self, ctx, *, search_term: str):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        # Getting all translations
        lang = language.get_server_lang(ctx.guild)
        useful = lang["translations"]["google"]

        # Search term ready to combine with the google prefix
        search_term = f"search?q={search_term}"

        # Combine the search term and make it a valid url
        link = self.ggl + valid_url(search_term, safe='=?')

        # Creates and sends the response embed
        response_embed = discord.Embed(title=useful["ur_link"].replace("%%url%%", link), color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Google(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
