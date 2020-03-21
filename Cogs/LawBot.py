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
    async def leaderboard(self,ctx):
        """Displays a leaderboard for this server's economy."""
        em = discord.Embed()
        em.title = "Leaderboard"
        em.description = ""
        users = []
        for item in data:
            worth = item["cash"] + item["balance"]
            try:
                users.append((worth,f"{ctx.guild.get_member(item['id']).display_name}"))
            except Exception as e:
                pass
        users.sort(reverse=True)
        n = 1
        em.color = 0x000099
        for top in users[:5]:
            em.description += f"**Rank #{n}:** {top[1]} - *Worth ¥{top[0]}*\n"
            n+=1
        em.set_footer(icon_url=ctx.author.avatar_url_as(static_format="png"),text=f"Requested by {ctx.author}")
        await ctx.send(embed=em)

    @commands.command()
    async def register(self,ctx):
        """Opens up a bank account for the user."""
        if len(data.search(User.id == ctx.author.id)) != 0:
            em = discord.Embed()
            em.title="**Error**"
            em.description = "You already have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        data.insert({"id":ctx.author.id,"cash":15000,"balance":0,"lastJobTime":None,"lastCrimeTime":None})
        em = discord.Embed()
        em.title = "**New Registration**"
        em.description = f"<@{ctx.author.id}> registered successfully! Your starting balance is **¥15000**"
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
        if int(amount) > info["cash"]:
            em.title = "**Error**"
            em.description = "You do not have that much cash."
            em.color = 0xff0000
            return await ctx.send(embed=em)

        em = discord.Embed()
        em.color = 0x00ff00
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
        if int(amount) > info["balance"]:
            em.title = "**Error**"
            em.description = "You do not have that much balance in your bank account."
            em.color = 0x00ff00
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
            nextAvailUse = lastUse.shift(hours=2)
            if nextAvailUse.timestamp > arrow.utcnow().timestamp:
                em.title = "**Error**"
                future = arrow.get(info['lastJobTime']).shift(hours=2)
                nextIn = future.humanize(arrow.utcnow(), only_distance=True, granularity=["hour","minute"])
                em.description = f"You cannot use this command for another **{nextIn}**"
                em.color = 0xff0000
                return await ctx.send(embed=em)
        earnings = random.randint(500,7500)
        data.update({"cash":info['cash']+earnings,"lastJobTime":arrow.utcnow().timestamp},User.id == ctx.author.id)
        em.title = "Money Earned!"
        em.description = f"You worked hard and earned **¥{earnings}!**"
        em.color = 0x00ff00
        await ctx.send(embed=em)

    @commands.command()
    async def rob(self,ctx):
        """Rob someone's cash."""
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        if len(ctx.message.mentions) != 1:
            em.title = "**Error**"
            em.description = "You need to @mention someone to use this command."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        target = ctx.message.mentions[0]
        if len(data.search(User.id == target.id)) != 1:
            em.title = "**Error**"
            em.description = "This target does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)

        info = data.search(User.id == ctx.author.id)[0]
        infoTarget = data.search(User.id == target.id)[0]
        
        if info["lastCrimeTime"] != None:
            lastUse = arrow.get(info["lastCrimeTime"])
            nextAvailUse = lastUse.shift(hours=6)
            if nextAvailUse.timestamp > arrow.utcnow().timestamp:
                em.title = "**Error**"
                future = arrow.get(info['lastCrimeTime']).shift(hours=6)
                nextIn = future.humanize(arrow.utcnow(), only_distance=True, granularity=["hour","minute"])
                em.description = f"You cannot use this command for another **{nextIn}**"
                em.color = 0xff0000
                return await ctx.send(embed=em)

        successRate = 40
        if random.randint(0,100) <= successRate:
            robAmount = random.randint(1,infoTarget["cash"])
            em = discord.Embed()
            em.color = 0x00ff00
            em.description = f"You robbed **{target.display_name}** for **¥{robAmount}**"
            await ctx.send(embed=em)
            data.update({"cash":infoTarget["cash"]-robAmount},User.id == target.id)
            data.update({"cash":info["cash"]+robAmount,"lastCrimeTime":arrow.utcnow().timestamp},User.id == ctx.author.id)
        else:
            fine = random.randint(1,info["cash"])
            em = discord.Embed()
            em.color = 0xff0000
            em.description = f"You got caught robbing **{target.display_name}** and got fined **¥{fine}**"
            await ctx.send(embed=em)
            data.update({"cash":info["cash"]-fine,"lastCrimeTime":arrow.utcnow().timestamp},User.id == ctx.author.id)

    @commands.command()
    async def roulette(self,ctx,numCol=None,bet=None):
        '''Spins a roulette.'''
        if numCol == None or bet == None:
            return await ctx.send("```.roulette color/number bet\n\nSpins a roulette. The amount in the cash account is changed based on the outcome.```")
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

    @commands.command()
    async def crash(self,ctx,bet=None):
        '''Multiply your bet by an increasing multiplier. However, the multiplier may crash.'''
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        info = data.search(User.id == ctx.author.id)[0]
        try:
            if int(bet) > info['cash']:
                em.title = "**Error**"
                em.description = "You do not have enough cash for that bet."
                em.color = 0xff0000
                return await ctx.send(embed=em)
        except:
            em.title = "**Error**"
            em.description = "That is not a valid bet amount.\n\nPlease follow this syntax: `.crash betAmount`"
            em.color = 0xff0000    
            return await ctx.send(embed=em)
        
        em = discord.Embed()
        multiplier = 10
        em.title = "Crash"
        em.set_footer(icon_url=ctx.author.avatar_url_as(static_format="png"),text=f"Started by {ctx.author} | Do .stop to stop")
        em.add_field(name="Multiplier",value=f"{multiplier/10}x")
        em.add_field(name="Profit",value=f"¥0")
        em.color = 0xffff00
        me = await ctx.send(embed=em)

        def check(m):
            return m.content == '.stop' and m.channel == ctx.message.channel and m.author == ctx.author

        while True:
            try:
                msg = await self.bot.wait_for('message', check=check,timeout=2.0)
                profit = (int(bet)*(multiplier-10)) // 10
                em = discord.Embed()
                em.title = "Crash Stopped"
                em.color = 0x00ff00
                em.set_footer(icon_url=ctx.author.avatar_url_as(static_format="png"),text=f"Started by {ctx.author}")
                em.add_field(name="Multiplier",value=f"{multiplier/10}x")
                em.add_field(name="Profit",value=f"¥{profit}")
                em.add_field(name="Cash",value=f"You have ¥{info['cash']+profit}",inline=False)
                await me.edit(embed=em)
                data.update({"cash":info['cash']+profit},User.id == ctx.author.id)
                break
            except Exception as e:
                if multiplier < 18: #upto 1.6x, there is 20% chance of crash
                    fail = random.choice([True,False,False,False,False])
                else:# 50/50 chances
                    fail = random.choice([True,True,False,False])
                if fail:
                    em = discord.Embed()
                    em.title = "Crashed"
                    em.color = 0xff0000
                    em.set_footer(icon_url=ctx.author.avatar_url_as(static_format="png"),text=f"Started by {ctx.author}")
                    em.add_field(name="Multiplier",value=f"{multiplier/10}x")
                    em.add_field(name="Loss",value=f"¥{int(bet)}")
                    em.add_field(name="Cash",value=f"You have ¥{info['cash']-int(bet)}",inline=False)
                    await me.edit(embed=em)
                    data.update({"cash":info['cash']-int(bet)},User.id == ctx.author.id)
                    break
                else:
                    multiplier+=2
                    profit = (int(bet)*(multiplier-10)) // 10
                    em = discord.Embed()
                    em.title = "Crashing"
                    em.color = 0xffff00
                    em.set_footer(icon_url=ctx.author.avatar_url_as(static_format="png"),text=f"Started by {ctx.author} | Do .stop to stop")
                    em.add_field(name="Multiplier",value=f"{multiplier/10}x")
                    em.add_field(name="Profit",value=f"¥{profit}")
                    await me.edit(embed=em)

    @commands.command()
    async def invest(self,ctx,cash=None):
        """Invests an amount of cash into a company."""
        em = discord.Embed()
        if len(data.search(User.id == ctx.author.id)) != 1:
            em.title = "**Error**"
            em.description = "This user does not have a bank account registered."
            em.color = 0xff0000
            return await ctx.send(embed=em)
        if cash == None:
            return await ctx.send("```.invest cashAmount\n\nInvests an amount of cash into a company. The payout is random at best.```")
        info = data.search(User.id == ctx.author.id)[0]
        try:
            if int(cash) > info['cash']:
                em.title = "**Error**"
                em.description = "You do not have enough cash for that investment."
                em.color = 0xff0000
                return await ctx.send(embed=em)
        except:
            em.title = "**Error**"
            em.description = "That is not a valid cash amount."
            em.color = 0xff0000    
            return await ctx.send(embed=em)
        luck = random.randint(0,100)
        if luck > 90:
            rate = random.randint(0,1000)
        else:
            rate = random.randint(0,200)

        returns = int(cash)*(rate/100)
        em = discord.Embed()
        em.set_footer(icon_url=ctx.author.avatar_url_as(static_format="png"),text=f"Invested by {ctx.author}")
        em.title = "Investment Results"
        if rate > 100:
            em.color = 0x00ff00
            em.add_field(name="Investment Value",value=f"{rate}%",inline=False)
            em.add_field(name="Profit",value=f"{round(returns-int(cash),2)}",inline=False)
            em.add_field(name="Cash",value=f"You have ¥{info['cash']+returns-int(cash)}",inline=False)
            data.update({"cash":int(info['cash']+returns-int(cash))},User.id == ctx.author.id)
            await ctx.send(embed=em)
        else:
            em.color = 0xff0000
            em.add_field(name="Investment Value",value=f"{rate}%",inline=False)
            em.add_field(name="Loss",value=f"{round(int(cash)-returns,2)}",inline=False)
            em.add_field(name="Cash",value=f"You have ¥{info['cash']-(int(cash) - returns)}",inline=False)
            data.update({"cash":int(info['cash']-(int(cash) - returns))},User.id == ctx.author.id)
            await ctx.send(embed=em)
        
def setup(bot):
    bot.add_cog(LawBot(bot))
