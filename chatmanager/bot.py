import constants
import configparser

from textwrap import dedent
from discord.ext.commands import Bot
from importlib import import_module

class ChatManager(Bot):
    command_list = []
    plugin_list = {}
    #TODO command rights w/ configparser

    @staticmethod
    def get_general_commands():
        cmd_list = [func for func in dir(ChatManager) if str(func).startswith("cmd_")]
        return cmd_list

    @staticmethod
    def get_plugin_list(plugin, general_list):
        cmd_list = [func for func in dir(plugin) if str(func).startswith("cmd_") and func not in general_list]
        return cmd_list

    async def send_msg(self, channel, message):
        if len(message) < constants.DISCORD_MSG_LIMIT:
            await self.send_message(channel, message)
        else:
            shorter_msg = message[constants.DISCORD_MSG_LIMIT]
            await self.send_msg(channel, shorter_msg)

    def get_plugins(self):
        for app in constants.PLUGINS:
            print("Found plugin:", app)
            _plugin = import_module("chatmanager." + app)
            plugin = _plugin.Plugin(self)
            self.plugin_list[app] = plugin

    def get_name(self, message):
        name = message.author.nick
        if not name:
            name = message.author.name
        return name

    def check_plugins(self, arg):
        for p in self.plugin_list.values():
            lst = p.get_plugin_list(p, self.command_list)
            if "cmd_" + arg in lst:
                return [p, "cmd_" + arg]
        return None

    def check_rights(self, message, arg):
        pass

    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.command_list = self.get_general_commands()
        self.cfg = configparser.ConfigParser().read("config/config.ini")

    async def incoming_message(self, message): # TODO check_rights()
        args = message.content.split(" ")
        arg = args.pop(0)[1:].lower() # get the command the user just sent and remove the !
        if "cmd_" + arg in self.command_list:    # check general commands
            await getattr(self, "cmd_" + arg)(message, args)
        else:
            cmd = self.check_plugins(arg)  # check plugin commands if it's not found in general
            if cmd is not None:
                await getattr(cmd[0], cmd[1])(message, args)
            else:          # If all else fails, tell them this isn't a command
                await self.send_msg(message.channel, "```That's not a command!"
                                                         "\nPlease use {0}help for a list of commands.```"
                                                         .format(self.command_prefix))

    async def cmd_help(self, message, *args):
        """
        Usage:
                !help [plugin | command]

        Describes a command or lists commands within a plugin.
        """
        valid_cmd = True
        while args[0] and valid_cmd:
            cmd = self.check_plugins(args[0][0])
            if args[0][0] in self.plugin_list.keys():
                plugin = self.plugin_list[args[0][0]]
                p_list = plugin.get_plugin_list(plugin, self.command_list)
                cmds = "**Here's the list of commands in the \"{0}\" plugin:**```".format(args[0][0])
                for cmd in p_list:
                    cmds += (self.command_prefix + cmd[4:] + " ")
                cmds += "```"
                await self.send_msg(message.channel, cmds); break
            elif "cmd_" + args[0][0] in self.command_list:
                help_msg = getattr(self, "cmd_" + args[0][0]).__doc__
                await self.send_msg(message.channel, "```{}```".format(dedent(help_msg))); break
            elif cmd is not None:
                help_msg = getattr(cmd[0], cmd[1]).__doc__
                await self.send_msg(message.channel, "```{}```".format(dedent(help_msg))); break
            valid_cmd = False
        else:
            cmds = "**Here's the current list of general commands:**```"
            for cmd in self.command_list:
                cmds += (self.command_prefix + cmd[4:] + ", ")
            cmds = cmds.rstrip(", ")
            cmds += "```\n**For help with a plugin, please use !help \"plugin\"**\n**Here's the list of plugins:**```"
            for plug in self.plugin_list.keys():
                cmds += plug + " "
            cmds += "```"
            await self.send_msg(message.channel, cmds)

    async def cmd_ping(self, message, *_):
        """
        Usage:
                !ping

        Sends back a pong.
        """
        await self.send_msg(message.channel, "Pong.")

    async def cmd_hello(self, message, *_):
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        await self.send_msg(message.channel, "Hello, {0}. I am {1}!".format(self.get_name(message), self.user.name))

    async def cmd_me(self, message, *_):
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        await self.send_message(message.channel, "You are {1} in {0.server.name} in the "
                                                 "{0.channel.name} channel".format(message, self.get_name(message)))
    async def cmd_joined(self, message, *_):   # make usable on other users
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        server = message.server.name
        date = message.author.joined_at.strftime("%B %d, %Y")
        await self.send_msg(message.channel, "{0} joined {1} on {2}!".format(self.get_name(message), server, date))

    async def cmd_online(self, message, *_):
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        users = message.server.members
        members = []
        online_count = 0
        for u in users:
            if str(u.status) != "offline":
                online_count += 1
                name = u.nick and u.nick or u.name
                members.append(name)
        online = "There are **{0}** users online.```".format(online_count)
        online += ", ".join(members) + "```"
        await self.send_msg(message.channel, online)

    async def cmd_motd(self, message, *_):
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        await self.send_msg(message.channel, "__**M O T D**__```{0}```".format(constants.MOTD))

    async def cmd_setmotd(self, message, *args):
        """
        Usage:
                !command [params]

        This describes what the command does.
        """
        if not args[0]:
            await self.send_msg(message.channel, "```You didn't set a new MOTD!```")
        else:
            new_motd = " ".join(args[0])
            constants.MOTD = new_motd
            await self.send_msg(message.channel, "**New MOTD set!**")

    async def cmd_disconnect(self, message, *args):
        """
        Usage:
                !disconnect

        Forces the bot to disconnect.
        """
        await self.send_msg(message.channel, "Shutting down...")
        await self.close()

    async def cmd_restart(self, message, *args):
        """
        Usage:
                !restart

        Forces the bot to disconnect, then reconnect.
        """
        await self.send_msg(message.channel, "I'll be back...")
        # Figure out how to restart bot
        pass