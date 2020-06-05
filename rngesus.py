async def roll_dice(arguments, bot, channel):
	total = 0
	for die in arguments.split():
		if 'd' not in die:
			total += int(die)
		num, sides = die.split('d')
		if num == '':
			num = '1'
		total += sum([random.randint(1, int(sides)) for n in range(int(num))])
	await channel.send("Result: "+str(total))
cmds = {"roll":("Rolls dice.", roll_dice)}
