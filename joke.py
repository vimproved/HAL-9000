async def open_pbd(arguments, bot, channel, message):
	if "pod bay doors" in arguments.lower():
		raise Exception()
cmds = {"open": ("Opens things, like pod bay doors.", open_pbd)}
desc = "Funny/joke commands."
