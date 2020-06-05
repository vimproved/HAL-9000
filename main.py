import legacy as cmds_legacy
import rngesus as cmds_rngesus
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
		try:
			await run_command(text.split()[0], ' '.join(text.split()[1:]), message.channel)
		except:
			await message.channel.send("I'm sorry, <@%d>, I'm afraid I can't do that." % message.author.id)
async def run_command(name, arguments, channel):
	for g in globals():
		m = globals()[g]
		if g.startswith("cmds_") and type(m) == type(__builtins__):
			if name == "help" and arguments == g[5:]:
				await channel.send("`%s`: %s" % (g[5:], g.desc))
				return
			for c in m.cmds:
				if name == "help" and arguments.split()[0] == g[5:] and arguments.split()[1] == c:
					await channel.send("`%s` from `%s`: %s" % (g[5:], c, m.cmds[c][0]))
				elif c == name:
					await m.cmds[c][1](arguments, client, channel)

client.run(open("token").read())
