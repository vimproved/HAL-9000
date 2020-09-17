from discord.ext import commands
import pickle
from discord.ext.commands import RoleConverter, TextChannelConverter


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Botlog(bot))


class Botlog(commands.Cog):
    """Commands related to the Botlogging system."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def config(self, ctx):
        """Configures botlogger."""
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

    @commands.command()
    async def read(self, ctx):
        guildchannellist = pickle.load(open("guildchannellist", "rb"))
        guildrolelist = pickle.load(open("guildrolelist", "rb"))
        await ctx.send("Channel: " + str(guildchannellist.get(ctx.guild.id)) + "\n Admin Roles: " + str(
            guildrolelist.get(ctx.guild.id)))
