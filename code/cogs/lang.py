import discord
from discord.ext import commands
import json


class Lang(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lang"])
    async def language(self, ctx, lang: str = "none"):
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            # Getting all translations
            lng = self.client.get_server_lang(ctx.guild)
            useful = lng["translations"]["lang"]

            # If a lang is provided
            if lang != "none":
                lang = lang.replace("-", "_")
                lang = lang.replace(" ", "_")
                lang = lang.split("_")
                try:
                    lang[0] = lang[0].lower()
                    lang[1] = lang[1].upper()
                    lang = "_".join(lang)
                except IndexError:
                    pass

            # If provided lang is valid
            if lang in self.client.valid_langs:

                # Change the language of the server in the config
                with open('config/config.json', 'r') as f:
                    config = json.load(f)

                with open("config/config.json", "w") as f:
                    config[str(ctx.message.guild.id)]["lang"] = lang
                    json.dump(config, f, indent=4)

                # Creates and sends the response embed
                embed = discord.Embed(title=useful["changed_lang"].format(lang), color=0x00ff00)
                await ctx.send(embed=embed)

            # If a lang is still none
            else:

                # Send all available langs
                response_embed = discord.Embed(title=useful["available_langs"], color=0x1ced23)
                response_embed.add_field(name=f"**🇺🇸 English (USA)**", value=f"Type `lang en_US` to set the bot to the English (USA) language")
                response_embed.add_field(name=f"**🇪🇸 Español (España) INCONCLUSO**", value=f"Escribe `lang es_ES` para modificar la lengua de bot de Español (España)")
                response_embed.add_field(name=f"**🇵🇱 Polski NIEDOKOŃCZONE**", value=f"Wpisz komendę `lang pl_PL` aby zmienić język bota na polski")
                response_embed.add_field(name=f"**🇧🇷 Português (Brazil) INACABADO**", value=f"Digite `lang pt_BR` para definir o bot para Português (Brazil)")
                response_embed.add_field(name=f"**🇷🇺 Pусский (Россия) НЕЗАКОНЧЕННЫЙ**", value=f"Введите `lang ru_RU`, чтобы изменить язык бота на русский (Россия).")
                await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Lang(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
