import constants
import discord
import time
import asyncio
import gc

from chatmanager.bot import ChatBot


def main():
    bot = ChatBot()
    bot.load_extension("chatmanager.chat")
    bot.run()


if __name__ == "__main__":
    main()
