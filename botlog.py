import pickle
async def botlog(subcmd):
    if subcmd=="config":
        message.channel.send("What channel would you like log messages to be posted in?")
        await on_message()