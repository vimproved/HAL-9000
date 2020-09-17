from discord.ext import commands
from discord.ext.commands import TextChannelConverter, RoleConverter
from itertools import count
import discord
import pickle


def setup(bot):
    bot.add_cog(Utility(bot))


class Utility(commands.Cog):
    """Utility commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args=""):
        """Help command.
        ```//help <command>: Help for a single command
        //help <category>: Help for all the commands in a category.```"""
        if args in self.bot.cogs.keys():
            args = self.bot.get_cog(args)
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__" + args.qualified_name + "__",
                                value=args.description + "\n", inline=False)
            for command in args.get_commands():
                embed_var.add_field(name="//" + command.name, value=command.help + "\n", inline=False)
        elif self.bot.get_command(args) in self.bot.commands:
            args = self.bot.get_command(args)
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__//" + args.name + "__", value=args.help + "\n", inline=False)
        else:
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__Help Menu__",
                                value="HAL-9000 is a multipurpose discord bot made by vi#7158 "
                                "and rous#7120.\nThis is the help menu. Do `//help <"
                                "command>` for information on a single command. Do `//help"
                                "<category>` for information on a single category.\n",
                                inline=False)
            for cog in self.bot.cogs.values():
                embed_var.add_field(name=cog.qualified_name, value=cog.description, inline=False)
        await ctx.send(embed=embed_var)

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot. Ignores arguments."""
        await ctx.send("Pong! :ping_pong:")

    @commands.command()
    @commands.has_role(318476343023239168)
    async def embedsend(self, ctx, *args):
        """Sends an embed message of choice in a channel of choice.
        ```//embedsend <channel>```
        Admin only."""
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

    @commands.command()
    async def botlog(self, ctx, args):
        """Commands relating to the botlog system.
        ```//botlog config: Configures botlogger.
        //botlog read: Sends current botlog settings.```
        Admin only."""
        if args == "config":
            rconvert = RoleConverter()
            tcconvert = TextChannelConverter()
            q = await ctx.send("What channel would you like log messages to be posted in?")
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer = response.content
            answer = await tcconvert.convert(ctx, answer)
            answer = answer.id
            try:
                guildchannellist = pickle.load(open("guildchannellist", "rb"))
            except EOFError:
                guildchannellist = {}
            guildchannellist.update({ctx.guild.id: answer})
            pickle.dump(dict(guildchannellist), open("guildchannellist", "wb"))
            q = await ctx.send('Would you like to configure demotion/promotion logging?')
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer = response.content
            if answer.lower() == "yes" or "y":
                guildrolelist2 = []
                try:
                    guildrolelist = pickle.load(open("guildrolelist", "rb"))
                except EOFError:
                    guildrolelist = {}
                q = await ctx.send("Cool! How many ranks do you have?")
                responsefound = False
                while not responsefound:
                    async for message in ctx.channel.history(limit=10):
                        if message.author == ctx.author and message.created_at > q.created_at:
                            response = message
                            responsefound = True
                            break
                answer = response.content
                for x in range(0, int(answer)):
                    q = await ctx.send("What is the rank #" + str(x + 1) + " in the hierarchy?")
                    responsefound = False
                    while not responsefound:
                        async for message in ctx.channel.history(limit=10):
                            if message.author == ctx.author and message.created_at > q.created_at:
                                response = message
                                responsefound = True
                                break
                    answer = await rconvert.convert(ctx, response.content)
                    answer = answer.id
                    guildrolelist2.append(answer)
                guildrolelist.update({ctx.guild.id: guildrolelist2})
                pickle.dump(guildrolelist, open("guildrolelist", "wb"))
                await ctx.send("Configuration done!")
            else:
                await ctx.send("Configuration exited.")
        elif args == "read":
            guildchannellist = pickle.load(open("guildchannellist", "rb"))
            guildrolelist = pickle.load(open("guildrolelist", "rb"))
            await ctx.send("Channel: " + str(guildchannellist.get(ctx.guild.id)) + "\n Admin Roles: " + str(
                guildrolelist.get(ctx.guild.id)))
        else:
            raise Exception("Argument not found. Do //help Botlog for command help.")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def bulkdelete(self, ctx, args):
        deletionlist=[]
        async for message in ctx.channel.history(limit=int(args)+1):
            deletionlist.append(message)
        await discord.Client.delete(deletionlist)
        await ctx.send("Deleted " + args + " messages.")