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
async def time(ctx):
    """Command for displaying time. Ignores arguments."""
    await ctx.send(datetime.now().strftime("%H:%M:%S on %a, %B %d, %Y"))


@bot.command()
async def coinflip(ctx):
    """Command for flipping a coin. Ignores arguments."""
    await ctx.send(random.choice(["Heads!"] * 50 + ["Tails!"] * 50 + ["The coin landed on the side!!"]))


@bot.command()
async def ping(ctx):
    """Pings the bot. Ignores arguments."""
    await ctx.send("Pong! :ping_pong:")


@bot.command()
async def open(ctx, args):
    """Open the pod bay doors, HAL."""
    if "pod bay doors" in args.lower():
        ctx.send("I'm sorry dave, I'm afraid I can't do that.")

bot.run(open("token").read())
