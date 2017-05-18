import constants
import discord
from chatmanager import bot
import asyncio  # learn this thing
import random
# import configparser at some point

server = None # declare a global variable tracking my main server
feather_bot = bot.ChatManager(command_prefix="!")

@feather_bot.event
async def on_ready():
    print("------------")
    print("Logged in as")
    print(feather_bot.user.name)
    print(feather_bot.user.id)
    print("------------")
    server = (list(feather_bot.servers)[0]) # servers returns a dict_values which is a view. use list() to convert
                                            # dict_values don't support indexing...

@feather_bot.event
async def on_message(message : discord.Message):
    if message.author.id != feather_bot.user.id:
        await feather_bot.incoming_message(message)
        # await feather_bot.send_message(message.channel, "I saw a message")  # feather_bot.say("I saw a message!")

# calculate command "1+1" "8%2"

feather_bot.run(constants.BOT_TOKEN)
