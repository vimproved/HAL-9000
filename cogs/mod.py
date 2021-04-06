from discord.ext import commands
from discord.ext.commands import MemberConverter


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Mod(bot))


class Mod(commands.Cog):
    """Commands for server moderation."""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, *args):
        """Bans a user.
        Requires ban users.

        Syntax:
        `//ban <user> <reason>`"""
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

        Syntax:
        `//bulkdelete <# of messages>`"""
        deletionlist = []
        async for message in ctx.channel.history(limit=int(args) + 1):
            deletionlist.append(message)
        await ctx.channel.delete_messages(deletionlist)
        await ctx.send("Deleted " + args + " messages.")
