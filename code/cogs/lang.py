import discord
from discord.ext import commands
import json


class Lang(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["lang"])
    async def language(self, ctx, lang: str = "none"):
        lng = self.client.get_server_lang(str(ctx.guild.id))
        useful = lng["translations"]["lang"]
        lang = lang.replace("-", "_")
        lang = lang.split("_")
        lang[0] = lang[0].lower()
        lang[1] = lang[1].upper()
        lang = "_".join(lang)
        if lang in self.client.valid_langs:
            with open('config/config.json', 'r') as f:
                config = json.load(f)

            with open("config/config.json", "w") as f:
                config[str(ctx.message.guild.id)]["lang"] = lang
                json.dump(config, f, indent=4)
            embed = discord.Embed(title=useful["changed_lang"].format(lang), color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            response_embed = discord.Embed(title=useful["available_langs"], color=0x1ced23)
            response_embed.add_field(name=f"**🇺🇸 English (USA)**", value=f"Type `lang en_US` to set the bot to the English (USA) language")
            response_embed.add_field(name=f"**🇪🇸 Español (España) INCONCLUSO**", value=f"Escribe `lang es_ES` para modificar la lengua de bot de Español (España)")
            response_embed.add_field(name=f"**🇵🇱 Polski**", value=f"Wpisz komendę `lang pl_PL` aby zmienić język bota na polski")
            response_embed.add_field(name=f"**🇧🇷 Português (Brazil) INACABADO**", value=f"Digite `lang pr_BR` para definir o bot para Português (Brazil)")
            response_embed.add_field(name=f"**🇷🇺 Pусский (Россия) НЕЗАКОНЧЕННЫЙ**", value=f"Введите `lang ru_RU`, чтобы изменить язык бота на русский (Россия).")
            await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Lang(client))
