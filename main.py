import legacy as cmds_legacy
import rngesus as cmds_rngesus
import dnd as cmds_dnd
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
		if text == "help":
			s = "Command sets: "
			for g in globals():
				m = globals()[g]
				if g.startswith("cmds_") and type(m) == type(__builtins__):
					s += "\n`%s`: %s" % (g[5:], m.desc)
			s += "\nTry `"+prefix+"help <command set>` to list commands in a set."
			await message.channel.send(s)
			return
		try:
			await run_command(text.split()[0], ' '.join(text.split()[1:]), message.channel)
		except Exception as e:
			print(e)
			await message.channel.send("I'm sorry, <@%d>, I'm afraid I can't do that." % message.author.id)
async def run_command(name, arguments, channel):
	for g in globals():
		m = globals()[g]
		if g.startswith("cmds_") and type(m) == type(__builtins__):
			if name == "help" and arguments == g[5:]:
				s = "Commands in set `%s`:" % (g[5:])
				for c in m.cmds:
					s += "\n`%s` from `%s`" % (c, g[5:])
				s += "\nTry `"+prefix+"help <command set> <command>` for individual command help."
				await channel.send(s)
				return
			for c in m.cmds:
				if name == "help" and arguments.split()[0] == g[5:] and arguments.split()[1] == c:
					await channel.send("`%s` from `%s`: %s" % (c, g[5:], m.cmds[c][0]))
				elif c == name:
					await m.cmds[c][1](arguments, client, channel)

client.run(open("token").read())
