import discord
from discord.ext import commands
from urllib.parse import quote as valid_url
import random

class Translate(commands.Cog):

    def __init__(self, client):
        self.client = client
		self.supported_free_langs = \
{
	"en": "english",
	"pl": "polish",
	'es': 'spanish',
    'pt': 'portuguese',
	'zh-tw': 'chinese (traditional)'
}
		self.supported_premium_langs = \
{
	'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

    @commands.command(aliases=["ggl"])
    async def google(self, ctx, src_lang: str, dest_lang: str, *, to_translate):
        # Getting all translations
        # lang = self.client.get_server_lang(str(ctx.guild.id))
        # useful = lang["translations"]["translate"]
		
		if dest_lang == "auto" or "none":
			dest_lang = "en"
		
		if dest_lang not in self.supported_premium_langs or dest_lang not in self.supported_free_langs:
			return
		
		# Going to check if guild is premium later on
		if (src_lang not in self.supported_free_langs or src_lang not in self.supported_premium_langs) and (src_lang != "auto" or src_lang != "none"):
			return
			# TODO: Add fail response

        if src_lang == "auto" or src_lang == "none":
			translated = translator.translate(to_translate, dest=dest_lang)
		else:
			translated = translator.translate(to_translate, src='la', dest=dest_lang)

        # Creates and sends the response embed
        response_embed = discord.Embed(title=f"Here's your translated phrase: {translated.text}", color=random.randint(0, 0xFFFFFF))
        await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(Translate(client))
