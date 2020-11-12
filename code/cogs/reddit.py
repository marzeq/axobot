import discord
from discord.ext import commands
import random


class Reddit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def reddit(self, ctx, subreddit: str):
        # Deleting `r/` before subreddit name because PRAW doesn't like it when we put it
        subreddit = subreddit[2:] if subreddit.startswith("r/") else subreddit

        # Getting all translations
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["reddit"]

        # Getting the Subreddit object from the provided name
        memes_submissions = self.client.reddit.subreddit(subreddit).hot()

        # Stackoverflow dark magic that I don't understand
        # I just know it gives us one of the 10 most hottest posts of the provided subreddit
        post_to_pick = random.randint(1, 10)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        # Checking if post if NSFW and the channel is not, because we do not want our bot to get taken down
        if submission.over_18 and not ctx.channel.is_nsfw(): # noqa
            response_embed = discord.Embed(title=useful["submission_nsfw"], color=0xdb2a2a)
            await ctx.send(embed=response_embed)
            return

        # Setting the post title, author, upvote ratio and link in the embed, and giving it a random color
        response_embed = discord.Embed(title=useful["title"].format(submission.title, submission.author.name), color=random.randint(0, 0xFFFFFF)) # noqa
        response_embed.set_footer(text=useful["footer"].format(submission.upvote_ratio, submission.shortlink))

        # Checking if submission has actual text in it
        if submission.selftext != "":

            # If the content is longer than 1024 chars, making it shorter so it can fit (that's why we need a link in the footer)
            submission.selftext = submission.selftext[:1018] + " [...]"

            # Finally adding the content
            response_embed.add_field(name=useful["content"], value=submission.selftext)

            # Sending back the final embed
            await ctx.send(embed=response_embed)  # noqa

        # If submission has for example a link or a image, and not text
        else:

            # We send just the title, author, upvote ratio and the link, because whats the point in sending empty content
            await ctx.send(embed=response_embed)

            # Sending the link, image etc. that's attached to the reddit submission
            await ctx.send(submission.url)


def setup(client):
    client.add_cog(Reddit(client))
