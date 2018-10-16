import constants
import extensions.utils as util
from discord.ext import commands


class ChatCog:
    @commands.command()
    async def ping(self, ctx):
        #embed = util.make_embed(ctx, random.choice(["Bong.", "Pong.", "Dong."]))
        #await ctx.send(embed=embed)
        # call a send_msg?
        await util.send(ctx, "Pong.")

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
        this = ctx.bot.cogs
        print(this)
        await util.send(ctx, ctx.bot.get_cog_commands("ChatCog"))

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
    async def disconnect(self, ctx):
        text = "Shutting down..."
        await util.send(ctx, text)
        await ctx.bot.close()

    @commands.command()
    async def restart(self, ctx):
        text = "Restarting..."
        await util.send(ctx, text)


def setup(bot):
    bot.add_cog(ChatCog())
