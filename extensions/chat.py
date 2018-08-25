import random
import extensions.utils as util
from discord.ext import commands


class ChatCog:
    """ These are our general chat commands that will always be loaded
    Also, context is always passed: author, guild, channel, me, voice_client"""

    @commands.command()
    async def ping(self, ctx):
        #embed = util.make_embed(ctx, random.choice(["Bong.", "Pong.", "Dong."]))
        #await ctx.send(embed=embed)
        # call a send_msg?
        await util.send(ctx, "Pong.")

    @commands.command()
    async def test(self, ctx, arg1, arg2):
        text = ("I received a test command!\n"
                "The first argument was **{}**\n"
                "The second argument was **{}**".format(arg1, arg2))
        await util.send(ctx, text)

    @commands.command()
    async def pyramid(self, ctx, arg1, arg2):
        size = int(arg2)
        output = ""
        for i in range(1, size+1):
            output += "{}\n".format(" ".join([arg1 for _ in range(i)]))
        for i in range(size-1, 0, -1):
            output += "{}\n".format(" ".join([arg1 for _ in range(i)]))
        await util.send(ctx, output)

    # TODO: Figure out how to override the help command
    @commands.command()
    async def help(self, ctx):
        await ctx.send("I'll do this later.")

    @commands.command()
    async def hello(self, ctx):
        text = "Hello {0.author.name}!".format(ctx)
        await util.send(ctx, text)

    @commands.command()
    async def me(self, ctx):
        text = "You are {0.author} in the {0.channel} channel.".format(ctx)
        await util.send(ctx, text)

    @commands.command()
    async def joined(self, ctx):
        text = "{0.author} joined {0.guild} on {0.author.joined_at}".format(ctx)
        await util.send(ctx, text)

    @commands.command()
    async def motd(self, ctx):
        text = "No MOTD at the moment."
        await util.send(ctx, text)

    @commands.command()
    async def setmotd(self, ctx):
        text = "Yeah, it's not set at all."
        await util.send(ctx, text)

    @commands.command()
    async def disconnect(self, ctx):
        text = "You can't kill me."
        await util.send(ctx, text)

    @commands.command()
    async def restart(self, ctx):
        text = "*blinks*"
        await util.send(ctx, text)


def setup(bot):
    bot.add_cog(ChatCog())

'''
# Old class to tbe adjust later
class ChatManager(Bot):
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

    #TODO THIS TOTES DOESN'T WORK WTF fix line 56
    def check_rights(self, message, arg):
        id = message.author.id; role_list = message.author.roles
        user_group = None
        if id == constants.OWNER_ID:
            return True
        for k in self.cfg:
            if k == "DEFAULT": continue
            roles = self.cfg[k]["GrantRoles"].split(" "); users = self.cfg[k]["GrantUsers"].split(" ")
            if (id in users) or any(r.id in roles for r in role_list):
                user_group = k; break
        if not user_group: user_group = "DEFAULT"
        whitelist = self.cfg[user_group]["CommandWhitelist"].split(" ")
        blacklist = self.cfg[user_group]["CommandBlacklist"].split(" ")
        if whitelist == [""]:
            if arg in blacklist: return False
            return True
        else:
            if arg in whitelist: return True
            return False

    def __init__(self):
        super().__init__(constants.PREFIX)
        self.command_list = self.get_general_commands()
        self.plugin_list = {}
        self.cfg = configparser.ConfigParser()
        self.cfg.read("config/permissions.ini")
        self.disconnect = False
        self.restart = False

    def run(self):
        super().run(constants.BOT_TOKEN)

    async def on_ready(self):
        print("------------")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------------")
        await self.change_presence(activity=discord.Game("with my developer"), status="dnd")

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))

    async def incoming_message(self, message): # TODO check_rights()
        args = message.content.split(" ")
        arg = args.pop(0)[1:].lower() # get the command the user just sent and remove the !
        if self.check_rights(message, arg):
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
        else:
            await self.send_msg(message.channel, ":no_entry_sign: **ACCESS DENIED** :no_entry_sign:")

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
                !hello

        Greets the bot.
        """
        await self.send_msg(message.channel, "Hello, {0}. I am {1}!".format(self.get_name(message), self.user.name))

    async def cmd_me(self, message, *_):
        """
        Usage:
                !me

        Gives some info about yourself.
        """
        await self.send_message(message.channel, "You are {1} in {0.server.name} in the "
                                                 "{0.channel.name} channel".format(message, self.get_name(message)))
    async def cmd_joined(self, message, *_):   # make usable on other users
        """
        Usage:
                !joined

        Gives the date of when you joined the server.
        """
        server = message.server.name
        date = message.author.joined_at.strftime("%B %d, %Y")
        await self.send_msg(message.channel, "{0} joined {1} on {2}!".format(self.get_name(message), server, date))

    async def cmd_online(self, message, *_):
        """
        Usage:
                !online

        Gives a list of all the users online on this server.
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
                !motd

        Displays the message of the day.
        """
        await self.send_msg(message.channel, "__**M O T D**__```{0}```".format(constants.MOTD))

    async def cmd_setmotd(self, message, *args):
        """
        Usage:
                !setmotd <motd>

        Sets the message of the day for other users to see.
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
        self.disconnect = True
        await self.send_msg(message.channel, "Shutting down...")
        await self.close()

    async def cmd_restart(self, message, *args):
        """
        Usage:
                !restart

        Forces the bot to disconnect, then reconnect.
        """
        self.restart = True
        await self.send_msg(message.channel, "I'll be back... :sunglasses: ")
        await self.logout()
'''
