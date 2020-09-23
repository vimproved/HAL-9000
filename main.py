from discord.ext import commands
from datetime import datetime
import discord
import pickle

try:
    globalconfig = pickle.load(open("config", "rb"))
except EOFError:
    print("Config file is blank. If you're seeing this your installation of HAL is probably new, or a critical error "
          "has occurred.")
    globalconfig = {}


class HAL(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.command_prefix = "//"
        self.description = "A multipurpose bot made by vi#7158 and rous#7120"
        self.token = open("token").read()
        self.loaded_cogs = ["cogs.mod", "cogs.util", "cogs.fun", "cogs.random"]
        self.startup()

    async def on_command_error(self, ctx, exception):
        await ctx.send("I'm sorry " + ctx.author.mention + ", I'm afraid I can't do that.")
        config = globalconfig[ctx.guild.id]
        logchannel = discord.Client.get_channel(self, config["logchannel"])
        await logchannel.send("Error log at " + str(datetime.now()) + ": " + str(exception) + ". Invoke message: " + ctx.message.jump_url)

    async def on_ready(self):
        print("HAL-9000")
        print("HAL is ready!")
        await bot.change_presence(activity=discord.Game(name='//help'))

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
        config = globalconfig[member.guild.id]
        systemchannel = discord.utils.get(member.guild.text_channels, id=config["systemchannel"])
        embed_var = discord.Embed(color=0xff0008)
        embed_var.add_field(name="__Ahoy There!__",
                            value=member.mention + "joined the server! Make sure to read #readme!")
        await systemchannel.send(embed=embed_var)

    async def on_member_remove(self, member):
        config = globalconfig[member.guild.id]
        systemchannel = discord.utils.get(member.guild.text_channels, id=config["systemchannel"])
        embed_var = discord.Embed(color=0xff0008)
        embed_var.add_field(name="__See You Later!__", value=member.mention + " left the server. See you next time!")
        await systemchannel.send(embed=embed_var)

    async def on_message_delete(self, message):
        config = globalconfig[message.guild.id]
        logchannel = discord.utils.get(message.guild.text_channels, id=config["logchannel"])
        await logchannel.send("Message sent by " + str(message.author) + " deleted at " + str(datetime.now()) + ". Contents: " + message.content)


bot = HAL("//")


@commands.is_owner()
@bot.command()
async def stop(ctx):
    await ctx.send("Shutting down bot.")
    await bot.logout()


bot.run()
