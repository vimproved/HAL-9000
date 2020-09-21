from discord.ext import commands
from discord.ext.commands import MemberConverter, RoleConverter
import discord


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Mod(bot))


class Mod(commands.Cog):
    """Commands for server moderation."""
    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        pass

    @commands.command()
    async def ban(self, ctx, args):
        """Adds the next banned role to a user.
        ```//ban <user>```
        Admin only."""
        if any([aghbo.permissions.manage_roles for aghbo in ctx.author.roles]):
            converter = MemberConverter()
            converter2 = RoleConverter()
            banroleids = [738456842707140700, 742128809129803806, 742128992286670910, 742129191277035590]
            for cycl in range(0, len(args.split())):
                user = await converter.convert(ctx, args.split()[cycl])
                userbanroles = []
                for bancycle in banroleids:
                    for x in user.roles:
                        if x.id == bancycle:
                            userbanroles.append(x.id)
                    if bancycle not in userbanroles:
                        break
                if len(userbanroles) != 0:
                    x = userbanroles[-1]
                else:
                    x = 0
                print(userbanroles)
                print(x)
                if x == 0:
                    y = await converter2.convert(ctx, "738456842707140700")
                    await user.add_roles(y)
                    await ctx.send("Ban role " + str(y) + " successfully added to user " + args.split()[cycl])
                elif x != 742129191277035590:
                    y = await converter2.convert(ctx, str(banroleids[banroleids.index(x) + 1]))
                    await user.add_roles(y)
                    [await user.remove_roles(thisshouldntbeplural) for thisshouldntbeplural in
                     ([await converter2.convert(ctx, str(banroleids[z])) for z in range(0, banroleids.index(x) + 1)])]
                    await ctx.send("Ban role " + str(y) + " successfully added to user " + args.split()[cycl])
                else:
                    await user.ban()
                    await ctx.send("User " + args.split()[cycl] + " hath been yeeted")
        else:
            await ctx.send("You do not have permission to use this command")

    @commands.has_permissions(administrator = True)
    @commands.command()
    async def yeet(self, ctx, args):
        '''ACTUALLY bans a user.
        ```//yeet <user>```
        Admin only.'''
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