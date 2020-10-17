import discord
from discord.ext import commands


class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.dsc = client.command_descriptions
        client.remove_command("help")

    @commands.command()
    async def help(self, ctx, command=None):
        if not command:
            response_embed = discord.Embed(title=f"**Here's your help {ctx.author}!**", color=0x1ced23)
            for command in self.dsc:
                args_to_put = ""
                for arg in self.dsc[command]:
                    if self.dsc[command][arg]["required"]:
                        args_to_put += f" [{arg}]"
                    else:
                        args_to_put += f" ({arg})"
                response_embed.add_field(name=f"`{command} {args_to_put}`", value="Shows this menu. If a")
            response_embed.set_footer(text="[] are required command arguments, () are optional command arguments")
            await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(HelpCommand(client))
