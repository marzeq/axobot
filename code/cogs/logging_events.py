import discord
from discord.ext import commands
import json


class LoggingEvents(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open('config/config.json', 'r') as file1:
            config = json.load(file1)
            config = config[str(message.guild.id)]["logging"]
        if config["channel"] == 0 or message.author.bot:
            return
        # Getting all translations
        lang = self.client.get_server_lang(str(message.guild.id))
        useful = lang["translations"]["logging"]
        logging_channel = self.client.get_channel(config["channel"])
        if message.content == "":
            message.content = "\"\""
        if message.channel.id == config["channel"] or message.channel.id in config["blacklist-channels"]:
            return
        embed = discord.Embed(title=useful["msg_deleted"], color=0xff0000)
        embed.add_field(name=useful["channel"], value=f"<#{message.channel.id}>", inline=False)
        embed.add_field(name=useful["content"], value=f"{message.content}", inline=False)
        embed.add_field(name=useful["author"], value=f"<@{message.author.id}>", inline=False)
        embed.add_field(name=useful["time"], value=f"{message.created_at} GMT", inline=False)
        embed.add_field(name=useful["tts"], value=f"{message.tts}", inline=False)
        embed.add_field(name=useful["pinned"], value=f"{message.pinned}", inline=False)
        embed.add_field(name=useful["everyone-here"], value=f"{message.mention_everyone}", inline=False)
        await logging_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        with open('config/config.json', 'r') as file1:
            config = json.load(file1)
            config = config[str(messages[0].guild.id)]["logging"]
        if config["channel"] == 0:
            return
        # Getting all translations
        lang = self.client.get_server_lang(str(messages[0].guild.id))
        useful = lang["translations"]["logging"]
        for message in messages:
            logging_channel = self.client.get_channel(config["channel"])
            if message.content == "":
                message.content = "\"\""
            if message.channel.id == config["channel"] or message.channel.id in config["blacklist-channels"] or message.author.bot:
                return
            embed = discord.Embed(title=useful["msg_deleted"], color=0xff0000)
            embed.add_field(name=useful["channel"], value=f"<#{message.channel.id}>", inline=False)
            embed.add_field(name=useful["content"], value=f"{message.content}", inline=False)
            embed.add_field(name=useful["author"], value=f"<@{message.author.id}>", inline=False)
            embed.add_field(name=useful["time"], value=f"{message.created_at} GMT", inline=False)
            embed.add_field(name=useful["tts"], value=f"{message.tts}", inline=False)
            embed.add_field(name=useful["pinned"], value=f"{message.pinned}", inline=False)
            embed.add_field(name=useful["everyone-here"], value=f"{message.mention_everyone}", inline=False)
            await logging_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after: discord.Message):
        if after.edited_at is None or after.author.bot:
            return
        with open('config/config.json', 'r') as file1:
            config = json.load(file1)
            config = config[str(after.guild.id)]["logging"]
        if config["channel"] == 0:
            return
        # Getting all translations
        lang = self.client.get_server_lang(str(after.guild.id))
        useful = lang["translations"]["logging_edit"]
        logging_channel = self.client.get_channel(config["channel"])
        if before.content == "":
            before.content = "\"\""
        if after.content == "":
            after.content = "\"\""
        if after.channel.id == config["channel"] or after.channel.id in config["blacklist-channels"]:
            return
        embed = discord.Embed(title=useful["msg_edited"], color=0xff0000)
        embed.add_field(name=useful["channel"], value=f"<#{after.channel.id}>", inline=False)
        embed.add_field(name=useful["content"], value=useful["content_value"].format(before.content, after.content), inline=False)
        embed.add_field(name=useful["author"], value=f"<@{after.author.id}>", inline=False)
        embed.add_field(name=useful["time"], value=useful["time_value"].format(before.created_at, after.edited_at), inline=False)
        embed.add_field(name=useful["tts"], value=f"{after.tts}", inline=False)
        embed.add_field(name=useful["pinned"], value=f"{after.pinned}", inline=False)
        embed.add_field(name=useful["everyone-here"], value=useful["everyone-here_value"].format(before.mention_everyone, after.mention_everyone), inline=False)
        await logging_channel.send(embed=embed)


def setup(client):
    client.add_cog(LoggingEvents(client))
