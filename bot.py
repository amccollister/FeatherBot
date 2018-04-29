import sys
import constants
import configparser
import discord

from textwrap import dedent
from discord.ext.commands import Bot
from importlib import import_module


class ChatBot(Bot):
    # on_member_join on_member_remove
    # on_member_update on_member_ban on_guild_join
    # on_command on_command_error on_command_completion
    def __init__(self):
        super().__init__(constants.PREFIX)

    def run(self):
        super().run(constants.BOT_TOKEN)

    async def on_ready(self):
        print("------------")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------------")
        await self.change_presence(activity=discord.Game("with my developer"), status="dnd")

    async def on_command(self, ctx):
        print("I think I saw a command?")

    async def on_message(self, message):
        if "meme" in message.content and message.author.id != self.user.id:
            output = [j.lower() if i%2==0 else j.upper() for i, j in enumerate(message.content)]
            await message.channel.send("".join(output))
        print("Message from {0.author}: {0.content}".format(message))

        await self.process_commands(message)

    async def on_error(self, event, *args, **kwargs):
        print(sys.exc_info())
        print("ERROR: {}".format(event))

    async def on_typing(self, channel, user, when):
        print("{0} starting typing in {1} at {2}".format(user, channel, when))

    async def on_message_delete(self, message):
        await message.channel.send("I saw you delete that.")

    async def on_raw_message_edit(self, payload):#before, after):
        print("Data {}".format(payload.data))
        #user = after.author
        #if before.content != after.content:
        #    await after.channel.send("{} changed his message from {} to {}".format(user, before.content, after.content))

    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        if reaction.custom_emoji:
            emoji = ":{}:".format(str(reaction.emoji).split(":")[1])
        await reaction.message.channel.send("{} reacted with {}".format(user, emoji))

