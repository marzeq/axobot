import discord
from discord.ext import commands
import random


class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reddit(self, ctx, subreddit: str):
        memes_submissions = self.client.reddit.subreddit(subreddit).hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url)  # noqa


def setup(client):
    client.add_cog(Reddit(client))
