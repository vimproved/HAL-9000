from datetime import datetime
import random
# To get descriptions: cmds[command][0]
# To run: cmds[command][1](arguments_as_a_string, bot_object, requested_channel)
async def display_time(args, bot, channel):
	"""Command for displaying time. Ignores arguments."""
	await channel.send(datetime.now().strftime("%H:%M:%S on %a, %B %d, %Y"))
async def flip_coin(args, bot, channel):
	"""Command for flipping a coin. Ignores arguments."""
	await channel.send(random.choice(["Heads!"]*50 + ["Tails!"]*50 +["The coin landed on the side!!"]))
async def ping_msg(args, bot, channel):
	"""Pings the bot. Ignores arguments."""
	await channel.send("Pong! :ping_pong:")
cmds = {"time": ("Displays the time.", display_time),
	"flip": ("Flips a coin.", flip_coin),
	"ping": ("Responds with a pong message.", ping_msg)}
