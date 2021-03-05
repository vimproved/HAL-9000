from discord.ext import commands, tasks
from discord.ext.commands import MemberConverter, RoleConverter, TextChannelConverter
import discord
from itertools import count
import time
import toml


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Mod(bot))


class Mod(commands.Cog):
    """Commands for server moderation."""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def config(self, ctx, *args):
        """Configures the local server settings of HAL.
        Requires administrator.
        ```//config logchannel <channel>: Sets the channel for HAL to send mod log messages in (HAL Errors, message deletions)
        //config systemchannel <channel>: Sets the channel for HAL to send member joins/leaves in.
        //config colorposition <integer>: Sets the role list position of new color roles.
        //config read: Sends the config settings.```"""
        config = toml.loads(open("config.toml", "rt").read())
        if args[0] == "systemchannel":
            systemchannel = await TextChannelConverter().convert(ctx, args[1])
            config.update({"systemchannel": systemchannel.id})
            open("config.toml", "w").write(toml.dumps(config))
            await ctx.send("System channel set to " + args[1] + ".")
        elif args[0] == "logchannel":
            logchannel = await TextChannelConverter().convert(ctx, args[1])
            config.update({"logchannel": logchannel.id})
            open("config.toml", "w").write(toml.dumps(config))
            await ctx.send("Log channel set to " + args[1] + ".")
        elif args[0] == "colorposition":
            position = (len(ctx.guild.roles) - int(args[1])) + 1
            config.update({"colorposition": position})
            open("config.toml", "w").write(toml.dumps(config))
            await ctx.send("Color position set to " + str(args[1]) + ".")
        elif args[0] == "read":
            await ctx.send("Config file:\n" + open("config.toml").read())
        else:
            await ctx.send("Please select a valid configuration option.")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, *args):
        """Bans a user.
        Requires ban users.
        ```//ban <user> <reason>```"""
        user = await MemberConverter().convert(ctx, args[0])
        try:
            await user.ban(reason=args[1])
        except IndexError:
            await user.ban()
        await ctx.send(user.mention + " has been banned.")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def bulkdelete(self, ctx, args):
        """Deletes messages in bulk.
        Requires manage messages.
        ```//bulkdelete <# of messages>```"""
        deletionlist = []
        async for message in ctx.channel.history(limit=int(args) + 1):
            deletionlist.append(message)
        await ctx.channel.delete_messages(deletionlist)
        await ctx.send("Deleted " + args + " messages.")
