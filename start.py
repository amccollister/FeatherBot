import constants
import discord
import time
import asyncio
import gc

from chatmanager.bot import ChatBot


def main():
    bot = ChatBot()

    @bot.command()
    async def test(ctx, arg):
        await ctx.send(arg)

    bot.run()


if __name__ == "__main__":
    main()
