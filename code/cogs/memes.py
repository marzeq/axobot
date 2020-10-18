import random
import discord
from discord.ext import commands
import praw


class Memes(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id='2EgK_dgbl9u5Kg',
                                  client_secret='yv0eRVKGY_JTrEGOtKcegblUqYQ',
                                  user_agent='RoboMarzeq by u/Marzeq_')

    @commands.command()
    async def meme(self, ctx):
        memes_submissions = self.reddit.subreddit('memes').new()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url) # noqa

    @commands.command()
    async def dankmeme(self, ctx):
        memes_submissions = self.reddit.subreddit('dankmemes').new()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        await ctx.send(submission.url)  # noqa

def setup(client):
    client.add_cog(Memes(client))
