import json
import discord
import os


def get_server_lang(guild: discord.Guild) -> dict:
    if guild is None:
        with open(f"translations/en_US.json", "r") as langf:
            lng = json.load(langf)
            return lng
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        lang_code = cfg[str(guild.id)]["lang"]
        with open(f"translations/{lang_code}.json", "r") as langf:
            lng = json.load(langf)
    return lng


def get_server_lang_code(guild: discord.Guild) -> str:
    if guild is None:
        return "en_US"
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        lang_code = cfg[str(guild.id)]["lang"]
    return lang_code


valid_langs = []

for lang in os.listdir("translations"):
    if lang.endswith(".json"):
        valid_langs.append(lang[:5])
