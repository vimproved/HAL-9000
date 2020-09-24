from discord.ext import commands
from discord.ext.commands import MemberConverter, RoleConverter, TextChannelConverter
import pickle
import discord
from itertools import count


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Mod(bot))


class Mod(commands.Cog):
    """Commands for server moderation."""
    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        pass

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def config(self, ctx, args):
        """Configures the local server settings of HAL.
        Requires administrator.
        ```//config logchannel
        //config systemchannel
        //config copypasta```"""
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
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            systemchannel = await TextChannelConverter().convert(ctx, response.content)
            config.update({"systemchannel": str(systemchannel.id)})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("System channel set to " + response.content)
        elif args == "logchannel":
            q = await ctx.send("Please enter the channel you would like HAL to send moderation logs and errors in.")
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            logchannel = await TextChannelConverter().convert(ctx, response.content)
            config.update({"logchannel": str(logchannel.id)})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("Log channel set to" + response.content)
        elif args == "copypasta":
            q = await ctx.send('Please enter "yes" or "no" to configure whether copypasta is enabled on this server.')
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            if response.content == "yes":
                enabled = True
            elif response.content == "no":
                enabled = False
            else:
                await ctx.send ("That is not a valid response")
                return
            config.update({"copypastaenabled": enabled})
            globalconfig.update({ctx.guild.id: config})
            pickle.dump(globalconfig, open("config", "wb"))
            await ctx.send("Copypasta enabled set to " + str(enabled).lower())

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, args):
        """Bans a user.
        Requires ban users.
        ```//ban <user>```"""
        user = await MemberConverter().convert(ctx, args)
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

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def rgive(self, ctx, *args):
        """Gives a user / users a role.
        Requires Manage Roles.
        ```//rgive <user(s)> <role>
        //rgive everyone <role>```"""
        converter = MemberConverter()
        converter2 = RoleConverter()
        if args[0] == "everyone" or args[0] == "@everyone":
            users = ctx.guild.members
        else:
            users = []
            assignments = args.remove(args[-1])
            for user in assignments:
                user = await converter.convert(ctx, user)
                users.append(user)
        role = await converter2.convert(ctx, args[-1])
        await ctx.send("Giving roles...")
        for user in users:
            await user.add_roles(role, reason="Assigned by " + ctx.author.name + ".")
        await ctx.send("Done!")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def embedsend(self, ctx, *args):
        """Sends an embed message of choice in a channel of choice.
        Requires administrator.
        ```//embedsend <channel>```"""
        converter = TextChannelConverter()
        converter2 = RoleConverter()
        try:
            channel = await converter.convert(ctx, args[0])
        except Exception:
            await ctx.send("Please input a channel.")
            return
        embed = discord.Embed(color=0xff0008)
        for x in count(1):
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="Name #" + str(x), value="Respond with the name of field #" + str(
                x) + ". If you are done type \"done\". If you would like to include a field with who sent this embed, "
                     "type \"userstamp\". The message will then be sent.    ",
                                inline=False)
            q = await ctx.send(embed=embed_var)
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer = response.content
            if answer == "done":
                break
            elif answer == "userstamp":
                embed.add_field(name="__Message Sent By__", value=ctx.author.mention, inline=False)
                break
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="Value #" + str(x), value="Respond with the name of field #" + str(x) + ".",
                                inline=False)
            q = await ctx.send(embed=embed_var)
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer2 = response.content
            embed.add_field(name=answer, value=answer2 + "\n", inline=False)
        try:
            if args[1] == "everyone":
                await channel.send("@everyone\n", embed=embed)
            elif args[1] == "here":
                await channel.send("@here\n", embed=embed)
            else:
                rolemention = await converter2.convert(ctx, args[1])
                await channel.send(rolemention.mention + "\n", embed=embed)
        except Exception:
            await channel.send(embed=embed)
        await ctx.send("Message sent!")
