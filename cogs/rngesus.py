from discord.ext import commands
import random


def setup(bot):
    bot.add_cog(RNGesus(bot))


class RNGesus(commands.Cog):
    """Commands that generate random results."""
    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        pass

    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin. Ignores arguments."""
        await ctx.send(random.choice(["Heads!"] * 50 + ["Tails!"] * 50 + ["The coin landed on the side!!"]))

    @commands.command()
    async def roll(self, ctx, args):
        """Rolls dice of any quantity and size.
        ```//roll XdX```"""
        total = 0
        crits = 0
        critf = 0
        for die in args.split():
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
        await ctx.send(
            "Result: " + str(total) + "\n***CRITICAL SUCCESS!***" * crits + "\n***CRITICAL FAILURE!***" * critf)

    @commands.command()
    async def choose(self, ctx, *args):
        """Chooses between multiple things if you can't decide yourself.
        ```//choose <args>```"""
        await ctx.send(random.choice(args))
