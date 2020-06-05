import random
async def roll_dice(arguments, bot, channel):
	total = 0
	crits = 0
	critf = 0
	for die in arguments.split():
		if 'd' not in die:
			total += int(die)
			continue
		num, sides = die.split('d')
		if num == '':
			num = '1'
		rolls = [random.randint(1, int(sides)) for n in range(int(num))]
		if sides == '20':
			crits += rolls.count(20)
			critf += rolls.count(1)
		total += sum(rolls)
	await channel.send("Result: "+str(total)+"\n***CRITICAL SUCCESS!***"*crits+"\n***CRITICAL FAILURE!***"*critf)
cmds = {"roll":("Rolls dice.\nSeparate dice to add up with spaces.\nThese are all valid dice: 'd6' '1d6' '5'", roll_dice)}
desc = "An advanced dice roller, with a basic placeholder for now."
