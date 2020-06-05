import requests
from fuzzywuzzy import process
async def dnd_test(arguments, bot, channel):
	await channel.send("HORSE")
async def dnd_get(arguments, bot, channel):
	endpoint, *args = arguments.split()
	name = ' '.join(args[:args.index('/')])
	vals = args[args.index('/')+1:]
	of_that_type = requests.get("https://www.dnd5eapi.co/api/"+endpoint).json()
	real_name = process.extractOne(name, of_that_type['results'])[0]
	await channel.send("Data for `%s`: " % real_name['name'])
	url = real_name['url']
	data = requests.get("https://www.dnd5eapi.co"+url).json()
	props = list(data.keys())
	for val in vals:
		real_val = process.extractOne(val, props)[0]
		if not real_val: 
			await channel.send("`%s`: *not defined*" % val)
		else:
			await channel.send("`%s`: %s" % (real_val, str(data[real_val])))
cmds = {"dnd-test": ("test dnd command", dnd_test),
	"dnd-get": ("Gets data from the D&D5e API.\nUsage: `dnd-get <endpoint type> <name (can be more than one word)> / <types of data you want to get separated by spaces>`\nAvailable endpoint types:\n`ability-scores`, `classes`, `conditions`, `damage-types`, `equipment-categories`, `equipment`, `features`, `languages`, `magic-schools`, `monsters`, `proficiencies`, `races`, `skills`, `spellcasting`, `spells`, `starting-equipment`, `subclasses`, `subraces`, `traits`, `weapon-properties`.\nExample: `dnd-get spell Acid Arrow / level`\nUses a fuzzy search algorithm to find the object/property name closest to what you typed.", dnd_get)}
desc = "Commands to assist with D&D."
