from discord.ext import commands
import requests
import discord
import random
import emojis


def setup(bot):
    bot.add_cog(Fun(bot))


class Fun(commands.Cog):
    """Fun commands!"""

    def __init__(self, bot):
        self.bot = bot

    def setup(self):
        pass

    @commands.command()
    async def dadjoke(self, ctx, args="random"):
        """Searches https://icanhazdadjoke.com for a dadjoke or sends a random dadjoke with no arguments.

        Syntax:
        `//dadjoke <keyword>`: Searches for a keyword."""
        try:
            if args.lower() == "random":
                dadjoke = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"})
            else:
                dadjoke = requests.get("https://icanhazdadjoke.com/search", params={"term": args, "limit": 1}, headers={"Accept": "text/plain"})
            await ctx.send(dadjoke.content.decode('utf-8'))
        except discord.HTTPException:
            await ctx.send("Hi " + args + ", I'm dad!", allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))

    @commands.command()
    async def alert(self, ctx, *args):
        """!BWOOP BWOOP! Sends an alert with sirens blaring!

        Syntax:
        `//alert <text>`"""
        alert_text = eval('"' + ' '.join(args).upper() + '"')
        if ctx.guild.id == 300718768747970560:
            for i in range (0, 5):
                await ctx.send(":rotating_light: ***bwoop bwoop*** :rotating_light: " + alert_text + " ALERT :rotating_light: ***bwoop bwoop*** :rotating_light:", allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
        else:
            await ctx.send(":rotating_light: ***bwoop bwoop*** :rotating_light: " + alert_text + " ALERT :rotating_light: ***bwoop bwoop*** :rotating_light:", allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))

    @commands.command()
    async def mc(self, ctx, *args):
        """Various Minecraft related functions.
        Subcommands:
        `profile <IGN>`: Sends IGN, UUID, and a skin render of a player.
        `skin <IGN>`: Sends the skin file of a player.
        `head <IGN>`: Sends a head render of a player.

        Syntax:
        `//mc <subcommand> <args>`
        """
        subcmd = args[0]
        args = args[1]
        if subcmd == "profile":
            uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/"+args).json()
            profile = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/"+uuidfromign["id"]).json()
            embed_var = discord.Embed(color=0xff0008, title=args)
            embed_var.set_image(url="https://crafatar.com/renders/body/" + profile["id"] + ".png?overlay")
            embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + profile["id"] + ".png?overlay")
            embed_var.add_field(name="__Name__", value=profile["name"], inline=False)
            embed_var.add_field(name="__UUID__", value=profile["id"], inline=False)
            embed_var.add_field(name="__Skin__", value=profile["name"] + "'s skin:")
            embed_var.set_author(name="HAL-9000", url="https://namemc.com/profile/"+args,  icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
            await ctx.send(embed=embed_var)
        elif subcmd == "skin":
            uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/"+args).json()
            uuid = uuidfromign["id"]
            embed_var = discord.Embed(color=0xff0008, title=args+"'s Skin", description="Skin for "+args+":")
            embed_var.set_thumbnail(url="https://crafatar.com/avatars/"+uuid+".png?size=32&overlay")
            embed_var.set_image(url="https://crafatar.com/skins/"+uuid+".png?overlay")
            embed_var.set_author(name="HAL-9000", url="https://namemc.com/profile/"+args, icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
            await ctx.send(embed=embed_var)
        elif subcmd == "head":
            uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/"+args).json()
            uuid = uuidfromign["id"]
            embed_var = discord.Embed(color=0xff0008, title=args+"'s Head", description="Head render for "+args+":")
            embed_var.set_thumbnail(url="https://crafatar.com/avatars/"+uuid+".png?size=32&overlay")
            embed_var.set_image(url="https://crafatar.com/renders/head/"+uuid+".png?overlay")
            embed_var.set_author(name="HAL-9000", url="https://namemc.com/profile/"+args,  icon_url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fchurchm.ag%2Fwp-content%2Fuploads%2F2015%2F12%2FHAL9000_iconic_eye.png&f=1&nofb=1")
            await ctx.send(embed=embed_var)
        else:
            raise commands.errors.MissingRequiredArgument

    @commands.command()
    async def emojify(self, ctx, *args):
        """Emojifies text.
        
Syntax:
        //emojify <args>"""
        response = ""
        for i in args:
            i = i + " " + random.choice(list(emojis.db.get_emoji_aliases().values()))
            response = response + i + " "
        try:
            await ctx.send(response)
        except discord.errors.HTTPException:
            await ctx.send("Message too long.")

    @commands.command()
    async def emojify2(self, ctx, *args):
        """Emojifies text.
        
Syntax:
        //emojify <args>"""
        output = ""
        text = ' '.join(args)
        emojiList = sorted([a[1:-1] for a in list(emojis.db.get_emoji_aliases().keys())])[::-1]
        while text:
            recent = None
            for emoji in emojiList:
                if text.startswith(emoji):
                    recent = ':' + emoji + ': '
                    text = text[len(emoji):]
                    break
            else:
                if text[0].lower() not in 'qwertyuiopasdfghjklxcvbnm':
                    recent = text[0]
                else:
                    recent = ':regional_indicator_' + text[0].lower() + ': '
                text = text[1:]
            if len(output) + len(emojis.encode(recent)) > 2000:
                await ctx.send(output)
                output = ""
            output += emojis.encode(recent)
        await ctx.send(output)

