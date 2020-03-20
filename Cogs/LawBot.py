import discord
from discord.ext import commands,tasks

from tinydb import TinyDB, Query

import random
import arrow
import asyncio

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
            em = discord.Embed()
            em.title="**Error**"
            em.description = "You already have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
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
    async def deposit(self,ctx,amount=None):
        '''Deposits an amount of cash to the bank balance.'''
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        if amount == None:
            return await ctx.send("```.deposit amount\n\nDeposits an amount of cash to the bank balance.```")
        try:
            amount = int(amount)
        except:
            em.title = "**Error**"
            em.description = "That is not a valid amount."
            em.color = 0xff0000
            return await ctx.send(embed=em)       

        info = data.search(User.id == ctx.author.id)[0]
        if int(amount) > info["cash"]
            em.title = "**Error**"
            em.description = "You do not have that much cash."
            em.color = 0xff0000
            return await ctx.send(embed=em)

        em = discord.Embed()
        em.color = 0xff0000
        em.title = "Cash Deposited"
        data.update({"cash":info['cash']-int(amount),"balance":info['balance']+int(amount)},User.id == ctx.author.id)
        info = data.search(User.id == ctx.author.id)[0]
        em.add_field(name="Amount Deposited",value=f"¥{int(amount)}",inline=False)
        em.add_field(name="New Cash Value",value=f"¥{info['cash']}",inline=False)
        em.add_field(name="New Bank Balance",value=f"¥{info['balance']}",inline=False)
        await ctx.send(embed=em)

    @commands.command()
    async def withdraw(self,ctx,amount=None):
        '''Deposits an amount of cash to the bank balance.'''
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        if amount == None:
            return await ctx.send("```.withdraw amount\n\nWithdraws an amount of cash from the bank balance.```")
        try:
            amount = int(amount)
        except:
            em.title = "**Error**"
            em.description = "That is not a valid amount."
            em.color = 0xff0000
            return await ctx.send(embed=em)       

        info = data.search(User.id == ctx.author.id)[0]
        if int(amount) > info["balance"]
            em.title = "**Error**"
            em.description = "You do not have that much balance in your bank account."
            em.color = 0xff0000
            return await ctx.send(embed=em)

        em = discord.Embed()
        em.color = 0xff0000
        em.title = "Cash Withdrawn"
        data.update({"cash":info['cash']+int(amount),"balance":info['balance']-int(amount)},User.id == ctx.author.id)
        info = data.search(User.id == ctx.author.id)[0]
        em.add_field(name="Amount Withdrawn",value=f"¥{int(amount)}",inline=False)
        em.add_field(name="New Cash Value",value=f"¥{info['cash']}",inline=False)
        em.add_field(name="New Bank Balance",value=f"¥{info['balance']}",inline=False)
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
            lastUse = arrow.get(info["lastJobTime"])
            nextAvailUse = lastUse.shift(hours=24)
            if nextAvailUse.timestamp > arrow.utcnow().timestamp:
                em.title = "**Error**"
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

    @commands.command()
    async def roulette(self,ctx,numCol=None,bet=None):
        '''Spins a roulette.'''
        if numCol == None or bet == None:
            await ctx.send("```.roulette color/number bet\n\nSpins a roulette. The amount in the cash account is changed based on the outcome.```")
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        info = data.search(User.id == ctx.author.id)[0]
        color = False
        try:
            pos = int(numCol)
            if pos not in range(1,61):
                em.title = "**Error**"
                em.description = "That is not a valid color/number."
                em.color = 0xff0000
                return await ctx.send(embed=em)       
        except:
            color = True
            if numCol.lower() == "black":
                pass
            elif numCol.lower() == "red":
                pass
            else:
                em.title = "**Error**"
                em.description = "That is not a valid color/number."
                em.color = 0xff0000
                return await ctx.send(embed=em)
        try:
            if int(bet) > info['cash']:
                em.title = "**Error**"
                em.description = "You do not have enough cash for that bet."
                em.color = 0xff0000
                return await ctx.send(embed=em)
        except:
            em.title = "**Error**"
            em.description = "That is not a valid bet amount."
            em.color = 0xff0000    
            return await ctx.send(embed=em)

        em.title = "Roulette Spinning"
        em.set_image(url="https://media1.giphy.com/media/1DEJwfwdknKZq/giphy.gif")
        em.color = 0xffff00
        m = await ctx.send(embed=em)
        await asyncio.sleep(2)
        if color:
            spin = random.randint(1,60)
            if spin % 2 == 0:
                winner = "red"
            else:
                winner = "black"
            if winner == numCol.lower():
                em = discord.Embed()
                em.title = "**You Win**"
                em.color = 0x00ff00
                em.add_field(name="**Your Bet**",value=numCol.capitalize(),inline=False)
                em.add_field(name="**The Spin**",value=spin,inline=False)
                em.add_field(name="**Profit**",value=f"¥{int(bet)}")
                await m.edit(embed=em)
                data.update({"cash":info['cash']+int(bet)},User.id == ctx.author.id)
            else:
                em.title = "**You Lose**"
                em = discord.Embed()
                em.color = 0xff0000
                em.add_field(name="**Your Bet**",value=numCol.capitalize(),inline=False)
                em.add_field(name="**The Spin**",value=spin,inline=False)
                em.add_field(name="**Loss**",value=f"¥{int(bet)}")
                await m.edit(embed=em)
                data.update({"cash":info['cash']-int(bet)},User.id == ctx.author.id)
        else:
            winner = random.randint(1,60)
            if int(bet) == winner:
                em = discord.Embed()
                em.title = "**You Win**"
                em.color = 0x00ff00
                em.add_field(name="**Your Bet**",value=numCol.capitalize(),inline=False)
                em.add_field(name="**The Spin**",value=winner,inline=False)
                em.add_field(name="**Profit**",value=f"¥{int(bet)*59}")
                await m.edit(embed=em)
                data.update({"cash":info['cash']+(int(bet)*59)},User.id == ctx.author.id)
            else:
                em = discord.Embed()
                em.title = "**You Lose**"
                em.color = 0xff0000
                em.add_field(name="**Your Bet**",value=numCol.capitalize(),inline=False)
                em.add_field(name="**The Spin**",value=winner,inline=False)
                em.add_field(name="**Loss**",value=f"¥{int(bet)}")
                await m.edit(embed=em)
                data.update({"cash":info['cash']-int(bet)},User.id == ctx.author.id)

def setup(bot):
    bot.add_cog(LawBot(bot))
