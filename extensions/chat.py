import extensions.utils as util
from discord.ext import commands


class ChatCog(commands.Cog):
    @commands.command()
    async def ping(self, ctx):
        """
        Usage:
                !ping

        Tests the responsiveness of the bot.
        Pong.
        """
        await util.send(ctx, "Pong.")

    @commands.command()
    async def pyramid(self, ctx, arg1, arg2):
        """
        Usage:
                !pyramid [emote] [size]

        Creates an emote pyramid of the desired size.
        """
        size = int(arg2)
        output = ""
        for i in range(1, size+1):
            output += "{}\n".format(" ".join([arg1 for _ in range(i)]))
        for i in range(size-1, 0, -1):
            output += "{}\n".format(" ".join([arg1 for _ in range(i)]))
        await util.send(ctx, output)

    @commands.command()
    async def help(self, ctx, *arg):
        """
        Usage:
                !help <plugin|command>

        That's this command!
        Gives you help based on the desired plugin or command you specify.
        If no arguments are specified, it displays all available plugins.
        """
        cogs = ctx.bot.cogs.keys()
        if not arg:
            text = "__**PLUGINS**__\n"
            for cog in cogs:
                text += cog[:-3] + "\n"
            return await util.send(ctx, text)
        else:
            cog = arg[0].lower().capitalize() + "Cog"
            if cog in cogs:
                command = [x.name for x in ctx.bot.get_cog(cog).get_commands()]
                text = "__**{0} Commands**__\n".format(cog[:-3])
                for c in command:
                    text += c + "\n"
                await util.send(ctx, text)
            else:
                command = arg[0].lower()
                if command in [x.name for x in ctx.bot.commands]:
                    await util.send(ctx, ctx.bot.get_command(command).help)
                else:
                    await util.send(ctx, "That plugin does not exist or is not currently installed.")

    @commands.command()
    async def joined(self, ctx):
        """
        Usage:
                !joined

        Tells you when you joined the server.
        """
        text = "{0.author} joined {0.guild} on {0.author.joined_at}".format(ctx)
        await util.send(ctx, text)

def setup(bot):
    bot.add_cog(ChatCog())

