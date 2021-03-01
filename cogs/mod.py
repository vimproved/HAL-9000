from discord.ext import commands, tasks
from discord.ext.commands import MemberConverter, RoleConverter, TextChannelConverter
import pickle
import discord
from itertools import count
import time


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Mod(bot))


class Mod(commands.Cog):
    """Commands for server moderation."""
    def __init__(self, bot):
        self.bot = bot
        self.update_mutes.start()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def config(self, ctx, args):
        """Configures the local server settings of HAL.
        Requires administrator.
        ```//config logchannel: Sets the channel for HAL to send mod log messages in (HAL Errors, message deletions)
        //config systemchannel: Sets the channel for HAL to send member joins/leaves in.
        //config copypasta: Sets whether //copypasta is enabled for this server.
        //config colorposition: Sets the role list position of new color roles.
        //config read: Sends the config settings.```"""
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError or KeyError:
            globalconfig = {}
        try:
            config = globalconfig[ctx.guild.id]
        except KeyError:
            config = {}
        if args == "systemchannel":
            q = await ctx.send("Please enter the channel you would like HAL to send server updates in.")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            systemchannel = await TextChannelConverter().convert(ctx, answer)
            config.update({"systemchannel": systemchannel.id})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("System channel set to " + response.content)
        elif args == "logchannel":
            q = await ctx.send("Please enter the channel you would like HAL to send moderation logs and errors in.")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            logchannel = await TextChannelConverter().convert(ctx, answer)
            config.update({"logchannel": logchannel.id})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("Log channel set to " + response.content)
        elif args == "copypasta":
            q = await ctx.send('Please enter "yes" or "no" to configure whether copypasta is enabled on this server.')
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            if answer == "yes":
                enabled = True
            elif answer == "no":
                enabled = False
            else:
                await ctx.send("That is not a valid response")
                return
            config.update({"copypastaenabled": enabled})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("Copypasta enabled set to " + str(enabled).lower() + ".")
        elif args == "read":
            message = ""
            for x in config.keys():
                try:
                    value = (await TextChannelConverter().convert(ctx, str(config[x]))).mention
                except commands.errors.BadArgument:
                    value = str(config[x])
                message = message + "\n" + str(x) + ": " + value
            await ctx.send(message)
        elif args == "muterole":
            q = await ctx.send("What would you like the new muted role to be?")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            try:
                muterole = await RoleConverter().convert(ctx, answer)
                config.update({"muterole": muterole.id})
                globalconfig.update({ctx.guild.id: config})
                pickle.dump(globalconfig, open("config", "wb"))
                await ctx.send("Set muted role to " + muterole.name + ".")
            except commands.errors.BadArgument:
                await ctx.send("Role not found.")
        elif args == "colorposition":
            q = await ctx.send("What position (from the top of the roles list) would you like new colors to be "
                               "inserted at?")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = int(response.content)
            answer = (len(ctx.guild.roles) - answer) + 1
            position = answer
            config.update({"colorposition": position})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("Done!")
        elif args == "wipe":
            q = await ctx.send("What config element would you like to wipe?")
            response = ""
            while type(response) != discord.Message:
                async for message in ctx.channel.history(limit=5):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        break
            answer = response.content
            config.pop(answer)
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))

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

