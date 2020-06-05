import requests
async def dnd_test(arguments, bot, channel):
	await channel.send("HORSE")
cmds = {"dnd-test": ("test dnd command", dnd_test)}
desc = "Commands to assist with D&D."
