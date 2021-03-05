from discord.ext import commands
import requests
import discord


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
        """Searches https://icanhazdadjoke.com for a dadjoke. Put no args or "random" for a random joke.
        ```//dadjoke <joke>```"""
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
        """!BWOOP BWOOP! Sends an alert 5 times.
        ```//alert <text>```"""
        alert_text = eval('"' + ' '.join(args).upper() + '"')
        for n in range(5): await ctx.send(":rotating_light: ***bwoop bwoop*** :rotating_light: " + alert_text + " ALERT :rotating_light: ***bwoop bwoop*** :rotating_light:", allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))

    @commands.command()
    async def mcprofile(self, ctx, args):
        """Gets a Minecraft profile from IGN.
        ```//mcprofile <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        profile = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + uuidfromign["id"]).json()
        embed_var = discord.Embed(color=0xff0008, title=args)
        embed_var.set_image(url="https://crafatar.com/renders/body/" + profile["id"] + ".png?overlay")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + profile["id"] + ".png?overlay")
        embed_var.add_field(name="__Name__", value=profile["name"], inline=False)
        embed_var.add_field(name="__UUID__", value=profile["id"], inline=False)
        embed_var.add_field(name="__Skin__", value=profile["name"]+"'s skin:")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mcskin(self, ctx, args):
        """Gets the Minecraft skin file of a player.
        ```//mcskin <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Skin", description="Skin for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32&overlay")
        embed_var.set_image(url="https://crafatar.com/skins/" + uuid + ".png?overlay")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mchead(self, ctx, args):
        """Gets a render of a Minecraft user's head.
        ```//mchead <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Head", description="Head render for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32&overlay")
        embed_var.set_image(url="https://crafatar.com/renders/head/" + uuid + ".png?overlay")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mccape(self, ctx, args):
        """Gets a user's Minecraft cape. Note: Cape must be mojang supported cape.
        ```//mccape <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Cape", description="Cape for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32&overlay")
        embed_var.set_image(url="https://crafatar.com/cape/" + uuid + ".png?default=https://media.discordapp.net"
                                                                      "/attachments/717043951835676755"
                                                                      "/763783489107001394/Untitled.png")
        await ctx.send(embed=embed_var)
