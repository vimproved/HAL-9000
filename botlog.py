import pickle
async def botlog(ctx, args, bot, channel):
    if args=="channel":
        msgauth1 = ctx.message.author
        await channel.send("What channel would you like log messages to be posted in?")
        botlogchannel = await channel.history().find(lambda m: m.author.id == msgauth1)
        guildchannellist = pickle.load( open( "guildchannellist", "rb" ))
        guildchannellist.update({ctx.message.guild : botlogchannel})
        pickle.dump(guildchannellist, open("guildchannellist", "wb"))
cmds = {"botlog": ("configures botlogger.", botlog  )}
desc = "The Botlogger module of HAL."
