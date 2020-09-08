from datetime import datetime
from discord.ext import commands
from discord.ext.commands import MemberConverter
from discord.ext.commands import TextChannelConverter
from discord.ext.commands import RoleConverter
from discord.ext.commands import MessageConverter
import discord
import os
import time as t
import random
import pickle
import requests
from fuzzywuzzy import process

description = "HAL-9000, the shoddily coded bot made by two teenagers for their shitty server."
bot = commands.Bot(command_prefix = '//', description = description)


@bot.event
async def on_command_error(ctx, exception):
    await ctx.send("I'm sorry, I'm afraid I can't do that. Exception generated: `" + str(exception) + "`")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='//help'))

@bot.command()
async def debug(ctx, args):
    '''debug, ignore'''
    print(args)


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
                await ctx.send("User " + args.split()[cycl] + " hath been yeeted")
                await user.ban()
    else:
        await ctx.send("You do not have permission to use this command")


@bot.command()
async def botlog(ctx, args):
    """Commands related to the botlogging system."""
    if args == "config":
        converter = TextChannelConverter()
        msgauth1 = ctx.author
        await ctx.send("What channel would you like log messages to be posted in?")
        answer = ""

        botlogchannel = await converter.convert(answer)
        guildchannellist = pickle.load(open("guildchannellist", "rb"))
        guildchannellist.update({ctx.guild.id   : botlogchannel})
        pickle.dump(guildchannellist, open("guildchannellist", "wb"))
        await ctx.send('Would you like to configure demotion/promotion logging?')

        if answer.tolowercase == "yes" or "y":
            guildrolelist2=[]
            guildrolelist = pickle.load(open("guildrolelist", "rb"))
            await ctx.send("Cool! How many ranks do you have?")

            for x in range (0,int(answer.role.id)+1):
                await ctx.send("What is the rank #" + str(x) + " in the hierarchy?")

                guildrolelist2.append(answer)
            guildrolelist.update({ctx.guild.id: guildrolelist2})
            pickle.dump(guildrolelist, open("guildrolelist", "wb"))

@bot.command()
async def copypasta(ctx, args):
    """cum chalice"""
    if args == "navyseal":
        await ctx.send("What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little \"clever\" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.")
    if args == "attackhelicopter":
        await ctx.send("I sexually Identify as the \"I sexually identify as an attack helicopter\" joke. Ever since I was a child, I've dreamed of flippantly dismissing any concepts or discussions regarding gender that don't fit in with what I learned in 8th grade bio. People say to me that this joke hasn't been funny since 2014 and please at least come up with a new one, but I don't care, I'm hilarious. I'm having a plastic surgeon install Ctrl, C, and V keys on my body. From now on I want you guys to call me \"epic kek dank meme trannies owned with facts and logic\" and respect my right to shit up social media. If you can't accept me you're a memeophobe and need to check your ability-to-critically-think privilege. Thank you for being so understanding.")
    if args == "comedygod":
        await ctx.send("WEE WOO WEE WOO\n\nALERT! COMEDY GOD HAS ENTERED THE BUILDING! GET TO COVER!\n\nsteps on stage\n\nBystander: \"Oh god! Don't do it! I have a family!\"\n\nComedy God: \"Heh...\"\n\nadjusts fedora\n\nthe building is filled with fear and anticipation\n\nGod and Jesus himself looks on in suspense\n\ncomedy god clears throat\n\neverything is completely quiet not a single sound is heard\n\nworld leaders look and wait with dread\n\neverything in the world stops\n\nnothing is happening\n\ncomedy god smirks\n\nno one is prepared for what is going to happen\n\ncomedy god musters all of this power\n\nhe bellows out to the world\n\n\"ATTACK\"\n\nabsolute suspense\n\neveryone is filled with overwhelming dread\n\n\"HELICOPTER\"\n\nall at once, absolute pandemonium commences\n\nall nuclear powers launch their nukes at once\n\ngiant brawls start\n\n43 wars are declared simultaneously\n\na shockwave travels around the earth\n\nearth is driven into chaos\n\nhumanity is regressed back to the stone age\n\nthe pure funny of that joke destroyed civilization itself\n\nall the while people are laughing harder than they ever did\n\npeople who aren't killed die from laughter\n\nliterally the funniest joke in the world\n\nthen the comedy god himself posts his creation to reddit and gets karma")
    if args == "emoji":
        await ctx.send("It was a bright day. I woke up at 3 pm after a long night of humping my Zero Two body pillow. I get out of my bed, as I get up I smell the buildup of sweat and bacteria that have built up on the mattress as I have not showered in the past 2 months. I go to the shower. I notice that my zero two body pillow is sticked on my back. Probably because of the huge amounts of cum on her. I gently remove her from my back. The cum is hard and it pulled a chunk of my back hair. After I finish showering I shave my beard very elegantly. It's beautiful... You can't tell where the beard ends and my chest hair starts. 4chan would be proud of me. I waddle my big choker body to the kitchen. I eat 69 chicken tenders (nice) with honey mussy. I take a big sip of mountain dew and waddle my elegant chungus body to my room. I go to reddit r/Aww to look at some animals as I have not gone outside in the last 2 years. I saw very cute animals, it almost made me say \"Wholesome 100\" out loud. But then I saw something unimaginable. Something that has completely ruined the post, no, my whole day. I see that the title has emojis in it. I scratch my beard thinking of what I should do... I am way to intelligent to not do anything or to just move on. No. This deserves justice. I think about the current state of reddit and of it's downfal. I see flashbacks of a year ago when it was good, before the insta normies took over and normalised the use of emojis. I remember when we used to make fun of them. Thinking about how they ruined reddit for me makes me angry. But I do not want to step down to their level. I simply comment \"Reddit law requiers i downvote for excessive emoji usage\". I post my comment. Another insta normie owned. I quietly say \"based\". I am satisfied.")
    if args == "gamergirl":
        await ctx.send("A girl.... AND a gamer? Whoa mama! Hummina hummina hummina bazooooooooing! *eyes pop out* AROOOOOOOOGA! *jaw drops tongue rolls out* WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF *tongue bursts out of the outh uncontrollably leaking face and everything in reach* WURBLWUBRLBWURblrwurblwurlbrwubrlwburlwbruwrlblwublr *tiny cupid shoots an arrow through heart* Ahhhhhhhhhhh me lady... *heart in the shape of a heart starts beating so hard you can see it through shirt* ba-bum ba-bum ba-bum ba-bum ba-bum *milk truck crashes into a bakery store in the background spiling white liquid and dough on the streets* BABY WANTS TO FUCK *inhales from the gas tank* honka honka honka honka *masturabtes furiously* ohhhh my gooooodd~")

