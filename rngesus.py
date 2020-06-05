async def roll_dice(arguments, bot, channel):
	await channel.send("You rolled a 1")
cmds = {"roll":("Rolls dice.", roll_dice)}
