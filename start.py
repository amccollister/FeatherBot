import constants
import discord
import asyncio  # learn this thing
import random

from discord.ext.commands import Bot
# import configparser at some point

# figure out how implementing this will help
class ChatManager(Bot):
    pass

feather_bot = ChatManager(command_prefix="!")  # command_prefix="!")

quotes = open("quotes.txt", "w")

@feather_bot.event
async def on_ready():
    print("------------")
    print("Logged in as")
    print(feather_bot.user.name)
    print(feather_bot.user.id)
    print("------------")

@feather_bot.event
async def on_message(message : discord.Message):
    if message.author.id != feather_bot.user.id:
        await feather_bot.send_message(message.channel, "I saw a message")  # feather_bot.say("I saw a message!")

# calculate command "1+1" "8%2"
@feather_bot.command()
async def hello():
    await feather_bot.say("Hello I am {0}!".format(feather_bot.user.name))

@feather_bot.command(pass_context=True)
async def me(ctx):
    await feather_bot.say("You are {0.author.name} in {0.channel.name}".format(ctx.message))

@feather_bot.command()
async def joined(member : discord.Member):
    await feather_bot.say("{0.name} joined on {0.joined_at}".format(member))

@feather_bot.command()
async def add(*nums : float):
    sumNum = 0
    for i in nums:
        sumNum += i
    await feather_bot.say("The sum of all these numbers is {0}".format(sumNum))

@feather_bot.command()
async def choose(*choice : str):
    await feather_bot.say("The best is " + random.choice(choice))

feather_bot.run(constants.BOT_TOKEN)
