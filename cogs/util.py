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
                                " <category>` for information on a single category.\n",
                                inline=False)
            for cog in self.bot.cogs.values():
                embed_var.add_field(name=cog.qualified_name, value=cog.description, inline=False)
        await ctx.send(embed=embed_var)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def config(self, ctx, args):
        """Configures the local server settings of HAL.
        Requires administrator.
        ```//config logchannel
        //config systemchannel```"""
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

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot. Ignores arguments."""
        await ctx.send("Pong! :ping_pong:")

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

    @commands.command()
    async def invite(self, ctx):
        """Sends an oath2 link for HAL. Ignores arguments."""
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=717042126776434728&permissions=8&scope=bot")

    @commands.command()
    async def repo(self, ctx):
        """Sends the link to the GitHub repo for HAL. Ignores arguments."""
        await ctx.send("https://github.com/Paradigmmmm/HAL-9000")
