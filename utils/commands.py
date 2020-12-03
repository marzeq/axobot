import json
import discord


def if_command_disabled(name: str, guild: discord.Guild):
    if guild is None:
        return False
    with open("config/config.json", "r") as configf:
        cfg = json.load(configf)
        try:
            disabled = cfg[str(guild.id)]["disabled_commands"]
        except KeyError:
            cfg[str(guild.id)]["disabled_commands"] = []
            return False
        return name in disabled
