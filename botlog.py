import pickle
@bot.command()
async def botlog(ctx, args, bot, channel):
    if args=="logchannel ":
        msgauth1 = message.author
        await channel.send("What channel would you like log messages to be posted in?")
        botlogchannel = await channel.history().find(lambda m: m.author.id == msgauth1)
        guildchannellist = pickle.load(open( "guildchannellist", "rb" ))
        guildcnhannellist.update({ctx.message.guild : botlogchannel})
        pickle.dump(guildchannellist, open("guildchannellist", "wb"))
        await channel.send('Would you like to configure demotion/promotion logging?')
        answer = await channel.history().find(lambda m: m.author.id == msgauth1)
        if answer.tolowercase == "yes" or "y":
            guildrolelist2=[]
            guildrolelist = pickle.load(open("guildrolelist", "rb"))
            await channel.send("Cool! How many ranks do you have?")
            answer = await channel.history().find(lambda m: m.author.id == msgauth1)
            for x in range (0,int(answer.role.id)+1):
                await channel.send("Tag the rank that is #" + x + " in the hierarchy.")
                answer = await channel.history().find(lambda m: m.author.id == msgauth1)
                guildrolelist2.append(answer)
                guildrolelist.update({ctx.message.guild: guildrolelist2})
                pickle.dump(guildrolelist, open("guildrolelist", "wb"))
cmds = {"botlog": ("configures botlogger.", botlog  )}
desc = "The Botlogger module of HAL."
