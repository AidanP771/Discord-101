import discord
from discord.ext import commands,tasks

from tinydb import TinyDB, Query

data = TinyDB("data/LawData.json")
User = Query()

class LawBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def hi(self,ctx):
        await ctx.send("Hi")

def setup(bot):
    bot.add_cog(LawBot(bot))     
