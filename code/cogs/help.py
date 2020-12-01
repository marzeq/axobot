import discord
from discord.ext import commands


class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.adm_dsc = client.admin_command_descriptions
        client.remove_command("help")

    @commands.command()
    async def help(self, ctx, *, command=None):
        # Get all required translations and command descriptions
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["help"]
        cmds = lang["command_descriptions"]
        categories = lang["help_cattegories"]

        # If a command is not provided
        if not command:
            # Make the initial embed
            response_embed = discord.Embed(title=useful["heres_your_help"].format(ctx.author), color=0x1ced23)

            # Loop through all the available commands
            for command in cmds:
                args_to_put = ""

                # Loop through all args for the command
                for arg in cmds[command]["args"]:

                    # If an arg is required
                    if cmds[command]["args"][arg]["required"]:
                        args_to_put += f" [{arg}]"

                    # Else
                    else:
                        args_to_put += f" ({arg})"

                # Final command usage
                command_usage = f"{command}{args_to_put}\n"

                # Assign to the appropriate category
                categories[cmds[command]["cattegory"]][1] += command_usage
            for cat in categories:
                response_embed.add_field(name=categories[cat][0], value=f"```\n{categories[cat][1]}```")
            response_embed.set_footer(text=useful["required_notrequired_args"])
            await ctx.send(embed=response_embed)

        # Else
        else:
            # Check if provided command exists
            try:
                # Basically the same as above
                response_embed = discord.Embed(title=useful["the_cmd"].format(command), color=0x1ced23)
                args_to_put = ""
                for arg in cmds[command]["args"]:
                    if cmds[command]["args"][arg]["required"]:
                        args_to_put += f" [{arg}]"
                    else:
                        args_to_put += f" ({arg})"
                response_embed.add_field(name=useful["usage"], value=f"```{command}{args_to_put}```")
                response_embed.add_field(name=useful["required_perms"], value=f"```{cmds[command]['required_perms']}```")
                response_embed.add_field(name=useful["aliases"], value=f"```{cmds[command]['aliases']}```")
                response_embed.add_field(name=useful["desc"], value=f"```{cmds[command]['desc']}```")
                response_embed.add_field(name="Category", value=f"```{cmds[command]['cattegory']}```")
                response_embed.set_footer(text=useful["required_notrequired_args"])
                await ctx.send(embed=response_embed)

            # Else
            except KeyError:
                response_embed = discord.Embed(title=lang["translations"]["command_error"]["nonexistent_command"], color=0xdb2a2a)
                await ctx.send(embed=response_embed)

    @commands.command(aliases=["adminhelp", "admhelp"])
    async def admin_help(self, ctx, *, command=None):
        # Same as above, but without categories
        if not await self.client.is_owner(ctx.author):
            return
        if not command:
            response_embed = discord.Embed(title=f"**Here's your help {ctx.author}!**", color=0x1ced23)
            command_list = ""
            for command in self.adm_dsc:
                args_to_put = ""
                for arg in self.adm_dsc[command]["args"]:
                    if self.adm_dsc[command]["args"][arg]["required"]:
                        args_to_put += f" [{arg}]"
                    else:
                        args_to_put += f" ({arg})"
                command_list += f"{command}{args_to_put}\n"
            response_embed.add_field(name="Avalible Commands:", value=f"```{command_list}```")
            response_embed.set_footer(text="[] are required command arguments, () are optional command arguments")
            await ctx.send(embed=response_embed)
        else:
            try:
                response_embed = discord.Embed(title=f"**The {command} command:**", color=0x1ced23)
                args_to_put = ""
                for arg in self.adm_dsc[command]["args"]:
                    if self.adm_dsc[command]["args"][arg]["required"]:
                        args_to_put += f" [{arg}]"
                    else:
                        args_to_put += f" ({arg})"
                response_embed.add_field(name=f"**Usage:**", value=f"```{command}{args_to_put}```")
                response_embed.add_field(name=f"**Required Permissions:**",
                                         value=f"```Bot Owner```")
                response_embed.add_field(name=f"**Aliases:**", value=f"```{self.adm_dsc[command]['aliases']}```")
                response_embed.add_field(name=f"**Description:**", value=f"```{self.adm_dsc[command]['desc']}```")
                response_embed.set_footer(text="[] are required command arguments, () are optional command arguments")
                await ctx.send(embed=response_embed)
            except KeyError:
                # TODO: Translate this
                response_embed = discord.Embed(title=f"**The {command} command sadly doesn't exist!**", color=0xdb2a2a)
                await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(HelpCommand(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
