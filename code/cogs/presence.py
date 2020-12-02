import discord
from discord.ext import commands


class Presence(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.command()
    async def presence(self, ctx: commands.Context, type_of_activity: int, *, presence: str):
        if self.client.if_command_disabled(ctx.command.name, ctx.guild):
            return
        if not await self.client.is_owner(ctx.author):
            return
        if type_of_activity == 3:
            await self.client.change_presence()
            await ctx.send(embed=discord.Embed(title=f"Reset the presence!", color=0x2be040))
            return
        activities = [discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing]
        activity = discord.Activity(name=presence, type=activities[type_of_activity])
        await self.client.change_presence(activity=activity)
        await ctx.send(embed=discord.Embed(title=f"Updated the presence to {presence}", color=0x2be040))


def setup(client):
    client.add_cog(Presence(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib

    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
