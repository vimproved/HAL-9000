from discord.ext import commands
from discord.ext.commands import MemberConverter, RoleConverter


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Mod(bot))


class Mod(commands.Cog):
    """Commands for server moderation."""
    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        pass

    @commands.has_permissions(ban_users=True)
    @commands.command()
    async def ban(self, ctx, args):
        """Bans a user.
        ```//ban <user>```
        Admin only."""
        user = await MemberConverter().convert(ctx, args)
        await user.ban()
        await ctx.send(user.mention + " has been banned.")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def bulkdelete(self, ctx, args):
        """Deleted messages in bulk.
        ```//bulkdelete <# of messages>```
        Requires Manage Messages."""
        deletionlist = []
        async for message in ctx.channel.history(limit=int(args) + 1):
            deletionlist.append(message)
        await ctx.channel.delete_messages(deletionlist)
        await ctx.send("Deleted " + args + " messages.")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def rgive(self, ctx, *args):
        """Gives a user / users a role.
        `//rgive everyone`: Gives every member a role.
        Requires Manage Roles."""
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
