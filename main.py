import NAME as cmds_NAME
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
client.run('NzE3MDQyMTI2Nzc2NDM0NzI4.XtmFVQ.X19EEdNIgbKuYpy5frWM5cXQlHg')