import legacy as cmds_legacy
import rngesus as cmds_rngesus
import dnd as cmds_dnd
import joke as cmds_joke
import botlog as cmds_botlog
import mod as cmds_mod
import discord
from datetime import datetime
import random
from discord.ext import commands

description = "HAL-9000, the shoddily coded bot made by two teenagers for their shitty server."
bot = commands.Bot(command_prefix = '//', description = description)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def time():
    """Command for displaying time. Ignores arguments."""
    await bot.say(datetime.now().strftime("%H:%M:%S on %a, %B %d, %Y"))


@bot.command()
async def coinflip():
    """Command for flipping a coin. Ignores arguments."""
    await bot.say(random.choice(["Heads!"] * 50 + ["Tails!"] * 50 + ["The coin landed on the side!!"]))


@bot.command(name="ping")
async def ping():
    """Pings the bot. Ignores arguments."""
    await bot.say("Pong! :ping_pong:")


bot.run(open("token").read())
