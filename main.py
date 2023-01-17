import asyncio
import random
import os
import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

bot = Bot('!', intents=intents) #command_prefix='!', intents=intents)

@bot.command(name='test', help='just a test function. prints "Hello World!"')
async def HelloWorld(message):
    await message.send("Hello World!")

@bot.command(name='edit_chore', help='edit chore score', pass_context=True)
async def edit_chore(ctx, score):
    new_score = 0
    try:
        new_score = int(score)
    except ValueError:
        await ctx.channel.send("incorrect value. use a integer")
        return
    with open('names/' + ctx.message.author.name + '.txt', 'w') as f:
        f.write(str(new_score))

@bot.command(name='clear', help='!clear [n_messages]: clears n_messages from chat in called channel. clear limit is 100 messages at a time.', pass_context=True)
async def clear(ctx, n_messages=100):
    if n_messages > 100:
        print('f{ctx.message.author} tried to clear ' + n_messages)
        n_messages = 100
    await ctx.channel.purge(limit = n_messages)

@bot.command(name='chore', help='return chore stats', pass_context=True)
async def chore(ctx, name='notaname'):
    names = {}
    if name == 'notaname':
        for filename in os.listdir('names'):
            with open('names/' + filename, 'r') as f:
                names[str(filename)] = int(f.read())
    elif name+'.txt' not in os.listdir("names"):
        await ctx.channel.send(f'{name} not recorded')
        return
    else:
        with open('names/' +name+'.txt', 'r') as f:
            names[name+'.txt'] = f.read()

    for n in names:
        await ctx.channel.send(f'{n[0:-4]} : {str(names[n])}\n')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name == 'quiet-room':
        await message.channel.send('Shh')
    elif message.channel.name == 'chore' and '/' in message.content:
        old_number = 0
        if message.author.name + '.txt' in os.listdir("names"):
            with open('names/' + message.author.name + '.txt', 'r') as f:
                old_number = int(f.read())
        with open('names/' + message.author.name + '.txt', 'w') as f:
            f.write(str(old_number + 1))
            
    await bot.process_commands(message)

keep_alive()
try:
  bot.run(TOKEN)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system('kill 1')
  os.system("python restarter.py")
