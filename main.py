from datetime import datetime
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import TextChannelConverter
from discord.ext.commands import RoleConverter
from discord.ext.commands import MessageConverter
import discord
import random
import pickle
import requests
from fuzzywuzzy import process

description = "HAL-9000, the shoddily coded bot made by two teenagers for their shitty server."
bot = commands.Bot(command_prefix='//', description=description)


async def response(ctx, user, channel):
    converter = MessageConverter()
    lastmessage = await converter.convert(ctx, channel.last_message_id)
    while lastmessage.author != user:
        lastmessage = await converter.convert(ctx, channel.last_message_id)
    return(str(lastmessage))



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
    if (any([aghbo.permissions.manage_roles for aghbo in ctx.author.roles])):
        converter = MemberConverter()
        converter2 = RoleConverter()
        banroleids = [738456842707140700, 742128809129803806, 742128992286670910, 742129191277035590]
        for cycl in range(0,len(args.split())):
            user = await converter.convert(ctx, args.split()[cycl])
            userbanroles = []
            for bancycle in banroleids:
                for x in user.roles:
                    if x.id == bancycle:
                        userbanroles.append(x.id)
                if (not bancycle in userbanroles):
                    break
            if len(userbanroles) != 0:
                x = userbanroles[-1]
            else:
                x = 0
            print(userbanroles)
            print(x)
            if x == 0:
                y = await converter2.convert(ctx, "738456842707140700")
                await user.add_roles(y)
                await ctx.send("Ban role " + str(y) + " successfully added to user " + args.split()[cycl])
            elif x != 742129191277035590:
                y = await converter2.convert(ctx, str(banroleids[banroleids.index(x) + 1]))
                await user.add_roles(y)
                [await user.remove_roles(thisshouldntbeplural) for thisshouldntbeplural in ([await converter2.convert(ctx, str(banroleids[z])) for z in range(0,banroleids.index(x)+1)])]
                await ctx.send("Ban role " + str(y) + " successfully added to user " + args.split()[cycl])
            else:
                await ctx.send("User " + args.split()[cycl] + " has all the banned roles already.")
    else:
        await ctx.send("You do not have permission to use this command")


@bot.command()
async def botlog(ctx, args):
    if args == "config":
        converter = TextChannelConverter()
        msgauth1 = ctx.author
        await ctx.send("What channel would you like log messages to be posted in?")
        answer = await response(ctx, ctx.author, ctx.channel)
        botlogchannel = await converter.convert(answer)
        guildchannellist = pickle.load(open("guildchannellist", "rb"))
        guildchannellist.update({ctx.guild.id   : botlogchannel})
        pickle.dump(guildchannellist, open("guildchannellist", "wb"))
        await ctx.send('Would you like to configure demotion/promotion logging?')
        if answer.tolowercase == "yes" or "y":
            guildrolelist2=[]
            guildrolelist = pickle.load(open("guildrolelist", "rb"))
            await ctx.send("Cool! How many ranks do you have?")
            answer = await response(ctx, ctx.author, ctx.channel)
            for x in range (0,int(answer.role.id)+1):
                await ctx.send("What is your ")
                answer = await response(ctx, ctx.author, ctx.channel)
                guildrolelist2.append(answer)
                guildrolelist.update({ctx.guild.id: guildrolelist2})
                pickle.dump(guildrolelist, open("guildrolelist", "wb"))


bot.run(open("token").read())
