from discord.ext import commands
from datetime import datetime
import discord
import sys
import toml
from cogs.util import Utility


class HAL(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.description = "A multipurpose bot made by vi#7158."
        self.token = open("token").read()
        self.loaded_cogs = ["cogs.mod", "cogs.util", "cogs.fun"]
        self.startup()
        self.util = Utility(self)
        # Open config file in append mode.
        open("config.toml", "a")

    async def on_command_error(self, ctx, exception):
        # Exception handling happens here.
        if type(exception) is commands.errors.CommandNotFound:
            return
        elif type(exception) is commands.errors.MissingPermissions:
            await ctx.send("You are missing permissions required to run this command.")
            return
        elif type(exception) is commands.errors.MissingRequiredArgument or IndexError:
            await self.util.help(self.util, ctx, ctx.command.name)
            return
        await ctx.send(str(exception))
        config = toml.loads(open("config.toml", "rt").read())
        logchannel = self.get_channel(config['logchannel'])
        await logchannel.send("Error log at " + str(datetime.now()) + ": " + str(exception) + " Type: " + str(type(exception)) + ". Invoke message: " + ctx.message.jump_url)

    @staticmethod
    async def on_ready():
        print("HAL-9000")
        print("HAL is ready!")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='//help'))

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
            print("Loading " + cog + ".")
            try:
                self.load_extension(cog)
                print("Cog loaded.")
            except Exception as e:
                print("Failed to load cog. Reason: " + str(e))

    async def on_member_ban(self, guild, user):
        config = toml.loads(open("config.toml", "rt").read())
        systemchannel = self.get_channel(config['systemchannel'])
        ban = await guild.fetch_ban(user)
        reason = ban[0]
        if reason is None:
            embed_var = discord.Embed(color=0xff0008, title="__Member banned.__", description=user.mention + " was banned from the server.")
        else:
            embed_var = discord.Embed(color=0xff0008, title="__Member banned.__", description=user.mention + " was banned from the server with reason \"" + reason + "\"")
        await systemchannel.send(embed=embed_var)

    async def on_member_join(self, member):
        config = toml.loads(open("config.toml", "rt").read())
        systemchannel = self.get_channel(config['systemchannel'])
        embed_var = discord.Embed(color=0xff0008, title="__Ahoy There!__", description=member.mention + " joined the server! Make sure to read #readme!")
        await systemchannel.send(embed=embed_var)

    async def on_member_remove(self, member):
        config = toml.loads(open("config.toml", "rt").read())
        systemchannel = self.get_channel(config['systemchannel'])
        embed_var = discord.Embed(color=0xff0008)
        embed_var.add_field(name="__See You Later!__", value=member.mention + " left the server. See you next time!")
        await systemchannel.send(embed=embed_var)

    async def on_message_delete(self, message):
        config = toml.loads(open("config.toml", "rt").read())
        logchannel = self.get_channel(config['logchannel'])
        await logchannel.send("Message sent by " + str(message.author) + " deleted at " + str(datetime.now()) + ". Contents: " + message.content)


bot = HAL("//")


@commands.is_owner()
@bot.command()
async def stop(ctx):
    await ctx.send("Shutting down bot.")
    await bot.logout()
    sys.exit()


bot.run()
