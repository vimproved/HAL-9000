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
        await ctx.send("What channel would you like log messages to be posted in?")
        response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
        while response.author != ctx.author:
            response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
        answer = response.content
        answer = await tcconvert.convert(ctx, answer)
        try:
            guildchannellist = pickle.load(open("guildchannellist", "rb"))
        except EOFError:
            guildchannellist = {}
        guildchannellist.update({ctx.guild.id: answer})
        pickle.dump(dict(guildchannellist), open("guildchannellist", "wb"))
        await ctx.send('Would you like to configure demotion/promotion logging?')
        response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
        while response.author != ctx.author:
            response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
        answer = response.content
        if answer.lower() == "yes" or "y":
            guildrolelist2 = []
            try:
                guildrolelist = pickle.load(open("guildrolelist", "rb"))
            except EOFError:
                guildrolelist = {}
            await ctx.send("Cool! How many ranks do you have?")
            response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
            while response.author != ctx.author:
                response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
            answer = response.content
            for x in range(0, int(answer)):
                await ctx.send("What is the rank #" + str(x + 1) + " in the hierarchy?")
                response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
                while response.author != ctx.author:
                    response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
                answer = await rconvert.convert(ctx, response.content)
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
