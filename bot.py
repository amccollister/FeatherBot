import sys
import constants

from discord.ext.commands import Bot


class ChatBot(Bot):
    # on_member_join on_member_remove
    # on_member_update on_member_ban on_guild_join
    # on_command on_command_error on_command_completion
    def __init__(self):
        super().__init__(constants.PREFIX)
        self.remove_command('help')  # We will be implementing our own.

    def run(self):
        super().run(constants.BOT_TOKEN)

    async def on_ready(self):
        print("------------")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------------")
        for plugin in constants.PLUGINS:
            self.load_extension("extensions.{}".format(plugin))

    async def on_message(self, ctx):
        str_id = str(ctx.channel.id)
        if ctx.author.id != self.user.id:
            #await ctx.author.send("DevBot sees you messaging")
            print("Message from {0.author}: {0.content}".format(ctx))
        if constants.WHITELIST and str_id in constants.WHITELIST:
            await self.process_commands(ctx)
        elif str_id not in constants.BLACKLIST:
            await self.process_commands(ctx)

    async def on_error(self, event, *args, **kwargs):
        print(sys.exc_info())
        print("ERROR: {}".format(event))
