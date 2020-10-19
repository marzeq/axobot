import discord
from discord.ext import commands
import random


class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reddit(self, ctx, subreddit: str):
        subreddit = subreddit[2:] if subreddit.startswith("r/") else subreddit
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["reddit"]
        memes_submissions = self.client.reddit.subreddit(subreddit).hot()
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        if submission.over_18 and not ctx.channel.is_nsfw(): # noqa
            response_embed = discord.Embed(title=useful["submission_nsfw"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return
        response_embed = discord.Embed(title=useful["title"].format(submission.title, submission.author.name), color=random.randint(0, 0xFFFFFF)) # noqa
        response_embed.set_footer(text=useful["footer"].format(submission.upvote_ratio, submission.shortlink))
        if submission.selftext != "":
            submission.selftext = submission.selftext[:1018] + " [...]"
            response_embed.add_field(name=useful["content"], value=submission.selftext)
            await ctx.send(embed=response_embed)  # noqa
        else:
            await ctx.send(embed=response_embed)
            await ctx.send(submission.url)


def setup(client):
    client.add_cog(Reddit(client))
