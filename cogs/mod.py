from discord.ext import commands
import discord
import toml
from discord.ext.commands import TextChannelConverter, MemberConverter


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
            await user.ban(reason=' '.join(args[1:]))
        except IndexError:
            await user.ban()
        await ctx.send(user.mention + " has been banned.")
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def warn(self, ctx, *args):
        """Warns a user.
        Requires manage roles.

        Syntax:
        `//warn <user> <reason>`"""
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(ctx.guild.id)]
        except KeyError:
            config = {}
        user = await MemberConverter().convert(ctx, args[0])
        try:
            warns = config["warns"][str(user.id)]
        except KeyError:
            warns = []
        except IndexError:
            warns = []
        try:
            systemchannel = await TextChannelConverter().convert(ctx, str(config["systemchannel"]))
        except KeyError:
            systemchannel = ctx.channel
        try:
            reason = ' '.join(args[1:])
            warns.append(reason)
            warns = {str(user.id): warns}
        except IndexError:
            raise commands.errors.MissingRequiredArguments
        config.update({"warns": warns})
        globalconfig[str(ctx.guild.id)] = config
        open("config.toml", "w").write(toml.dumps(globalconfig))
        await ctx.send("User warned.")
        embed_var = discord.Embed(color=0xff0008, title="__Member warned.__", description=user.mention + " was warned with reason \"" + reason + "\"")
        embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
        await systemchannel.send(embed=embed_var)

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def warns(self, ctx, args):
        user = await MemberConverter().convert(ctx, args)
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(ctx.guild.id)]
        except KeyError:
            config = {}
        try:
            warns = config["warns"][str(user.id)]
        except KeyError:
            warns = []
        except IndexError:
            warns = []
        if len(warns) == 0:
            await ctx.send("Member has no warnings.")
            return
        embed_var = discord.Embed(color=0xff0008, title="__Warnings for " + str(user) + ".__", description=user.name + "'s warnings.")
        embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
        for warn in warns:
            embed_var.add_field(name="Warning " + str(warns.index(warn)+1), value=warn, inline=False)
        await ctx.send(embed=embed_var)

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
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def poll(self, ctx, *args):
        """Creates a poll in a the specified channel via an attatched text file.
        All 3 fields must be proceeded by 3 uppercase hexidecimal characters that specify the length of the field.
        Admin only.
        ```//poll <channel> <role (optional)>```"""
        global cone
        try:
        	pchan = await TextChannelConverter().convert(ctx, args[0])
        except:
        	await ctx.send('Error processing channel')
        	return
        try:
                mesgurl = requests.get("https://discord.com/api/v6/channels/"+str(ctx.channel.id)+"/messages/"+str(ctx.message.id), headers={"Authorization": "Bot "+open("token").read()[:-1], "Accept": "*/*"})
                mesgurl = json.loads(mesgurl.content.decode('utf-8'))['attachments'][0]['url']
                passtoc = bytes(requests.get(mesgurl, headers={"Authorization": "Bot "+open("token").read()[:-1], "Accept": "*/*"}).content.decode('utf-8'),'utf-8')
                agh = cone.parsepoll(passtoc,len(passtoc))
        except:
                await ctx.send('Error obtaining embed')
                agh = 257
        if (agh==257):
                await ctx.send('Error processing embed')
        else:
                segf = [int.from_bytes(agh[i*8:i*8+7],byteorder='little') for i in [0,1,2]]
                agb  = agh[24:].decode('utf-8')
                poll = discord.Embed(color=0xc04080,title=agb[0:segf[1]],description=agb[segf[1]:segf[2]]).add_field(name="Things",value=agb[segf[2]:],inline=False)
                await pchan.send('',embed=poll)
