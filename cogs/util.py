from discord.ext import commands
import discord
from discord.ext.commands import TextChannelConverter, EmojiConverter


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
        nameslower = []
        names = []
        for x in self.bot.cogs.keys():
            nameslower.append(x.lower())
            names.append(x)
        if args.lower() in nameslower:
            try:
                args = self.bot.get_cog(names[nameslower.index(args)])
            except Exception:
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

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot. Ignores arguments."""
        await ctx.send("Pong! :ping_pong:")

    @commands.command()
    async def invite(self, ctx):
        """Sends an oath2 link for HAL. Ignores arguments."""
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=717042126776434728&permissions=8&scope=bot")

    @commands.command()
    async def repo(self, ctx):
        """Sends the link to the GitHub repo for HAL. Ignores arguments."""
        await ctx.send("https://github.com/Paradigmmmm/HAL-9000")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def poll(self, ctx, *args):
        """Creates a poll in a the specified channel and optionally pings a role.
        Admin only.
        ```//poll <channel> <role(optional)>```"""
        pollchannel = await TextChannelConverter().convert(ctx, args[0])
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="__Poll Creation__", value='What is the name of your poll?\nType "cancel" at any time to cancel poll creation.', inline=False)
        q = await ctx.send(embed=embed)
        responsefound = False
        while not responsefound:
            async for message in ctx.channel.history(limit=10):
                if message.author == ctx.author and message.created_at > q.created_at:
                    response = message
                    responsefound = True
                    break
        answer = response.content
        if answer.lower() == "cancel":
            return
        title = answer
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="__Poll Creation__",
                        value='Type a brief description of your poll.\nType "cancel" at any time to cancel poll creation.',
                        inline=False)
        q = await ctx.send(embed=embed)
        responsefound = False
        while not responsefound:
            async for message in ctx.channel.history(limit=10):
                if message.author == ctx.author and message.created_at > q.created_at:
                    response = message
                    responsefound = True
                    break
        answer = response.content
        if answer.lower() == "cancel":
            return
        description = answer
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="__Poll Creation__",
                        value='How many voting options would you like?.\nType "cancel" at any time to cancel poll creation.',
                        inline=False)
        q = await ctx.send(embed=embed)
        responsefound = False
        while not responsefound:
            async for message in ctx.channel.history(limit=10):
                if message.author == ctx.author and message.created_at > q.created_at:
                    response = message
                    responsefound = True
                    break
        answer = response.content
        numresps = answer
        if answer.lower() == "cancel":
            return
        options = {}
        for x in range(0, int(numresps)):
            embed = discord.Embed(color=0xff0008)
            embed.add_field(name="__Poll Creation__",
                            value='Type the text for response #' + str(x+1) + '.\nType "cancel" at any time to cancel poll creation.',
                            inline=False)
            q = await ctx.send(embed=embed)
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer = response.content
            if answer.lower() == "cancel":
                return
            text = answer
            embed = discord.Embed(color=0xff0008)
            embed.add_field(name="__Poll Creation__",
                            value='Type the emoji for response #' + str(x+1) + '. MAKE SURE THAT THE EMOJI IS EITHER FROM THIS SERVER, OR A GLOBAL EMOJI.\nType "cancel" at any time to cancel poll creation.',
                            inline=False)
            q = await ctx.send(embed=embed)
            responsefound = False
            while not responsefound:
                async for message in ctx.channel.history(limit=10):
                    if message.author == ctx.author and message.created_at > q.created_at:
                        response = message
                        responsefound = True
                        break
            answer = response.content
            emoji = answer
            options.update({emoji: text})
        await ctx.send("Sending poll message.")
        respstr = ""
        for x in options.keys():
            respstr = respstr + "\n\n" + x + ": " + options[x]
        embed = discord.Embed(color=0xff0008)
        embed.add_field(name="*__POLL: " + title + "__*",
                        value='Description:\n' + description,
                        inline=False)
        embed.add_field(name="*Responses*",
                        value=respstr,
                        inline=False)
        embed.add_field(name="*Created by:*",
                        value=ctx.author.mention,
                        inline=False)
        if args[1] == "everyone":
            thing = "@everyone"
        else:
            thing = args[1]
        poll = await pollchannel.send(thing, embed=embed)
        for x in options.keys():
            await poll.add_reaction(x)
