from datetime import datetime
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import RoleConverter
import discord
import random
import requests
from fuzzywuzzy import process

description = "HAL-9000, the shoddily coded bot made by two teenagers for their shitty server."
bot = commands.Bot(command_prefix='//', description=description)


@bot.event
async def on_command_error(ctx, exception):
    await ctx.send("I'm sorry, I'm afraid I can't do that. Exception generated: `" + str(exception) + "`")


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
async def roll(ctx, args):
    """Rolls any amount of dice with any amount of sides. Format: //roll XdX"""
    total = 0
    crits = 0
    critf = 0
    for die in args.split():
        if 'd' not in die:
            total += int(die)
            continue
        num, sides = die.split('d')
        if num == '':
            num = '1'
        rolls = [random.randint(1, int(sides)) for n in range(int(num))]
        if sides == '20':
            crits += rolls.count(20)
            critf += rolls.count(1)
        total += sum(rolls)
    await ctx.send("Result: " + str(total) + "\n***CRITICAL SUCCESS!***" * crits + "\n***CRITICAL FAILURE!***" * critf)


@bot.command()
async def ban(ctx, args):
    """'Bans' a user."""
    converter = MemberConverter()
    converter2 = RoleConverter()
    user = await converter.convert(ctx, args)
    banroleids = [738456842707140700, 742128809129803806, 742128992286670910, 742129191277035590]
    userbanroles = []
    for bancycle in banroleids:
        for x in user.roles:
            if x.id == bancycle:
                userbanroles.append(x.id)
        if (not bancycle in user.roles):
            break
    if len(userbanroles) != 0:
        x = userbanroles[0]
    else:
        x = 0
    print(userbanroles)
    print(x)
    if x == 0:
        y = await converter2.convert(ctx, "738456842707140700")
        await user.add_roles(y)
        await ctx.send("Ban role " + str(y) + " successfully added to user " + args)
    elif x != 742129191277035590:
        y = await converter2.convert(ctx, str(banroleids[banroleids.index(x) + 1]))
        await user.add_roles(y)
        [await user.remove_roles(thisshouldntbeplural) for thisshouldntbeplural in ([await converter2.convert(ctx, str(banroleids[z])) for z in range(0,banroleids.index(x))])]
        await ctx.send("Ban role " + str(y) + " successfully added to user " + args)
    else:
        await ctx.send("User " + args + " has all the banned roles already.")


bot.run(open("token").read())
