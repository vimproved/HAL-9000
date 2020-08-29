import legacy as cmds_legacy
import rngesus as cmds_rngesus
import dnd as cmds_dnd
import joke as cmds_joke
import botlog as cmds_botlog
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
			await run_command(text.split()[0], ' '.join((text.split()+[''])[1:]), message.channel, await perm_level(message.author), message)
		except Exception as e:
			print(e)
			await message.channel.send(("I'm sorry, <@%d>, I'm afraid I can't do that." % message.author.id)+str(e))
perm_roles = ['user', 'Contributor', 'Admin']
async def perm_level(user):
	perm = 0
	for role in user.roles:
		if role.name in perm_roles:
			perm = max(perm, perm_roles.index(role.name))
	return perm
async def run_command(name, arguments, channel, perm, message):
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
				if name == "help" and (arguments.split()+[''])[0] == g[5:] and (arguments.split()+['',''])[1] == c:
					await channel.send("`%s` from `%s`: %s" % (c, g[5:], m.cmds[c][0]))
				elif c == name:
					if len(m.cmds[c]) > 2:
						req_perm = m.cmds[c][2]
						if perm < req_perm:
							await channel.send("Sorry, this command needs %s permissions; you only have %s permissions." % (perm_roles[req_perm], perm_roles[perm]))
							return
					await m.cmds[c][1](arguments, client, channel, message)

client.run(open("token").read())
