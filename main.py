import legacy as cmds_legacy
import discord

client = discord.Client()
prefix = "//"

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author != client.user and message.content.startswith(prefix):
		text = message.content[len(prefix):]
		await run_command(text.split()[0], ' '.join(text.split()[1:]), message.channel)

async def run_command(name, arguments, channel):
	for g in globals():
		m = globals()[g]
		if g.startswith("cmds_") and type(m) == type(__builtins__):
			for c in m.cmds:
				if c == arg:
					await m.cmds[c][1](arguments, client, channel)

client.run(open("token").read())
