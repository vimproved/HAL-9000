from discord.ext import commands
from discord.ext.commands import TextChannelConverter, RoleConverter
from itertools import count
import discord


def setup(bot):
    bot.add_cog(Utility(bot))


class Utility(commands.Cog):
    """Utility commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args=""):
        args = args.lower()
        if args in self.bot.cogs.keys():
            args = self.bot.get_cog(args)
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__" + args.qualified_name + "__",
                                value=args.description, inline=False)
            for command in args.get_commands():
                embed_var.add_field(name="//" + command.name, value=command.help, inline=False)
        elif self.bot.get_command(args) in self.bot.commands:
            args = self.bot.get_command(args)
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__//" + args.name + "__", value=args.help, inline=False)
        else:
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="__Help Menu__",  value="HAL-9000 is a multipurpose discord bot made by vi#7158 "
                                                             "and rous#7120.\nThis is the help menu. Do //help ("
                                                             "command) for information on a single command. Do //help "
                                                             "(category) for information on a single category.", inline=False)
            for cog in self.bot.cogs.values():
                embed_var.add_field(name=cog.qualified_name, value=cog.description, inline=False)
        await ctx.send(embed=embed_var)

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot. Ignores arguments."""
        await ctx.send("Pong! :ping_pong:")

    @commands.command()
    @commands.has_role(318476343023239168)
    async def embedsend(self, ctx, *args):
        embed = discord.Embed(color=0xff0008)
        for x in count(1):
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="Name #" + str(x), value="Respond with the name of field #" + str(
                x) + ". If you are done type \"done\". If you would like to include a field with who sent this embed, "
                     "type \"userstamp\". The message will then be sent.    ",
                                inline=False)
            await ctx.send(embed=embed_var)
            response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
            while response.author != ctx.author:
                response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
            answer = response.content
            if answer == "done":
                break
            elif answer == "userstamp":
                embed.add_field(name="__Message Sent By__", value=ctx.author.mention, inline=False)
                break
            embed_var = discord.Embed(color=0xff0008)
            embed_var.add_field(name="Value #" + str(x), value="Respond with the name of field #" + str(x) + ".",
                                inline=False)
            await ctx.send(embed=embed_var)
            response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
            while response.author != ctx.author:
                response = await ctx.channel.fetch_message_fast(ctx.channel.last_message_id)
            answer2 = response.content
            embed.add_field(name=answer, value=answer2, inline=False)
        converter = TextChannelConverter()
        converter2 = RoleConverter()
        channel = await converter.convert(ctx, args[0])
        try:
            if args[1] == "everyone":
                await channel.send("@everyone\n", embed=embed)
            elif args[1] == "here":
                await channel.send("@here\n", embed=embed)
            else:
                rolemention = await converter2.convert(ctx, args[1])
                await channel.send(rolemention.mention + "\n", embed=embed)
        except Exception as e:
            await channel.send(embed=embed)
            await ctx.send("Note: exception was generated in attempt to send embed. Exception: " + str(e))
        await ctx.send("Message sent!")
