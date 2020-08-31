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
async def time(message):
    try:
        """Command for displaying time. Ignores arguments."""
        await bot.say(datetime.now().strftime("%H:%M:%S on %a, %B %d, %Y"))
    except Exception as e:
        print(e)
        await bot.say(
            ("I'm sorry, <@%d>, I'm afraid I can't do that. Exception generated: " % message.author.id) + str(e))


@bot.command()
async def coinflip(times : int):
    """Command for flipping a coin. Ignores arguments."""
	for x in range [0, times]:
    	await bot.say(random.choice(["Heads!"] * 50 + ["Tails!"] * 50 + ["The coin landed on the side!!"]))


@bot.command(name="ping")
async def ping():
    """Pings the bot. Ignores arguments."""
    await bot.say("Pong! :ping_pong:")


bot.run(open("token").read())
