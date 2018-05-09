import constants
import discord
import time
import asyncio
import gc

from bot import ChatBot


def main():
    bot = ChatBot()

    for plugin in constants.PLUGINS:
        bot.load_extension("extensions.{}".format(plugin))

    bot.run()


if __name__ == "__main__":
    main()
