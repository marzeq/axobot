import random
import discord
from discord.ext import commands


class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        memes_submissions = self.client.reddit.subreddit('memes').new()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url) # noqa

    @commands.command()
    async def dankmeme(self, ctx):
        memes_submissions = self.client.reddit.subreddit('dankmemes').new()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url)  # noqa

def setup(client):
    client.add_cog(Memes(client))
