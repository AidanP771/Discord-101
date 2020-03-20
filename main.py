from discord.ext import commands

startup_extensions = ["Cogs.LawBot"]

bot = commands.Bot(command_prefix=".")

@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name)
    await bot.change_presence(activity=discord.Activity(name="em' earn!",type=3))
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

@commands.is_owner()
@bot.command(hidden=True)
async def load(ctx,extension_name : str):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@commands.is_owner()
@bot.command(hidden=True)
async def unload(ctx,extension_name : str):
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))

@commands.is_owner()
@bot.command(hidden=True)
async def reload(ctx):
    bot.unload_extension("Cogs.LawBot")
    try:
        bot.load_extension("Cogs.LawBot")
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} re-loaded.".format("All cogs"))

@commands.is_owner()
@bot.command(hidden=True)
async def add(ctx,left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

bot.help_command=commands.DefaultHelpCommand(command_attrs={"hidden": True,"dm_help":True,"sort_commands":False})
if __name__ == "__main__":
    #bot.run(input("Insert Token Please: "))
    bot.run("NjkwMDEzMjU4MDMxNDMxNzQ0.XnQFCg.y2slNZkYDS-SvdvzxBauWNRUklU")