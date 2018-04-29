import constants
import discord
import time
import asyncio
import gc

from bot import ChatBot

def main():
    bot = ChatBot()
    bot.load_extension("extensions.chat")
    bot.run()


if __name__ == "__main__":
    main()
