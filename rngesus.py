async def roll_dice(arguments, bot, channel):
	await channel.send("rngesus has smited you")
cmds = {"roll":("Rolls dice.", roll_dice)}
