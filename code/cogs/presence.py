# activity = discord.Activity(name=next(status), type=discord.ActivityType.watching)
#    await client.change_presence(activity=activity)

import discord
from discord.ext import commands

class Presence(commands.Cog):

    def __init__(self, client):
        self.client: commands.Bot = client

    # Dont translate or add to help command, lets make this a secret
    @commands.command()
    async def presence(self, ctx: commands.Context, type_of_activity: int, *, presence: str):
        if not await self.client.is_owner(ctx.author):
            return
        if type_of_activity == 3:
            await self.client.change_presence()
            await ctx.send(embed=discord.Embed(title=f"Reseted the presence!", color=0x2be040))
            return
        activities = [discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.playing]
        activity = discord.Activity(name=presence, type=activities[type_of_activity])
        await self.client.change_presence(activity=activity)
        await ctx.send(embed=discord.Embed(title=f"Updated the presence to {presence}", color=0x2be040))


def setup(client):
    client.add_cog(Presence(client))
