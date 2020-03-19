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

    @commands.command()
    async def register(self,ctx):
    	"""Opens up a bank account for the user."""
    	if len(data.search(User.id == ctx.author.id)) != 0:
    		return await ctx.send("You already have a bank account registered.")
    	data.insert({"id":ctx.author.id,"cash":500,"balance":0,"lastJobTime":None,"lastCrimeTime":None})
    	await ctx.send(f"<@{ctx.author.id}> registered successfully! Your starting balance is **¥500**")

def setup(bot):
    bot.add_cog(LawBot(bot))     
