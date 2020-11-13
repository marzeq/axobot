import random
from googletrans import Translator
import discord
from discord.ext import commands


class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.translator = Translator()

    @commands.command()
    async def translate(self, ctx, src_lang: str, dest_lang: str, *, to_translate):
        # Getting all translations
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["translate"]

        try:
            if src_lang == "auto" or src_lang == "none":
                translated = self.translator.translate(text=to_translate, dest=dest_lang)
            else:
                translated = self.translator.translate(text=to_translate, src=src_lang, dest=dest_lang)
        except ValueError:
            response_embed = discord.Embed(title=useful["lang_not_supported"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return

        # Creates and sends the response embed
        response_embed = discord.Embed(title=useful["heres_translated"].format(translated.text), color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Translate(client))

if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")