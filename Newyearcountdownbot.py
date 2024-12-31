import discord
from discord.ext import commands
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

NEW_YEAR=datetime(2025,1,1,0,0,1)
Scheduler=AsyncIOScheduler()
channel=None
last_message=None

intents=discord.Intents.default()
intents.message_content=True
bot=commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    Scheduler.add_job(realtime,"interval",seconds=60)
    Scheduler.start()

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")

@bot.command()

async def greet(ctx):
    global channel
    channel=ctx.channel
    name=ctx.author.display_name
    current_time=datetime.now()
    current_hour=current_time.hour
    if current_hour<12:
        greeting='Good morning'
    elif current_hour<16:
        greeting='Good Afternoon'
    elif current_hour<19:
        greeting='Good Evening'
    else:
        greeting='Good Night'
    await ctx.send(f"{greeting},{name}!")

@bot.command()
async def newyearcountdown(ctx):
    global channel
    channel=ctx.channel
    now=datetime.now()
    if now>=NEW_YEAR:
        await ctx.send("Wishing you a happy New year !")
        Scheduler.shutdown()
    else:
        time=NEW_YEAR-now
        day,hour,minutes,second=time.days,time.seconds//3600,(time.seconds//60)%60,time.seconds%60
        countdown=(
            f" 2025 ARRIVES IN:\n"
            f"{day}days,{hour}hours,{minutes}mins,{second}seconds***")
    global last_message
    last_message=await channel.send(countdown)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"Error: {error}")
async def realtime():
    global last_message
    global channel
    if channel is None:
        print('Channel not set')
        return
    now=datetime.now()
    if now>=NEW_YEAR:
        if last_message:
            await last_message.edit(content="Wishing you a happy New year !")
        Scheduler.shutdown()
    else:
        time=NEW_YEAR-now
        day,hour,minutes,second=time.days,time.seconds//3600,(time.seconds//60)%60,time.seconds%60
        countdown=(
            f" 2025 ARRIVES IN:\n"
            f"{day}days,{hour}hours,{minutes}mins,{second}seconds***")
    if last_message:
        await last_message.edit(content=countdown)
    else:
        last_message=await channel.send(countdown)


bot.run("DISCORD_TOKEN")

