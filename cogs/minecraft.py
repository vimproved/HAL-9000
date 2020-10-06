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
        base64textures = profile["properties"][0]["value"]
        base64_bytes = base64textures.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        textures = message_bytes.decode('ascii')
        textures = json.loads(textures)
        skinurl = textures["textures"]["SKIN"]["url"]
        embed_var = discord.Embed(color=0xff0008)
        embed_var.set_image(url=skinurl)
        embed_var.add_field(name="__Name__", value=profile["name"], inline=False)
        embed_var.add_field(name="__UUID__", value=profile["id"], inline=False)
        embed_var.add_field(name="__Skin__", value=profile["name"]+"'s skin:")
        await ctx.send(embed=embed_var)
