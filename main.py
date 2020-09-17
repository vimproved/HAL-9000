from discord.ext import commands
import discord
import pickle


class HAL(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.command_prefix = "//"
        self.description = "A multipurpose bot made by vi#7158 and rous#7120"
        self.token = open("token").read()
        self.loaded_cogs = ["cogs.mod", "cogs.util", "cogs.fun", "cogs.rngesus"]
        self.startup()

    async def on_command_error(self, ctx, exception):
        await ctx.send("I'm sorry " + ctx.author.mention + ", I'm afraid I can't do that. " + str(exception).lstrip("Command raised an exception: Exception:"))

    async def on_ready(self):
        print("HAL-9000")
        print("HAL is ready!")
        await bot.change_presence(activity=discord.Game(name='is cereal a soup?'))

    async def on_connect(self):
        print("HAL is connected!")

    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.token))
        except KeyboardInterrupt:
            pass
        except discord.LoginFailure:
            print("Invalid token")
        except Exception:
            print("Fatal exception")
        finally:
            self.loop.run_until_complete(self.logout())

    def startup(self):
        print("Loading cogs...")
        for cog in self.loaded_cogs:
            print("Loading", cog)
            try:
                self.load_extension(cog)
                print("Cog loaded.")
            except Exception as e:
                print("Failed to load cog. Reason: " + str(e))

    async def on_member_join(self, member):
        try:
            guildchannellist = pickle.load(open("guildchannellist", "rb"))
            logchannel = discord.Client.get_channel(self, guildchannellist.get(member.guild.id))
        except EOFError:
            logchannel = member.guild.system_channel
        embed_var = discord.Embed(color=0xff0008)
        embed_var.add_field(name="__Ahoy There!__", value=member.mention + " joined the server! Make sure to read #readme!")
        await logchannel.send(embed=embed_var)

    async def on_member_remove(self, member):
        try:
            guildchannellist = pickle.load(open("guildchannellist", "rb"))
            logchannel = discord.Client.get_channel(self, guildchannellist.get(member.guild.id))
        except EOFError:
            logchannel = member.guild.system_channel
        embed_var = discord.Embed(color=0xff0008)
        embed_var.add_field(name="__See You Later!__", value=member.mention + " left the server. See you next time!")
        await logchannel.send(embed=embed_var)

    async def on_member_update(self, before, after):
        guildchannellist = pickle.load(open("guildchannellist", "rb"))
        logchannel = discord.Client.get_channel(self, guildchannellist.get(after.guild.id))
        if len(before.roles) > len(after.roles):
            smaller = after.roles
            bigger = before.roles
        elif len(after.roles) > len(before.roles):
            smaller = before.roles
            bigger = after.roles
        else:
            return
        difference = list(set(bigger) - set(smaller))
        guildrolelist = pickle.load(open("guildrolelist", "rb"))
        guildrolelist = guildrolelist.get(after.guild.id)
        for x in guildrolelist:
            x = after.guild.get_role(x)
            if x in difference:
                if len(before.roles) > len(after.roles):
                    try:
                        afterrole = (after.guild.get_role(guildrolelist(guildrolelist.index(x)-1))).name
                    except Exception:
                        afterrole = "user"
                    embed_var.add_field(name="__Demotion.__",
                                        value=after.mention + " has been demoted from *" + x.name + "* to *" + afterrole + "*.")
                    await logchannel.send(ember=embed_var)
                elif len(after.roles) > len(before.roles):
                    try:
                        beforerole = (after.guild.get_role(guildrolelist(guildrolelist.index(x)+1))).name
                    except Exception:
                        beforerole = "user"
                        embed_var = discord.Embed(color=0xff0008)
                        embed_var.add_field(name="__Promotion!__",
                                            value=after.mention + " has been promoted from *" + beforerole + "* to *" + x.name + "*.")
                        await logchannel.send(embed=embed_var)


bot = HAL("//")
bot.run()
