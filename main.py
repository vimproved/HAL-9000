from discord.ext import commands
import discord


class HAL(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.command_prefix = "//"
        self.description = "A multipurpose bot made by vi#7158 and rous#7120"
        self.token = open("token").read()
        self.loaded_cogs = ["cogs.botlog", "cogs.util", "cogs.mod", "cogs.fun", "cogs.rngesus"]
        self.startup()

#    async def on_command_error(self, ctx, exception):
#        await ctx.send("I'm sorry " + ctx.author.mention + ", I'm afraid I can't do that. Exception generated: `" + str(exception) + "`")

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
            print("loading %s", cog)
            try:
                self.load_extension(cog)
                print("Cog loaded.")
            except Exception as e:
                print("Failed to load cog. Reason: " + str(e))



bot = HAL("//")
bot.run()
