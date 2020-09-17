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
        await logchannel.send(member.mention + " joined the server :), welcome!")

    async def on_member_remove(self, member):
        try:
            guildchannellist = pickle.load(open("guildchannellist", "rb"))
            logchannel = discord.Client.get_channel(self, guildchannellist.get(member.guild.id))
        except EOFError:
            logchannel = member.guild.system_channel
        await logchannel.send(member.mention + " left the server :(, we'll miss you!")


bot = HAL("//")
bot.run()
