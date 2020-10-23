import discord
from discord.ext import commands

# Fuck it I'm not translating this now

class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.adm_dsc = client.admin_command_descriptions
        client.remove_command("help")

    @commands.command()
    async def help(self, ctx, *, command=None):
        lang = self.client.get_server_lang(str(ctx.guild.id))
        useful = lang["translations"]["help"]
        cmds = lang["command_descriptions"]
        if not command:
            response_embed = discord.Embed(title=useful["heres_your_help"].format(ctx.author), color=0x1ced23)
            command_list = ""
            for command in cmds:
                args_to_put = ""
                for arg in cmds[command]["args"]:
                    if cmds[command]["args"][arg]["required"]:
                        args_to_put += f" [{arg}]"
                    else:
                        args_to_put += f" ({arg})"
                command_list += f"{command}{args_to_put}\n"
            response_embed.add_field(name=useful["available_commands"], value=f"```{command_list}```")
            response_embed.set_footer(text=useful["required_notrequired_args"])
            await ctx.send(embed=response_embed)
        else:
            try:
                response_embed = discord.Embed(title=useful["the_cmd"].format(command), color=0x1ced23)
                args_to_put = ""
                for arg in cmds[command]["args"]:
                    if cmds[command]["args"][arg]["required"]:
                        args_to_put += f" [{arg}]"
                    else:
                        args_to_put += f" ({arg})"
                response_embed.add_field(name=useful["usage"], value=f"```{command}{args_to_put}```")
                response_embed.add_field(name=useful["desc"], value=f"```{cmds[command]['desc']}```")
                response_embed.add_field(name=useful["required_perms"], value=f"```{cmds[command]['required_perms']}```")
                response_embed.add_field(name=useful["aliases"], value=f"```{cmds[command]['aliases']}```")
                response_embed.set_footer(text=useful["required_notrequired_args"])
                await ctx.send(embed=response_embed)
            except KeyError:
                response_embed = discord.Embed(title=lang["translations"]["command_error"]["nonexistent_command"], color=0xdb2a2a)
                await ctx.send(embed=response_embed)

    @commands.command(aliases=["adminhelp", "admhelp"])
    async def admin_help(self, ctx, *, command=None):
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
                response_embed.add_field(name=f"**Description:**", value=f"```{self.adm_dsc[command]['desc']}```")
                response_embed.add_field(name=f"**Required Permissions:**",
                                         value=f"```Bot Owner```")
                response_embed.add_field(name=f"**Aliases:**", value=f"```{self.adm_dsc[command]['aliases']}```")
                response_embed.set_footer(text="[] are required command arguments, () are optional command arguments")
                await ctx.send(embed=response_embed)
            except KeyError:
                response_embed = discord.Embed(title=f"**The {command} command sadly doesn't exist!**", color=0xdb2a2a)
                await ctx.send(embed=response_embed)


def setup(client):
    client.add_cog(HelpCommand(client))
