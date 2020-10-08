from discord.ext import commands
import base64
import requests
import discord
import json


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
        embed_var.set_image(url="https://crafatar.com/renders/body/" + profile["id"] + ".png")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + profile["id"] + ".png")
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
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32")
        embed_var.set_image(url="https://crafatar.com/skins/" + uuid + ".png")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mchead(self, ctx, args):
        """Gets a render of a user's head.
        ```//mchead <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Head", description="Head render for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32")
        embed_var.set_image(url="https://crafatar.com/renders/head/" + uuid + ".png")
        await ctx.send(embed=embed_var)

    @commands.command()
    async def mccape(self, ctx, args):
        """Gets a user's cape. Note: Cape must be mojang supported cape.
        ```//mccape <IGN>```"""
        uuidfromign = requests.get("https://api.mojang.com/users/profiles/minecraft/" + args).json()
        uuid = uuidfromign["id"]
        embed_var = discord.Embed(color=0xff0008, title=args + "'s Cape", description="Cape for " + args + ":")
        embed_var.set_thumbnail(url="https://crafatar.com/avatars/" + uuid + ".png?size=32")
        embed_var.set_image(url="https://crafatar.com/cape/" + uuid + ".png?default=https://media.discordapp.net"
                                                                      "/attachments/717043951835676755"
                                                                      "/763783489107001394/Untitled.png")
        await ctx.send(embed=embed_var)
