from discord.ext import commands
import requests
import pickle
import discord


def setup(bot):
    bot.add_cog(Fun(bot))


class Fun(commands.Cog):
    """Fun commands!"""

    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        pass

    @commands.command()
    async def dadjoke(self, ctx, args="random"):
        """Searches https://icanhazdadjoke.com for a dadjoke. Put no args or "random" for a random joke.
        ```//dadjoke <joke>```"""
        try:
            if args.lower() == "random":
                dadjoke = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"})
            else:
                dadjoke = requests.get("https://icanhazdadjoke.com/search", params={"term": args, "limit": 1}, headers={
                    "Accept": "text/plain"})
            await ctx.send(dadjoke.content.decode('utf-8'))
        except discord.HTTPException:
            await ctx.send("Hi " + args + ", I'm dad!", allowed_mentions=discord.AllowedMentions(everyone=False,
                                                                                                 users=False,
                                                                                                 roles=False))

    @commands.command()
    async def copypasta(self, ctx, *args):
        """Cum chalice.
        ```//copypasta navyseal
        //copypasta comedygod
        //copypasta emoji
        //copypasta gamergirl
        //copypasta mcultimate
        //copypasta election
        //copypasta ti (written by @rous#7120)```"""
        try:
            globalconfig = pickle.load(open("config", "rb"))
        except EOFError or KeyError:
            globalconfig = {}
        try:
            config = globalconfig[ctx.guild.id]
        except KeyError:
            config = {}
        try:
            enabled = config["copypastaenabled"]
        except KeyError:
            enabled = False
        if enabled:
            cpname = ' '.join(args)
            if cpname == "navyseal":
                await ctx.send(
                    "What the fuck did you just fucking say about me, you little bitch? I'll have you know I "
                    "graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on "
                    "Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top "
                    "sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe "
                    "you the fuck out with precision the likes of which has never been seen before on this Earth, "
                    "mark my fucking words. You think you can get away with saying that shit to me over the Internet? "
                    "Think again, fucker. As we speak I am contacting my secret network of spies across the USA and "
                    "your IP is being traced right now so you better prepare for the storm, maggot. The storm that "
                    "wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be "
                    "anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare "
                    "hands. Not only am I extensively trained in unarmed combat, but I have access to the entire "
                    "arsenal of the United States Marine Corps and I will use it to its full extent to wipe your "
                    "miserable ass off the face of the continent, you little shit. If only you could have known what "
                    "unholy retribution your little \"clever\" comment was about to bring down upon you, "
                    "maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're "
                    "paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. "
                    "You're fucking dead, kiddo.")
            elif cpname == "attackhelicopter":
                await ctx.send(
                    "I sexually Identify as the \"I sexually identify as an attack helicopter\" joke. Ever since I "
                    "was a child, I've dreamed of flippantly dismissing any concepts or discussions regarding gender "
                    "that don't fit in with what I learned in 8th grade bio. People say to me that this joke hasn't "
                    "been funny since 2014 and please at least come up with a new one, but I don't care, "
                    "I'm hilarious. I'm having a plastic surgeon install Ctrl, C, and V keys on my body. From now on "
                    "I want you guys to call me \"epic kek dank meme trannies owned with facts and logic\" and "
                    "respect my right to shit up social media. If you can't accept me you're a memeophobe and need to "
                    "check your ability-to-critically-think privilege. Thank you for being so understanding.")
            elif cpname == "comedygod":
                await ctx.send(
                    "WEE WOO WEE WOO\n\nALERT! COMEDY GOD HAS ENTERED THE BUILDING! GET TO COVER!\n\nsteps on "
                    "stage\n\nBystander: \"Oh god! Don't do it! I have a family!\"\n\nComedy God: "
                    "\"Heh...\"\n\nadjusts fedora\n\nthe building is filled with fear and anticipation\n\nGod and "
                    "Jesus himself looks on in suspense\n\ncomedy god clears throat\n\neverything is completely quiet "
                    "not a single sound is heard\n\nworld leaders look and wait with dread\n\neverything in the world "
                    "stops\n\nnothing is happening\n\ncomedy god smirks\n\nno one is prepared for what is going to "
                    "happen\n\ncomedy god musters all of this power\n\nhe bellows out to the "
                    "world\n\n\"ATTACK\"\n\nabsolute suspense\n\neveryone is filled with overwhelming "
                    "dread\n\n\"HELICOPTER\"\n\nall at once, absolute pandemonium commences\n\nall nuclear powers "
                    "launch their nukes at once\n\ngiant brawls start\n\n43 wars are declared simultaneously\n\na "
                    "shockwave travels around the earth\n\nearth is driven into chaos\n\nhumanity is regressed back "
                    "to the stone age\n\nthe pure funny of that joke destroyed civilization itself\n\nall the while "
                    "people are laughing harder than they ever did\n\npeople who aren't killed die from "
                    "laughter\n\nliterally the funniest joke in the world\n\nthen the comedy god himself posts his "
                    "creation to reddit and gets karma")
            elif cpname == "emoji":
                await ctx.send(
                    "It was a bright day. I woke up at 3 pm after a long night of humping my Zero Two body "
                    "pillow. I get out of my bed, as I get up I smell the buildup of sweat and bacteria "
                    "that have built up on the mattress as I have not showered in the past 2 months. I go "
                    "to the shower. I notice that my zero two body pillow is sticked on my back. Probably "
                    "because of the huge amounts of cum on her. I gently remove her from my back. The cum "
                    "is hard and it pulled a chunk of my back hair. After I finish showering I shave my "
                    "beard very elegantly. It's beautiful... You can't tell where the beard ends and my "
                    "chest hair starts. 4chan would be proud of me. I waddle my big choker body to the "
                    "kitchen. I eat 69 chicken tenders (nice) with honey mussy. I take a big sip of "
                    "mountain dew and waddle my elegant chungus body to my room. I go to reddit r/Aww to "
                    "look at some animals as I have not gone outside in the last 2 years. I saw very cute "
                    "animals, it almost made me say \"Wholesome 100\" out loud. But then I saw something "
                    "unimaginable. Something that has completely ruined the post, no, my whole day. I see "
                    "that the title has emojis in it. I scratch my beard thinking of what I should do... I "
                    "am way to intelligent to not do anything or to just move on. No. This deserves "
                    "justice. I think about the current state of reddit and of it's downfal. I see "
                    "flashbacks of a year ago when it was good, before the insta normies took over and "
                    "normalised the use of emojis. I remember when we used to make fun of them. Thinking "
                    "about how they ruined reddit for me makes me angry. But I do not want to step down to "
                    "their level. I simply comment \"Reddit law requiers i downvote for excessive emoji "
                    "usage\". I post my comment. Another insta normie owned. I quietly say \"based\". I am "
                    "satisfied.")
            elif cpname == "gamergirl":
                await ctx.send(
                    "A girl.... AND a gamer? Whoa mama! Hummina hummina hummina bazooooooooing! *eyes pop out* "
                    "AROOOOOOOOGA! *jaw drops tongue rolls out* WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF WOOF "
                    "WOOF WOOF WOOF WOOF *tongue bursts out of the outh uncontrollably leaking face and everything in "
                    "reach* WURBLWUBRLBWURblrwurblwurlbrwubrlwburlwbruwrlblwublr *tiny cupid shoots an arrow through "
                    "heart* Ahhhhhhhhhhh me lady... *heart in the shape of a heart starts beating so hard you can see "
                    "it through shirt* ba-bum ba-bum ba-bum ba-bum ba-bum *milk truck crashes into a bakery store in "
                    "the background spiling white liquid and dough on the streets* BABY WANTS TO FUCK *inhales from "
                    "the gas tank* honka honka honka honka *masturabtes furiously* ohhhh my gooooodd~")
            elif cpname == "mcultimate":
                await ctx.send(
                    "Unpopular opinion but I don’t actually think Nestor, Cal, and Techno are gonna win tomorrow. "
                    "I’ve challenged them with an immediate disadvantage of being a team of 3 in a team of 4 event on "
                    "1.12... that’s gonna be really hard no matter how good they might be")
            elif cpname == "ti":
                await ctx.send(
                    "we've all been to the store and seen those TI-84+s and TI-83+ and CEs and SEs and all the other "
                    "garbage that TI released, and on the box it says something like SAT CERTIFIED :tm: "
                    ":copyright::tm: but what we DON'T notice is the price tag of OVER ONE HUNDRED DOLLARS. now "
                    "that's all good and fine, you might say, it seems like a lot for a calculator but it *is* a "
                    "piece of precision electronics with some pretty advanced processing capacities. actually, "
                    "you won't (i hope), because you're HOPEFULLY smart enough to think your way around the RUSE "
                    "created by the DEVILS RUNNING TI. those pieces of shit have about 128 kilobytes of memory apiece "
                    "- oh and let's not forget that 100kb of it is just completely inaccessible because OPERATING "
                    "SYSTEM **BUT WAIT**! it has a whole three and a half MEGABYTES of storage and of course if you "
                    "want to run apps from the storage you have to TRANSFER IT INTO THE TWENTY FUCKING KILOBYTES OF "
                    "MEMORY. and to top all of this shit off it has a CPU from the 1990s. did i say 1990s? i meant "
                    "1970s.  its clock rate is a whole TWO AND A HALF "
                    "FUCKING MEGAHERTZ, only A THOUSAND TIMES LESS THAN THAT OF YOUR COMPUTER. but, you say, "
                    "that's all reasonable for a calculator - after all, it's not a computer. you're right, "
                    "it's reasonable to have terrible hardware for a calculator, BUT NOT FOR ONE THAT COSTS ONE "
                    "HUNDRED FUCKING DOLLARS. i've seen estimates that run from five to twenty-five dollars on how "
                    "much ti spends per calculator actually making it. so WHY would they do this? the answer isn't "
                    "very hard to guess: fucking CAPITALISM. ti is one of the world's best examples of CAPITALIST "
                    "SCUM. it's a three step process to success:")
                await ctx.send(
                    "1. make a product that's OKAY but not worth a $100 price tag, or, even better, make a product "
                    "that's an ABSOLUTE PIECE OF SHIT 2: SELL IT FOR $100 BECAUSE YOU HAVE A FUCKING MONOPOLY ON THE "
                    "CALCULATOR MARKET. 3: using your money that you got by SCAMMING EVERY STUDENT WHO'S EVER LIVED, "
                    "bribe test boards into only accepting the latest and greatest TI CALCULATOR:tm: 4 (!!EXTRA BONUS "
                    "STEP!!) completely ignoring even the most primitive of moral compasses, continue to commit "
                    "heinous acts by branding it as ADVANCED, CHEAP and WORTH THE PRICE. and of course, nobody will "
                    "know any better and if they do? FUCK THEM, THEY DON'T HAVE A FUCKING CHOICE. these executives "
                    "are going to BURN IN HELL and i don't even believe that hell exists, it's just THAT IMPERATIVE "
                    "that they SUFFER FOR THIS. but UNTIL THEN, it's time for $100 BRICKS that have 96x64 pixel "
                    "screens - oh wait, you can pay for the ULTRA BULLSHIT PRICE EDITION, only like $150 and you get "
                    "a COLOR SCREEN that's almost 1/20th the resolution of your computer BUT WAIT!!! this is the "
                    "HIGH:tm: RESOLUTION :copyright: VERSION WITH IMMERSIVE COLOR GRAPHICS! anyway to sum this all up "
                    "fuck ti they are pieces of shit")
            elif cpname == "novysole":
                await ctx.send(
                    "As far as I know about my son, I received a letter from a famous naval station stating that I "
                    "was involved with more than 300 people in a secret protest against Al Qaeda. My gorilla trained "
                    "me to be the most powerful hunter and sniper in the United States Army. It does not matter to "
                    "me, I will bring you here in person. You think you can see other people. Stupid, think again. In "
                    "fact, I contacted the US Secret Service and tried to find an IP address in the best possible "
                    "way. Storms wreak havoc on the little things that keep you alive. Honey, I can kill you 100 "
                    "times at a time. Not only will I have more training in the unarmed war, but I will also have "
                    "full access to the U.S. Army. I will use it to help. Shame on you on this continent. Knowing bad "
                    "warnings will give you \"wisdom\" and guidance will help you move forward. But you can not, "
                    "you can not and you have to pay and lose. I was threatened with drowning. I'm in love")
            else:
                await ctx.send("List of copypastas:\n```//copypasta navyseal\n//copypasta comedygod\n//copypasta emoji\n//copypasta gamergirl\n//copypasta mcultimate\n//copypasta ti (written by @rous#7120)\n//copypasta novysole```")
            await ctx.message.delete()
        else:
            await ctx.send("Copypastas are not enabled on this server.")

    @commands.command()
    async def bonk(self, ctx):
        """BONK! Ignores arguments."""
        await ctx.send("go to #horny-jail")
        await ctx.send(
            "https://media.discordapp.net/attachments/536731263764267009/752009497681068062/Screen_Shot_2020-04"
            "-28_at_12.png?width=1273&height=684")
        await ctx.message.delete()

    @commands.command()
    async def alert(self, ctx, *args):
        """!BWOOP BWOOP! Sends an alert 5 times.
        ```//alert <text>```"""
        alert_text = eval('"' + ' '.join(args).upper() + '"')
        await ctx.send(":rotating_light: ***bwoop bwoop*** :rotating_light: " + alert_text + " ALERT :rotating_light: "
                                                                                             "***bwoop bwoop*** "
                                                                                             ":rotating_light:",
                       allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
