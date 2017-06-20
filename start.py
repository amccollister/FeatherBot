import constants
import discord
import time
import asyncio
import gc

from chatmanager import bot


def main():
    disconnect = False
    restart = True
    feather_bot = bot.ChatManager(constants.PREFIX)

    while True:
        @feather_bot.event
        async def on_ready():
            print("------------")
            print("Logged in as")
            print(feather_bot.user.name)
            print(feather_bot.user.id)
            print("------------")
            feather_bot.get_plugins()

        @feather_bot.event
        async def on_message(message: discord.Message):
            if message.author.id != feather_bot.user.id and \
               message.content.startswith(feather_bot.command_prefix) and \
              (message.channel.id in constants.WHITELIST or
              (constants.WHITELIST == [""] and message.channel.id not in constants.BLACKLIST)):
                await feather_bot.incoming_message(message)

        feather_bot.run(constants.BOT_TOKEN)
        restart = feather_bot.restart
        disconnect = feather_bot.disconnect

        if restart:     # Pretty much lifted from https://github.com/Just-Some-Bots/MusicBot/blob/master/run.py line 210
            time.sleep(5)
            gc.collect()
            asyncio.set_event_loop(asyncio.new_event_loop())
            feather_bot = bot.ChatManager(constants.PREFIX)

        if disconnect:
            return

if __name__ == "__main__":
    main()
