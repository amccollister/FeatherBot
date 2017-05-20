import discord
import random
import constants

from discord.ext.commands import Bot
from importlib import import_module

class ChatManager(Bot):
    command_list = []
    plugin_list = {}
    # TODO ping addquote quote currency? 8Ball Reminder Cleverbot Online motd?/rules? rngImage 1d20 RPS! facts emoteText
    # TODO wiki strawpoll youtube weather joke???
    @staticmethod
    def get_general_commands():
        cmd_list = [func for func in dir(ChatManager) if str(func).startswith("cmd_")]
        return cmd_list

    def get_plugin_list(self, plugin, general_list):
        cmd_list = [func for func in dir(plugin) if str(func).startswith("cmd_") and func not in general_list]
        return cmd_list

    def get_plugins(self):
        for app in constants.PLUGINS:
            print("Found plugin:", app)
            _plugin = import_module("chatmanager." + app)
            plugin = _plugin.Plugin(self.command_prefix, self.whitelist)
            self.plugin_list[app] = plugin

    def __init__(self, command_prefix, whitelist):
        super().__init__(command_prefix)
        self.whitelist = whitelist
        self.command_list = self.get_general_commands()

    async def incoming_message(self, message : discord.Message):  # check plugin commands then reject
        if message.content.startswith(self.command_prefix) and message.channel.id == self.whitelist:
                args = message.content.split(" ")
                arg = args.pop(0)[1:]
                if "cmd_" + arg in self.command_list:    # check general commands
                    await getattr(self, "cmd_" + arg)(message, args)
                else:
                    for p in self.plugin_list.values():  # check plugin commands if it's not found in general
                        lst = p.get_plugin_list(p, self.command_list)
                        if "cmd_" + arg in lst:
                            await self.send_message(message.channel, getattr(p, "cmd_" + arg)(args))
                            break  # Once the cmd is found, break to avoid the else statement
                    else:          # If all else fails, tell them this isn't a command
                        await self.send_message(message.channel, "```That's not a command!"
                                                                 "\nPlease use !help for a list of commands.```")

    async def cmd_help(self, message, *args):
        if args[0] == [] or args[0][0] not in self.plugin_list.keys():
            cmds = "**Here's the current list of general commands:**```"
            for cmd in self.command_list:
                cmds += (self.command_prefix + cmd[4:] + ", ")
            cmds = cmds.rstrip(", ")
            cmds += "```\n**For help with a plugin, please use !help \"plugin\"**\n**Here's the list of plugins:**```"
            for plug in self.plugin_list.keys():
                cmds += plug + " "
            cmds += "```"
            await self.send_message(message.channel, cmds)
        else:
            plugin = self.plugin_list[args[0][0]]
            p_list = plugin.get_plugin_list(plugin, self.command_list)
            cmds = "**Here's the list of commands in the \"{0}\" plugin:**```".format(args[0][0])
            for cmd in p_list:
                cmds += (self.command_prefix + cmd[4:] + " ")
            cmds += "```"
            await self.send_message(message.channel, cmds)

    async def cmd_coolest(self, message, *_):
        await self.send_message(message.channel, "{0} is the coolest!".format(message.author.name))

    async def cmd_test(self, message, *_):
        await self.send_message(message.channel, "If you see this, Andrew did something right.")

    async def cmd_choose(self, message, *choice):
        await self.send_message(message.channel, "The best is " + random.choice(choice[0]))

    async def cmd_hello(self, message, *_):
        await self.send_message(message.channel, "Hello I am {0}!".format(self.user.name))

    async def cmd_me(self, message, *_):
        await self.send_message(message.channel, "You are {0.author.name} in {0.channel.name}".format(message))

    async def cmd_joined(self, message, *_):
        await self.send_message(message.channel, "{0.name} joined on {0.joined_at}".format(message.author))