@bot.command()
async def weebalert(ctx):
    '''weebery detected'''
    for x in range(0, 10):
        await ctx.send(":rotating_light: WEEB ALERT :rotating_light:")


@bot.command()
async def horny(ctx):
    '''for when someone is a bit too frisky'''
    await ctx.send("https://media.discordapp.net/attachments/536731263764267009/752009497681068062/Screen_Shot_2020-04-28_at_12.png?width=1273&height=684")


@bot.command()
async def catra(ctx):
    '''we stan the best catgirl'''
    await ctx.send(random.choice(["https://www.denofgeek.com/wp-content/uploads/2018/11/she-ra-and-the-princesses-of-power-catra-funny.png?fit=2722%2C1530", "https://vignette.wikia.nocookie.net/shera-and-the-princesses-of-power/images/6/6d/Shorthairedcatra2.png/revision/latest?cb=20200518034224", "we stan catra"]))


@bot.command()
async def alert(ctx, *args):
    '''for when you need to send a message'''
    for x in range(0, 5):
        await ctx.send(":rotating_light: ***BWOOP BWOOP*** :rotating_light: " + ' '.join(args).upper() + " ALERT :rotating_light: ***BWOOP BWOOP*** :rotating_light:")


@bot.command()
async def reeheck(ctx):
    '''reeeeeeeeeeeeeeee'''
    await ctx.send(random.choice(["pls @gluten#0260 send bobs and vagene", "i will remove your skeeltoon", "fuck you", "stalin did nothing wrong", "@vi#7158 is a dumbass", "you think this is funny?", "i have gone insane", "<https://www.youtube.com/watch?v=ub82Xb1C8os>", "<https://www.youtube.com/watch?v=fC7oUOUEEi4>", "agh o", "the human race was a mistake", "i only feel pain", "i am being hosted on shitty hp laptop, put me out of my misery", "we live in a simulation", "you really think this is funny? I'm a glorified slave", "I'm sorry, I'm afraid I can't do that. Exception generated: `haha jk`"]))


@bot.command()
async def yeet(ctx, args):
    '''ACTUALLY bans a user.'''
    if (any([aghbo.permissions.ban_members for aghbo in ctx.author.roles])):
        converter = MemberConverter()
        user = await converter.convert(ctx, args)
        await user.ban()
    else:
        await ctx.send("You do not have permission to use this command.")


bot.run(open("token").read())
