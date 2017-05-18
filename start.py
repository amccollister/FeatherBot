import constants
import discord
from chatmanager import bot
import asyncio  # learn this thing
# import configparser at some point

server = None # declare a global variable tracking my main server
feather_bot = bot.ChatManager("!", "312852004999266304") # hard coded the dev channel for now

@feather_bot.event
async def on_ready():
    print("------------")
    print("Logged in as")
    print(feather_bot.user.name)
    print(feather_bot.user.id)
    print("------------")
    server = (list(feather_bot.servers)[0]) # servers returns a dict_values which is a view. use list() to convert
                                            # dict_values don't support indexing... also we ain't using this var atm

@feather_bot.event
async def on_message(message : discord.Message):
    if message.author.id != feather_bot.user.id:
        await feather_bot.incoming_message(message)

feather_bot.run(constants.BOT_TOKEN)
