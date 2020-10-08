from discord.ext import commands
import requests
import discord


def setup(bot):
    bot.add_cog(Minecraft(bot))


class Minecraft(commands.Cog):
    """Commands relating to Minecraft."""
    def __init__(self, bot):
        self.bot = bot

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
        """Gets the skin file of a player.
        ```//mcskin <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Skin", description="Skin for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32&overlay")
        embed_var.set_image(url="https://crafatar.com/skins/" + uuid + ".png?overlay")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mchead(self, ctx, args):
        """Gets a render of a user's head.
        ```//mchead <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Head", description="Head render for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32&overlay")
        embed_var.set_image(url="https://crafatar.com/renders/head/" + uuid + ".png?overlay")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mccape(self, ctx, args):
        """Gets a user's cape. Note: Cape must be mojang supported cape.
        ```//mccape <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Cape", description="Cape for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32&overlay")
        embed_var.set_image(url="https://crafatar.com/cape/" + uuid + ".png?default=https://media.discordapp.net"
                                                                      "/attachments/717043951835676755"
                                                                      "/763783489107001394/Untitled.png")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def hypixel(self, ctx, *args):
        """Gets Hypixel stats for a player.
        ```//hypixel <IGN>: Gets general hypixel stats.
        //hypixel <IGN> <game>: Gets stats for a specific game.
        ```"""
        player = args[0]
        try:
            field = args[1]
        except IndexError:
            field = None
        if field == "Skyblock":
            pass
        else:
            uuidfromign = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()
            uuid = uuidfromign["id"]
            stats = requests.get(f"https://api.slothpixel.me/api/players/{player}").json()
            embed = discord.Embed(color=0xff0008, title=player, description=f"Hypixel stats for {player}.")
            embed.set_image(url="https://crafatar.com/renders/body/" + uuid + ".png?overlay")
            embed.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?overlay")
            if stats["online"]:
                status = "Online"
            else:
                status = "Offline"
            embed.add_field(name="Status", value=status, inline=True)
            embed.add_field(name="Rank", value=stats["rank"].replace("_PLUS", "+"), inline=True)
            embed.add_field(name="Level", value=stats["level"], inline=True)
            embed.add_field(name="Hypixel EXP", value=stats["exp"], inline=True)
            embed.add_field(name="Karma", value=stats["karma"], inline=True)
            embed.add_field(name="Achievement Points", value=stats["achievement_points"], inline=True)
            socials = stats["links"]
            embed.add_field(name="Social Media", value=f"Twitter: {socials['TWITTER']}\nYoutube: {socials['YOUTUBE']}\n"
                                                       f"Instagram: {socials['INSTAGRAM']}\nTwitch: {socials['TWITCH']}"
                                                       f"\nDiscord: {socials['DISCORD']}\nHypixel Forums: "
                                                       f"{socials['HYPIXEL']}")
            await ctx.send(embed=embed)
