import pickle
import time
async def botlog(args, bot, channel, message):
    if args=="logchannel ":
        msgauth1 = message.author
        await channel.send("What channel would you like log messages to be posted in?")
        answer = await fetch_message(channel.last_message_id)
        while answer != msgauth1:
            time.sleep(0.1)
            print(answer)
            print(msgauth1)
        guildchannellist = pickle.load(open("guildchannellist", "rb"))
        guildchannellist.update({message.guild.id: botlogchannel})
        pickle.dump(guildchannellist, open("guildchannellist", "wb"))
        await channel.send('Would you like to configure demotion/promotion logging?')
        answer = await fetch_message(channel.last_message_id)
        if answer.tolowercase == "yes" or "y":
            guildrolelist2=[]
            guildrolelist = pickle.load(open("guildrolelist", "rb"))
            await channel.send("Cool! How many ranks do you have?")
            answer = await fetch_message(channel.last_message_id)
            for x in range (0,int(answer.role.id)+1):
                await channel.send(channel.last_message)
                answer = channel.last_message
                guildrolelist2.append(answer)
                guildrolelist.update({message.guild.id: guildrolelist2})
                pickle.dump(guildrolelist, open("guildrolelist", "wb"))
cmds = {"botlog": ("configures botlogger.", botlog)}
desc = "The Botlogger module of HAL."