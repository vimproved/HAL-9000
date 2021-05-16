from discord.ext import commands
import discord
from discord.ext.commands import CommandRegistrationError, TextChannelConverter, RoleConverter, command
from PIL import Image
import random
import itertools
import toml


def setup(bot):
    bot.add_cog(Utility(bot))


class Utility(commands.Cog):
    """Commands for server / bot utility."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, args=""):
        """Help command.

        Syntax:
        `//help <command>`"""
        cmds = [i.name for i in self.bot.commands]
        cmds_lower = [i.lower() for i in cmds]
        if args.lower() in cmds_lower:
            cmd = self.bot.get_command(cmds[cmds_lower.index(args.lower())])
            embed_var = discord.Embed(color=0xff0008, title=cmd.name, description=cmd.help + "\n")
            embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
        else:
            embed_var = discord.Embed(color=0xff0008, title="Help Menu", description="HAL-9000 is a multipurpose discord bot made by vi#7402. This is a list of commands. Do `//help <command>` for information on a command.")
            embed_var.set_author(name="HAL-9000", icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
            for cog in self.bot.cogs.values():
                embed_var.add_field(name=cog.qualified_name, value="`"+"`, `".join([i.name for i in cog.get_commands()])+"`", inline=False)
        await ctx.send(embed=embed_var)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def config(self, ctx, *args):
        """Configures the local server settings of HAL.
        Requires administrator.

        Subcommands:
        `logchannel <channel>`: Sets the channel for HAL to send mod log messages in (HAL Errors, message deletions)
        `systemchannel <channel>`: Sets the channel for HAL to send member joins/leaves in.
        `colorposition <integer>`: Sets the role list position of new color roles.
        `read`: Sends the config settings.

        Syntax:
        `//config <subcommand> <value>`"""
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(ctx.guild.id)]
        except KeyError:
            config = {}
        if args[0] == "systemchannel":
            systemchannel = await TextChannelConverter().convert(ctx, args[1])
            config.update({"systemchannel": systemchannel.id})
        elif args[0] == "logchannel":
            logchannel = await TextChannelConverter().convert(ctx, args[1])
            config.update({"logchannel": logchannel.id})
        elif args[0] == "colorposition":
            position = (len(ctx.guild.roles) - int(args[1])) + 1
            config.update({"colorposition": position})
        elif args[0] == "read":
            await ctx.send("Config file:\n" + toml.dumps(config))
        else:
            await ctx.send("Please select a valid configuration option.")
        globalconfig.update({str(ctx.guild.id): config})
        open("config.toml", "w").write(toml.dumps(globalconfig))
        await ctx.send("Configuration set.")

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot and displays the time in milliseconds between your message being sent and the ping message
        being sent.
        Ignores arguments. """
        m = await ctx.send("Pong?")
        latency = m.created_at - ctx.message.created_at
        await m.edit(content=f"Pong in {int(latency.microseconds / 1000)} ms! :ping_pong:")

    @commands.command()
    async def invite(self, ctx):
        """Sends an oath2 link for HAL.
        Ignores arguments."""
        await ctx.send("https://discord.com/api/oauth2/authorize?client_id=717042126776434728&permissions=8&scope=bot")

    @commands.command()
    async def repo(self, ctx):
        """Sends the link to the GitHub repo for HAL.
        Ignores arguments."""
        await ctx.send("https://github.com/Paradigmmmm/HAL-9000")

    @commands.command()
    async def color(self, ctx, *args):
        """Commands relating to the color system.

        Subcommands:
        `list`: Lists all color names.
        `set <color name>`: Sets your color to the specified color.
        `preview <name>`: Sends an image containing the color of the role.
        `add <hex code> <color name>`: Adds a color with the specified hex codes (Requires manage roles).
        `delete <name/number on list>`: Deletes a color (Requires manage roles).
        `addexisting <role>`: Adds an existing role to the color list. (Requires manage roles)

        Syntax:
        `//color <subcommand> <arguments>`"""
        subcmd = args[0]
        args = args[1:]
        config = toml.loads(open("config.toml", "rt").read())
        if subcmd == "add":
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("Invalid permissions.")
                return
            color = args[0]
            if "#" in color:
                color = color.replace("#", "")
            try:
                color = discord.Colour(int(color, 16))
            except ValueError:
                await ctx.send("Invalid color.")
                return
            name = ' '.join(args[1:])
            try:
                colorposition = config["colorposition"]
            except KeyError:
                await ctx.send("You haven't set up a position to move colors to in this server yet. Do //config "
                               "colorposition to set up a position. For now I've created the role at the bottom of "
                               "the list.")
                colorposition = 1
            try:
                colorrole = await ctx.guild.create_role(name=name, colour=color, reason="Automated colour addition.")
                await ctx.guild.edit_role_positions({colorrole: colorposition})
                await ctx.send("Color created.")
            except discord.Forbidden:
                await ctx.send("HAL-9000 does not have the manage roles permission.")
                return
            except discord.InvalidArgument:
                await ctx.send("Invalid args.")
                return
            except discord.HTTPException:
                await ctx.send("An unexpected exception occurred. Try again later.")
                return
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            colors.append(colorrole.id)
            config.update({"colors": colors})
            open("config.toml", "w").write(toml.dumps(config))
        elif subcmd == "list":
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            colorroles = []
            for x in colors:
                color = ctx.guild.get_role(x)
                print(type(color))
                if type(color) != discord.role.Role:
                    colors.remove(x)
                else:
                    colorroles.append(color)
            text = ""
            for x in colorroles:
                text = text + "\n**" + str(colorroles.index(x) + 1) + ":** " + x.name
            await ctx.send(text + "\n\n *Do* `//color preview <color>` *for a preview of the color!*")
            config.update({"colors": colors})
            open("config.toml", "w").write(toml.dumps(config))
        elif subcmd == "delete":
            if not ctx.author.guild_permissions.manage_roles:
                raise discord.ext.commands.MissingPermissions
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            answer = ' '.join(args)
            try:
                answer = int(answer) - 1
                answer = colors[answer]
                role = await RoleConverter().convert(ctx, str(answer))
                colors.remove(answer)
                await role.delete()
            except ValueError:
                try:
                    answer = await RoleConverter().convert(ctx, answer)
                    await answer.delete()
                except commands.errors.BadArgument:
                    await ctx.send("Invalid color.")
                    return
                if answer.id not in colors:
                    await ctx.send("Invalid color in config list.")
                    return
                print(colors)
                print(answer.id)
                colors.remove(answer.id)
            except IndexError:
                await ctx.send("There is no color at that position.")
                return
            await ctx.send("Color deleted successfully.")
            config.update({"colors": colors})
            open("config.toml", "w").write(toml.dumps(config))
        elif subcmd == "forcedelete":
            if not ctx.author.guild_permissions.manage_roles:
                raise discord.ext.commands.MissingPermissions
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            answer = args[0]
            try:
                colors.pop(int(answer))
            except ValueError:
                await ctx.sednd("Please enter an integer.")
                return
            await ctx.send("Color removed.")
            config.update({"colors": colors})
            open("config.toml", "w").write(toml.dumps(config))
        elif subcmd == "addexisting":
            if not ctx.author.guild_permissions.manage_roles:
                raise discord.ext.commands.MissingPermissions
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            answer = ' '.join(args)
            try:
                colorrole = await RoleConverter().convert(ctx, answer)
            except commands.errors.BadArgument:
                await ctx.send("Invalid role.")
                return
            colors.append(colorrole.id)
            config.update({"colors": colors})
            open("config.toml", "w").write(toml.dumps(config))
            await ctx.send("Done!")
        elif subcmd == "preview":
            color = ' '.join(args)
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            colorc = []
            for x in colors:
                x = await RoleConverter().convert(ctx, str(x))
                x = str(x.name)
                colorc.append(x)
            if color in colorc:
                color = await RoleConverter().convert(ctx, str(colors[colorc.index(color)]))
                color = str(color.color)
            if "#" in color:
                color = color.replace("#", "")
            try:
                print(color)
                image = Image.new('RGB', (256, 256), color=tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)))
            except ValueError:
                await ctx.send("Invalid color name/hex color.")
                return
            image.save("previewimg.png")
            await ctx.send("Here is the color preview:", file=discord.File(open("previewimg.png", "rb")))
        elif subcmd == "set":
            args = ' '.join(args)
            try:
                colors = config["colors"]
            except KeyError:
                colors = []
            colorsthing = []
            colorsl = []
            for colorrrr in colors:
                colorsthing.append((ctx.guild.get_role(colorrrr)).name)
                colorsl.append((ctx.guild.get_role(colorrrr)).name.lower())
            if args.lower() in colorsl:
                try:
                    colorrole = await RoleConverter().convert(ctx, colorsthing[colorsl.index(args.lower())])
                except ValueError:
                    colorrole = await RoleConverter().convert(ctx, args)
            else:
                await ctx.send("That is not a valid color.")
                return
            if colorrole.id not in colors:
                await ctx.send("That is not a valid color.")
                return
            for x in ctx.author.roles:
                if x.id in colors:
                    await ctx.author.remove_roles(x)
            await ctx.author.add_roles(colorrole)
            await ctx.send("Color set to " + colorrole.name + "!")

    @commands.command()
    async def coinflip(self, ctx):
        """Flips a coin.
        Ignores arguments."""
        await ctx.send(random.choice(["Heads!"] * 50 + ["Tails!"] * 50 + ["The coin landed on the side!!"]))

    @commands.command()
    async def roll(self, ctx, args):
        """Rolls dice of any quantity and size.

        Syntax:
        `//roll <integer>d<integer>`"""
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
            num = int(num)
            sides = int(sides)
            if num >= 100:
                await ctx.send("That number is too large. To prevent crashes, I have exited the command.")
                return
            rolls = [random.randint(1, sides) for _ in itertools.repeat(None, num)]
            if sides == '20':
                crits += rolls.count(20)
                critf += rolls.count(1)
            total += sum(rolls)
        await ctx.send(
            "Result: " + str(total) + "\n***CRITICAL SUCCESS!***" * crits + "\n***CRITICAL FAILURE!***" * critf)

    @commands.command()
    async def choose(self, ctx, *args):
        """Chooses between multiple things if you can't decide yourself.

        Syntax:
        `//choose <arg1> <arg2> <arg3> ...`"""
        await ctx.send(random.choice(args), allowed_mentions=discord.AllowedMentions(everyone=False, users=False,
                                                                                     roles=False))
    @commands.command()
    async def alias(self, ctx, newname, oldname, *aliasargs):
        """Aliases one command to another. Optionally adds fixed arguments to the command; use $$ to insert the normal argument list.
        Example: //alias mycommand choose no $$ yes, then doing //mycommand maybe will choose between no, yes and maybe.
        This is just as if you had run //choose no maybe yes.

        Syntax:
        `//alias <newname> <oldname> [aliasargs...]`"""
        if ctx.guild is None:
            await ctx.send("You must be in a guild for this.")
            return
        try:
            globalconfig = toml.loads(open("config.toml", "rt").read())
        except KeyError:
            globalconfig = {}
        try:
            config = globalconfig[str(ctx.guild.id)]
        except KeyError:
            config = {}
        
        cmd = self.bot.get_command(oldname)
        if cmd is None:
            await ctx.send("No existing command with that name.")
            return
        if not config.get("aliases"):
            config["aliases"] = []
        await self.register_alias(ctx.guild.id, cmd, newname, *aliasargs)
        config["aliases"].append((oldname, newname, *aliasargs,))

        globalconfig.update({str(ctx.guild.id): config})
        open("config.toml", "w").write(toml.dumps(globalconfig))

    async def register_alias(self, guildid, cmd, newname, *aliasargs):
        async def coro(actx, *aargs):
            if actx.guild is None or actx.guild.id != guildid: 
                return
            nargs = []
            for a in aliasargs:
                if a == "$$":
                    nargs += aargs
                else:
                    nargs.append(a)
            actx.command = cmd
            actx.args = nargs
            #await cmd(actx, *nargs)
            await self.bot.invoke(actx)
        coro.__doc__ = ["ALIAS", guildid, cmd.name + " " + ' '.join(aliasargs)]
        try:
            newcmd = self.bot.command(newname, hidden=True)(coro)
        except CommandRegistrationError:
            self.bot.remove_command(newname)
            newcmd = self.bot.command(newname, hidden=True)(coro)

    @commands.command()
    async def whatis(self, ctx, cmdname):
        """What is a particular command: an alias or not?
        
        Syntax:
        `//whatis <cmdname>`
        """
        cmd = self.bot.get_command(cmdname)
        if cmd is None:
            await ctx.send(cmdname + " is: nonexistent")
        elif cmd.callback.__doc__[0] == "ALIAS" and ctx.guild is not None and cmd.callback.__doc__[1] == ctx.guild.id:
            await ctx.send(cmdname + " is: an alias of //"+ cmd.callback.__doc__[2])
        elif cmd.callback.__doc__[0] == "ALIAS":
            await ctx.send(cmdname + " is: nonexistent")
        else:
            await ctx.send(cmdname + " is: builtin")

    @commands.command()
    async def rmalias(self, ctx, aliasname):
        """Removes an existing alias.

        Syntax:
        `//rmalias <aliasname>`"""
        cmd = self.bot.get_command(aliasname)
        if cmd.callback.__doc__[0] == "ALIAS" and ctx.guild is not None and cmd.callback.__doc__[1] == ctx.guild.id:
            self.bot.remove_command(aliasname)
        else:
            await ctx.send("That's not an alias.")

    @commands.command()
    async def echo(self, ctx, *stuff):
        await ctx.send(' '.join(stuff))
