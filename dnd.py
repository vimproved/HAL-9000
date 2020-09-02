import requests


cmds = {"dnd-get": ("Gets data from the D&D5e API.\nUsage: `dnd-get <endpoint type> <name (can be more than one word)> / <types of data you want to get separated by spaces>`\nAvailable endpoint types:\n`ability-scores`, `classes`, `conditions`, `damage-types`, `equipment-categories`, `equipment`, `features`, `languages`, `magic-schools`, `monsters`, `proficiencies`, `races`, `skills`, `spellcasting`, `spells`, `starting-equipment`, `subclasses`, `subraces`, `traits`, `weapon-properties`.\nExample: `dnd-get spells Acid Arrow / level`\nUses a fuzzy search algorithm to find the object/property name closest to what you typed.", dnd_get)}
desc = "Commands to assist with D&D."
