import constants
import discord

from chatmanager import bot

def main():
    feather_bot = bot.ChatManager(constants.PREFIX)

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
          (not constants.WHITELIST and message.channel.id not in constants.BLACKLIST)):
            await feather_bot.incoming_message(message)

    feather_bot.run(constants.BOT_TOKEN)

if __name__ == "__main__":
    main()
