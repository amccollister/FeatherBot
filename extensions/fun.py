import re
import random
import string
import urllib.error
import urllib.request

from discord.ext import commands
import extensions.utils as util


class FunCog:
    @commands.command()
    async def magic8ball(self, ctx, *arg):
        answers = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it",
                   "As I see it, yes", "Most likely", "Very doubtful", "Yes", "Signs point to yes", "Ask again later",
                   "Reply hazy try again", "Better not tell you now", "Cannot predict it now", "My reply is no",
                   "Concentrate and ask again", "Don't count on it", "My sources say no", "Outlook not so good"]
        text = random.choice(answers)
        if not arg:
            text = "It's blank. You didn't ask it anything."
        await util.send(ctx, text)

    @commands.command()
    async def coolest(self, ctx):
        text = "{0.author.name} is the coolest.".format(ctx)
        await util.send(ctx, text)

    @commands.command()
    async def choose(self, ctx, *args):
        text = "I pick {0}".format(random.choice(args))
        await util.send(ctx, text)

    @commands.command()
    async def rps(self, ctx, arg):
        choice = ["rock", "paper", "scissors"]
        ai_choice = random.choice(choice)
        if arg not in choice:
            text = "That's not a valid choice. Try again."
            await util.send(ctx, text); return
        result = choice.index(arg) - choice.index(ai_choice)
        text = "You chose **{0}**.\nI chose **{1}**.\n".format(arg, ai_choice)
        if result == -1 or result == 2:
            text += "You lose!"
        elif result == 0:
            text += "We tied. Let's try again."
        else:
            text += "You win!"
        await util.send(ctx, text)

    @commands.command()
    async def emoter(self, ctx, arg1, arg2):
        emote = " {0} ".format(arg1)
        sentence = arg2.split(" ")
        text = "{0}{1}{0}".format(emote, emote.join(sentence))
        await util.send(ctx, text)

    @commands.command()
    async def roll(self, ctx, arg):
        roll = re.split("[d+]", arg)
        total = 0
        text = "Rolled a "
        try:
            if len(roll[0]) > 3 or arg[0] not in string.digits: raise Exception
            count = int(roll[0])
            sides = int(roll[1])
            for i in range(count):
                r = random.randint(1, sides)
                total += r
                text += "{} + ".format(r)
            if len(roll) > 2:
                add = int(roll[2])
                total += add
                text += "{}".format(add)
            else:
                text = text[:-2]
            text += " for a total of **{}!**".format(total)
        except:
            text = "The dice landed on the floor. Please try again!"
        await util.send(ctx, text)

    @commands.command()
    async def imgur(self, ctx):
        prefix = "https://i.imgur.com/"
        chars = string.ascii_letters + string.digits
        attempts = 1
        while True:
            suffix = (random.choice(chars) for x in range(random.choice([5, 7])))
            link = prefix + "".join(suffix)
            try:
                with urllib.request.urlopen(link) as response:
                    if response.getcode() == 200:
                        text = "Found {0} after **{1}** attempts.".format(link, attempts)
                        await util.send(ctx, text, link+".png"); break  # add .png to adjust for proxy_url
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    attempts += 1; continue
                else: raise

    @commands.command()
    async def wiki(self, ctx, *arg):
        """
        Usage:
                !wiki [thing]

        Displays an article for a specific thing based on the parameter.
        If no arguments are provided, a random link is displayed.
        """
        if not arg:
            link = "https://en.wikipedia.org/wiki/Special:Random"
        else:
            link = "https://en.wikipedia.org/wiki/" + str(arg[0]).replace(" ", "_")
            print("Testing {}".format(link))
        with urllib.request.urlopen(link) as response:
            text = response.geturl()
            await util.send(ctx, text)


def setup(bot):
    bot.add_cog(FunCog())
