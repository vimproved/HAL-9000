from discord.ext import commands
from datetime import datetime
import discord
import pickle
import sys

class HAL(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.description = "A multipurpose bot made by vi#7158."
        self.token = open("token").read()
        self.loaded_cogs = ["cogs.mod", "cogs.util", "cogs.fun"]
        self.startup()

    async def on_command_error(self, ctx, exception):
        if type(exception) is commands.errors.CommandNotFound:
            return
        elif type(exception) is commands.errors.MissingPermissions:
            await ctx.send("You are missing permissions required to run this command.")
            return
        elif str(exception).startswith("Command raised an exception: IndexError:"):
            await ctx.send("This command requires arguments that you did not specify. Do //help <command> for information on how to use this command.")
            return
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError:
            print("Config file is blank. If you're seeing this your installation of HAL is probably new, or a critical error has occurred.")
            globalconfig = {}
        await ctx.send(str(exception))
        config = globalconfig[ctx.guild.id]
        logchannel = self.get_channel(int(config['logchannel']))
        await logchannel.send("Error log at " + str(datetime.now()) + ": " + str(exception) + " Type: " + str(type(exception)) + ". Invoke message: " + ctx.message.jump_url)

    @staticmethod
    async def on_ready():
        print("HAL-9000")
        print("HAL is ready!")
        await bot.change_presence(activity=discord.Game(name='//help'))

    @staticmethod
    async def on_connect():
        print("HAL is connected!")

    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.token))
        except KeyboardInterrupt:
            pass
        except discord.LoginFailure:
            print("Invalid token")
        except discord.HTTPException:
            print("Could not connect.")
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

    async def on_member_ban(self, guild, user):
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError:
            print("Config file is blank. If you're seeing this your installation of HAL is probably new, or a critical error has occurred.")
            globalconfig = {}
        config = globalconfig[guild.id]
        systemchannel = self.get_channel(int(config['systemchannel']))
        ban = await guild.fetch_ban(user)
        reason = ban[0]
        if reason == None:
            embed_var = discord.Embed(color=0xff0008, title="__Member banned.__", description=user.mention + " was banned from the server.")
        else:
            embed_var = discord.Embed(color=0xff0008, title="__Member banned.__", description=user.mention + " was banned from the server with reason \"" + reason + "\"")
        await systemchannel.send(embed=embed_var)

    async def on_member_join(self, member):
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError:
            print("Config file is blank. If you're seeing this your installation of HAL is probably new, or a critical error has occurred.")
            globalconfig = {}
        config = globalconfig[member.guild.id]
        systemchannel = self.get_channel(int(config['systemchannel']))
        embed_var = discord.Embed(color=0xff0008, title="__Ahoy There!__", description=member.mention + " joined the server! Make sure to read #readme!")
        await systemchannel.send(embed=embed_var)

    async def on_member_remove(self, member):
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError:
            print("Config file is blank. If you're seeing this your installation of HAL is probably new, or a critical error has occurred.")
            globalconfig = {}
        config = globalconfig[member.guild.id]
        systemchannel = self.get_channel(int(config['systemchannel']))
        embed_var = discord.Embed(color=0xff0008)
        embed_var.add_field(name="__See You Later!__", value=member.mention + " left the server. See you next time!")
        await systemchannel.send(embed=embed_var)

    async def on_message_delete(self, message):
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError:
            print("Config file is blank. If you're seeing this your installation of HAL is probably new, or a critical error has occurred.")
            globalconfig = {}
        config = globalconfig[message.guild.id]
        logchannel = self.get_channel(int(config['logchannel']))
        await logchannel.send("Message sent by " + str(message.author) + " deleted at " + str(datetime.now()) + ". Contents: " + message.content)


bot = HAL("//")


@commands.is_owner()
@bot.command()
async def stop(ctx):
    await ctx.send("Shutting down bot.")
    await bot.logout()
	os.exit()


bot.run()
