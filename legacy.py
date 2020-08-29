from datetime import datetime
import random
# To get descriptions: cmds[command][0]
# To run: cmds[command][1](arguments_as_a_string, bot_object, requested_channel)
async def display_time(args, bot, channel, message):
	"""Command for displaying time. Ignores arguments."""
	await channel.send(datetime.now().strftime("%H:%M:%S on %a, %B %d, %Y"))
async def flip_coin(args, bot, channel, message):
	"""Command for flipping a coin. Ignores arguments."""
	await channel.send(random.choice(["Heads!"]*50 + ["Tails!"]*50 +["The coin landed on the side!!"]))
async def ping_msg(args, bot, channel, message):
	"""Pings the bot. Ignores arguments."""
	await channel.send("Pong! :ping_pong:")
cmds = {"time": ("Displays the time.", display_time),
	"ping": ("Responds with a pong message.", ping_msg),
	"coinflip": ("Flips a coin.", flip_coin)}
#i am a gnome
desc = "Old commands from previous iterations of the bot."
