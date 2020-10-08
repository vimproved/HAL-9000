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
        embed_var = discord.Embed(color=0xff0008)
        embed_var.set_image(url="https://crafatar.com/renders/body/" + profile["id"] + ".png")
        embed_var.add_field(name="__Name__", value=profile["name"], inline=False)
        embed_var.add_field(name="__UUID__", value=profile["id"], inline=False)
        embed_var.add_field(name="__Skin__", value=profile["name"]+"'s skin:")
        await ctx.send(embed=embed_var)
