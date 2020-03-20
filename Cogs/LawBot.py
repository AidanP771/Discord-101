import discord
from discord.ext import commands,tasks

from tinydb import TinyDB, Query

import random
import arrow

data = TinyDB("data/LawData.json")
User = Query()

class LawBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    '''
    @commands.command()
    async def hi(self,ctx):
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        info = data.search(User.id == ctx.author.id)[0]
        await ctx.send(embed=em)'''

    @commands.command()
    async def register(self,ctx):
        """Opens up a bank account for the user."""
        if len(data.search(User.id == ctx.author.id)) != 0:
            return await ctx.send("You already have a bank account registered.")
        data.insert({"id":ctx.author.id,"cash":500,"balance":0,"lastJobTime":None,"lastCrimeTime":None})
        em = discord.Embed()
        em.title = "**New Registration**"
        em.description = f"<@{ctx.author.id}> registered successfully! Your starting balance is **¥500**"
        em.color = 0xffff00
        await ctx.send(embed=em)

    @commands.command()
    async def balance(self,ctx):
        """Displays the balance of the user's cash and bank account."""
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        em.title = "Bank Balance <:cash:690343545730891836>"
        em.color = 0x00ff00
        user = data.search(User.id == ctx.author.id)[0]
        em.add_field(name="Cash",value=f"¥{user['cash']}",inline=False)
        em.add_field(name="Bank Balance",value=f"¥{user['balance']}",inline=False)
        await ctx.send(embed=em)

    @commands.command()
    async def work(self,ctx):
        """The user works to earn some cash."""
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        info = data.search(User.id == ctx.author.id)[0]
        if info["lastJobTime"] != None:
            if ((arrow.utcnow() - arrow.get(info["lastJobTime"])).seconds)/3600 < 24:
                em.title = "Error"
                future = arrow.get(info['lastJobTime']).shift(hours=24)
                nextIn = future.humanize(arrow.utcnow(), only_distance=True, granularity=["hour","minute"])
                em.description = f"You cannot use this command for another **{nextIn}**"
                em.color = 0xff0000
                return await ctx.send(embed=em)
        earnings = random.randint(20,1500)
        data.update({"cash":info['cash']+earnings,"lastJobTime":arrow.utcnow().timestamp},User.id == ctx.author.id)
        em.title = "Money Earned!"
        em.description = f"You worked hard and earned **¥{earnings}!**"
        em.color = 0x00ff00
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(LawBot(bot))
