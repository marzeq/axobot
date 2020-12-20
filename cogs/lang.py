import discord
from discord.ext import commands
import json
from utils import language
from utils import commands as command


class Lang(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lang"])
    async def language(self, ctx, lang: str = "none"):
        if command.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.administrator:
            # Getting all translations
            lng = language.get_server_lang(ctx.guild)
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
            if lang in language.valid_langs:

                # Change the language of the server in the config
                with open('config/config.json', 'r') as f:
                    config = json.load(f)

                with open("config/config.json", "w") as f:
                    config[str(ctx.message.guild.id)]["lang"] = lang
                    json.dump(config, f, indent=4)

                # Creates and sends the response embed
                embed = discord.Embed(title=useful["changed_lang"].replace("%%lang_code%%", lang), color=0x00ff00)
                await ctx.send(embed=embed)

            # If a lang is still none
            else:

                # Send all available langs
                response_embed = discord.Embed(title=useful["available_langs"], color=0x1ced23)
                response_embed.add_field(name=f"🇺🇸", value=f"`lang en_US`")
                response_embed.add_field(name=f"🇪🇸", value=f"`lang es_ES`")
                response_embed.add_field(name=f"🇵🇱", value=f"`lang pl_PL`")
                response_embed.add_field(name=f"🇧🇷", value=f"`lang pt_BR`")
                response_embed.add_field(name=f"🇵🇹", value=f"`lang pt_PT`")
                response_embed.add_field(name=f"🇷🇺", value=f"`lang ru_RU`")
                response_embed.add_field(name=f"🇨🇳", value=f"`lang zh_CN`")
                response_embed.add_field(name=f"🇹🇼", value=f"`lang zh_TW`")
                response_embed.add_field(name=f"🇮🇳 (Hindi)", value=f"`lang hi_IN`")
                response_embed.add_field(name=f"🇫🇷", value=f"`lang fr_FR`")
                response_embed.add_field(name=f"🇸🇦", value=f"`lang ar_SA`")
                response_embed.add_field(name=f"🇨🇿", value=f"`lang cz_CZ`")
                response_embed.add_field(name=f"🇮🇹", value=f"`lang it_IT`")
                response_embed.add_field(name=f"🇳🇱", value=f"`lang nl_NL`")
                response_embed.add_field(name=f"🇺🇦", value=f"`lang uk_UA`")
                response_embed.add_field(name=f"🇲🇾", value=f"`lang ms_MY`")
                response_embed.add_field(name=f"🇳🇴", value=f"`lang no_NO`")
                response_embed.add_field(name=f"🇸🇪", value=f"`lang sv_SE`")
                response_embed.add_field(name=f"🇬🇷", value=f"`lang el_GR`")
                response_embed.add_field(name=f"🇩🇪", value=f"`lang de_DE`")
                response_embed.add_field(name=f"<:ib:790329225608560671>", value=f"`lang ib_IB`")
                response_embed.add_field(name=f"🏴‍☠️", value=f"`lang en_PT`")
                response_embed.add_field(name=f"AE", value=f"`lang ae_AE`")
                await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Lang(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
